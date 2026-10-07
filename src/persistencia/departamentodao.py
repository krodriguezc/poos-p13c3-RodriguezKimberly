from dominio.departamento import Departamento
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion
from persistencia.empleadodao import EmpleadoDAO

COLUMNAS = "id, nombre, gerente_id"


class DepartamentoDAO(BaseDAO):
    @staticmethod
    def fila_a_departamento(fila, empleados_por_id: dict) -> Departamento:
        return Departamento(nombre=fila[1], gerente=empleados_por_id.get(fila[2]), id=fila[0])

    @staticmethod
    def insertar(departamento: Departamento) -> Departamento:
        m = Conexion.marcador_sql()
        gerente_id = departamento.gerente.id if departamento.gerente else None
        _, nuevo_id = DepartamentoDAO.ejecutar_escritura(
            f"INSERT INTO departamento (nombre, gerente_id) VALUES ({m}, {m})",
            (departamento.nombre, gerente_id))
        departamento.id = nuevo_id                       # la BD genera el id
        return departamento

    @staticmethod
    def listar() -> list:
        filas = DepartamentoDAO.ejecutar_consulta(f"SELECT {COLUMNAS} FROM departamento ORDER BY id")
        empleados = {e.id: e for e in EmpleadoDAO.listar()}
        return [DepartamentoDAO.fila_a_departamento(f, empleados) for f in filas]

    @staticmethod
    def buscar_por_id(id_departamento: int):
        m = Conexion.marcador_sql()
        fila = DepartamentoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM departamento WHERE id = {m}", (id_departamento,), uno=True)
        if fila is None:
            return None
        gerente = EmpleadoDAO.buscar_por_id(fila[2]) if fila[2] else None
        return DepartamentoDAO.fila_a_departamento(fila, {fila[2]: gerente})

#Llena la colección Departamento 1 — 0..* Empleado desde la BD.
    @staticmethod
    def cargar_empleados(departamento: Departamento) -> Departamento:
        for empleado in EmpleadoDAO.listar_por_departamento(departamento.id):
            departamento.agregar_empleado(empleado)
        return departamento

    @staticmethod
    def actualizar(departamento: Departamento) -> bool:
        m = Conexion.marcador_sql()
        gerente_id = departamento.gerente.id if departamento.gerente else None
        filas, _ = DepartamentoDAO.ejecutar_escritura(
            f"UPDATE departamento SET nombre = {m}, gerente_id = {m} WHERE id = {m}",
            (departamento.nombre, gerente_id, departamento.id))
        return filas > 0

    @staticmethod
    def eliminar(id_departamento: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = DepartamentoDAO.ejecutar_escritura(
            f"DELETE FROM departamento WHERE id = {m}", (id_departamento,))
        return filas > 0
