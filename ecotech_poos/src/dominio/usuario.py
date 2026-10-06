import hashlib
import hmac
import secrets

from dominio.validador_entrada import ValidadorEntrada


class Usuario:
    _ITERACIONES = 200_000

    def __init__(self, nombre_usuario: str, rol: str, empleado_id: int,
                contrasena_hash: str = None, activo: bool = True, id: int = None):
        self._id = id
        self._nombre_usuario = ValidadorEntrada.validar_nombre_usuario(nombre_usuario)
        self._rol = ValidadorEntrada.validar_texto_no_vacio(rol, "El rol")
        self._empleado_id = empleado_id
        self._contrasena_hash = contrasena_hash
        self._activo = bool(activo)

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre_usuario(self) -> str: return self._nombre_usuario

    @property
    def rol(self) -> str: return self._rol

    @property
    def empleado_id(self): return self._empleado_id

    @property
    def contrasena_hash(self) -> str: return self._contrasena_hash  

    @property
    def activo(self) -> bool: return self._activo
    @activo.setter
    def activo(self, valor: bool): self._activo = bool(valor)

    @staticmethod
    def _calcular_hash(contrasena: str, sal: bytes) -> str:
        derivado = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, Usuario._ITERACIONES)
        return f"pbkdf2_sha256${Usuario._ITERACIONES}${sal.hex()}${derivado.hex()}"

    def establecer_contrasena(self, contrasena: str) -> None:
        contrasena = ValidadorEntrada.validar_contrasena(contrasena)
        self._contrasena_hash = Usuario._calcular_hash(contrasena, secrets.token_bytes(16))

    def autenticar(self, contrasena: str) -> bool:
        if not self._activo or not self._contrasena_hash:
            return False
        try:
            _, iteraciones, sal_hex, _ = self._contrasena_hash.split("$")
            esperado = hashlib.pbkdf2_hmac("sha256", (contrasena or "").encode("utf-8"),
                                            bytes.fromhex(sal_hex), int(iteraciones))
            guardado = self._contrasena_hash.split("$")[3]
            return hmac.compare_digest(esperado.hex(), guardado)    
        except ValueError:
            return False

    def cambiar_contrasena(self, actual: str, nueva: str) -> bool:
        """Devuelve False si la contraseña actual no coincide; ValueError si la nueva es débil."""
        if not self.autenticar(actual):
            return False
        self.establecer_contrasena(nueva)
        return True
