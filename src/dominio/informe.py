from dominio.validador_entrada import ValidadorEntrada

# reune informacion de las clases con usa
class Informe:
    TIPOS = ("empleados", "proyectos", "departamentos", "horas", "completo")

    def __init__(self, tipo_informe: str = "completo", id: int = None):
        self._id = id
        self._tipo_informe = Informe.validar_tipo(tipo_informe)

    @staticmethod
    def validar_tipo(tipo: str) -> str:
        tipo = ValidadorEntrada.validar_texto_no_vacio(tipo, "El tipo de informe").lower()
        if tipo not in Informe.TIPOS:
            raise ValueError(f"Tipo de informe no válido. Opciones: {', '.join(Informe.TIPOS)}.")
        return tipo

    @property
    def id(self): return self._id

    @property
    def tipo_informe(self) -> str: return self._tipo_informe

    def generar_informe(self, tipo: str, empleados: list, proyectos: list,
                        departamentos: list, registros: list) -> str:
        """Firma del UML: recibe los cuatro conjuntos de datos y devuelve el texto del informe."""
        self._tipo_informe = Informe.validar_tipo(tipo)
        secciones = {
            "empleados": lambda: self._seccion_empleados(empleados, departamentos),
            "proyectos": lambda: self._seccion_proyectos(proyectos),
            "departamentos": lambda: self._seccion_departamentos(departamentos, empleados),
            "horas": lambda: self._seccion_horas(empleados, proyectos, registros),
        }
        if self._tipo_informe == "completo":
            return "\n\n".join(secciones[k]() for k in ("departamentos", "empleados", "proyectos", "horas"))
        return secciones[self._tipo_informe]()

    @staticmethod
    def _titulo(texto: str) -> str:
        return f"=== {texto} ==="

    def _seccion_empleados(self, empleados, departamentos) -> str:
        nombres = {d.id: d.nombre for d in departamentos}
        lineas = [self._titulo("INFORME DE EMPLEADOS")]
        lineas += [f"{e.mostrar_datos()} | Depto: {nombres.get(e.departamento_id, 'Sin asignar')}" for e in empleados]
        lineas.append(f"Total de empleados: {len(empleados)}")
        return "\n".join(lineas)

    def _seccion_proyectos(self, proyectos) -> str:
        lineas = [self._titulo("INFORME DE PROYECTOS")]
        lineas += [p.mostrar_datos() for p in proyectos]
        lineas.append(f"Total de proyectos: {len(proyectos)} | Presupuesto total: ${sum(p.presupuesto for p in proyectos):,.2f}")
        return "\n".join(lineas)

    def _seccion_departamentos(self, departamentos, empleados) -> str:
        lineas = [self._titulo("INFORME DE DEPARTAMENTOS")]
        for d in departamentos:
            cantidad = sum(1 for e in empleados if e.departamento_id == d.id)
            lineas.append(f"{d.mostrar_datos()} | Empleados: {cantidad}")
        lineas.append(f"Empleados sin departamento: {sum(1 for e in empleados if e.departamento_id is None)}")
        return "\n".join(lineas)

    def _seccion_horas(self, empleados, proyectos, registros) -> str:
        nom_emp = {e.id: e.nombre for e in empleados}
        nom_pro = {p.id: p.nombre for p in proyectos}
        por_emp, por_pro = {}, {}
        lineas = [self._titulo("INFORME DE REGISTROS DE TIEMPO")]
        for r in registros:
            lineas.append(f"{r.fecha} | {nom_emp.get(r.id_empleado, '?')} -> {nom_pro.get(r.id_proyecto, '?')} "
                        f"| {r.horas} hrs | {r.descripcion_tarea}")
            por_emp[r.id_empleado] = por_emp.get(r.id_empleado, 0) + r.horas
            por_pro[r.id_proyecto] = por_pro.get(r.id_proyecto, 0) + r.horas
        lineas.append("Horas por empleado: " + (", ".join(f"{nom_emp.get(k, '?')}: {v}" for k, v in por_emp.items()) or "sin datos"))
        lineas.append("Horas por proyecto: " + (", ".join(f"{nom_pro.get(k, '?')}: {v}" for k, v in por_pro.items()) or "sin datos"))
        return "\n".join(lineas)