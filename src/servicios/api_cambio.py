"""Consulta del tipo de cambio (open.er-api.com). Reemplaza al antiguo main_prueba.py."""
from email.utils import parsedate_to_datetime

from dominio.validador_entrada import ValidadorEntrada as Val
from servicios import cliente_http as http

URL = "https://open.er-api.com/v6/latest/USD"
MONEDAS = {"USD": "Dólar estadounidense", "EUR": "Euro", "BRL": "Real brasileño",
        "PEN": "Sol peruano", "ARS": "Peso argentino", "COP": "Peso colombiano", "MXN": "Peso mexicano"}


def validar_moneda_admitida(codigo) -> str:
    codigo = Val.validar_moneda(codigo)
    if codigo not in MONEDAS:
        raise ValueError(f"Moneda no admitida. Opciones: {', '.join(MONEDAS)}.")
    return codigo


def obtener_datos() -> dict:
    http.limitador.autorizar()
    return http.obtener_json(URL)


def extraer_tasa(datos, moneda: str = "USD") -> tuple:
    """Valida la respuesta y devuelve (fecha ISO AAAA-MM-DD, pesos chilenos por 1 unidad de la moneda)."""
    if not isinstance(datos, dict) or datos.get("result") != "success":
        raise ValueError("Respuesta inesperada.")
    texto = datos.get("time_last_update_utc")
    if not isinstance(texto, str) or not texto:
        raise ValueError("Fecha de actualización no disponible.")
    try:
        fecha = parsedate_to_datetime(texto).date().isoformat()
    except (TypeError, ValueError):
        raise ValueError("Fecha de actualización inválida.") from None
    rates = datos.get("rates")
    if not isinstance(rates, dict):
        raise ValueError("No hay tasas de cambio disponibles.")
    clp, otra = rates.get("CLP"), rates.get(str(moneda).upper())
    if not (http.es_numero(clp, 1e-12, 1e12) and http.es_numero(otra, 1e-12, 1e12)):
        raise ValueError(f"Valor del indicador para '{moneda}' inválido.")
    return fecha, round(clp / otra, 4)