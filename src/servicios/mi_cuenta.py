from persistencia.empleadodao import EmpleadoDAO
from servicios.permisos import exigir_permiso


def actualizar_mis_datos(sesion, nombre: str, direccion: str, telefono: str, correo: str) -> None:
    """Solo modifica al empleado de la sesión. No toca salario, departamento, RUT ni rol."""
    exigir_permiso(sesion, "gestionar_mi_ficha")
    empleado = EmpleadoDAO.buscar_por_id(sesion.id)        # el ID sale de la sesión, no del teclado
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    empleado.nombre = nombre
    empleado.actualizar_datos(direccion, telefono, correo)
    if not EmpleadoDAO.actualizar(empleado):
        raise ValueError("No se pudo actualizar la ficha.")
    sesion.nombre = empleado.nombre
    sesion.actualizar_datos(empleado.direccion, empleado.telefono, empleado.correo)