class ErrorPersistencia(Exception):
    """Fallo al leer o escribir en la base de datos."""


class ErrorConexion(ErrorPersistencia):
    """No fue posible conectarse a la base de datos."""


class ErrorIntegridad(ErrorPersistencia):
    """Una restricción de la BD rechazó los datos (RUT repetido, referencia inexistente...)."""
