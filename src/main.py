from dominio.departamento import Departamento
from dominio.empleado import Administrador, EmpleadoRegular
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO


crear_tablas()


emp1 = EmpleadoRegular(nombre="Ana Pérez", correo="ana@ecotech.cl")
admin1 = Administrador(nombre="Carlos Ruiz", correo="carlos@ecotech.cl")


EmpleadoDAO.insertar(emp1)
EmpleadoDAO.insertar(admin1)

proyecto1 = Proyecto(nombre="Planta Solar EcoTech", presupuesto=1500000.0)
ProyectoDAO.insertar(proyecto1)


desarrollo = Departamento(nombre="Desarrollo Sustentable")
desarrollo.agregar_empleado(emp1)
desarrollo.agregar_empleado(admin1)

tiempo = RegistroTiempo(fecha="20/10/2026", horas=8.0)
emp1.agregar_registro_tiempo(tiempo)


print("=== VERIFICACIÓN DE BASE DE DATOS Y DOMINIO ===")
print(f"Departamento: {desarrollo.nombre}")
print(f"Total empleados asociados: {desarrollo.cantidad_empleados()}")

print("\n--- Registros Recuperados de BD empleado ---")
for emp in EmpleadoDAO.obtener_todos():
    print(f"ID: {emp[0]} | Nombre: {emp[1]} | Correo: {emp[2]}")

print("\n--- Registros Recuperados de BD proyecto ---")
for proy in ProyectoDAO.obtener_todos():
    print(f"ID: {proy[0]} | Nombre: {proy[1]} | Presupuesto: ${proy[2]:,.2f}")