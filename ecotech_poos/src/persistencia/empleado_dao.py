from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoDAO:

    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
            INSERT INTO empleado (nombre, correo)
            VALUES ({marcador}, {marcador})
        """
        cursor.execute(sql, (empleado.nombre, empleado.correo))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def obtener_todos():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, correo FROM empleado")
        filas = cursor.fetchall()
        conexion.close()
        return filas