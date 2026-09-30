from dominio.proyecto import Proyecto
from persistencia.conexion import abrir_conexion, marcador_sql


class ProyectoDAO:

    @staticmethod
    def _fila_a_proyecto(fila):
        if fila is None:
            return None
        return Proyecto(id=fila[0], nombre=fila[1], presupuesto=fila[2])

    @staticmethod
    def insertar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = f"INSERT INTO proyecto (nombre, presupuesto) VALUES ({marca}, {marca})"
            cursor.execute(sql, (proyecto.nombre, proyecto.presupuesto))
            proyecto.id = cursor.lastrowid
            conexion.commit()
            return proyecto
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            sql = "SELECT id, nombre, presupuesto FROM proyecto"
            cursor.execute(sql)
            filas = cursor.fetchall()

            proyectos = []
            for fila in filas:
                proyectos.append(ProyectoDAO._fila_a_proyecto(fila))
            return proyectos
        finally:
            if conexion:
                conexion.close()