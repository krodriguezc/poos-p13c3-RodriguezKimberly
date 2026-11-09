import math
from datetime import datetime

from dominio.validador_entrada import ValidadorEntrada as Val


# Una observación de un indicador económico
class Indicador:
    FUENTE_POR_DEFECTO = "open_er_api"

    def __init__(self, fecha: str, valor: float, codigo: str = "USD", verificado_en: str = None,
                fuente: str = FUENTE_POR_DEFECTO, id: int = None):
        self._id = id
        self._fecha = Val.validar_fecha(fecha)
        self._valor = Indicador.validar_valor(valor)
        self._codigo = Val.validar_moneda(codigo)
        self._unidad = f"CLP/{self._codigo}"
        self._fuente = Val.validar_texto_no_vacio(fuente, "La fuente")
        self._verificado_en = verificado_en or datetime.now().isoformat(timespec="seconds")

    @staticmethod
    def validar_valor(valor) -> float:
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El valor del indicador debe ser un número.") from None
        if not math.isfinite(numero) or numero <= 0:
            raise ValueError("El valor del indicador debe ser un número finito mayor que cero.")
        return numero

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def fecha(self) -> str: return self._fecha

    @property
    def valor(self) -> float: return self._valor

    @property
    def codigo(self) -> str: return self._codigo

    @property
    def unidad(self) -> str: return self._unidad

    @property
    def fuente(self) -> str: return self._fuente

    @property
    def verificado_en(self) -> str: return self._verificado_en

    def mostrar_datos(self) -> str:
        return f"{self._fecha}: {self._valor:,.2f} {self._unidad} (fuente: {self._fuente})"