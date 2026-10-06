from dominio.departamento import Departamento
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion


class DepartamentoDAO(BaseDAO):
    @staticmethod
    def _fila_a_departamento(fila) -> Departamento:
        return Departamento(nombre=fila[1], id=fila[0])

    @staticmethod
    def insertar(departamento: Departamento) -> Departamento:
        m = Conexion.marcador_sql()
        _, nuevo_id = DepartamentoDAO.ejecutar_escritura(
            f"INSERT INTO departamento (nombre) VALUES ({m})", (departamento.nombre,))
        departamento.id = nuevo_id                      
        return departamento

    @staticmethod
    def listar() -> list:
        filas = DepartamentoDAO.ejecutar_consulta("SELECT id, nombre FROM departamento ORDER BY id")
        return [DepartamentoDAO._fila_a_departamento(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_departamento: int):
        m = Conexion.marcador_sql()
        fila = DepartamentoDAO.ejecutar_consulta(
            f"SELECT id, nombre FROM departamento WHERE id = {m}", (id_departamento,), uno=True)
        return None if fila is None else DepartamentoDAO._fila_a_departamento(fila)

    @staticmethod
    def actualizar(departamento: Departamento) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = DepartamentoDAO.ejecutar_escritura(
            f"UPDATE departamento SET nombre = {m} WHERE id = {m}",
            (departamento.nombre, departamento.id))
        return filas > 0

    @staticmethod
    def eliminar(id_departamento: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = DepartamentoDAO.ejecutar_escritura(
            f"DELETE FROM departamento WHERE id = {m}", (id_departamento,))
        return filas > 0
