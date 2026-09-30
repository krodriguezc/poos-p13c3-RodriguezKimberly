from dominio.departamento import Departamento
from dominio.empleado import EmpleadoRegular
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO


def main():

    crear_tablas()
    print("=== Base de datos inicializada ===")

    print("\n--- 1. OBJETOS Y POO ---")
    depto = Departamento("Tecnología")
    emp = EmpleadoRegular("Ana Torres", "ana.torres@ecotech.cl")
    reg = RegistroTiempo("2026-03-30", 8.0)

    emp.agregar_registro_tiempo(reg)
    depto.agregar_empleado(emp)

    print(f"Departamento: {depto.nombre}")
    print(f"Cantidad de empleados: {depto.cantidad_empleados()}")
    print(f"Registro cargado: {reg.mostrardatos()}")

    print("\n--- 2. CRUD EMPLEADO EN BASE DE DATOS ---")

    EmpleadoDAO.insertar(emp)
    print(f"Empleado insertado con ID: {emp.id}")

    emp.correo = "ana.nueva@ecotech.cl"
    try:
        if EmpleadoDAO.actualizar(emp):
            print("Empleado actualizado con éxito en la BD.")
        else:
            print("No se pudo actualizar.")
    except Exception as e:
        print(f"Error al actualizar: {e}")

    buscado = EmpleadoDAO.buscar_por_id(emp.id)
    if buscado:
        print(f"Empleado en BD: {buscado.mostrar_datos()}")

    try:
        if EmpleadoDAO.eliminar(99999):
            print("Eliminado.")
        else:
            print("ID 99999 no existe (Resultado normal, no es un error).")
    except Exception as e:
        print(f"Error inesperado: {e}")

    print("\nLista general de empleados:")
    for item in EmpleadoDAO.listar():
        print(f" - {item.mostrar_datos()}")

    print("\n--- 3. PERSISTENCIA PROYECTO ---")
    proy = Proyecto("Sistema Solar", 2500000.0)
    ProyectoDAO.insertar(proy)
    print(f"Proyecto guardado: {proy.mostrar_datos()}")

    print("\nLista general de proyectos:")
    for p in ProyectoDAO.obtener_todos():
        print(f" - {p.mostrar_datos()}")


if __name__ == "__main__":
    main()