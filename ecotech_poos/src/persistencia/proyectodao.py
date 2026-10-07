from dominio.proyecto import Proyecto
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion
from persistencia.registrotiempodao import RegistroTiempoDAO

COLUMNAS = "id, nombre, descripcion, fecha_inicio, presupuesto"


class ProyectoDAO(BaseDAO):
    @staticmethod
    def fila_a_proyecto(fila) -> Proyecto:
        return Proyecto(nombre=fila[1], descripcion=fila[2] or "", fecha_inicio=str(fila[3]),
                        presupuesto=float(fila[4]), id=fila[0])

    @staticmethod
    def insertar(proyecto: Proyecto) -> Proyecto:
        m = Conexion.marcador_sql()
        _, nuevo_id = ProyectoDAO.ejecutar_escritura(
            f"INSERT INTO proyecto (nombre, descripcion, fecha_inicio, presupuesto) VALUES ({m}, {m}, {m}, {m})",
            (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.presupuesto))
        proyecto.id = nuevo_id
        return proyecto

    @staticmethod
    def listar() -> list:
        filas = ProyectoDAO.ejecutar_consulta(f"SELECT {COLUMNAS} FROM proyecto ORDER BY id")
        return [ProyectoDAO.fila_a_proyecto(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_proyecto: int):
        m = Conexion.marcador_sql()
        fila = ProyectoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM proyecto WHERE id = {m}", (id_proyecto,), uno=True)
        return None if fila is None else ProyectoDAO.fila_a_proyecto(fila)

    @staticmethod
    def cargar_registros(proyecto: Proyecto) -> Proyecto:
        """Llena la composición Proyecto 1 — 0..* RegistroTiempo desde la BD."""
        for registro in RegistroTiempoDAO.listar_por_proyecto(proyecto.id):
            proyecto.agregar_registro_tiempo(registro)
        return proyecto

    @staticmethod
    def actualizar(proyecto: Proyecto) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = ProyectoDAO.ejecutar_escritura(
            f"UPDATE proyecto SET nombre = {m}, descripcion = {m}, presupuesto = {m} WHERE id = {m}",
            (proyecto.nombre, proyecto.descripcion, proyecto.presupuesto, proyecto.id))
        return filas > 0

    @staticmethod
    def eliminar(id_proyecto: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = ProyectoDAO.ejecutar_escritura(
            f"DELETE FROM proyecto WHERE id = {m}", (id_proyecto,))
        return filas > 0