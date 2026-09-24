# Ficha de trabajo – Clase 3

## Identificación

- **Nombre:** Kimberly Rodriguez Cruz
- **Sección:** COMPLETAR
- **Fecha:** 19-08-2026
- **Compañero(a) de trabajo:** COMPLETAR
- **Repositorio individual:** `completar`

# Parte 0. Punto de partida validado

Este caso representa el **mínimo esperado al finalizar la Clase 2**. Se utilizará como evidencia común para comenzar el diseño orientado a objetos. No reemplaza la entrega individual de la ficha anterior.

## Funcionalidad

Captura básica de una criatura.

## Actor principal

Entrenador.

## Necesidad

Capturar una criatura salvaje disponible utilizando una cápsula de su inventario.

## Entradas

- Criatura seleccionada.
- Disponibilidad de la criatura.
- Distancia entre el entrenador y la criatura.
- Cantidad de cápsulas.
- Probabilidad de captura.

## Proceso

1. Verificar que la criatura esté disponible.
2. Verificar que se encuentre dentro de la distancia permitida.
3. Verificar que el entrenador tenga cápsulas.
4. Consumir una cápsula.
5. Determinar si la captura tiene éxito.
6. Registrar la criatura si la captura es exitosa.
7. Informar el resultado.

## Salidas

- Captura exitosa.
- Captura fallida.
- Mensaje de rechazo por criatura no disponible.
- Mensaje de rechazo por distancia.
- Mensaje de rechazo por falta de cápsulas.
- Cantidad actualizada de cápsulas.

## Reglas

- Solo se puede intentar capturar una criatura por operación.
- Cada intento válido consume una cápsula.
- Un intento rechazado no consume cápsulas.
- La criatura se registra únicamente si la captura tiene éxito.
- La criatura debe estar disponible y dentro de la distancia permitida.

## Dentro del alcance

- Selección de la criatura.
- Validaciones de disponibilidad, distancia e inventario.
- Consumo de la cápsula.
- Resolución del intento.
- Registro de la criatura.
- Información del resultado.

## Fuera del alcance

- GPS real.
- Combates.
- Animaciones.
- Intercambio de criaturas.
- Funciones sociales.

## Criterios de aceptación

### Criterio 1: intento sin cápsulas

- **Dado** que el entrenador no tiene cápsulas,
- **cuando** intenta capturar una criatura,
- **entonces** el sistema rechaza la acción, no modifica el inventario e informa que no hay cápsulas disponibles.

### Criterio 2: intento válido

- **Dado** que la criatura está disponible, se encuentra dentro de la distancia permitida y el entrenador tiene cápsulas,
- **cuando** realiza un intento de captura,
- **entonces** el sistema consume exactamente una cápsula, determina el resultado e informa si la captura tuvo éxito o falló.

### Criterio 3: criatura fuera de rango

- **Dado** que la criatura se encuentra fuera de la distancia permitida,
- **cuando** el entrenador intenta capturarla,
- **entonces** el sistema rechaza la acción, no consume cápsulas e informa que la criatura está fuera de rango.

### Criterio 4: captura exitosa

- **Dado** que el entrenador realiza un intento válido,
- **cuando** el resultado de la captura es exitoso,
- **entonces** la criatura se registra en su colección y el sistema informa la captura exitosa.

---


# Tarjetas de clase y responsabilidades


## Clase Plantilla

- **Nombre:** Criaturas
- **Responsabilidad principal:** Atacar
- **Atributos necesarios:** Nombre, estatura, peso, vida, escudo, habilidad
- **Métodos posibles:** Camuflaje, ataque, correr
- **Clase con la que necesita colaborar:** Entrenador
- **Regla o criterio de aceptación que la justifica:** Solo puede hacer un ataque por turno 
- **Responsabilidad que no debería asumir:** Regenerar vida


## Comprobación de coherencia

1. ¿Existe una clase que concentre casi todas las acciones? ¿Cuál y qué responsabilidad debería trasladarse?

   **Respuesta:** Sí, la clase Entrenador podría sobrecargarse de responsabilidades. La responsabilidad de validar si una criatura está en rango y disponible debe ser delegada a la propia clase Criatura, mientras que el cálculo de probabilidad o el proceso técnico de resolución de captura puede trasladarse a una clase colaboradora como Captura o mantenerse estrictamente encapsulado según sus datos.

2. ¿Existe un método en una clase que no posee los datos necesarios para realizarlo?

   **Respuesta:** Sí. Verificar la posición o disponibilidad debe ser responsabilidad de Criatura, que posee directamente esos datos.

3. ¿Existe el mismo atributo en varias clases sin una justificación clara?

   **Respuesta:** No por ahora.

---

# Instancias u objetos concretos

Elige una de tus clases y crea dos objetos con estados distintos.

- **Clase seleccionada:** Criatura

| Atributo | Objeto 1: `Pikachu' | Objeto 2: `Charmander` |
|----------|-----------------------|-----------------------|
| Nombre | "Pikachu" | "Charmander" |
| Vida | 100 | 80 |
| Distancia | 5 | 18 |

- **Método que ambos objetos pueden ejecutar:** cambiarDistancia()
- **¿Qué comparten por pertenecer a la misma clase?:** Comparten la misma estructura de atributos
- **¿Qué cambia entre ambos objetos?:** El estado de sus atributos

---

# Trazabilidad con los criterios de aceptación

Relaciona cada comportamiento esperado con las responsabilidades propuestas.

| Criterio | ¿Qué información se necesita? | ¿Qué clase debería conocerla? | ¿Qué acción debe realizarse? | ¿Qué clase debería realizarla? |
|----------|-------------------------------|-------------------------------|------------------------------|--------------------------------|
| Sin cápsulas | Cantidad actual de cápsulas en el inventario. | Entrenador | Verificar stock de cápsulas y rechazar la acción sin descontar recursos. | Entrenador |
| Intento válido | Disponibilidad, distancia, stock de cápsulas y probabilidad de captura. | Entrenador y criatura | Descontar 1 cápsula, evaluar éxito o fallo e informar el resultado. | Entrenador |
| Fuera de rango | Distancia de la criatura y distancia máxima permitida. | Criatura | Validar si la distancia supera el límite y rechazar el intento sin consumir cápsulas. | Criatura |
| Captura exitosa | Confirmación de éxito del intento y datos de la criatura. | Entrenador y criatura | Agregar la criatura capturada a la colección del entrenador y notificar la captura. | Entrenador |

## Pregunta de análisis

¿Existe algún criterio de aceptación que no pueda cumplirse con las clases y responsabilidades propuestas?

**Respuesta y ajuste necesario:** Si, en la plantilla de la clase criatura solo tenia como responsabilidad principal "atacar", lo cual no correspondia a los criterios de aceptacion del caso. Se redefinió la clase Criatura enfocándola en los atributos exigidos por las reglas del caso y se asignaron correctamente las responsabilidades de verificación e inventario a Entrenador, asegurando que todos los criterios de aceptación puedan cumplirse.

