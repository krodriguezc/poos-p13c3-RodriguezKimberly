"""Cliente HTTP común para las APIs externas: timeout, códigos HTTP, JSON y control de flujo."""
import logging
import math
import time

import requests

logger = logging.getLogger(__name__)

TIMEOUT = (3, 5)

class ErrorServicioExterno(Exception):
    """Fallo controlado al usar una API externa. Su mensaje es seguro para mostrar al usuario."""


class LimitadorConsultas:
    """Control de flujo: máximo de consultas por sesión del programa y espera mínima entre ellas."""

    def __init__(self, maximo: int = 30, espera_segundos: float = 1.0):
        self._maximo, self._espera = maximo, espera_segundos
        self._total, self._ultima = 0, float("-inf")

    def autorizar(self) -> None:
        ahora = time.monotonic()
        if self._total >= self._maximo:
            raise ErrorServicioExterno("Se alcanzó el máximo de consultas externas permitidas en esta sesión.")
        if ahora - self._ultima < self._espera:
            raise ErrorServicioExterno("Espere un segundo antes de hacer otra consulta externa.")
        self._total += 1
        self._ultima = ahora


limitador = LimitadorConsultas()


def es_numero(valor, minimo: float, maximo: float) -> bool:
    return (isinstance(valor, (int, float)) and not isinstance(valor, bool)
            and math.isfinite(valor) and minimo <= valor <= maximo)


def _mensaje_http(codigo: int) -> str:
    if codigo == 404:
        return "El recurso solicitado no existe en el servicio externo (404)."
    if codigo in (401, 403):
        return f"El servicio externo rechazó el acceso ({codigo})."
    if codigo == 429:
        return "Se superó el límite de consultas del servicio externo (429). Intente más tarde."
    if 500 <= codigo < 600:
        return f"El servicio externo presenta fallas ({codigo}). Intente más tarde."
    return f"El servicio externo respondió con un código inesperado ({codigo})."


def obtener_json(url: str, parametros: dict = None) -> dict:
    """GET con timeout; valida el código HTTP y que el cuerpo sea un objeto JSON."""
    try:
        respuesta = requests.get(url, params=parametros, timeout=TIMEOUT)
        respuesta.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Tiempo de espera agotado en %s", url)
        raise ErrorServicioExterno("El servicio externo tardó demasiado en responder.") from None
    except requests.exceptions.ConnectionError:
        logger.error("Sin conexión con %s", url)
        raise ErrorServicioExterno("No hay conexión con el servicio externo. Revise su red.") from None
    except requests.exceptions.HTTPError as error:
        codigo = error.response.status_code if error.response is not None else 0
        logger.error("HTTP %s en %s", codigo, url)
        raise ErrorServicioExterno(_mensaje_http(codigo)) from None
    except requests.exceptions.RequestException:
        logger.error("Error de requests en %s", url)
        raise ErrorServicioExterno("No fue posible consultar el servicio externo.") from None

    if respuesta.status_code != 200:                       # 204, 3xx, etc.
        raise ErrorServicioExterno(_mensaje_http(respuesta.status_code))
    try:
        datos = respuesta.json()
    except ValueError:
        logger.error("Respuesta no JSON desde %s", url)
        raise ErrorServicioExterno("El servicio externo devolvió una respuesta ilegible.") from None
    if not isinstance(datos, dict):
        raise ErrorServicioExterno("El servicio externo devolvió una estructura inesperada.")
    return datos