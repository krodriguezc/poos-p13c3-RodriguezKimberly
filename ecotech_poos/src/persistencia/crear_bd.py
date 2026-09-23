from persistencia.conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
        sql_empleado = """
        CREATE TABLE IF NOT EXISTS empleado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
        """
        sql_proyecto = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            presupuesto REAL NOT NULL
        )
        """
    else:
        sql_empleado = """
        CREATE TABLE IF NOT EXISTS empleado (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(150) NOT NULL
        )
        """
        sql_proyecto = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            presupuesto DECIMAL(12, 2) NOT NULL
        )
        """

    cursor.execute(sql_empleado)
    cursor.execute(sql_proyecto)
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos y tablas empleado y proyecto preparadas correctamente.")