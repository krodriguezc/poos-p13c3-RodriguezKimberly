import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from persistencia.conexion import Conexion


def _crear_base_mysql_si_falta() -> None:
    nombre = os.getenv("DB_NAME", "ecotech")
    conexion = Conexion.obtener_conexion(con_base_de_datos=False)
    try:
        conexion.cursor().execute(
            f"CREATE DATABASE IF NOT EXISTS `{nombre}` CHARACTER SET utf8mb4"
        )
        conexion.commit()
    finally:
        Conexion.cerrar_conexion(conexion)


def crear_tablas() -> None:
    motor = Conexion.obtener_motor()
    if motor == "mysql":
        _crear_base_mysql_si_falta()
        pk = "INT PRIMARY KEY AUTO_INCREMENT"
    else:
        pk = "INTEGER PRIMARY KEY AUTOINCREMENT"

    conexion = None
    try:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS departamento (
                id {pk},
                nombre VARCHAR(100) NOT NULL
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS empleado (
                id {pk},
                rut VARCHAR(12) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) DEFAULT '',
                departamento_id INT,
                tipo_empleado VARCHAR(20) NOT NULL,
                salario_base FLOAT NOT NULL DEFAULT 0.0,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS proyecto (
                id {pk},
                nombre VARCHAR(100) NOT NULL,
                presupuesto FLOAT NOT NULL
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id {pk},
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                horas FLOAT NOT NULL,
                fecha VARCHAR(20) NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id) ON DELETE CASCADE,
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleado_proyecto (
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                PRIMARY KEY (id_empleado, id_proyecto),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id) ON DELETE CASCADE,
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id) ON DELETE CASCADE
            )
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS usuario (
                id {pk},
                empleado_id INT NOT NULL UNIQUE,
                nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
                contrasena_hash VARCHAR(255) NOT NULL,
                rol VARCHAR(20) NOT NULL,
                activo INT NOT NULL DEFAULT 1,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
            )
        """)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        Conexion.cerrar_conexion(conexion)


if __name__ == "__main__":
    try:
        crear_tablas()
        print(f"Base de datos preparada correctamente ({Conexion.obtener_motor()}).")
    except Exception as error:
        print(f"No se pudo preparar la base de datos: {error}")
