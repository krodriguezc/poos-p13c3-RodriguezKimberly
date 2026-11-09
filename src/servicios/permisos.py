from dominio.empleado import Empleado


def exigir_sesion(sesion) -> None:
    """La sesión es el Empleado autenticado. Si no hay sesión válida, se rechaza antes de tocar la BD o la API."""
    if not isinstance(sesion, Empleado) or type(sesion.id) is not int or sesion.id <= 0:
        raise PermissionError("Inicie sesión.")


def exigir_permiso(sesion, permiso: str) -> None:
    exigir_sesion(sesion)
    if not sesion.tiene_permiso(permiso):
        raise PermissionError(permiso)