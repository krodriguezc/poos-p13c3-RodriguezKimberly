from dominio.empleado import Administrador, EmpleadoRegular
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion
from persistencia.registrotiempodao import RegistroTiempoDAO

COLUMNAS = ("id, rut, nombre, correo, direccion, telefono, fecha_inicio_contrato, "
            "departamento_id, tipo_empleado, salario_base")


class EmpleadoDAO(BaseDAO):
    @staticmethod
    def fila_a_empleado(fila):
        id_, rut, nombre, correo, direccion, telefono, fecha, dep_id, tipo, salario = fila
        clase = Administrador if tipo == "ADMINISTRADOR" else EmpleadoRegular
        return clase(rut=rut, nombre=nombre, correo=correo or "", direccion=direccion, telefono=telefono,
                    fecha_inicio_contrato=str(fecha), salario_base=float(salario or 0),
                    departamento_id=dep_id, id=id_)

    @staticmethod
    def insertar(empleado):
        m = Conexion.marcador_sql()
        sql = (f"INSERT INTO empleado (rut, nombre, correo, direccion, telefono, fecha_inicio_contrato, "
            f"departamento_id, tipo_empleado, salario_base) VALUES ({m}, {m}, {m}, {m}, {m}, {m}, {m}, {m}, {m})")
        _, nuevo_id = EmpleadoDAO.ejecutar_escritura(sql, (
            empleado.rut, empleado.nombre, empleado.correo, empleado.direccion, empleado.telefono,
            empleado.fecha_inicio_contrato, empleado.departamento_id, empleado.tipo, empleado.salario_base))
        empleado.id = nuevo_id
        return empleado

    @staticmethod
    def listar() -> list:
        filas = EmpleadoDAO.ejecutar_consulta(f"SELECT {COLUMNAS} FROM empleado ORDER BY id")
        return [EmpleadoDAO.fila_a_empleado(f) for f in filas]

    @staticmethod
    def listar_por_departamento(id_departamento: int) -> list:
        m = Conexion.marcador_sql()
        filas = EmpleadoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM empleado WHERE departamento_id = {m} ORDER BY id", (id_departamento,))
        return [EmpleadoDAO.fila_a_empleado(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_empleado: int):
        m = Conexion.marcador_sql()
        fila = EmpleadoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM empleado WHERE id = {m}", (id_empleado,), uno=True)
        return None if fila is None else EmpleadoDAO.fila_a_empleado(fila)

    @staticmethod
    def cargar_registros(empleado):
        for registro in RegistroTiempoDAO.listar_por_empleado(empleado.id):
            empleado.agregar_registro_tiempo(registro)
        return empleado

#Aqui el rut y el tipo de empleado no se modifican
    @staticmethod
    def actualizar(empleado) -> bool:
        m = Conexion.marcador_sql()
        sql = (f"UPDATE empleado SET nombre = {m}, correo = {m}, direccion = {m}, telefono = {m}, "
                f"departamento_id = {m}, salario_base = {m} WHERE id = {m}")
        filas, _ = EmpleadoDAO.ejecutar_escritura(sql, (
            empleado.nombre, empleado.correo, empleado.direccion, empleado.telefono,
            empleado.departamento_id, empleado.salario_base, empleado.id))
        return filas > 0

    @staticmethod
    def eliminar(id_empleado: int) -> bool:
        m = Conexion.marcador_sql()
        resultados = EmpleadoDAO.ejecutar_transaccion([
            (f"UPDATE departamento SET gerente_id = NULL WHERE gerente_id = {m}", (id_empleado,)),
            (f"DELETE FROM empleado WHERE id = {m}", (id_empleado,)),
        ])
        return resultados[1][0] > 0
