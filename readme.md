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

| Le pedi a la IA que me adapte el json | propuso json adaptado | adopte | 

| Carpeta servicios y sus archivos dentro | Propuso crear una capa de servicios entre el menú y los DAO | el menú pide datos, el servicio decide y comprueba permisos, el DAO consulta la BD. Antes, el código de la API vivía en un script suelto sin conexión al sistema | Adopté. El menú sigue en main.py; solo moví a servicios/ la lógica nueva de APIs, permisos y datos propios

| cliente_http.py (reemplaza a main_prueba.py) | Propuso un cliente HTTP único con timeout, validación del código HTTP, lectura segura del JSON y LimitadorConsultas | El script original se ejecutaba al importarse, usaba el mismo mensaje para cualquier falla, no distinguía 404, 429 y 5xx, e importaba math a mitad de archivo. Un usuario autenticado podía saturar la API | Modifiqué: excepción propia ErrorServicioExterno con mensajes seguros, el detalle técnico va al log, y límite de 30 consultas por ejecución con 1 s entre ellas

| api_cambio.py, deserializador_indicador.py, dominio/indicador.py, persistencia/indicador_dao.py y tabla indicador_api | Propuso convertir la respuesta JSON en un objeto Indicador validado y guardarlo con clave única | Evita duplicar la misma observación al consultar varias veces y permite un historial local. La sentencia ON CONFLICT propuesta solo funciona en SQLite, pero mi proyecto también usa MySQL | Modifiqué: el DAO elige ON CONFLICT o ON DUPLICATE KEY UPDATE según DB_ENGINE. Probado en SQLite; falta confirmar en MySQL con WampServer

| indicadores.py y pagos.py | Propuso un flujo con respaldo: si la API falla o responde datos inválidos, mostrar el último dato guardado e indicar su origen | Continuidad operativa sin inventar datos: se muestra “Origen: BD local” y aviso. Sin respaldo se informa y se vuelve al menú. El pago internacional usa esa misma tasa validada |  Adopté

| permisos.py, mi_cuenta.py y clima.py | Propuso que cada servicio vuelva a comprobar el permiso (aunque el menú oculte la opción), que “Mi ficha” use el ID de la sesión y que la ciudad se valide antes de llamar a la API | Defensa en profundidad: la función puede llamarse por otra ruta. Un funcionario no debe poder editar a otro. Una entrada sin validar no debe llegar a una URL externa | Adopté. Descarté la columna rol en usuario sugerida en la clase, porque ya existen Empleado.tipo y obtener_permisos() (polimorfismo del UML) y duplicarla crearía dos fuentes de verdad


Pasos de git. 

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
10. python src/semilla_bd.py. pide contrasenas
11. python src/main.py.
Iniciar sesión:
Administrador: admin.
Funcionarios: ana.torres o bruno.soto.








