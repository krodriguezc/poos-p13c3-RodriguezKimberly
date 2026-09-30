from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql


class EmpleadoDAO:

    @staticmethod
    def _fila_a_empleado(fila):
        if fila is None:
            return None
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2])

    @staticmethod
    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = f"INSERT INTO empleado (nombre, correo) VALUES ({marca}, {marca})"
            cursor.execute(sql, (empleado.nombre, empleado.correo))
            empleado.id = cursor.lastrowid
            conexion.commit()
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = f"SELECT id, nombre, correo FROM empleado WHERE id = {marca}"
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            return EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            sql = "SELECT id, nombre, correo FROM empleado"
            cursor.execute(sql)
            filas = cursor.fetchall()

            empleados = []
            for fila in filas:
                empleados.append(EmpleadoDAO._fila_a_empleado(fila))
            return empleados
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_correo(correo):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = f"SELECT id, nombre, correo FROM empleado WHERE correo = {marca}"
            cursor.execute(sql, (correo,))
            fila = cursor.fetchone()
            return EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = (
                f"UPDATE empleado SET nombre = {marca}, correo = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(sql, (empleado.nombre, empleado.correo, empleado.id))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = f"DELETE FROM empleado WHERE id = {marca}"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()
