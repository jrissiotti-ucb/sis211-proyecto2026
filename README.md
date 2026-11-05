# SIS-211 · Proyecto de curso (2/2026)

Un mismo software que **crece**: v1 (estructuras simples) → v2 (jerárquicas) → v3 (grafos).

Esta es la branch **`v2`**, creada desde `v1`. v1 no se reescribió: v2 le **agrega** un BST.
Sin grafos (eso es v3).

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
python src/sistema.py --demo   # recorrido automático (v1 + BST + casos límite)
python tests/test_limites.py   # tests de v1 (cola, hash, lista)
python tests/test_bst.py       # tests de v2 (BST de asientos)
```

En Windows, si `python` no funciona, probar `py src/sistema.py`.

El menú arranca con 2 eventos y 5 entradas de ejemplo (`A-01`..`A-03` en `E1`,
`B-01`..`B-02` en `E2`). Opciones 1–6: flujo de venta de v1. Opciones 7–9: lo nuevo de v2
(ver una fila en orden, ver un rango de asientos, saber si un asiento existe).

## Mapa v1 (tres familias distintas, sin cambios)

| Flujo del dominio | Qué llega / sale / se busca | Familia | La uso porque… | Archivo |
| --- | --- | --- | --- | --- |
| Siguiente comprador en espera | Llegan compradores y se atiende al primero que llegó | Cola | El orden de llegada importa: el primero que llega es el primero que compra (FIFO). | `src/cola_compradores.py` |
| Buscar entrada por id | Se busca una entrada concreta por su id | Tabla hash | Da acceso inmediato por clave sin recorrer todo el catálogo. | `src/catalogo.py` |
| Eventos disponibles / historial de reservas | Secuencia ordenada de eventos o de reservas de un comprador | Lista | Mantiene el orden cronológico y permite recorrer todos los elementos. | `src/historial.py` |

## Mapa v2 (una familia jerárquica)

| Flujo nuevo | ¿Qué se ordena, se busca en rango o se anida? | Familia | La uso porque… | Caso límite | Archivo |
| --- | --- | --- | --- | --- | --- |
| Asientos de una fila en orden de código, asientos entre dos códigos, o saber si un código existe | Se **ordena** por `entrada_id` y se **busca en rango** | **BST** | El hash de v1 encuentra un id pero no lo lista en orden ni devuelve un rango. El BST sí: el recorrido inorden da los códigos ordenados, y el rango no recorre las ramas que no pueden tener resultados. | El asiento no existe, o ningún asiento cae en el rango / la fila | `src/asientos_bst.py` |

**Dónde se usa en el flujo:** `SistemaVentaEntradas.agregar_entrada` inserta cada código
en el BST (además de guardarlo en el hash de v1). Las consultas `listar_fila`,
`asientos_entre`, `listar_asientos` y `existe_asiento` usan el BST y devuelven las
`Entrada` del catálogo, con su estado (disponible / vendida).

**Limitación conocida:** es un BST sin autobalanceo. Si los códigos se insertan ya
ordenados el árbol queda en forma de lista (búsqueda O(n)). Los recorridos son
iterativos, así que funcionan igual aunque quede profundo (probado con 3000 asientos).

## Casos límite

| Situación | Resultado |
| --- | --- |
| Atender con la cola vacía | `IndexError("No hay compradores en espera")` |
| Buscar una entrada que no existe | `KeyError("Entrada no encontrada: ...")` |
| Historial de un comprador sin compras | Lista vacía; el menú muestra "No hay reservas" |
| Vender una entrada ya vendida | `ValueError`; el comprador **no pierde su lugar** en la cola |
| Agregar una entrada o evento con id repetido | `ValueError`; no se pisa el existente |
| **v2:** asiento que no existe | `existe_asiento` → `False`; el menú muestra "No existe ese asiento" |
| **v2:** fila sin asientos o rango sin resultados | Lista vacía; el menú muestra "No hay asientos en esa fila / ese rango" |
| **v2:** sistema sin entradas | `listar_asientos()` → `[]` |

## Carpetas

- `src/` — clases del dominio (POO) y el programa principal (`sistema.py`).
- `tests/` — `test_limites.py` (v1) y `test_bst.py` (v2).

## Alcance

- v1: estructuras simples + clases. v2: agrega **una** jerarquía (BST) usada en un flujo.
- Este README **no** sustituye la tarea de Moodle.
- v3: otra branch, más adelante, a partir de `v2`.
