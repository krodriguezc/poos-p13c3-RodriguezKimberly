from dominio.usuario import Usuario
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

_COLUMNAS = "id, empleado_id, nombre_usuario, contrasena_hash, rol, activo"


class UsuarioDAO(BaseDAO):
    @staticmethod
    def _fila_a_usuario(fila) -> Usuario:
        return Usuario(nombre_usuario=fila[2], rol=fila[4], empleado_id=fila[1],
                       contrasena_hash=fila[3], activo=bool(fila[5]), id=fila[0])

    @staticmethod
    def insertar(usuario: Usuario) -> Usuario:
        m = Conexion.marcador_sql()
        _, nuevo_id = UsuarioDAO.ejecutar_escritura(
            f"INSERT INTO usuario (empleado_id, nombre_usuario, contrasena_hash, rol, activo) "
            f"VALUES ({m}, {m}, {m}, {m}, {m})",
            (usuario.empleado_id, usuario.nombre_usuario, usuario.contrasena_hash,
             usuario.rol, 1 if usuario.activo else 0))
        usuario.id = nuevo_id
        return usuario

    @staticmethod
    def contar() -> int:
        return UsuarioDAO.ejecutar_consulta("SELECT COUNT(*) FROM usuario", uno=True)[0]

    @staticmethod
    def buscar_por_nombre(nombre_usuario: str):
        m = Conexion.marcador_sql()
        fila = UsuarioDAO.ejecutar_consulta(
            f"SELECT {_COLUMNAS} FROM usuario WHERE nombre_usuario = {m}", (nombre_usuario,), uno=True)
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def buscar_por_empleado(id_empleado: int):
        m = Conexion.marcador_sql()
        fila = UsuarioDAO.ejecutar_consulta(
            f"SELECT {_COLUMNAS} FROM usuario WHERE empleado_id = {m}", (id_empleado,), uno=True)
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def actualizar_contrasena(usuario: Usuario) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = UsuarioDAO.ejecutar_escritura(
            f"UPDATE usuario SET contrasena_hash = {m} WHERE id = {m}",
            (usuario.contrasena_hash, usuario.id))
        return filas > 0
