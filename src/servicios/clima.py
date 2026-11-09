"""Consulta del clima (Open-Meteo): geocodificación de la ciudad y clima actual."""
from dominio.validador_entrada import ValidadorEntrada as Val
from servicios import cliente_http as http
from servicios.permisos import exigir_permiso

URL_GEOCODIFICACION = "https://geocoding-api.open-meteo.com/v1/search"
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"

_ESTADOS = [((0,), "Despejado"), ((1, 2, 3), "Parcialmente nublado o nublado"), ((45, 48), "Niebla"),
            ((51, 53, 55, 56, 57), "Llovizna"), ((61, 63, 65, 66, 67, 80, 81, 82), "Lluvia"),
            ((71, 73, 75, 77, 85, 86), "Nieve"), ((95, 96, 99), "Tormenta eléctrica")]


def obtener_clima(sesion, ciudad: str) -> dict:
    exigir_permiso(sesion, "consultar_clima")
    ciudad = Val.validar_ciudad(ciudad)                    # se valida ANTES de llamar a la API
    http.limitador.autorizar()
    geo = http.obtener_json(URL_GEOCODIFICACION, {"name": ciudad, "count": 1, "language": "es", "format": "json"})
    resultados = geo.get("results")
    if not isinstance(resultados, list) or not resultados or not isinstance(resultados[0], dict):
        raise ValueError(f"No se encontró la ciudad '{ciudad}'.")
    lugar = resultados[0]
    lat, lon = lugar.get("latitude"), lugar.get("longitude")
    if not (http.es_numero(lat, -90, 90) and http.es_numero(lon, -180, 180)):
        raise http.ErrorServicioExterno("El servicio devolvió coordenadas inválidas.")

    datos = http.obtener_json(URL_CLIMA, {"latitude": lat, "longitude": lon, "timezone": "auto",
                                        "current": "temperature_2m,relative_humidity_2m,weather_code"})
    actual = datos.get("current")
    if not isinstance(actual, dict):
        raise http.ErrorServicioExterno("El servicio de clima devolvió datos incompletos.")
    temperatura, humedad, codigo = (actual.get("temperature_2m"), actual.get("relative_humidity_2m"),
                                    actual.get("weather_code"))
    if not (http.es_numero(temperatura, -90, 60) and http.es_numero(humedad, 0, 100) and http.es_numero(codigo, 0, 99)):
        raise http.ErrorServicioExterno("El servicio de clima devolvió valores fuera de rango.")
    codigo = int(codigo)
    estado = next((texto for codigos, texto in _ESTADOS if codigo in codigos), "Sin descripción")
    return {"ciudad": str(lugar.get("name", ciudad)), "pais": str(lugar.get("country", "-")),
            "temperatura": temperatura, "humedad": humedad, "codigo": codigo, "estado": estado}


def recomendar_actividad(clima: dict) -> str:
    if clima["codigo"] >= 51 or clima["temperatura"] <= 0 or clima["temperatura"] >= 35:
        return "Condiciones adversas: se recomienda reprogramar las actividades al aire libre."
    if clima["codigo"] in (45, 48):
        return "Visibilidad reducida: realizar las actividades al aire libre con precaución."
    return "Condiciones favorables para actividades al aire libre."