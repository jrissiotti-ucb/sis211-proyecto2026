# SIS-211 · Proyecto de curso (2/2026)

Un mismo software que **crece**: v1 (estructuras simples) → v2 (jerárquicas) → v3 (grafos).

**Hoy solo existe la branch `v1`.** No creen `v2` ni `v3`.

| | |
| --- | --- |
| **Estudiante** | Jorge Alejandro Rissiotti Martinez |
| **Dominio** | Venta de entradas para eventos |
| **Repo** | https://github.com/jrissiotti-ucb/sis211-proyecto2026.git |

## Mapa v1 (mínimo tres familias distintas)

Familias: arreglo, lista, pila, cola, tabla hash.  
`dict` y `set` son **la misma** familia (hash). Sin árboles ni grafos en v1.

| Flujo del dominio | Qué llega / sale / se busca | Familia | La uso porque… |
| --- | --- | --- | --- |
|Siguiente comprador en espera |Llega gente que quiere comprar y se atiende al primero que llegó |Cola |el orden de llegada importa y el primero que llega será el primero que compre, se aplicara FIFO. |
|Buscar entrada o asiento por código |Se busca rápido una entrada concreta por su código o número de asiento |Tabla hash |ayuda a un acceso inmediato por clave sin tener que recorrer todo. |
|Lista de eventos disponibles / historial de reservas del usuario |Se muestra una secuencia ordenada de eventos o de las reservas que hizo un usuario |Lista |ayuda a mantener el orden cronológico y poder recorrer todos los elementos. |

Cómo probar un caso límite (vacío, no encontrado o duplicado):

> - Cola vacía: intentar atender al siguiente comprador cuando no hay nadie deberia  responder "No hay compradores en espera" o algo similar.
> - Entrada inexistente: buscar un código de asiento que no existe deberia responder "Entrada no encontrada" o algo similar.
> - Lista vacía: pedir el historial de reservas de un usuario sin compras debería responder "No hay reservas" o algo similar.
> - Duplicado: intentar vender una entrada que ya está vendida debería rechazar la operación.

## Carpetas

- `src/` — clases del dominio (POO). Hoy no codeen.
- `tests/` — un caso límite, cuando implementen.

## Alcance

- v1: clases en `.py` (POO). Entrega Moodle: **2026-10-07 23:59**.
- Este README **no** sustituye la tarea de Moodle.
- v2 y v3: otras branches, más adelante, a partir de `v1`.
