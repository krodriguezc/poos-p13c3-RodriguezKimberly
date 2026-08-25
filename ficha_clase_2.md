# Ficha de trabajo - Clase 2

## Comprensión del problema y alcance

**Asignatura:** Programación Orientada a Objeto Seguro (TI3021)  
**Unidad:** 1  
**Modalidad:** Parejas  
**Tipo de actividad:** Formativa  

| Identificación | Información |
|---|---|
| Integrante 1 | Kimberly Rodriguez Cruz |
| Integrante 2 | COMPLETAR |
| Sección y fecha | COMPLETAR |
| URL del repositorio | COMPLETAR AL FINAL |

## Propósito

Analizar y delimitar una funcionalidad antes de diseñar clases o escribir código. La ficha final debe permitir que otra persona comprenda qué necesita el sistema, qué reglas debe respetar y cómo comprobar si responde correctamente.

> **Regla de trabajo:** en esta clase no se diseñan clases, atributos ni métodos. Primero se justifica qué se necesita; la solución técnica comenzará en la Clase 3.

## Situación inicial

> Un entrenador se encuentra con una criatura salvaje cercana e intenta capturarla utilizando una cápsula de su inventario.

## 1. Lectura activa: hechos, dudas y supuestos

### 1.1 Tres hechos explícitos

1. Hay un entrenador.
2. Hay una criatura.
3. Hay una capsula.

### 1.2 Tres ambigüedades convertidas en preguntas

| N.º | Expresión ambigua | Pregunta que debe responder el cliente |
|---:|---|---|
| 1 | "Cercana" | ¿Que condicion tecnica o distancia define que la criatura este en rango para inicar el intento? |
| 2 | "Intenta capturarla" | ¿De qué factores depende el cálculo de probabilidad para determinar el éxito o fracaso de la captura? |
| 3 | "Una cápsula de su inventario"| ¿Qué sucede si el jugador no posee cápsulas disponibles en el inventario al intentar la acción? |

### 1.3 Supuesto provisional

**Supuesto:** La cápsula elegida siempre se descuenta del inventario al momento de lanzarla, independientemente de si la captura es exitosa o no.
**Por qué es provisional:** El enunciado no aclara si un intento fallido destruye, recupera o conserva la cápsula. 
**Cómo podría confirmarse:** Confirmando con el cliente la regla de negocio sobre el consumo de ítems de consumo único.

Un supuesto no es una verdad del caso. Debe quedar marcado hasta que el cliente, una regla oficial o una evidencia lo confirme.

## 2. Del enunciado a una necesidad clara

Fórmula orientadora:

> Permitir que **[actor]** realice **[acción]** sobre **[elemento]**, bajo **[condición]**, y obtenga **[resultado observable]**.

### 2.1 Actor, necesidad y objetivo

**Actor principal:** Entrenador 
**Necesidad:** Capturar una criatura salvaje cercana mediante el uso de una cápsula de su inventario.
**Objetivo reescrito:** Permitir que el entrenador realice un intento de captura sobre una criatura salvaje cercana, bajo la condición de tener al menos una cápsula disponible en su inventario, y obtenga como resultado observable la confirmación del éxito o fallo, la actualización de su inventario y el cambio de estado del encuentro.

### 2.2 Entrada, proceso y salida (EPS)

#### Entradas necesarias

1. Selección de la criatura objetivo en el encuentro.
2. Selección del tipo de cápsula a utilizar desde el inventario.
3. Cantidad disponible de la cápsula elegida en el inventario.
4. Estado actual de la vida de la criatura salvaje.

#### Proceso observable

1. Verificar que el entrenador posea al menos una unidad de la cápsula seleccionada.
2. Comprobar que la criatura salvaje esté en condición válida de ser capturada.
3. Consumir y descontar una cápsula del inventario del entrenador.
4. Evaluar la probabilidad de captura en función del estado de la criatura y el tipo de cápsula.
5. Determinar el resultado final de la acción.
6. Dar el mensaje correspondiente y actualizar registros.

#### Salidas esperadas

1. Mensaje en pantalla indicando el resultado del intento.
2. Inventario actualizado mostrando una unidad menos de la cápsula utilizada.
3. Registro de la criatura capturada asignada al entrenador.
4. Actualización del estado del encuentro.

**Prueba de coherencia:** cada salida debe poder explicarse a partir de una entrada, una regla conocida y un paso del proceso.

## 3. Reglas, restricciones y alcance

Una **regla** define qué comportamiento es válido. Una **restricción** limita la solución posible. Un **supuesto** es una condición aceptada temporalmente.

### 3.1 Reglas del problema

1. Solo se puede intentar la captura si el entrenador tiene al menos 1 cápsula en el inventario
2. Cada intento de captura reduce en 1 unidad el stock de la cápsula seleccionada.
3. Una captura exitosa finaliza el combate e integra la criatura al equipo del entrenador.
4. Un intento fallido mantiene el combate activo y consume el turno del entrenador.

### 3.2 Restricciones

1. No se permite diseñar ni implementar código en esta fase del proyecto.
2. No se contempla la compra o reabastecimiento de cápsulas en medio del flujo de captura.
3. La acción debe resolverse utilizando únicamente la información y recursos disponibles en la sesión actual del encuentro.

### 3.3 Delimitación de la primera versión

#### Dentro del alcance

1. Verificación de existencia de cápsulas en el inventario previo al lanzamiento.
2. Procesamiento del intento de captura con respuesta inmediata de éxito o fallo.
3. Actualización directa del inventario y del estado de la criatura según el resultado.

#### Fuera del alcance

1. Mecánicas de combate previas
2. Uso de múltiples cápsulas de forma simultánea en un mismo turno.
3. Transferencia o intercambio de criaturas entre entrenadores.

#### Supuestos por confirmar

1. Las cápsulas utilizadas se pierden permanentemente tras un intento fallido.
2. El porcentaje base de captura es fijo para todas las criaturas salvajes en esta versión.
3. El entrenador cuenta con espacio libre en su equipo para recibir la criatura

### 3.4 Preguntas pendientes

1. ¿La criatura salvaje puede escapar del combate inmediatamente después de un intento de captura fallido?
2. ¿Existen diferentes tipos de cápsulas con distintas probabilidades de efectividad?

## 4. Criterios de aceptación y revisión entre pares

Un **criterio de aceptación** es una condición concreta y comprobable que permite decidir si una necesidad fue resuelta correctamente.

Estructura sugerida:

> Dado **[contexto]**, cuando **[acción]**, entonces **[resultado observable]**.

**Criterio 1:** El entrenador tiene 1 cápsula en su inventario y se encuentra con una criatura salvaje, cuando selecciona la cápsula e inicia la captura y el resultado es exitoso, entonces el sistema muestra el mensaje de éxito, descuenta la cápsula dejando el stock en 0 y añade la criatura al registro del entrenador. 
**Criterio 2:** El entrenador no tiene cápsulas en su inventario, cuando intenta ejecutar la acción de captura sobre una criatura salvaje, entonces el sistema bloquea el lanzamiento y muestra un mensaje indicando la falta de insumos sin alterar el estado del encuentro.

### 4.1 Intercambio con otra pareja

La pareja revisora debe leer la ficha sin una explicación oral y detectar una ambigüedad que obligaría a inventar una regla al diseñar la solución.

**Pareja revisora:** Mejor amigo (claude)  
**Ambigüedad detectada:** No se especificaba qué sucede si el inventario se queda en cero durante la captura.
**Pregunta sugerida:** ¿Se deshabilita la opción de captura en la interfaz cuando el contador de cápsulas llega a cero? 
**Decisión del equipo:** ACEPTAR  
**Justificación:** Aclarar este comportamiento evita que el sistema intente procesar capturas sin recursos en fases posteriores.

## 5. IA como auditora de requisitos

Primero guarden la ficha original. La IA puede detectar vacíos y formular preguntas, pero el equipo conserva la responsabilidad de decidir y justificar cada cambio.

### 5.1 Registro de la consulta

**Herramienta y fecha:** Claude  
**Versión original guardada:** SÍ 

**Prompt sugerido:**

> Actúa como revisor de requisitos. Analiza esta ficha de captura sin diseñar clases ni escribir código. Detecta ambigüedades o contradicciones; formula cinco preguntas; señala reglas no verificables; no inventes respuestas y marca cada supuesto.

### 5.2 Evaluación de observaciones

| Observación de la IA | Decisión | Justificación del equipo | Cambio realizado |
|---|---|---|---|
| Mencionan 'efectividad de la cápsula' pero no especifican cómo se calcula. | Aceptar | definir fórmulas pertenece a la lógica detallada del cliente.| Se aclaró que la probabilidad es una regla fija temporal. |
| No queda claro qué ocurre si el equipo del entrenador está lleno. | Ajustar | Es un caso de borde importante para no perder datos. | Se derivó este escenario al mini desafío de la Sección 6. |
| Sugiere crear una clase 'Inventario' para estructurar los datos. | rechazar | Incumple | No se realizó ningún cambio técnico. |

### 5.3 Pregunta de autoría

**¿Qué sugerencia rechazaron?** La propuesta de definir diagramas de clases, atributos y métodos para estructurar el inventario. 
**¿Por qué no correspondía?** Porque la consigna prohíbe explícitamente el diseño técnico en esta etapa conceptual. 
**¿Qué decisión fue exclusivamente del equipo?** Establecer que las cápsulas consumidas no se recuperan tras un fallo.

> No publiquen contraseñas, correos personales, claves, tokens ni información sensible en la consulta o en el repositorio.

## 6. Mini desafío: cambia una condición

> Cada entrenador puede llevar como máximo seis criaturas activas. Si su equipo está completo, una captura exitosa debe enviarse a la reserva.

### 6.1 Análisis del impacto

**Qué cambió:** Se añade una condición sobre la capacidad del equipo activo (máximo 6) y un nuevo destino para la criatura capturada (la reserva).  
**Secciones afectadas:** ENTRADA / PROCESO / SALIDA / REGLA / ALCANCE / SUPUESTO  
**Nueva decisión:** Validar la cantidad de criaturas activas del entrenador antes de asignar la nueva criatura capturada al equipo o a la reserva. 
**Justificación:** Evita sobrescribir datos del equipo cuando el límite de 6 criaturas ha sido alcanzado.

### 6.2 Actualización

| Elemento | Antes | Después del cambio |
|---|---|---|
| Entrada/EPS | No se requería evaluar el tamaño del equipo. | Se incluye la cantidad de criaturas activas actuales como entrada necesaria. |
| Proceso | La criatura capturada se agregaba siempre al equipo principal. | Se evalúa si el equipo < 6: si es verdadero, va al equipo; si es falso, se envía a la reserva. |
| Regla | La captura exitosa siempre añade la criatura al equipo del entrenador. | El equipo activo no puede superar las 6 criaturas; las excedentes van a la reserva |
| Alcance | Manejo de un único contenedor de criaturas (equipo). | Manejo de dos destinos posibles para la criatura (equipo activo o reserva). |

### 6.3 Nuevo criterio de aceptación

**Criterio:** un entrenador posee 6 criaturas en su equipo activo y realiza una captura exitosa sobre una criatura salvaje, cuando el sistema procesa el resultado, entonces la criatura capturada es enviada a la reserva y se notifica al entrenador que su equipo principal está lleno.  
**Evidencia esperada:** Registro en pantalla del mensaje "Criatura capturada y enviada a la reserva" y confirmación de que el equipo principal mantiene exactamente 6 integrantes.

## 7. Ticket de salida

**Resumen en una frase con actor, necesidad, regla principal y resultado:** Permitir que el entrenador intente capturar una criatura salvaje consumiendo una cápsula de su inventario, de modo que si la captura tiene éxito y el equipo tiene menos de seis miembros se agregue al equipo activo, o de lo contrario se envíe a la reserva. 
**Evidencia más clara:** La reducción en 1 unidad del stock de cápsulas en el inventario y la emisión del mensaje de confirmación con el destino final de la criatura. 
**Ambigüedad pendiente:** Determinar las condiciones exactas o la probabilidad porcentual fija que definen el éxito o fracaso del lanzamiento. 
**Mejora concreta:** Incorporación de la regla de desborde del equipo hacia la reserva para evitar la pérdida de criaturas capturadas.

## 8. Comprobación final

- [ ] Conservamos una versión anterior a la auditoría con IA.
- [ ] Actor, necesidad, entradas, proceso y salidas son coherentes.
- [ ] Reglas, restricciones, supuestos y alcance están diferenciados.
- [ ] Los criterios de aceptación son observables y verificables.
- [ ] El cambio del cliente quedó incorporado y justificado.
- [ ] No diseñamos clases ni escribimos código antes de tiempo.

## 9. Entrega

1. Crear un repositorio privado por pareja y agregar al docente como colaborador.
2. Guardar este archivo como `docs/ficha_clase_2.md`.
3. Realizar commits con mensajes claros. Se espera al menos un aporte identificable de cada integrante.
4. Cada estudiante debe pegar el mismo enlace del repositorio en AAI/Intranet e identificar a su pareja.
5. Incluir el identificador del commit final en la entrega.

Convención sugerida para el repositorio:

```text
  poos-p13-c3-portafolio-apellido-nombre
```

Primer flujo Git:

```bash
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
git status
git add docs/ficha_clase_2.md
git commit -m "Completa ficha de alcance de captura"
git push
```

Si existe un bloqueo real de cuenta, autenticación o conectividad, cada integrante debe subir temporalmente la ficha en DOCX o PDF a AAI/Intranet y regularizar el repositorio en la clase siguiente. En esta primera práctica, el dominio técnico de Git no modifica la valoración conceptual de la ficha.
