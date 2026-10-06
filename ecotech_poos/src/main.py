import getpass
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dominio.departamento import Departamento
from dominio.empleado import Administrador, EmpleadoRegular
from dominio.informe import Informe
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from dominio.usuario import Usuario
from dominio.validador_entrada import ValidadorEntrada as Val
from persistencia.asignaciondao import AsignacionDAO
from persistencia.crearbd import crear_tablas
from persistencia.departamentodao import DepartamentoDAO
from persistencia.empleadodao import EmpleadoDAO
from persistencia.excepciones import ErrorConexion, ErrorIntegridad, ErrorPersistencia
from persistencia.proyectodao import ProyectoDAO
from persistencia.registrotiempodao import RegistroTiempoDAO
from persistencia.usuariodao import UsuarioDAO

logging.basicConfig(filename="ecotech_errores.log", level=logging.ERROR,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def solicitar_opcion(maximo: int) -> int:
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if 0 <= opcion <= maximo:
                return opcion
            print(f"Opción fuera de rango (0-{maximo}).")
        except ValueError:
            print("Debe ingresar un número.")


def pedir(mensaje: str, validador, actual=None):
    while True:
        texto = input(mensaje).strip()
        if texto == "" and actual is not None:
            return actual
        try:
            return validador(texto)
        except ValueError as error:
            print(f"  -> {error}")


def pedir_id_existente(mensaje: str, buscador, entidad: str, opcional: bool = False):
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return None
        try:
            id_ = Val.validar_entero_positivo(texto, "El ID")
        except ValueError as error:
            print(f"  -> {error}")
            continue
        if buscador(id_) is not None:
            return id_
        print(f"  -> No existe {entidad} con ID {id_}.")


def confirmar(mensaje: str) -> bool:
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def texto_no_vacio(campo: str):
    return lambda t: Val.validar_texto_no_vacio(t, campo)


def ejecutar_accion(accion) -> None:
    try:
        accion()
    except ValueError as error:           
        print(f"[DATO INVÁLIDO] {error}")
    except ErrorConexion:
        print("[ERROR] No se pudo conectar a la base de datos. "
                "Revise que MySQL (WampServer) esté encendido y que el archivo .env sea correcto.")
    except ErrorIntegridad:
        print("[ERROR] No se pudo guardar: ya existe un registro con esos datos "
                "o hace referencia a algo que no existe.")
    except ErrorPersistencia:
        print("[ERROR] No fue posible completar la operación. Intente nuevamente.")

def registrar_departamento():
    nombre = pedir("Nombre del departamento: ", texto_no_vacio("El nombre"))
    departamento = DepartamentoDAO.insertar(Departamento(nombre=nombre))
    print(f"[ÉXITO] Departamento guardado con ID {departamento.id}.")


def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("No hay departamentos registrados.")
    for d in departamentos:
        print(d.mostrar_datos())


def buscar_departamento():
    id_ = pedir("ID a buscar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    d = DepartamentoDAO.buscar_por_id(id_)
    print(d.mostrar_datos() if d else "Departamento no encontrado.")


def actualizar_departamento():
    id_ = pedir_id_existente("ID del departamento a actualizar: ", DepartamentoDAO.buscar_por_id, "un departamento")
    d = DepartamentoDAO.buscar_por_id(id_)
    d.nombre = pedir(f"Nuevo nombre [{d.nombre}]: ", texto_no_vacio("El nombre"), actual=d.nombre)
    print("[ÉXITO] Departamento actualizado." if DepartamentoDAO.actualizar(d) else "Departamento no encontrado.")


def eliminar_departamento():
    id_ = pedir("ID del departamento a eliminar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    if not confirmar("Sus empleados quedarán sin departamento. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Departamento eliminado." if DepartamentoDAO.eliminar(id_) else "No existe un departamento con ese ID.")


# ------------------------------------------------------------------ empleados
def registrar_empleado():
    print("Tipo de empleado: 1) Regular  2) Administrador")
    tipo = pedir("Tipo: ", lambda t: Val.validar_entero_positivo(t, "El tipo"))
    if tipo not in (1, 2):
        print("[DATO INVÁLIDO] Tipo de empleado no válido.")
        return
    rut = pedir("RUT (ej. 12345678-5): ", Val.validar_rut)
    nombre = pedir("Nombre completo: ", texto_no_vacio("El nombre"))
    correo = pedir("Correo (Enter para omitir): ", Val.validar_email_opcional)
    dep_id = pedir_id_existente("ID del departamento (Enter = sin departamento): ",
                                DepartamentoDAO.buscar_por_id, "un departamento", opcional=True)
    salario = pedir("Salario base ($): ", lambda t: Val.validar_monto(t, "El salario"))
    clase = EmpleadoRegular if tipo == 1 else Administrador
    empleado = clase(rut=rut, nombre=nombre, correo=correo, departamento_id=dep_id, salario_base=salario)
    EmpleadoDAO.insertar(empleado)
    print(f"[ÉXITO] Empleado registrado con ID {empleado.id}.")


def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados.")
        return
    nombres = {d.id: d.nombre for d in DepartamentoDAO.listar()}
    for e in empleados:
        print(f"{e.mostrar_datos()} | Depto: {nombres.get(e.departamento_id, 'Sin asignar')}")


def buscar_empleado():
    id_ = pedir("ID a buscar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    e = EmpleadoDAO.buscar_por_id(id_)
    print(e.mostrar_datos() if e else "Empleado no encontrado.")


def actualizar_empleado():
    id_ = pedir_id_existente("ID del empleado a actualizar: ", EmpleadoDAO.buscar_por_id, "un empleado")
    e = EmpleadoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    e.nombre = pedir(f"Nombre [{e.nombre}]: ", texto_no_vacio("El nombre"), actual=e.nombre)
    e.correo = pedir(f"Correo [{e.correo}]: ", Val.validar_email_opcional, actual=e.correo)
    e.salario_base = pedir(f"Salario base [{e.salario_base}]: ",
                            lambda t: Val.validar_monto(t, "El salario"), actual=e.salario_base)
    print("[ÉXITO] Empleado actualizado." if EmpleadoDAO.actualizar(e) else "Empleado no encontrado.")


def eliminar_empleado():
    id_ = pedir("ID del empleado a eliminar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    if not confirmar("Se eliminarán también sus registros de tiempo. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Empleado eliminado." if EmpleadoDAO.eliminar(id_) else "No existe un empleado con ese ID.")


def registrar_proyecto():
    nombre = pedir("Nombre del proyecto: ", texto_no_vacio("El nombre"))
    presupuesto = pedir("Presupuesto ($): ", lambda t: Val.validar_monto(t, "El presupuesto"))
    proyecto = ProyectoDAO.insertar(Proyecto(nombre=nombre, presupuesto=presupuesto))
    print(f"[ÉXITO] Proyecto guardado con ID {proyecto.id}.")


def listar_proyectos():
    proyectos = ProyectoDAO.listar()
    if not proyectos:
        print("No hay proyectos registrados.")
    for p in proyectos:
        print(p.mostrar_datos())


def buscar_proyecto():
    id_ = pedir("ID a buscar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    p = ProyectoDAO.buscar_por_id(id_)
    print(p.mostrar_datos() if p else "Proyecto no encontrado.")


def actualizar_proyecto():
    id_ = pedir_id_existente("ID del proyecto a actualizar: ", ProyectoDAO.buscar_por_id, "un proyecto")
    p = ProyectoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    p.nombre = pedir(f"Nombre [{p.nombre}]: ", texto_no_vacio("El nombre"), actual=p.nombre)
    p.presupuesto = pedir(f"Presupuesto [{p.presupuesto}]: ",
                            lambda t: Val.validar_monto(t, "El presupuesto"), actual=p.presupuesto)
    print("[ÉXITO] Proyecto actualizado." if ProyectoDAO.actualizar(p) else "Proyecto no encontrado.")


def eliminar_proyecto():
    id_ = pedir("ID del proyecto a eliminar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    if not confirmar("Se eliminarán también sus registros de tiempo. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Proyecto eliminado." if ProyectoDAO.eliminar(id_) else "No existe un proyecto con ese ID.")


def registrar_horas():
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    horas = pedir("Horas trabajadas: ", Val.validar_horas)
    fecha = pedir("Fecha (AAAA-MM-DD): ", Val.validar_fecha)
    registro = RegistroTiempoDAO.insertar(
        RegistroTiempo(id_empleado=id_emp, id_proyecto=id_proy, horas=horas, fecha=fecha))
    print(f"[ÉXITO] Horas registradas con ID {registro.id}.")


def listar_registros():
    registros = RegistroTiempoDAO.listar()
    if not registros:
        print("No hay registros de tiempo.")
        return
    empleados = {e.id: e.nombre for e in EmpleadoDAO.listar()}
    proyectos = {p.id: p.nombre for p in ProyectoDAO.listar()}
    for r in registros:
        print(f"ID: {r.id} | {r.fecha} | {empleados.get(r.id_empleado, '?')} -> "
                f"{proyectos.get(r.id_proyecto, '?')} | {r.horas} hrs")


def buscar_registro():
    id_ = pedir("ID a buscar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    r = RegistroTiempoDAO.buscar_por_id(id_)
    print(r.mostrar_datos() if r else "Registro no encontrado.")


def actualizar_registro():
    id_ = pedir_id_existente("ID del registro a actualizar: ", RegistroTiempoDAO.buscar_por_id, "un registro")
    r = RegistroTiempoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    r.horas = pedir(f"Horas [{r.horas}]: ", Val.validar_horas, actual=r.horas)
    r.fecha = pedir(f"Fecha [{r.fecha}]: ", Val.validar_fecha, actual=r.fecha)
    print("[ÉXITO] Registro actualizado." if RegistroTiempoDAO.actualizar(r) else "Registro no encontrado.")


def eliminar_registro():
    id_ = pedir("ID del registro a eliminar: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
    if not confirmar("¿Eliminar el registro?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Registro eliminado." if RegistroTiempoDAO.eliminar(id_) else "No existe un registro con ese ID.")


def cargar_proyectos_asignados(empleado) -> None:
    for proyecto in AsignacionDAO.proyectos_de_empleado(empleado.id):
        empleado.agregar_proyecto(proyecto)


def asignar_empleado(admin: Administrador):
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    empleado, proyecto = EmpleadoDAO.buscar_por_id(id_emp), ProyectoDAO.buscar_por_id(id_proy)
    cargar_proyectos_asignados(empleado)
    if not admin.asignar_empleado_proyecto(empleado, proyecto):    
        print("Ese empleado ya está asignado a ese proyecto.")
        return
    AsignacionDAO.asignar(empleado.id, proyecto.id)                
    print(f"[ÉXITO] {empleado.nombre} asignado a {proyecto.nombre}.")


def desasignar_empleado(admin: Administrador):
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    empleado, proyecto = EmpleadoDAO.buscar_por_id(id_emp), ProyectoDAO.buscar_por_id(id_proy)
    cargar_proyectos_asignados(empleado)
    if not admin.desasignar_empleado_de_proyecto(empleado, proyecto):
        print("Ese empleado no estaba asignado a ese proyecto.")
        return
    AsignacionDAO.desasignar(empleado.id, proyecto.id)
    print(f"[ÉXITO] {empleado.nombre} desasignado de {proyecto.nombre}.")


def listar_asignados():
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    asignados = AsignacionDAO.empleados_de_proyecto(id_proy)
    print("Empleados asignados:" if asignados else "Ese proyecto no tiene empleados asignados.")
    for e in asignados:
        print(f"  - {e.nombre} ({e.tipo})")


def menu_asignaciones(admin: Administrador) -> None:
    while True:
        print("\n--- ASIGNACIONES EMPLEADO-PROYECTO ---")
        print("1. Asignar empleado a proyecto")
        print("2. Desasignar empleado de proyecto")
        print("3. Ver empleados de un proyecto")
        print("0. Volver")
        opcion = solicitar_opcion(3)
        if opcion == 0:
            return
        acciones = {1: lambda: asignar_empleado(admin), 2: lambda: desasignar_empleado(admin), 3: listar_asignados}
        ejecutar_accion(acciones[opcion])


# ------------------------------------------------------------------ informes
def generar_informe():
    print("Tipos: " + ", ".join(Informe.TIPOS))
    tipo = pedir("Tipo de informe: ", Informe._validar_tipo)
    informe = Informe(tipo)
    print()
    print(informe.generar_informe(tipo, EmpleadoDAO.listar(), ProyectoDAO.listar(),
                                    DepartamentoDAO.listar(), RegistroTiempoDAO.listar()))


def pedir_contrasena_nueva() -> str:
    while True:
        clave = getpass.getpass("Contraseña (mín. 8 caracteres): ")
        try:
            Val.validar_contrasena(clave)
        except ValueError as error:
            print(f"  -> {error}")
            continue
        if clave == getpass.getpass("Repita la contraseña: "):
            return clave
        print("  -> Las contraseñas no coinciden.")


def crear_usuario_para(empleado) -> None:
    nombre_usuario = pedir("Nombre de usuario: ", Val.validar_nombre_usuario)
    usuario = Usuario(nombre_usuario=nombre_usuario, rol=empleado.tipo, empleado_id=empleado.id)
    usuario.establecer_contrasena(pedir_contrasena_nueva())
    UsuarioDAO.insertar(usuario)


def crear_usuario_empleado():
    id_emp = pedir_id_existente("ID del empleado que tendrá acceso: ", EmpleadoDAO.buscar_por_id, "un empleado")
    if UsuarioDAO.buscar_por_empleado(id_emp):
        print("Ese empleado ya tiene un usuario.")
        return
    crear_usuario_para(EmpleadoDAO.buscar_por_id(id_emp))
    print("[ÉXITO] Usuario creado.")


def cambiar_mi_contrasena(sesion):
    usuario = UsuarioDAO.buscar_por_empleado(sesion.id)
    actual = getpass.getpass("Contraseña actual: ")
    nueva = pedir_contrasena_nueva()
    if usuario.cambiar_contrasena(actual, nueva):
        UsuarioDAO.actualizar_contrasena(usuario)
        print("[ÉXITO] Contraseña actualizada.")
    else:
        print("La contraseña actual no es correcta.")


def configuracion_inicial() -> None:
    print("\nNo hay usuarios registrados. Cree la cuenta del administrador del sistema.")
    rut = pedir("RUT (ej. 12345678-5): ", Val.validar_rut)
    nombre = pedir("Nombre completo: ", texto_no_vacio("El nombre"))
    correo = pedir("Correo (Enter para omitir): ", Val.validar_email_opcional)
    salario = pedir("Salario base ($): ", lambda t: Val.validar_monto(t, "El salario"))
    admin = EmpleadoDAO.insertar(Administrador(rut=rut, nombre=nombre, correo=correo, salario_base=salario))
    try:
        crear_usuario_para(admin)
    except (ErrorPersistencia, ValueError):
        EmpleadoDAO.eliminar(admin.id)         
        raise
    print("[ÉXITO] Administrador creado. Inicie sesión.")


def iniciar_sesion():
    for intento in range(3):
        nombre_usuario = input("\nUsuario: ").strip()
        contrasena = getpass.getpass("Contraseña: ")
        usuario = UsuarioDAO.buscar_por_nombre(nombre_usuario)
        if usuario is not None and usuario.autenticar(contrasena):
            return EmpleadoDAO.buscar_por_id(usuario.empleado_id)
        print("Usuario o contraseña incorrectos.")        
    print("Demasiados intentos fallidos.")
    return None


def ver_mis_proyectos(sesion):
    cargar_proyectos_asignados(sesion)
    proyectos = sesion.ver_proyectos()
    print("Sus proyectos: " + ", ".join(proyectos) if proyectos else "No tiene proyectos asignados.")


def registrar_mis_horas(sesion):
    asignados = AsignacionDAO.proyectos_de_empleado(sesion.id)
    if not asignados:
        print("No tiene proyectos asignados; pida a un administrador que lo asigne.")
        return
    ids = {p.id: p for p in asignados}
    for p in asignados:
        print(f"  {p.id}) {p.nombre}")
    while True:
        id_proy = pedir("ID del proyecto: ", lambda t: Val.validar_entero_positivo(t, "El ID"))
        if id_proy in ids:
            break
        print("  -> Solo puede registrar horas en proyectos donde está asignado.")
    horas = pedir("Horas trabajadas: ", Val.validar_horas)
    fecha = pedir("Fecha (AAAA-MM-DD): ", Val.validar_fecha)
    registro = RegistroTiempoDAO.insertar(
        RegistroTiempo(id_empleado=sesion.id, id_proyecto=id_proy, horas=horas, fecha=fecha))
    print(f"[ÉXITO] Horas registradas con ID {registro.id}.")


def ver_mis_registros(sesion):
    propios = [r for r in RegistroTiempoDAO.listar() if r.id_empleado == sesion.id]
    print(f"Total de registros: {len(propios)}" if propios else "No tiene registros de tiempo.")
    for r in propios:
        print(r.mostrar_datos())


def menu_regular(sesion) -> None:
    while True:
        print(f"\n=== EcoTech - {sesion.nombre} (Empleado regular) ===")
        print("1. Ver mis proyectos")
        print("2. Registrar mis horas")
        print("3. Ver mis registros de tiempo")
        print("4. Cambiar mi contraseña")
        print("0. Salir")
        opcion = solicitar_opcion(4)
        if opcion == 0:
            print("\nSesión cerrada. ¡Hasta luego!")
            return
        acciones = {1: lambda: ver_mis_proyectos(sesion), 2: lambda: registrar_mis_horas(sesion),
                    3: lambda: ver_mis_registros(sesion), 4: lambda: cambiar_mi_contrasena(sesion)}
        ejecutar_accion(acciones[opcion])


def submenu(titulo: str, singular: str, acciones: dict) -> None:
    while True:
        print(f"\n--- {titulo} ---")
        print(f"1. Registrar {singular}")
        print("2. Listar")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = solicitar_opcion(5)
        if opcion == 0:
            return
        ejecutar_accion(acciones[opcion])


def menu_administrador(sesion: Administrador) -> None:
    while True:
        print("\n" + "=" * 55)
        print("   SISTEMA DE GESTIÓN CORPORATIVA ECOTECH SOLUTIONS")
        print(f"   Sesión: {sesion.nombre} (Administrador)")
        print("=" * 55)
        print("1. Gestionar Departamentos")
        print("2. Gestionar Empleados")
        print("3. Gestionar Proyectos")
        print("4. Gestionar Registros de Tiempo")
        print("5. Asignar / desasignar empleados a proyectos")
        print("6. Generar informes")
        print("7. Crear usuario para un empleado")
        print("8. Cambiar mi contraseña")
        print("0. Salir")
        opcion = solicitar_opcion(8)
        if opcion == 1:
            submenu("DEPARTAMENTOS", "departamento", {1: registrar_departamento, 2: listar_departamentos,
                    3: buscar_departamento, 4: actualizar_departamento, 5: eliminar_departamento})
        elif opcion == 2:
            submenu("EMPLEADOS", "empleado", {1: registrar_empleado, 2: listar_empleados,
                    3: buscar_empleado, 4: actualizar_empleado, 5: eliminar_empleado})
        elif opcion == 3:
            submenu("PROYECTOS", "proyecto", {1: registrar_proyecto, 2: listar_proyectos,
                    3: buscar_proyecto, 4: actualizar_proyecto, 5: eliminar_proyecto})
        elif opcion == 4:
            submenu("REGISTROS DE TIEMPO", "horas trabajadas", {1: registrar_horas, 2: listar_registros,
                    3: buscar_registro, 4: actualizar_registro, 5: eliminar_registro})
        elif opcion == 5:
            menu_asignaciones(sesion)
        elif opcion == 6:
            ejecutar_accion(generar_informe)
        elif opcion == 7:
            ejecutar_accion(crear_usuario_empleado)
        elif opcion == 8:
            ejecutar_accion(lambda: cambiar_mi_contrasena(sesion))
        else:
            print("\nSesión cerrada. ¡Hasta luego!")
            return


def arrancar_sesion() -> None:
    if UsuarioDAO.contar() == 0:
        configuracion_inicial()
    sesion = iniciar_sesion()
    if sesion is None:
        return
    if isinstance(sesion, Administrador):
        menu_administrador(sesion)
    else:
        menu_regular(sesion)


def main() -> None:
    try:
        crear_tablas()     
    except Exception:
        logging.exception("No se pudo preparar la base de datos")
        print("[ERROR] No se pudo conectar o preparar la base de datos.")
        print("Revise el archivo .env y que MySQL (WampServer) esté encendido, "
                "o cambie a DB_ENGINE=sqlite.")
        return
    try:
        ejecutar_accion(arrancar_sesion)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado por el usuario.")


if __name__ == "__main__":
    main()
