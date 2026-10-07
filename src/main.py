import getpass
import logging
import os
import sys
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dominio.departamento import Departamento
from dominio.empleado import Administrador, EmpleadoRegular
from dominio.informe import Informe
from dominio.proyecto import Proyecto
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

# hace que los errores vayan al archivo de log y no a la pantalla del usuario.
logging.basicConfig(filename="ecotech_errores.log", level=logging.ERROR,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")


# entrada de datos
def hoy() -> str:
    return date.today().isoformat()

#valida el rango y da ValueError
def solicitar_opcion(maximo: int) -> int:
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if 0 <= opcion <= maximo:
                return opcion
            print(f"Opción fuera de rango (0-{maximo}).")
        except ValueError:
            print("Debe ingresar un número.")

#Aqui repite la pregunta, hasta que sea valido
def pedir(mensaje: str, validador, actual=None):
    while True:
        texto = input(mensaje).strip()
        if texto == "" and actual is not None:
            return actual
        try:
            return validador(texto)
        except ValueError as error:
            print(f"  -> {error}")

#Aqui pide el id y comprueba si existe
def pedir_id_existente(mensaje: str, buscador, entidad: str, opcional: bool = False, por_defecto=None):
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return por_defecto
        try:
            id_ = Val.validar_entero_positivo(texto, "El ID")
        except ValueError as error:
            print(f"  -> {error}")
            continue
        if buscador(id_) is not None:
            return id_
        print(f"  -> No existe {entidad} con ID {id_}.")


def pedir_id(mensaje: str) -> int:
    return pedir(mensaje, lambda t: Val.validar_entero_positivo(t, "El ID"))


def confirmar(mensaje: str) -> bool:
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def texto_no_vacio(campo: str):
    return lambda t: Val.validar_texto_no_vacio(t, campo)


def monto(campo: str):
    return lambda t: Val.validar_monto(t, campo)


# permisos y errores
def exigir_permiso(sesion, permiso: str) -> None:
    if not sesion.tiene_permiso(permiso):
        raise PermissionError(permiso)


def con_permiso(sesion, permiso: str, accion):
    def accion_protegida():
        exigir_permiso(sesion, permiso)
        accion()
    return accion_protegida

#Aqui se traducen las excepciones en mensajes seguros 
def ejecutar_accion(accion) -> None:
    try:
        accion()
    except PermissionError:
        print("[ACCESO DENEGADO] Su rol no tiene permiso para esta acción.")
    except ValueError as error:            # validación del dominio
        print(f"[DATO INVÁLIDO] {error}")
    except ErrorConexion:
        print("[ERROR] No se pudo conectar a la base de datos. "
            "Revise que MySQL (WampServer) esté encendido y que el archivo .env sea correcto.")
    except ErrorIntegridad:
        print("[ERROR] No se pudo guardar: ya existe un registro con esos datos "
            "o hace referencia a algo que no existe.")
    except ErrorPersistencia:
        print("[ERROR] No fue posible completar la operación. Intente nuevamente.")
    except Exception:                      
        logging.exception("Error inesperado")
        print("[ERROR] Ocurrió un error inesperado. El detalle quedó registrado en ecotech_errores.log.")

# departamentos
def registrar_departamento():
    nombre = pedir("Nombre del departamento: ", texto_no_vacio("El nombre"))
    gerente_id = pedir_id_existente("ID del gerente (Enter = sin gerente): ",
                                    EmpleadoDAO.buscar_por_id, "un empleado", opcional=True)
    gerente = EmpleadoDAO.buscar_por_id(gerente_id) if gerente_id else None
    departamento = DepartamentoDAO.insertar(Departamento(nombre=nombre, gerente=gerente))
    print(f"[ÉXITO] Departamento guardado con ID {departamento.id}.")


def mostrar_departamento(d: Departamento) -> None:
    DepartamentoDAO.cargar_empleados(d)                  # llena la colección de empleados desde la BD
    print(f"{d.mostrar_datos()} | Empleados: {d.cantidad_empleados()}")
    for e in d.empleados:
        print(f"    - {e.nombre} ({e.tipo})")


def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("No hay departamentos registrados.")
    for d in departamentos:
        mostrar_departamento(d)


def buscar_departamento():
    d = DepartamentoDAO.buscar_por_id(pedir_id("ID a buscar: "))
    mostrar_departamento(d) if d else print("Departamento no encontrado.")


def actualizar_departamento():
    id_ = pedir_id_existente("ID del departamento a actualizar: ", DepartamentoDAO.buscar_por_id, "un departamento")
    d = DepartamentoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    d.nombre = pedir(f"Nombre [{d.nombre}]: ", texto_no_vacio("El nombre"), actual=d.nombre)
    actual_id = d.gerente.id if d.gerente else None
    gerente_id = pedir_id_existente(f"ID del gerente [{actual_id or 'ninguno'}]: ", EmpleadoDAO.buscar_por_id,
                                    "un empleado", opcional=True, por_defecto=actual_id)
    d.gerente = EmpleadoDAO.buscar_por_id(gerente_id) if gerente_id else None
    print("[ÉXITO] Departamento actualizado." if DepartamentoDAO.actualizar(d) else "Departamento no encontrado.")


def eliminar_departamento():
    id_ = pedir_id("ID del departamento a eliminar: ")
    if not confirmar("Sus empleados quedarán sin departamento. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Departamento eliminado." if DepartamentoDAO.eliminar(id_) else "No existe un departamento con ese ID.")


# empleados
def pedir_datos_empleado() -> dict:
    return dict(
        rut=pedir("RUT (ej. 12345678-5): ", Val.validar_rut),
        nombre=pedir("Nombre completo: ", texto_no_vacio("El nombre")),
        correo=pedir("Correo (Enter para omitir): ", Val.validar_email_opcional),
        direccion=pedir("Dirección: ", texto_no_vacio("La dirección")),
        telefono=pedir("Teléfono (ej. +56912345678): ", Val.validar_telefono),
        fecha_inicio_contrato=pedir(f"Inicio de contrato AAAA-MM-DD [{hoy()}]: ", Val.validar_fecha, actual=hoy()),
        salario_base=pedir("Salario base ($): ", monto("El salario")),
    )


def registrar_empleado():
    print("Tipo de empleado: 1) Regular  2) Administrador")
    tipo = pedir("Tipo: ", lambda t: Val.validar_entero_positivo(t, "El tipo"))
    if tipo not in (1, 2):
        print("[DATO INVÁLIDO] Tipo de empleado no válido.")
        return
    datos = pedir_datos_empleado()
    dep_id = pedir_id_existente("ID del departamento (Enter = sin departamento): ",
                                DepartamentoDAO.buscar_por_id, "un departamento", opcional=True)
    clase = EmpleadoRegular if tipo == 1 else Administrador
    empleado = EmpleadoDAO.insertar(clase(**datos, departamento_id=dep_id))
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
    e = EmpleadoDAO.buscar_por_id(pedir_id("ID a buscar: "))
    print(e.mostrar_datos() if e else "Empleado no encontrado.")


def actualizar_empleado():
    id_ = pedir_id_existente("ID del empleado a actualizar: ", EmpleadoDAO.buscar_por_id, "un empleado")
    e = EmpleadoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    e.nombre = pedir(f"Nombre [{e.nombre}]: ", texto_no_vacio("El nombre"), actual=e.nombre)
    direccion = pedir(f"Dirección [{e.direccion}]: ", texto_no_vacio("La dirección"), actual=e.direccion)
    telefono = pedir(f"Teléfono [{e.telefono}]: ", Val.validar_telefono, actual=e.telefono)
    correo = pedir(f"Correo [{e.correo}]: ", Val.validar_email_opcional, actual=e.correo)
    e.actualizar_datos(direccion, telefono, correo)                 # ActualizarDatos() del UML
    e.salario_base = pedir(f"Salario base [{e.salario_base}]: ", monto("El salario"), actual=e.salario_base)
    print("[ÉXITO] Empleado actualizado." if EmpleadoDAO.actualizar(e) else "Empleado no encontrado.")


def eliminar_empleado():
    id_ = pedir_id("ID del empleado a eliminar: ")
    if not confirmar("Se eliminarán también sus registros de tiempo. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Empleado eliminado." if EmpleadoDAO.eliminar(id_) else "No existe un empleado con ese ID.")


# proyectos
def registrar_proyecto():
    nombre = pedir("Nombre del proyecto: ", texto_no_vacio("El nombre"))
    descripcion = pedir("Descripción (Enter para omitir): ", Val.validar_texto_opcional)
    fecha = pedir(f"Fecha de inicio AAAA-MM-DD [{hoy()}]: ", Val.validar_fecha, actual=hoy())
    presupuesto = pedir("Presupuesto ($): ", monto("El presupuesto"))
    proyecto = ProyectoDAO.insertar(Proyecto(nombre=nombre, presupuesto=presupuesto,
                                            descripcion=descripcion, fecha_inicio=fecha))
    print(f"[ÉXITO] Proyecto guardado con ID {proyecto.id}.")


def mostrar_proyecto(p: Proyecto) -> None:
    ProyectoDAO.cargar_registros(p)                      # llena la composición de registros desde la BD
    print(f"{p.mostrar_datos()} | Registros: {len(p.registros)} | Horas totales: {p.total_horas()}")


def listar_proyectos():
    proyectos = ProyectoDAO.listar()
    if not proyectos:
        print("No hay proyectos registrados.")
    for p in proyectos:
        mostrar_proyecto(p)


def buscar_proyecto():
    p = ProyectoDAO.buscar_por_id(pedir_id("ID a buscar: "))
    mostrar_proyecto(p) if p else print("Proyecto no encontrado.")


def actualizar_proyecto():
    id_ = pedir_id_existente("ID del proyecto a actualizar: ", ProyectoDAO.buscar_por_id, "un proyecto")
    p = ProyectoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    nombre = pedir(f"Nombre [{p.nombre}]: ", texto_no_vacio("El nombre"), actual=p.nombre)
    descripcion = pedir(f"Descripción [{p.descripcion}]: ", Val.validar_texto_opcional, actual=p.descripcion)
    p.editar(nombre, descripcion)                                   
    p.presupuesto = pedir(f"Presupuesto [{p.presupuesto}]: ", monto("El presupuesto"), actual=p.presupuesto)
    print("[ÉXITO] Proyecto actualizado." if ProyectoDAO.actualizar(p) else "Proyecto no encontrado.")


def eliminar_proyecto():
    id_ = pedir_id("ID del proyecto a eliminar: ")
    if not confirmar("Se eliminarán también sus registros de tiempo. ¿Eliminar?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Proyecto eliminado." if ProyectoDAO.eliminar(id_) else "No existe un proyecto con ese ID.")


# registros de tiempo, donde se registran las horas trabajadas por los empleados
def registrar_horas_para(empleado) -> None:
    asignados = AsignacionDAO.proyectos_de_empleado(empleado.id)
    if not asignados:
        print(f"{empleado.nombre} no tiene proyectos asignados; un administrador debe asignarlo primero.")
        return
    print("Proyectos asignados:")
    for p in asignados:
        print(f"  {p.id}) {p.nombre}")
    ids_validos = {p.id for p in asignados}
    while True:
        id_proy = pedir_id("ID del proyecto: ")
        if id_proy in ids_validos:
            break
        print("  -> Solo puede registrar horas en un proyecto donde está asignado.")
    horas = pedir("Horas trabajadas: ", Val.validar_horas)
    fecha = pedir(f"Fecha AAAA-MM-DD [{hoy()}]: ", Val.validar_fecha, actual=hoy())
    tarea = pedir("Descripción de la tarea: ", texto_no_vacio("La descripción"))
    registro = empleado.registrar_horas(id_proy, horas, fecha, tarea)   # RegistrarHoras() crea el registro
    RegistroTiempoDAO.insertar(registro)
    print(f"[ÉXITO] Horas registradas con ID {registro.id}.")


def registrar_horas_de_empleado():
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    registrar_horas_para(EmpleadoDAO.buscar_por_id(id_emp))


def listar_registros():
    registros = RegistroTiempoDAO.listar()
    if not registros:
        print("No hay registros de tiempo.")
        return
    empleados = {e.id: e.nombre for e in EmpleadoDAO.listar()}
    proyectos = {p.id: p.nombre for p in ProyectoDAO.listar()}
    for r in registros:
        print(f"ID: {r.id} | {r.fecha} | {empleados.get(r.id_empleado, '?')} -> "
            f"{proyectos.get(r.id_proyecto, '?')} | {r.horas} hrs | {r.descripcion_tarea}")


def buscar_registro():
    r = RegistroTiempoDAO.buscar_por_id(pedir_id("ID a buscar: "))
    print(r.mostrar_datos() if r else "Registro no encontrado.")


def actualizar_registro():
    id_ = pedir_id_existente("ID del registro a actualizar: ", RegistroTiempoDAO.buscar_por_id, "un registro")
    r = RegistroTiempoDAO.buscar_por_id(id_)
    print("(Enter conserva el valor actual)")
    r.horas = pedir(f"Horas [{r.horas}]: ", Val.validar_horas, actual=r.horas)
    r.fecha = pedir(f"Fecha [{r.fecha}]: ", Val.validar_fecha, actual=r.fecha)
    r.descripcion_tarea = pedir(f"Tarea [{r.descripcion_tarea}]: ", texto_no_vacio("La descripción"),
                                actual=r.descripcion_tarea)
    print("[ÉXITO] Registro actualizado." if RegistroTiempoDAO.actualizar(r) else "Registro no encontrado.")


def eliminar_registro():
    id_ = pedir_id("ID del registro a eliminar: ")
    if not confirmar("¿Eliminar el registro?"):
        print("Operación cancelada.")
        return
    print("[ÉXITO] Registro eliminado." if RegistroTiempoDAO.eliminar(id_) else "No existe un registro con ese ID.")


# asignaciones del administrador
def cargar_proyectos_asignados(empleado) -> None:
    for proyecto in AsignacionDAO.proyectos_de_empleado(empleado.id):
        empleado.agregar_proyecto(proyecto)


def asignar_empleado(sesion):
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    empleado, proyecto = EmpleadoDAO.buscar_por_id(id_emp), ProyectoDAO.buscar_por_id(id_proy)
    cargar_proyectos_asignados(empleado)
    if not sesion.asignar_empleado_proyecto(empleado, proyecto):    
        print("Ese empleado ya está asignado a ese proyecto.")
        return
    AsignacionDAO.asignar(empleado.id, proyecto.id)                 # persistencia
    print(f"[ÉXITO] {empleado.nombre} asignado a {proyecto.nombre}.")


def desasignar_empleado(sesion):
    id_emp = pedir_id_existente("ID del empleado: ", EmpleadoDAO.buscar_por_id, "un empleado")
    id_proy = pedir_id_existente("ID del proyecto: ", ProyectoDAO.buscar_por_id, "un proyecto")
    empleado, proyecto = EmpleadoDAO.buscar_por_id(id_emp), ProyectoDAO.buscar_por_id(id_proy)
    cargar_proyectos_asignados(empleado)
    if not sesion.desasignar_empleado_de_proyecto(empleado, proyecto):
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


def menu_asignaciones(sesion) -> None:
    while True:
        print("\n--- ASIGNACIONES EMPLEADO-PROYECTO ---")
        print("1. Asignar empleado a proyecto")
        print("2. Desasignar empleado de proyecto")
        print("3. Ver empleados de un proyecto")
        print("0. Volver")
        opcion = solicitar_opcion(3)
        if opcion == 0:
            return
        acciones = {1: lambda: asignar_empleado(sesion), 2: lambda: desasignar_empleado(sesion),
                    3: listar_asignados}
        ejecutar_accion(con_permiso(sesion, "asignar_empleados", acciones[opcion]))


# informes
def generar_informe():
    print("Tipos: " + ", ".join(Informe.TIPOS))
    tipo = pedir("Tipo de informe: ", Informe.validar_tipo)
    informe = Informe(tipo)
    print()
    print(informe.generar_informe(tipo, EmpleadoDAO.listar(), ProyectoDAO.listar(),
                                    DepartamentoDAO.listar(), RegistroTiempoDAO.listar()))


#  usuarios y sesión
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
    usuario = Usuario(nombre_usuario=nombre_usuario, empleado=empleado)
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

#Es la primera ejecucion donde se hace la cuenta de administrador
def configuracion_inicial() -> None:
    print("\nNo hay usuarios registrados. Cree la cuenta del administrador del sistema.")
    admin = EmpleadoDAO.insertar(Administrador(**pedir_datos_empleado()))
    try:
        crear_usuario_para(admin)
    except (ErrorPersistencia, ValueError):
        EmpleadoDAO.eliminar(admin.id)         # si falla el usuario, el empleado sigue 
        raise
    print("[ÉXITO] Administrador creado. Inicie sesión.")

#Devuelve el Empleado autenticado o None tras 3 intentos fallidos
def iniciar_sesion():
    for _ in range(3):
        nombre_usuario = input("\nUsuario: ").strip()
        contrasena = getpass.getpass("Contraseña: ")
        usuario = UsuarioDAO.buscar_por_nombre(nombre_usuario)
        if usuario is not None and usuario.autenticar(contrasena):
            return usuario.empleado
        print("Usuario o contraseña incorrectos.")        #  no revela cuál falló en el mensaje
    print("Demasiados intentos fallidos.")
    return None


# menú del empleado regular
def ver_mis_proyectos(sesion):
    cargar_proyectos_asignados(sesion)
    proyectos = sesion.ver_proyectos()
    print("Sus proyectos: " + ", ".join(proyectos) if proyectos else "No tiene proyectos asignados.")


def ver_mis_registros(sesion):
    EmpleadoDAO.cargar_registros(sesion)                 # llena la colección del empleado desde la BD
    if not sesion.registros_tiempo:
        print("No tiene registros de tiempo.")
        return
    for r in sesion.registros_tiempo:
        print(r.mostrar_datos())
    print(f"Total de horas: {sesion.total_horas()}")


def menu_regular(sesion) -> None:
    while True:
        print(f"\n=== EcoTech - {sesion.nombre} ({sesion.tipo.capitalize()}) ===")
        print("1. Ver mis proyectos")
        print("2. Registrar mis horas")
        print("3. Ver mis registros de tiempo")
        print("4. Cambiar mi contraseña")
        print("0. Salir")
        opcion = solicitar_opcion(4)
        if opcion == 0:
            print("\nSesión cerrada. ¡Hasta luego!")
            return
        acciones = {1: ("ver_proyectos", lambda: ver_mis_proyectos(sesion)),
                    2: ("registrar_horas", lambda: registrar_horas_para(sesion)),
                    3: ("ver_proyectos", lambda: ver_mis_registros(sesion)),
                    4: ("cambiar_contrasena", lambda: cambiar_mi_contrasena(sesion))}
        permiso, accion = acciones[opcion]
        ejecutar_accion(con_permiso(sesion, permiso, accion))


# menú del administrador
def submenu(sesion, titulo: str, singular: str, acciones: dict) -> None:
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
        ejecutar_accion(con_permiso(sesion, "gestionar_datos", acciones[opcion]))


def menu_administrador(sesion) -> None:
    while True:
        print("\n" + "=" * 55)
        print("   SISTEMA DE GESTIÓN CORPORATIVA ECOTECH SOLUTIONS")
        print(f"   Sesión: {sesion.nombre} ({sesion.tipo.capitalize()})")
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
            submenu(sesion, "DEPARTAMENTOS", "departamento", {1: registrar_departamento, 2: listar_departamentos,
                    3: buscar_departamento, 4: actualizar_departamento, 5: eliminar_departamento})
        elif opcion == 2:
            submenu(sesion, "EMPLEADOS", "empleado", {1: registrar_empleado, 2: listar_empleados,
                    3: buscar_empleado, 4: actualizar_empleado, 5: eliminar_empleado})
        elif opcion == 3:
            submenu(sesion, "PROYECTOS", "proyecto", {1: registrar_proyecto, 2: listar_proyectos,
                    3: buscar_proyecto, 4: actualizar_proyecto, 5: eliminar_proyecto})
        elif opcion == 4:
            submenu(sesion, "REGISTROS DE TIEMPO", "horas trabajadas", {1: registrar_horas_de_empleado,
                    2: listar_registros, 3: buscar_registro, 4: actualizar_registro, 5: eliminar_registro})
        elif opcion == 5:
            menu_asignaciones(sesion)
        elif opcion == 6:
            ejecutar_accion(con_permiso(sesion, "generar_informes", generar_informe))
        elif opcion == 7:
            ejecutar_accion(con_permiso(sesion, "gestionar_usuarios", crear_usuario_empleado))
        elif opcion == 8:
            ejecutar_accion(con_permiso(sesion, "cambiar_contrasena", lambda: cambiar_mi_contrasena(sesion)))
        else:
            print("\nSesión cerrada. ¡Hasta luego!")
            return

#Login y menu segun los permisos del rol
def arrancar_sesion() -> None:
    if UsuarioDAO.contar() == 0:
        configuracion_inicial()
    sesion = iniciar_sesion()
    if sesion is None:
        return
    print(f"\nBienvenido/a, {sesion.nombre}. Permisos de su rol: {', '.join(sesion.obtener_permisos())}")
    if sesion.tiene_permiso("gestionar_datos"):
        menu_administrador(sesion)
    else:
        menu_regular(sesion)


def main() -> None:
    try:
        crear_tablas()     # deja la BD lista 
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