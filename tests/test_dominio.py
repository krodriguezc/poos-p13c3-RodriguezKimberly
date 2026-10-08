# aquí se validan las reglas de negocio de las clases del dominio, sin usar la base de datos ni la interfaz de usuario
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dominio.departamento import Departamento
from dominio.empleado import Administrador, Empleado, EmpleadoRegular
from dominio.informe import Informe
from dominio.proyecto import Proyecto
from dominio.usuario import Usuario
from dominio.validador_entrada import ValidadorEntrada as Val


def crear_regular(id=1, rut="12345678-5"):
    return EmpleadoRegular(rut=rut, nombre="Ana Torres", correo="ana@ecotech.cl", direccion="Calle 1",
                        telefono="+56912345678", fecha_inicio_contrato="2026-01-10",
                        salario_base=1000000, id=id)


class PruebasValidador(unittest.TestCase):
    def test_rut_valido(self):
        self.assertEqual(Val.validar_rut("12345678-5"), "12345678-5")
        self.assertEqual(Val.validar_rut("11111111-1"), "11111111-1")

    def test_rut_digito_verificador_incorrecto(self):
        with self.assertRaises(ValueError):
            Val.validar_rut("12345678-9")

    def test_rut_formato_incorrecto(self):
        for rut in ("12.345.678-5", "12345678", "", "abc"):
            with self.assertRaises(ValueError):
                Val.validar_rut(rut)

    def test_horas_limites(self):
        self.assertEqual(Val.validar_horas("8"), 8.0)
        self.assertEqual(Val.validar_horas("24"), 24.0)
        for valor in ("0", "-1", "25", "abc", ""):
            with self.assertRaises(ValueError):
                Val.validar_horas(valor)

    def test_fecha(self):
        self.assertEqual(Val.validar_fecha("2026-10-05"), "2026-10-05")
        for valor in ("2026-13-40", "05-10-2026", "hola", ""):
            with self.assertRaises(ValueError):
                Val.validar_fecha(valor)

    def test_correo_y_telefono(self):
        with self.assertRaises(ValueError):
            Val.validar_email("sin-arroba")
        self.assertEqual(Val.validar_email_opcional(""), "")
        with self.assertRaises(ValueError):
            Val.validar_telefono("123")

    def test_monto_negativo(self):
        with self.assertRaises(ValueError):
            Val.validar_monto("-5")


class PruebasEmpleado(unittest.TestCase):
    def test_empleado_es_abstracto(self):
        with self.assertRaises(TypeError):
            Empleado(rut="12345678-5", nombre="X")

    def test_permisos_polimorficos(self):
        admin = Administrador(rut="11111111-1", nombre="Jefe", direccion="Calle 2", telefono="+56911111111",
                              fecha_inicio_contrato="2026-01-01", salario_base=1, id=2)
        regular = crear_regular()
        self.assertTrue(admin.tiene_permiso("asignar_empleados"))
        self.assertFalse(regular.tiene_permiso("asignar_empleados"))
        self.assertTrue(regular.tiene_permiso("registrar_horas"))

    def test_registrar_horas_crea_registro_y_suma(self):
        emp = crear_regular()
        reg = emp.registrar_horas(7, 8, "2026-10-05", "Implementación")
        emp.registrar_horas(7, 2, "2026-10-06", "Pruebas")
        self.assertEqual(reg.id_empleado, 1)
        self.assertEqual(emp.total_horas(), 10)

    def test_registrar_horas_exige_empleado_guardado(self):
        emp = crear_regular(id=None)
        with self.assertRaises(ValueError):
            emp.registrar_horas(7, 8, "2026-10-05", "Tarea")

    def test_actualizar_datos_valida_antes_de_cambiar(self):
        emp = crear_regular()
        with self.assertRaises(ValueError):
            emp.actualizar_datos("Nueva dirección", "123", "ana@ecotech.cl")
        self.assertEqual(emp.direccion, "Calle 1")         


class PruebasRelaciones(unittest.TestCase):
    def test_departamento_no_duplica_empleado(self):
        dep, emp = Departamento("Desarrollo"), crear_regular()
        self.assertTrue(dep.agregar_empleado(emp))
        self.assertFalse(dep.agregar_empleado(crear_regular()))      
        self.assertEqual(dep.cantidad_empleados(), 1)
        self.assertTrue(dep.remover_empleado(emp))
        self.assertEqual(dep.cantidad_empleados(), 0)

    def test_departamento_exige_gerente_empleado(self):
        with self.assertRaises(ValueError):
            Departamento("RRHH", gerente="no soy empleado")

    def test_proyecto_suma_horas_de_sus_registros(self):
        proy, emp = Proyecto("EcoSolar", 5000000, fecha_inicio="2026-10-01", id=7), crear_regular()
        proy.agregar_registro_tiempo(emp.registrar_horas(7, 3, "2026-10-05", "A"))
        self.assertEqual(proy.total_horas(), 3)

    def test_asignacion_entre_administrador_empleado_y_proyecto(self):
        admin = Administrador(rut="11111111-1", nombre="Jefe", direccion="Calle 2", telefono="+56911111111",
                              fecha_inicio_contrato="2026-01-01", salario_base=1, id=2)
        emp, proy = crear_regular(), Proyecto("EcoSolar", 1, fecha_inicio="2026-10-01", id=7)
        self.assertTrue(admin.asignar_empleado_proyecto(emp, proy))
        self.assertFalse(admin.asignar_empleado_proyecto(emp, proy))   
        self.assertEqual(emp.ver_proyectos(), ["EcoSolar"])
        self.assertTrue(admin.desasignar_empleado_de_proyecto(emp, proy))


class PruebasUsuario(unittest.TestCase):
    def test_contrasena_no_se_guarda_en_texto_plano(self):
        u = Usuario("ana_t", crear_regular())
        u.establecer_contrasena("Clave12345")
        self.assertNotIn("Clave12345", u.contrasena_hash)
        self.assertTrue(u.autenticar("Clave12345"))
        self.assertFalse(u.autenticar("otra"))

    def test_misma_clave_genera_hash_distinto(self):
        a, b = Usuario("ana_t", crear_regular()), Usuario("ana_u", crear_regular())
        a.establecer_contrasena("Clave12345")
        b.establecer_contrasena("Clave12345")
        self.assertNotEqual(a.contrasena_hash, b.contrasena_hash)    

    def test_contrasena_corta_y_usuario_inactivo(self):
        u = Usuario("ana_t", crear_regular())
        with self.assertRaises(ValueError):
            u.establecer_contrasena("corta")
        u.establecer_contrasena("Clave12345")
        u.activo = False
        self.assertFalse(u.autenticar("Clave12345"))

    def test_cambiar_contrasena(self):
        u = Usuario("ana_t", crear_regular())
        u.establecer_contrasena("Clave12345")
        self.assertFalse(u.cambiar_contrasena("incorrecta", "Nueva12345"))
        self.assertTrue(u.cambiar_contrasena("Clave12345", "Nueva12345"))
        self.assertTrue(u.autenticar("Nueva12345"))

    def test_rol_viene_del_empleado(self):
        self.assertEqual(Usuario("ana_t", crear_regular()).rol, "REGULAR")


class PruebasInforme(unittest.TestCase):
    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Informe("inexistente")

    def test_informe_de_horas(self):
        emp, proy = crear_regular(), Proyecto("EcoSolar", 1, fecha_inicio="2026-10-01", id=7)
        reg = emp.registrar_horas(7, 8, "2026-10-05", "Implementación")
        texto = Informe().generar_informe("horas", [emp], [proy], [], [reg])
        self.assertIn("Ana Torres -> EcoSolar", texto)
        self.assertIn("8.0", texto)


if __name__ == "__main__":
    unittest.main()