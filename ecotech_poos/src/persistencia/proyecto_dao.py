from persistencia.conexion import abrir_conexion, obtener_motor

class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
            INSERT INTO proyecto (nombre, presupuesto)
            VALUES ({marcador}, {marcador})
        """
        cursor.execute(sql, (proyecto.nombre, proyecto.presupuesto))
        proyecto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return proyecto

    @staticmethod
    def obtener_todos():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, presupuesto FROM proyecto")
        filas = cursor.fetchall()
        conexion.close()
        return filas