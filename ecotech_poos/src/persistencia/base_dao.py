import logging

from persistencia.conexion import Conexion
from persistencia.excepciones import ErrorConexion, ErrorIntegridad, ErrorPersistencia

logger = logging.getLogger(__name__)


class BaseDAO:
    @staticmethod
    def ejecutar_escritura(sql: str, parametros: tuple = ()):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)         
            conexion.commit()
            return cursor.rowcount, cursor.lastrowid
        except ErrorConexion:
            raise                                
        except Conexion.errores_integridad() as error:
            if conexion:
                conexion.rollback()
            logger.error("Violación de integridad: %s", error, exc_info=True)
            raise ErrorIntegridad("Los datos violan una restricción de la base de datos.") from error
        except Exception as error:
            if conexion:
                conexion.rollback()
            logger.error("Error al escribir en la BD: %s", error, exc_info=True)
            raise ErrorPersistencia("No fue posible completar la operación.") from error
        finally:
            Conexion.cerrar_conexion(conexion)

    @staticmethod
    def ejecutar_consulta(sql: str, parametros: tuple = (), uno: bool = False):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            return cursor.fetchone() if uno else cursor.fetchall()
        except ErrorConexion:
            raise
        except Exception as error:
            logger.error("Error al consultar la BD: %s", error, exc_info=True)
            raise ErrorPersistencia("No fue posible consultar la información.") from error
        finally:
            Conexion.cerrar_conexion(conexion)
