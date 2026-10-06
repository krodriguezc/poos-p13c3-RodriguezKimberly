from dominio.empleado import Administrador, EmpleadoRegular
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

COLUMNAS = "id, rut, nombre, correo, departamento_id, tipo_empleado, salario_base"


class EmpleadoDAO(BaseDAO):
    @staticmethod
    def fila_a_empleado(fila):
        id_, rut, nombre, correo, dep_id, tipo, salario = fila
        clase = Administrador if tipo == "ADMINISTRADOR" else EmpleadoRegular
        return clase(rut=rut, nombre=nombre, correo=correo or "", departamento_id=dep_id,
                    salario_base=salario or 0.0, id=id_)

    @staticmethod
    def insertar(empleado):
        m = Conexion.marcador_sql()
        sql = (f"INSERT INTO empleado (rut, nombre, correo, departamento_id, tipo_empleado, salario_base) "
                f"VALUES ({m}, {m}, {m}, {m}, {m}, {m})")
        _, nuevo_id = EmpleadoDAO.ejecutar_escritura(sql, (
            empleado.rut, empleado.nombre, empleado.correo, empleado.departamento_id,
            empleado.tipo, empleado.salario_base))
        empleado.id = nuevo_id
        return empleado

    @staticmethod
    def listar() -> list:
        filas = EmpleadoDAO.ejecutar_consulta(f"SELECT {COLUMNAS} FROM empleado ORDER BY id")
        return [EmpleadoDAO.fila_a_empleado(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_empleado: int):
        m = Conexion.marcador_sql()
        fila = EmpleadoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM empleado WHERE id = {m}", (id_empleado,), uno=True)
        return None if fila is None else EmpleadoDAO.fila_a_empleado(fila)

    @staticmethod
    def actualizar(empleado) -> bool:
        """El RUT y el tipo de empleado no se modifican."""
        m = Conexion.marcador_sql()
        sql = (f"UPDATE empleado SET nombre = {m}, correo = {m}, departamento_id = {m}, "
                f"salario_base = {m} WHERE id = {m}")
        filas, _ = EmpleadoDAO.ejecutar_escritura(sql, (
            empleado.nombre, empleado.correo, empleado.departamento_id,
            empleado.salario_base, empleado.id))
        return filas > 0

    @staticmethod
    def eliminar(id_empleado: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = EmpleadoDAO.ejecutar_escritura(
            f"DELETE FROM empleado WHERE id = {m}", (id_empleado,))
        return filas > 0
