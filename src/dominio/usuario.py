import hashlib
import hmac
import secrets

from dominio.empleado import Empleado
from dominio.validador_entrada import ValidadorEntrada as Val

# credemciales de un empleado de 1 - 1
class Usuario:
    _ITERACIONES = 200_000

    def __init__(self, nombre_usuario: str, empleado: Empleado, contrasena_hash: str = None,
                activo: bool = True, id: int = None):
        if not isinstance(empleado, Empleado):
            raise ValueError("El usuario debe estar asociado a un empleado.")
        self._id = id
        self._nombre_usuario = Val.validar_nombre_usuario(nombre_usuario)
        self._empleado = empleado
        self._contrasena_hash = contrasena_hash
        self._activo = bool(activo)

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre_usuario(self) -> str: return self._nombre_usuario

    @property
    def empleado(self) -> Empleado: return self._empleado

    @property
    def empleado_id(self): return self._empleado.id

    @property
    def rol(self) -> str: return self._empleado.tipo

    @property
    def contrasena_hash(self) -> str: return self._contrasena_hash   # el DAO lo guarda

    @property
    def activo(self) -> bool: return self._activo
    @activo.setter
    def activo(self, valor: bool): self._activo = bool(valor)

    @staticmethod
    def _calcular_hash(contrasena: str, sal: bytes, iteraciones: int) -> str:
        derivado = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, iteraciones)
        return derivado.hex()

    def establecer_contrasena(self, contrasena: str) -> None:
        contrasena = Val.validar_contrasena(contrasena)
        sal = secrets.token_bytes(16)
        derivado = Usuario._calcular_hash(contrasena, sal, Usuario._ITERACIONES)
        self._contrasena_hash = f"pbkdf2_sha256${Usuario._ITERACIONES}${sal.hex()}${derivado}"

    def autenticar(self, contrasena: str) -> bool:
        if not self._activo or not self._contrasena_hash:
            return False
        try:
            _, iteraciones, sal_hex, guardado = self._contrasena_hash.split("$")
            calculado = Usuario._calcular_hash(contrasena or "", bytes.fromhex(sal_hex), int(iteraciones))
            return hmac.compare_digest(calculado, guardado)      # comparación en tiempo constante
        except ValueError:
            return False

    def cambiar_contrasena(self, actual: str, nueva: str) -> bool:
        """False si la contraseña actual no coincide; ValueError si la nueva es débil."""
        if not self.autenticar(actual):
            return False
        self.establecer_contrasena(nueva)
        return True