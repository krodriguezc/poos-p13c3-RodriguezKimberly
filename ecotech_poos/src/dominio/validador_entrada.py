import math
import re
from datetime import datetime


class ValidadorEntrada:
    @staticmethod
    def validar_texto_no_vacio(texto, campo: str = "El campo") -> str:
        if texto is None or not str(texto).strip():
            raise ValueError(f"{campo} no puede estar vacío.")
        return str(texto).strip()

    @staticmethod
    def validar_email(correo) -> str:
        correo = (correo or "").strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise ValueError("El correo no tiene un formato válido (ej. ana@ecotech.cl).")
        return correo

    @staticmethod
    def validar_email_opcional(correo) -> str:
        """El correo puede quedar vacío; si se escribe, debe ser válido."""
        correo = (correo or "").strip()
        return ValidadorEntrada.validar_email(correo) if correo else ""

    @staticmethod
    def validar_rut(rut) -> str:
        rut = ValidadorEntrada.validar_texto_no_vacio(rut, "El RUT").upper()
        if not re.fullmatch(r"\d{7,8}-[\dK]", rut):
            raise ValueError("El RUT debe tener el formato 12345678-5 (sin puntos y con guion).")
        return rut

    @staticmethod
    def validar_entero_positivo(valor, campo: str = "El valor") -> int:
        try:
            numero = int(str(valor).strip())
        except ValueError:
            raise ValueError(f"{campo} debe ser un número entero.") from None
        if numero <= 0:
            raise ValueError(f"{campo} debe ser mayor que cero.")
        return numero

    @staticmethod
    def validar_monto(valor, campo: str = "El monto") -> float:
        try:
            monto = float(str(valor).replace(",", ".").strip())
        except ValueError:
            raise ValueError(f"{campo} debe ser un número.") from None
        if not math.isfinite(monto) or monto < 0:
            raise ValueError(f"{campo} no puede ser negativo.")
        return monto

    @staticmethod
    def validar_horas(valor) -> float:
        try:
            horas = float(str(valor).replace(",", ".").strip())
        except ValueError:
            raise ValueError("Las horas deben ser un número.") from None
        if not (0 < horas <= 24):
            raise ValueError("Las horas deben ser mayores que 0 y no superar 24 por registro.")
        return horas

    @staticmethod
    def validar_fecha(fecha) -> str:
        fecha = str(fecha).strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD (ej. 2026-10-05).") from None
        return fecha

    @staticmethod
    def validar_nombre_usuario(nombre) -> str:
        nombre = ValidadorEntrada.validar_texto_no_vacio(nombre, "El nombre de usuario")
        if not re.fullmatch(r"[A-Za-z0-9_.]{4,30}", nombre):
            raise ValueError("El nombre de usuario debe tener 4 a 30 caracteres: letras, números, punto o guion bajo.")
        return nombre

    @staticmethod
    def validar_contrasena(contrasena) -> str:
        contrasena = contrasena or ""
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        return contrasena
