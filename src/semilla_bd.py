import getpass
import os
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Administrador, EmpleadoRegular
from dominio.proyecto import Proyecto
from dominio.usuario import Usuario
from persistencia.asignaciondao import AsignacionDAO
from persistencia.crearbd import crear_tablas
from persistencia.departamentodao import DepartamentoDAO
from persistencia.empleadodao import EmpleadoDAO
from persistencia.proyectodao import ProyectoDAO
from persistencia.registrotiempodao import RegistroTiempoDAO
from persistencia.usuariodao import UsuarioDAO
from persistencia.excepciones import ErrorConexion, ErrorPersistencia


def _clave(variable: str, quien: str) -> str:
    """La contraseña viene del .env o se pide por teclado; nunca está escrita en el código."""
    return os.getenv(variable) or getpass.getpass(f"Contraseña inicial de {quien} (mín. 8 caracteres): ")


def _empleado(clase, rut, nombre, correo, telefono, salario, departamento_id=None):
    for existente in EmpleadoDAO.listar():
        if existente.rut == rut:
            print(f"[SEMILLA] Empleado '{nombre}' ya existe (ID {existente.id}).")
            return existente
    empleado = EmpleadoDAO.insertar(clase(
        rut=rut, nombre=nombre, correo=correo, direccion="Oficina Central", telefono=telefono,
        fecha_inicio_contrato=date.today().isoformat(), salario_base=salario, departamento_id=departamento_id))
    print(f"[SEMILLA] Empleado '{nombre}' creado (ID {empleado.id}).")
    return empleado


def _usuario(nombre_usuario, empleado, variable_clave):
    if UsuarioDAO.buscar_por_nombre(nombre_usuario) or UsuarioDAO.buscar_por_empleado(empleado.id):
        print(f"[SEMILLA] Usuario de '{empleado.nombre}' ya existe; no se modifica.")
        return
    usuario = Usuario(nombre_usuario=nombre_usuario, empleado=empleado)
    usuario.establecer_contrasena(_clave(variable_clave, f"'{nombre_usuario}'"))
    UsuarioDAO.insertar(usuario)
    print(f"[SEMILLA] Usuario '{nombre_usuario}' creado.")


def ejecutar_semilla():
    print("Iniciando la semilla de la base de datos.")
    crear_tablas()

    admin = _empleado(Administrador, "11111111-1", "Administrador Sistema", "admin@ecotech.cl",
                    "+56911111111", 1500000.0)

    departamento = next((d for d in DepartamentoDAO.listar() if d.nombre == "Desarrollo"), None)
    if departamento is None:
        departamento = DepartamentoDAO.insertar(Departamento(nombre="Desarrollo", gerente=admin))
        print(f"[SEMILLA] Departamento 'Desarrollo' creado (ID {departamento.id}).")

    ana = _empleado(EmpleadoRegular, "20123456-5", "Ana Torres", "ana@ecotech.cl",
                    "+56922222222", 1000000.0, departamento.id)
    bruno = _empleado(EmpleadoRegular, "21234567-9", "Bruno Soto", "bruno@ecotech.cl",
                    "+56933333333", 950000.0, departamento.id)

    proyecto = next((p for p in ProyectoDAO.listar() if p.nombre == "EcoSolar"), None)
    if proyecto is None:
        proyecto = ProyectoDAO.insertar(Proyecto(nombre="EcoSolar", presupuesto=5000000.0,
                                                descripcion="Paneles solares", fecha_inicio=date.today().isoformat()))
        print(f"[SEMILLA] Proyecto 'EcoSolar' creado (ID {proyecto.id}).")

    for empleado, horas, tarea in ((ana, 8, "Instalación de paneles"), (bruno, 6, "Revisión de planos")):
        if not AsignacionDAO.existe(empleado.id, proyecto.id):
            AsignacionDAO.asignar(empleado.id, proyecto.id)
        if not RegistroTiempoDAO.listar_por_empleado(empleado.id):
            registro = empleado.registrar_horas(proyecto.id, horas, date.today().isoformat(), tarea)
            RegistroTiempoDAO.insertar(registro)

    _usuario("admin", admin, "ADMIN_CLAVE_INICIAL")
    _usuario("ana.torres", ana, "ANA_CLAVE_INICIAL")
    _usuario("bruno.soto", bruno, "BRUNO_CLAVE_INICIAL")
    print("[SEMILLA] Proceso finalizado. Puede repetirse sin duplicar datos.")


if __name__ == "__main__":
    try:
        ejecutar_semilla()
    except ErrorConexion:
        print("[ERROR] No se pudo conectar a la base de datos. Revise DB_ENGINE en el .env "
            "y, si usa MySQL, que WampServer esté en verde.")
    except (ErrorPersistencia, ValueError) as error:
        print(f"[ERROR] No se pudo completar la semilla: {error}")