from dominio.empleado import Empleado
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO


crear_tablas()


nuevo_empleado = Empleado(nombre="Ana Torres", correo="ana.torres@ecotech.cl")
EmpleadoDAO.insertar(nuevo_empleado)
print(f"-> Empleado insertado con ID: {nuevo_empleado.id}")


encontrado_id = EmpleadoDAO.buscar_por_id(nuevo_empleado.id)
print("\n--- Búsqueda por ID ---")
if encontrado_id:
    print(
        f"Encontrado: ID={encontrado_id.id} | Nombre={encontrado_id.nombre} | Correo={encontrado_id.correo}"
    )


encontrado_correo = EmpleadoDAO.buscar_por_correo("ana.torres@ecotech.cl")
print("\n--- Búsqueda por Correo ---")
if encontrado_correo:
    print(
        f"Encontrado: ID={encontrado_correo.id} | Nombre={encontrado_correo.nombre}"
    )

print("\n--- Listado Completo de Empleados (Objetos) ---")
for emp in EmpleadoDAO.listar():
    print(f"Objeto Empleado -> ID: {emp.id} | Nombre: {emp.nombre}")