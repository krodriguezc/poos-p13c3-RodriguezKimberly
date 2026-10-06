from dominio.proyecto import Proyecto
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion


class ProyectoDAO(BaseDAO):
    @staticmethod
    def _fila_a_proyecto(fila) -> Proyecto:
        return Proyecto(nombre=fila[1], presupuesto=fila[2], id=fila[0])

    @staticmethod
    def insertar(proyecto: Proyecto) -> Proyecto:
        m = Conexion.marcador_sql()
        _, nuevo_id = ProyectoDAO.ejecutar_escritura(
            f"INSERT INTO proyecto (nombre, presupuesto) VALUES ({m}, {m})",
            (proyecto.nombre, proyecto.presupuesto))
        proyecto.id = nuevo_id
        return proyecto

    @staticmethod
    def listar() -> list:
        filas = ProyectoDAO.ejecutar_consulta("SELECT id, nombre, presupuesto FROM proyecto ORDER BY id")
        return [ProyectoDAO._fila_a_proyecto(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_proyecto: int):
        m = Conexion.marcador_sql()
        fila = ProyectoDAO.ejecutar_consulta(
            f"SELECT id, nombre, presupuesto FROM proyecto WHERE id = {m}", (id_proyecto,), uno=True)
        return None if fila is None else ProyectoDAO._fila_a_proyecto(fila)

    @staticmethod
    def actualizar(proyecto: Proyecto) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = ProyectoDAO.ejecutar_escritura(
            f"UPDATE proyecto SET nombre = {m}, presupuesto = {m} WHERE id = {m}",
            (proyecto.nombre, proyecto.presupuesto, proyecto.id))
        return filas > 0

    @staticmethod
    def eliminar(id_proyecto: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = ProyectoDAO.ejecutar_escritura(
            f"DELETE FROM proyecto WHERE id = {m}", (id_proyecto,))
        return filas > 0
