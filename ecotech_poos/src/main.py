from dominio.empleado import Empleado
from dominio.registroTiempo import RegistroTiempo

empleado = Empleado(
nombre="Ana Torres",
correo="ana.torres@ecotech.cl"
)


print(empleado.mostrar_datos())

tiempo = RegistroTiempo(
    fecha = "10/20/2003", horas = 32.1
)

print(tiempo.mostrardatos())

print(tiempo.mostrardatos2("dfghjk  hghh"))