import logging

from persistencia.conexion import Conexion
from persistencia.excepciones import ErrorConexion, ErrorIntegridad, ErrorPersistencia

logger = logging.getLogger(__name__)


class BaseDAO:
    @staticmethod
    def ejecutar_transaccion(operaciones: list) -> list:
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            resultados = []
            for sql, parametros in operaciones:
                cursor.execute(sql, parametros)          # los valores viajan separados del SQL
                resultados.append((cursor.rowcount, cursor.lastrowid))
            conexion.commit()
            return resultados
        except ErrorConexion:
            raise                                        # ya viene con mensaje propio
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
    def ejecutar_escritura(sql: str, parametros: tuple = ()):
        """INSERT / UPDATE / DELETE. Devuelve (filas_afectadas, ultimo_id)."""
        return BaseDAO.ejecutar_transaccion([(sql, parametros)])[0]

    @staticmethod
    def ejecutar_consulta(sql: str, parametros: tuple = (), uno: bool = False):
        """SELECT. Devuelve una fila (o None) si uno=True; si no, la lista de filas."""
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