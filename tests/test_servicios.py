# Pruebas de la ES03: consumo de APIs (simuladas), persistencia del indicador, respaldo y permisos.
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dominio.empleado import Administrador, EmpleadoRegular
from dominio.indicador import Indicador
from persistencia.crearbd import crear_tablas
from persistencia.indicador_dao import IndicadorDAO
from servicios import api_cambio, clima, indicadores, pagos
from servicios import cliente_http as http
from servicios.cliente_http import ErrorServicioExterno, LimitadorConsultas
from servicios.deserializador_indicador import DeserializadorIndicador

TASAS = {"result": "success", "time_last_update_utc": "Sun, 08 Nov 2026 00:00:01 +0000",
         "rates": {"USD": 1, "CLP": 950.0, "EUR": 0.9}}
TASAS_OTRO_VALOR = {**TASAS, "rates": {"USD": 1, "CLP": 960.0, "EUR": 0.9}}
GEO = {"results": [{"name": "Santiago", "country": "Chile", "latitude": -33.4, "longitude": -70.6}]}
CLIMA = {"current": {"temperature_2m": 22.5, "relative_humidity_2m": 40, "weather_code": 0}}


class RespuestaFalsa:
    def __init__(self, status=200, datos=None, json_invalido=False):
        self.status_code, self._datos, self._invalido = status, datos, json_invalido

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(response=self)

    def json(self):
        if self._invalido:
            raise ValueError("no es JSON")
        return self._datos


def admin():
    return Administrador(rut="11111111-1", nombre="Jefe", direccion="Calle 2", telefono="+56911111111",
                         fecha_inicio_contrato="2026-01-01", salario_base=1000000, id=1)


def regular():
    return EmpleadoRegular(rut="12345678-5", nombre="Ana", direccion="Calle 1", telefono="+56912345678",
                           fecha_inicio_contrato="2026-01-01", salario_base=1000000, id=2)


class BaseConBD(unittest.TestCase):
    """Cada prueba usa una BD SQLite temporal y un limitador sin espera."""

    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        entorno = patch.dict(os.environ, {"DB_ENGINE": "sqlite", "DB_NAME": os.path.join(self.carpeta.name, "t.db")})
        entorno.start()
        limite = patch.object(http, "limitador", LimitadorConsultas(maximo=100, espera_segundos=0))
        limite.start()
        self.addCleanup(entorno.stop)
        self.addCleanup(limite.stop)
        self.addCleanup(self.carpeta.cleanup)
        crear_tablas()


class PruebasHttpYExtraccion(BaseConBD):
    @patch("servicios.cliente_http.requests.get")
    def test_errores_de_red(self, get):
        for excepcion in (requests.exceptions.Timeout(), requests.exceptions.ConnectionError()):
            get.side_effect = excepcion
            with self.assertRaises(ErrorServicioExterno):
                api_cambio.obtener_datos()

    @patch("servicios.cliente_http.requests.get")
    def test_codigos_http(self, get):
        for codigo in (404, 429, 500):
            get.return_value = RespuestaFalsa(codigo, {})
            with self.assertRaises(ErrorServicioExterno) as ctx:
                api_cambio.obtener_datos()
            self.assertIn(str(codigo), str(ctx.exception))

    @patch("servicios.cliente_http.requests.get")
    def test_json_invalido(self, get):
        get.return_value = RespuestaFalsa(200, json_invalido=True)
        with self.assertRaises(ErrorServicioExterno):
            api_cambio.obtener_datos()

    def test_extraer_tasa_valida_e_invalida(self):
        self.assertEqual(api_cambio.extraer_tasa(TASAS, "USD"), ("2026-11-08", 950.0))
        self.assertEqual(api_cambio.extraer_tasa(TASAS, "EUR")[1], round(950 / 0.9, 4))
        for malo in ({}, [], {"result": "error"}, {**TASAS, "rates": {"USD": 1}},
                     {**TASAS, "time_last_update_utc": "ayer"}, {**TASAS, "rates": {"USD": 0, "CLP": 950}},
                     {**TASAS, "rates": {"USD": "x", "CLP": 950}}):
            with self.assertRaises(ValueError):
                api_cambio.extraer_tasa(malo, "USD")

    def test_moneda_no_admitida(self):
        for valor in ("", "US", "DOLAR", "U$D", "XYZ"):
            with self.assertRaises(ValueError):
                api_cambio.validar_moneda_admitida(valor)

    def test_deserializador_crea_indicador(self):
        ind = DeserializadorIndicador.desde_api(TASAS, "USD")
        self.assertIsInstance(ind, Indicador)
        self.assertEqual((ind.fecha, ind.valor, ind.unidad), ("2026-11-08", 950.0, "CLP/USD"))

    def test_limitador(self):
        limite = LimitadorConsultas(maximo=2, espera_segundos=0)
        limite.autorizar(); limite.autorizar()
        with self.assertRaises(ErrorServicioExterno):
            limite.autorizar()


class PruebasPersistenciaYRespaldo(BaseConBD):
    @patch("servicios.cliente_http.requests.get")
    def test_guarda_sin_duplicar_y_actualiza(self, get):
        get.return_value = RespuestaFalsa(200, TASAS)
        r = indicadores.consultar_indicador(admin(), "USD")
        self.assertEqual(r["origen"], "API")
        indicadores.consultar_indicador(admin(), "usd")                 # misma observación
        self.assertEqual(len(IndicadorDAO.listar("USD")), 1)            # sin duplicar
        get.return_value = RespuestaFalsa(200, TASAS_OTRO_VALOR)        # mismo día, otro valor
        indicadores.consultar_indicador(admin(), "USD")
        historial = IndicadorDAO.listar("USD")
        self.assertEqual((len(historial), historial[0].valor), (1, 960.0))   # actualizó

    @patch("servicios.cliente_http.requests.get")
    def test_otra_fecha_agrega_fila_y_historial_ordenado(self, get):
        get.return_value = RespuestaFalsa(200, TASAS)
        indicadores.consultar_indicador(admin(), "USD")
        get.return_value = RespuestaFalsa(200, {**TASAS, "time_last_update_utc": "Mon, 09 Nov 2026 00:00:01 +0000"})
        indicadores.consultar_indicador(admin(), "USD")
        fechas = [i.fecha for i in indicadores.obtener_historial(regular(), "USD")]
        self.assertEqual(fechas, ["2026-11-09", "2026-11-08"])          # más reciente primero

    @patch("servicios.cliente_http.requests.get")
    def test_historial_no_llama_a_la_api(self, get):
        indicadores.obtener_historial(regular(), "USD")
        get.assert_not_called()

    @patch("servicios.cliente_http.requests.get")
    def test_respaldo_si_falla_la_api(self, get):
        get.return_value = RespuestaFalsa(200, TASAS)
        indicadores.consultar_indicador(admin(), "USD")
        get.side_effect = requests.exceptions.ConnectionError()
        r = indicadores.consultar_indicador(regular(), "USD")
        self.assertEqual((r["origen"], r["indicador"].valor), ("BD local", 950.0))
        get.side_effect = None
        get.return_value = RespuestaFalsa(200, {"result": "success", "rates": {}})  # respuesta inválida
        self.assertEqual(indicadores.consultar_indicador(regular(), "USD")["origen"], "BD local")

    @patch("servicios.cliente_http.requests.get")
    def test_sin_respaldo_informa_y_no_inventa(self, get):
        get.side_effect = requests.exceptions.Timeout()
        with self.assertRaises(ErrorServicioExterno) as ctx:
            indicadores.consultar_indicador(regular(), "EUR")
        self.assertIn("respaldo", str(ctx.exception))

    @patch("servicios.cliente_http.requests.get")
    def test_pago_internacional(self, get):
        get.return_value = RespuestaFalsa(200, TASAS)
        r = pagos.calcular_pago_internacional(admin(), regular(), "USD")
        self.assertEqual((r["pago"], r["moneda"]), (round(1000000 / 950.0, 2), "USD"))


class PruebasPermisosYClima(BaseConBD):
    @patch("servicios.cliente_http.requests.get")
    def test_servicios_exigen_sesion_y_permiso(self, get):
        for sesion in (None, "x", {}):
            with self.assertRaises(PermissionError):
                indicadores.consultar_indicador(sesion, "USD")
            with self.assertRaises(PermissionError):
                indicadores.obtener_historial(sesion, "USD")
        with self.assertRaises(PermissionError):                       # el funcionario no calcula pagos
            pagos.calcular_pago_internacional(regular(), regular(), "USD")
        get.assert_not_called()

    @patch("servicios.cliente_http.requests.get")
    def test_clima_valido_y_validaciones(self, get):
        get.side_effect = [RespuestaFalsa(200, GEO), RespuestaFalsa(200, CLIMA)]
        datos = clima.obtener_clima(regular(), "Santiago")
        self.assertEqual((datos["temperatura"], datos["estado"]), (22.5, "Despejado"))
        self.assertIn("favorables", clima.recomendar_actividad(datos))
        get.reset_mock()
        for malo in ("", "<script>", "Santiago; DROP TABLE", "A", "12345"):
            with self.assertRaises(ValueError):
                clima.obtener_clima(regular(), malo)
        get.assert_not_called()                                         # entrada inválida: no se llama a la API

    @patch("servicios.cliente_http.requests.get")
    def test_ciudad_inexistente(self, get):
        get.return_value = RespuestaFalsa(200, {"generationtime_ms": 0.1})
        with self.assertRaises(ValueError):
            clima.obtener_clima(regular(), "Zzzzzz")


if __name__ == "__main__":
    unittest.main()