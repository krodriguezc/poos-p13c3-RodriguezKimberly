from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql


class EmpleadoDAO:

    @staticmethod
    def _fila_a_empleado(fila):
        """Transforma una tupla de la BD en un objeto Empleado (evita duplicar código)"""
        if fila is None:
            return None
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2])

    @staticmethod
    def insertar(empleado: Empleado) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"INSERT INTO empleado (nombre, correo) VALUES ({marca}, {marca})"
        cursor.execute(sql, (empleado.nombre, empleado.correo))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado: int):
        """Busca un empleado por su ID y retorna un objeto Empleado o None"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"SELECT id, nombre, correo FROM empleado WHERE id = {marca}"
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        conexion.close()

        return EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def listar():
        """Recupera todos los registros y retorna una lista de objetos Empleado"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sql = "SELECT id, nombre, correo FROM empleado"
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()

        empleados = []
        for fila in filas:
            empleados.append(EmpleadoDAO._fila_a_empleado(fila))
        return empleados

    @staticmethod
    def buscar_por_correo(correo: str):
        """Mini desafío Clase 5: Búsqueda parametrizada por correo"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"SELECT id, nombre, correo FROM empleado WHERE correo = {marca}"
        cursor.execute(sql, (correo,))
        fila = cursor.fetchone()
        conexion.close()

        return EmpleadoDAO._fila_a_empleado(fila)