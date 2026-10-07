import os
import sqlite3

import pymysql
from dotenv import load_dotenv
from pymysql.constants import CLIENT

from persistencia.excepciones import ErrorConexion

load_dotenv()


class Conexion:
    @staticmethod
    def obtener_motor() -> str:
        return os.getenv("DB_ENGINE", "sqlite").lower()

    @staticmethod
    def marcador_sql() -> str:
        return "%s" if Conexion.obtener_motor() == "mysql" else "?"

    @staticmethod
    def errores_integridad() -> tuple:
        return (sqlite3.IntegrityError, pymysql.err.IntegrityError)

    @staticmethod
    def obtener_conexion(con_base_de_datos: bool = True):
        motor = Conexion.obtener_motor()
        try:
            if motor == "mysql":
                parametros = dict(
                    host=os.getenv("DB_HOST", "localhost"),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", ""),
                    port=int(os.getenv("DB_PORT", "3306")),
                    charset="utf8mb4",
                    autocommit=False,
                    client_flag=CLIENT.FOUND_ROWS,
                )
                if con_base_de_datos:
                    parametros["database"] = os.getenv("DB_NAME", "ecotech")
                return pymysql.connect(**parametros)
            if motor == "sqlite":
                conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
                conexion.execute("PRAGMA foreign_keys = ON") 
                return conexion
        except (pymysql.MySQLError, sqlite3.Error) as error:
            raise ErrorConexion("No fue posible conectarse a la base de datos.") from error
        raise ValueError(f"Motor no soportado en DB_ENGINE: {motor}")

    @staticmethod
    def cerrar_conexion(conexion) -> None:
        if conexion:
            conexion.close()
