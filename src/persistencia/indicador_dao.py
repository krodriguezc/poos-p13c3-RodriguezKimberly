from dominio.indicador import Indicador
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

COLUMNAS = "id, fuente, codigo, fecha, valor, unidad, verificado_en"


class IndicadorDAO(BaseDAO):
    @staticmethod
    def fila_a_indicador(fila) -> Indicador:
        return Indicador(fecha=str(fila[3]), valor=float(fila[4]), codigo=fila[2],
                        verificado_en=str(fila[6]), fuente=fila[1], id=fila[0])

    @staticmethod
    def guardar(indicador: Indicador) -> Indicador:
        """Inserta la observación o, si ya existe (fuente + código + fecha), actualiza valor y verificación."""
        m = Conexion.marcador_sql()
        base = (f"INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad, verificado_en) "
                f"VALUES ({m}, {m}, {m}, {m}, {m}, {m})")
        if Conexion.obtener_motor() == "mysql":
            sql = (base + " ON DUPLICATE KEY UPDATE valor = VALUES(valor), unidad = VALUES(unidad), "
                        "verificado_en = VALUES(verificado_en)")
        else:
            sql = (base + " ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET valor = excluded.valor, "
                        "unidad = excluded.unidad, verificado_en = excluded.verificado_en")
        IndicadorDAO.ejecutar_escritura(sql, (indicador.fuente, indicador.codigo, indicador.fecha,
                                            indicador.valor, indicador.unidad, indicador.verificado_en))
        return indicador

    @staticmethod
    def listar(codigo: str, fuente: str = Indicador.FUENTE_POR_DEFECTO) -> list:
        """Historial de una moneda, del más reciente al más antiguo. No llama a la API."""
        m = Conexion.marcador_sql()
        filas = IndicadorDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM indicador_api WHERE fuente = {m} AND codigo = {m} "
            f"ORDER BY fecha DESC, id DESC", (fuente, codigo))
        return [IndicadorDAO.fila_a_indicador(f) for f in filas]

    @staticmethod
    def ultimo(codigo: str, fuente: str = Indicador.FUENTE_POR_DEFECTO):
        m = Conexion.marcador_sql()
        fila = IndicadorDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM indicador_api WHERE fuente = {m} AND codigo = {m} "
            f"ORDER BY fecha DESC, id DESC LIMIT 1", (fuente, codigo), uno=True)
        return None if fila is None else IndicadorDAO.fila_a_indicador(fila)