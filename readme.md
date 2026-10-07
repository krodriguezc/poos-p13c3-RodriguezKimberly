# Uso de IA 
Herramienta: Mejor amigo Claude

| Fragmento  | Apoyo de la IA | Criterio técnico | Decisión |

| `BaseDAO` (`base_dao.py`) | Propuso centralizar try/commit/rollback | Evita duplicar código en 4 DAO | Adopté |

| Excepciones propias y `ejecutar_accion` (`excepciones.py`, `main.py`) | Propuso mensajes seguros y log | asi el usuario no ve detalles técnicos | Modifiqué con agregar `except Exception` al final |

| `FOUND_ROWS` (`conexion.py`) | Lo propuso para que UPDATE sin cambios no parezca "no encontrado" | Coherencia entre MySQL y SQLite | Adopté tras probarlo |

| Hash PBKDF2 (`usuario.py`) | Propuso no guardar la contraseña en texto plano | usa solo la biblioteca estándar | Adopté |

| Dígito verificador del RUT (`validador_entrada.py`) | Propuso algoritmo módulo 11 | Validación de datos reales | Adopté |

| `pedir()` (`main.py`) | Propuso un ciclo de validación reutilizable | Reutilización y estabilidad | Adopté |

| `obtener_permisos()` en el menú | La primera versión decidía con `isinstance` | Coherencia con el polimorfismo del UML | Modifiqué |

| `Usuario.rol` | La primera versión duplicaba `Empleado.tipo` | Una sola fuente de verdad | Modifiqué y ahora se obtiene del empleado |

| Registrar horas del administrador | La primera versión no exigía asignación | Regla consistente para todos los roles | Modifiqué |

| `EmpleadoContratista` | Estaba en mi código inicial | No existe en mi UML | Descarté y reemplacé por `Administrador` |

`Departamento.gerente` (`departamento.py`, `departamentodao.py`) | Propuso que el gerente sea un objeto `Empleado` cargado con `LEFT JOIN` | El UML define `Gerente: Empleado` referencia a objeto | Adopté |

| Dinero con `Decimal` y `DECIMAL(12,2)` (`validador_entrada.py`, `crearbd.py`) | Señaló que `FLOAT` no es adecuado para dinero | Evita errores de redondeo | Adopté y registré un adaptador en SQLite porque no guarda `Decimal` por sí solo |

| Fechas como `date` / `DATE`; las de registros no pueden ser futuras | Propuso dejar de guardarlas como texto | Se valida el rango y la BD las trata como fechas | Adopté |

| `listar_por_empleado()` y `listar_por_proyecto()` (`registrotiempodao.py`) | Señaló que `ver_mis_registros` traía todo y filtraba en Python | Filtrar en la BD con consulta parametrizada | Adopté |

| `COLUMNAS_E`, `COLUMNAS_P` y `fila_a_proyecto` público (`asignaciondao.py`) | Señaló columnas armadas con un `join` rebuscado y el uso de un método privado de otra clase | Legibilidad y encapsulamiento | Adopté |

| `Informe.validar_tipo` público (`informe.py`) | Señaló que `main.py` llamaba a un método privado | Encapsulamiento | Adopté |

| `cargar_proyectos()` y `cargar_registros_tiempo()` en `Empleado` | Propuso reemplazar la colección en memoria en vez de acumular | Evita datos obsoletos si otro usuario asigna o elimina | Adopté |

| Colecciones `Departamento.empleados` y `Proyecto.registros` con `total_horas()` | Señaló que existían pero nunca se cargaban ni se usaban | Que la agregación y la composición del UML se vean funcionando | Adopté |

| `exigir_permiso()` y mensaje `[ACCESO DENEGADO]` (`main.py`) | Propuso validar el permiso antes de cada acción | Defensa en profundidad usando `obtener_permisos()` | Adopté |

| Pruebas manuales (`docs/pruebas_manuales.md`) | Propuso 15 casos límite | pide probar casos límite | Adopté, ejecuté las pruebas y anoté los resultados |

1. git clone 
2. cd ecotech_poos
3. py -m venv .venv
4. source .venv/Scripts/activate        
5. pip install -r requirements.txt
6. cp .env.example .env   
7. code .(warmserver revisar) 
#bd  
8. python src/persistencia/crearbd.py
9. python -m unittest discover -s tests -v







