from persistencia.excepciones import ErrorPersistencia
from persistencia.indicador_dao import IndicadorDAO
from servicios import api_cambio
from servicios.cliente_http import ErrorServicioExterno
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.permisos import exigir_permiso


def consultar_indicador(sesion, moneda: str) -> dict:
    """API -> objeto Indicador -> BD local. Si la API falla, entrega el último dato guardado (respaldo)."""
    exigir_permiso(sesion, "consultar_indicadores")
    moneda = api_cambio.validar_moneda_admitida(moneda)
    try:
        datos = api_cambio.obtener_datos()
        dato = DeserializadorIndicador.desde_api(datos, moneda)
    except ErrorServicioExterno as error:
        return _respaldo(moneda, str(error))
    except (ValueError, KeyError, TypeError):
        return _respaldo(moneda, "El servicio devolvió una respuesta inválida.")

    try:
        IndicadorDAO.guardar(dato)
        mensaje = "Dato guardado en la base de datos local."
    except ErrorPersistencia:
        mensaje = "El dato es válido, pero no pudo guardarse en la base de datos local."
    return {"indicador": dato, "origen": "API", "mensaje": mensaje}


def _respaldo(moneda: str, motivo: str) -> dict:
    ultimo = IndicadorDAO.ultimo(moneda)
    if ultimo is None:
        raise ErrorServicioExterno(f"{motivo} Tampoco existe un dato guardado de {moneda} para usar como respaldo.")
    return {"indicador": ultimo, "origen": "BD local",
            "mensaje": f"{motivo} Se muestra el último dato guardado (respaldo); puede no estar actualizado."}


def obtener_historial(sesion, moneda: str) -> list:
    """Lee solo la BD local; no llama a la API."""
    exigir_permiso(sesion, "consultar_indicadores")
    return IndicadorDAO.listar(api_cambio.validar_moneda_admitida(moneda))