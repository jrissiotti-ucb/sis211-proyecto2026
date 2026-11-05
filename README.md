# SIS-211 · Proyecto de curso (2/2026)

Un mismo software que **crece**: v1 (estructuras simples) → v2 (jerárquicas) → v3 (grafos).

Esta es la branch **`v1`**: estructuras simples + clases (POO). Sin árboles ni grafos.

| | |
| --- | --- |
| **Estudiante** | Jorge Alejandro Rissiotti Martinez |
| **Dominio** | Venta de entradas para eventos |
| **Repo** | https://github.com/jrissiotti-ucb/sis211-proyecto2026 |

## Cómo ejecutar

Requisito: Python 3.8 o superior. No hay que instalar nada más.

Desde la **raíz del repo**:

```bash
python src/sistema.py          # programa con menú interactivo
python src/sistema.py --demo   # recorrido automático (cola, venta, casos límite)
python tests/test_limites.py   # tests de casos límite y flujo
```

En Windows, si `python` no funciona, probar `py src/sistema.py`.

El menú arranca con 2 eventos y 5 entradas de ejemplo (`A-01`..`A-03` para el
evento `E1`, `B-01`..`B-02` para `E2`). Un recorrido típico: opción 1 (llega
"Ana"), opción 2 (atender y vender `A-01`), opción 3 (buscar `A-01`),
opción 4 (historial de "Ana"), opción 0 (salir).

## Mapa v1 (tres familias distintas)

| Flujo del dominio | Qué llega / sale / se busca | Familia | La uso porque… | Archivo |
| --- | --- | --- | --- | --- |
| Siguiente comprador en espera | Llegan compradores y se atiende al primero que llegó | Cola | El orden de llegada importa: el primero que llega es el primero que compra (FIFO). | `src/cola_compradores.py` |
| Buscar entrada por id | Se busca una entrada concreta por su id | Tabla hash | Da acceso inmediato por clave sin recorrer todo el catálogo. | `src/catalogo.py` |
| Eventos disponibles / historial de reservas | Se muestra una secuencia ordenada de eventos o de las reservas de un comprador | Lista | Mantiene el orden cronológico y permite recorrer todos los elementos. | `src/historial.py` |

`src/sistema.py` (`SistemaVentaEntradas`) combina los tres flujos.

## Casos límite

| Situación | Resultado |
| --- | --- |
| Atender con la cola vacía | `IndexError("No hay compradores en espera")`; el menú muestra el mensaje |
| Buscar una entrada que no existe | `KeyError("Entrada no encontrada: ...")` |
| Historial de un comprador sin compras | Lista vacía; el menú muestra "No hay reservas" |
| Vender una entrada ya vendida | `ValueError("Entrada ya vendida: ...")`; el comprador **no pierde su lugar** en la cola |
| Agregar una entrada o evento con id repetido | `ValueError`; no se pisa el existente |

## Carpetas

- `src/` — clases del dominio (POO) y el programa principal (`sistema.py`).
- `tests/` — `test_limites.py`: casos límite y flujo completo.

## Alcance

- v1: clases en `.py` (POO). Entrega Moodle: **2026-10-07 23:59**.
- Este README **no** sustituye la tarea de Moodle.
- v2 y v3: otras branches, a partir de la anterior.
