from dominio.indicador import Indicador
from servicios.api_cambio import extraer_tasa


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos: dict, moneda: str = "USD") -> Indicador:
        """Recibe el diccionario de la API y devuelve un Indicador. No consulta ni guarda en la BD."""
        fecha, valor = extraer_tasa(datos, moneda)
        return Indicador(fecha=fecha, valor=valor, codigo=moneda)