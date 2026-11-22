# SIS-211 · Proyecto de curso (2/2026)

Un mismo software que **crece**: v1 (estructuras simples) → v2 (jerárquicas) → v3 (grafos).

Esta es la branch **`v3`**, creada desde `v2`. v1 y v2 no se reescribieron: v3 les **agrega**
un grafo (el mapa del recinto) usado en un flujo, y una interfaz web local.

| | |
| --- | --- |
| **Estudiante** | Jorge Alejandro Rissiotti Martinez |
| **Dominio** | Venta de entradas para eventos |
| **Repo** | https://github.com/jrissiotti-ucb/sis211-proyecto2026 |

## Cómo ejecutar

Requisito: Python 3.8 o superior. No hay que instalar nada más.

Desde la **raíz del repo**:

```bash
python src/interfaz.py         # interfaz web local (abre el navegador en http://127.0.0.1:8765)
python src/sistema.py          # programa con menú interactivo (terminal)
python src/sistema.py --demo   # recorrido automático (v1 + BST + grafo + casos límite)
python tests/test_limites.py   # tests de v1 (cola, hash, lista)
python tests/test_bst.py       # tests de v2 (BST de asientos)
python tests/test_grafo.py     # tests de v3 (grafo del recinto)
python tests/test_interfaz.py  # tests de v3 (capa de la interfaz)
```

En Windows, si `python` no funciona, probar `py src/sistema.py`.

El menú arranca con 2 eventos y 5 entradas de ejemplo (`A-01`..`A-03` en `E1`,
`B-01`..`B-02` en `E2`). Opciones 1–6: flujo de venta de v1. Opciones 7–9: lo de v2
(ver una fila en orden, ver un rango de asientos, saber si un asiento existe). Opciones 10–11: lo nuevo
de v3 (cómo llegar a un asiento, cerrar o abrir una zona del recinto).

La interfaz web (`src/interfaz.py`) usa solo la biblioteca estándar de Python: no hay que instalar
nada. Trae 32 asientos de ejemplo y tiene cuatro pantallas: **Taquilla** (cola, mapa de asientos y venta;
la entrada emitida muestra cómo llegar), **Recinto** (el grafo dibujado, con el recorrido pintado y
botones para cerrar zonas), **Asientos** (consultas del BST) e **Historial**. Con `--puerto 9000` cambia
el puerto y con `--sin-navegador` no abre el navegador.

## Mapa v1 (tres familias distintas, sin cambios)

| Flujo del dominio | Qué llega / sale / se busca | Familia | La uso porque… | Archivo |
| --- | --- | --- | --- | --- |
| Siguiente comprador en espera | Llegan compradores y se atiende al primero que llegó | Cola | El orden de llegada importa: el primero que llega es el primero que compra (FIFO). | `src/cola_compradores.py` |
| Buscar entrada por id | Se busca una entrada concreta por su id | Tabla hash | Da acceso inmediato por clave sin recorrer todo el catálogo. | `src/catalogo.py` |
| Eventos disponibles / historial de reservas | Secuencia ordenada de eventos o de reservas de un comprador | Lista | Mantiene el orden cronológico y permite recorrer todos los elementos. | `src/historial.py` |

## Mapa v2 (una familia jerárquica)

| Flujo nuevo | ¿Qué se ordena, se busca en rango o se anida? | Familia | La uso porque… | Caso límite | Archivo |
| --- | --- | --- | --- | --- | --- |
| Asientos de una fila en orden de código, asientos entre dos códigos, o saber si un código existe | Se **ordena** por `entrada_id` y se **busca en rango** | **BST autobalanceado (AVL)** | El hash de v1 encuentra un id pero no lo lista en orden ni devuelve un rango. El AVL mantiene el orden y el balance tras cada inserción; el recorrido inorden da los códigos ordenados y el rango evita ramas que no pueden tener resultados. | El asiento no existe, o ningún asiento cae en el rango / la fila | `src/asientos_bst.py` |

**Dónde se usa en el flujo:** `SistemaVentaEntradas.agregar_entrada` inserta cada código
en el BST (además de guardarlo en el hash de v1). Las consultas `listar_fila`,
`asientos_entre`, `listar_asientos` y `existe_asiento` usan el BST y devuelven las
`Entrada` del catálogo, con su estado (disponible / vendida).

**Balanceo:** el árbol usa AVL. Las inserciones aplican rotaciones para conservar
una diferencia de altura máxima de 1 entre los subárboles de cada nodo, por lo que
buscar e insertar toma O(log n), incluso si los códigos llegan ordenados. Los
recorridos siguen siendo iterativos. Hay una prueba con 3000 códigos insertados
en orden que verifica el balance y las consultas.

**Formato de códigos:** los ids son `Fila-NN` con ceros (`A-01`..`A-99`), para que el
orden alfabético coincida con el numérico. Con 100 o más asientos por fila habría que
usar más dígitos (`A-001`).

## Mapa v3 (un grafo usado en un flujo)

| Flujo nuevo | ¿Qué se conecta o se recorre? | Familia | La uso porque… | Caso límite | Archivo |
| --- | --- | --- | --- | --- | --- |
| Después de vender una entrada, decirle al comprador cómo llegar a su asiento desde la puerta | Las zonas del recinto (puerta, hall, pasillos, zonas A–D, baños, salida) y los pasillos que las unen, en los dos sentidos | **Grafo** (lista de adyacencia) con **BFS** | Las zonas no forman un árbol: hay un ciclo (Hall → Pasillo norte → Zona B → Zona C → Pasillo sur → Hall) y zonas vecinas que se comunican entre pares (A–B, C–D). El BST de v2 ordena códigos pero no dice por dónde se llega de una zona a otra. El BFS da el recorrido con menos tramos y, si se cierra una zona, busca otro por el resto del mapa. | El destino no se alcanza: la zona está cerrada o aislada → no hay ruta (`None`, distancia `-1`) | `src/recinto_grafo.py` |

**Por qué no es una segunda jerarquía:** un árbol tiene un solo camino entre dos nodos y cada nodo un
solo padre. Aquí hay dos recorridos posibles entre la puerta y la Zona B, y cerrar el Pasillo norte
no deja a la Zona A sin acceso: la ruta pasa a ser Hall → Pasillo sur → Zona C → Zona B → Zona A.

**Dónde se usa en el flujo:** `SistemaVentaEntradas.ruta_a_asiento` toma la entrada del catálogo (hash,
v1), deduce su zona (la fila `A` es `Zona A`) y le pide el camino al grafo. La venta
(`atender_y_vender`, v1) no cambia; la opción 2 del menú y la pantalla Taquilla de la interfaz llaman
después a `ruta_a_asiento` para mostrar el recorrido. `cerrar_zona` / `abrir_zona` cambian el mapa.

**Cómo se recorre:** `GrafoRecinto.camino` es un BFS. La cola es una `list` (`append` y `pop(0)`),
igual que `ColaCompradores`; guarda el camino entero de cada candidato. Si dos caminos tienen los mismos
tramos, gana el que el BFS encuentra primero (el orden en que se crearon los pasillos). Cada pasillo
vale 1: no se cuentan minutos.

**Limitación conocida:** `bfs` y `camino` revisan con `in` sobre listas, así que son O(V²) en el peor
caso; con un mapa de recinto (decenas de zonas) no se nota. Solo las zonas con nombre `Zona X`
reciben asientos: una fila sin zona en el mapa devuelve `None`.

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
| **v3:** destino al que no se llega (zona cerrada o aislada) | `ruta_a_asiento` → `None`; `distancia` → `-1`; el menú muestra "No hay ruta" y la interfaz un aviso |
| **v3:** recinto vacío | `GrafoRecinto.esta_vacio()` → `True`; `zonas()` → `[]` |
| **v3:** zona que no existe | `KeyError("Zona no encontrada: ...")` |
| **v3:** pasillo repetido, o una zona unida con ella misma | Repetido: no duplica al vecino. Consigo misma: `ValueError` |
| **v3:** fila sin zona en el mapa | `ruta_a_asiento` → `None` |

## Carpetas

- `src/` — clases del dominio (POO), el programa principal (`sistema.py`) y la interfaz web
  (`interfaz.py` con la página en `pagina.py`).
- `tests/` — `test_limites.py` (v1), `test_bst.py` (v2), `test_grafo.py` y `test_interfaz.py` (v3).

## Alcance

- v1: estructuras simples + clases. v2: agrega **una** jerarquía (BST) usada en un flujo.
  v3: agrega **un** grafo usado en un flujo (más la interfaz). No se reescribió v2: los cambios en
  `sistema.py` solo suman (atributo `recinto`, métodos `ruta_a_asiento`, `cerrar_zona`, `abrir_zona`
  y las opciones 10–11 del menú) y `ColaCompradores` ganó `en_espera()` para que la interfaz muestre la cola.
- Este README **no** sustituye la tarea de Moodle.
