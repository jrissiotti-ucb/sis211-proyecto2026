"""
Orquesta cola (FIFO), catálogo (hash) e historial (lista) [v1],
el BST de asientos [v2] y el grafo del recinto [v3].
"""

import sys
from pathlib import Path

# Permite ejecutar `python src/sistema.py` (como script) y también importar
# el módulo como paquete (`from src.sistema import ...`).
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.evento import Evento
    from src.entrada import Entrada
    from src.cola_compradores import ColaCompradores
    from src.catalogo import CatalogoEntradas
    from src.historial import HistorialReservas
    from src.asientos_bst import ArbolAsientos
    from src.recinto_grafo import GrafoRecinto
else:
    from .evento import Evento
    from .entrada import Entrada
    from .cola_compradores import ColaCompradores
    from .catalogo import CatalogoEntradas
    from .historial import HistorialReservas
    from .asientos_bst import ArbolAsientos
    from .recinto_grafo import GrafoRecinto

PUERTA_PRINCIPAL = "Puerta principal"


class SistemaVentaEntradas:
    def __init__(self):
        self.eventos = {}
        self.catalogo = CatalogoEntradas()
        self.cola = ColaCompradores()
        self.historial = HistorialReservas()
        self.asientos = ArbolAsientos()  # v2: índice ordenado por entrada_id
        self.recinto = GrafoRecinto()    # v3: mapa de zonas y pasillos

    def agregar_evento(self, evento_id, nombre):
        """Evento ya existente → ValueError (no se pisa)."""
        if evento_id in self.eventos:
            raise ValueError(f"Evento ya existe: {evento_id}")
        self.eventos[evento_id] = Evento(evento_id, nombre)

    def listar_eventos(self):
        """Lista de eventos en orden de inserción."""
        return list(self.eventos.values())

    def agregar_entrada(self, entrada_id, evento_id, precio=0.0):
        """
        - Evento inexistente → KeyError
        - entrada_id repetido → ValueError (no pisa una entrada, vendida o no)
        """
        if evento_id not in self.eventos:
            raise KeyError(f"Evento no encontrado: {evento_id}")
        if self.catalogo.contiene(entrada_id):
            raise ValueError(f"Entrada ya existe: {entrada_id}")
        entrada = Entrada(entrada_id, evento_id, precio)
        self.catalogo.alta(entrada)
        self.asientos.insertar(entrada_id)  # v2
        return entrada

    def buscar_entrada(self, entrada_id):
        """Consulta por entrada_id (hash). No encontrada → KeyError."""
        return self.catalogo.consulta(entrada_id)

    def llegar_comprador(self, comprador):
        self.cola.encolar(comprador)

    def atender_siguiente(self):
        """Saca al siguiente. Cola vacía → IndexError."""
        return self.cola.atender()

    def vender_a(self, entrada_id, comprador):
        """
        Vende la entrada y la registra en el historial.
        - Inexistente → KeyError
        - Ya vendida → ValueError
        """
        entrada = self.catalogo.vender(entrada_id, comprador)
        self.historial.registrar(comprador, entrada_id, entrada.evento_id)
        return entrada

    def atender_y_vender(self, entrada_id):
        """
        Atiende al frente de la cola y le vende esa entrada.
        Valida la entrada ANTES de sacar al comprador: si falla, el
        comprador no pierde su lugar en la fila.
        - Entrada inexistente → KeyError
        - Ya vendida → ValueError
        - Cola vacía → IndexError
        """
        entrada = self.catalogo.consulta(entrada_id)
        if entrada.vendida:
            raise ValueError(f"Entrada ya vendida: {entrada_id}")
        if self.cola.esta_vacia():
            raise IndexError("No hay compradores en espera")
        comprador = self.atender_siguiente()
        return self.vender_a(entrada_id, comprador)

    def historial_de(self, comprador):
        """Reservas del usuario (lista). Vacío → []."""
        return self.historial.de_usuario(comprador)

    # --- v2: consultas ordenadas con el BST de asientos -------------------

    def existe_asiento(self, entrada_id):
        """¿Existe ese código de asiento? (BST)"""
        return self.asientos.existe(entrada_id)

    def listar_fila(self, fila):
        """
        Entradas de una fila (ej. 'A' → A-01, A-02...), en orden de código.
        Fila sin asientos → [].
        """
        codigos = self.asientos.con_prefijo(f"{fila}-")
        return [self.catalogo.consulta(c) for c in codigos]

    def asientos_entre(self, desde, hasta):
        """Entradas con desde <= entrada_id <= hasta, en orden. Ninguna → []."""
        return [self.catalogo.consulta(c) for c in self.asientos.rango(desde, hasta)]

    def listar_asientos(self):
        """Todas las entradas en orden de código. Sin entradas → []."""
        return [self.catalogo.consulta(c) for c in self.asientos.listar_en_orden()]

    # --- v3: cómo llegar al asiento con el grafo del recinto --------------

    def zona_de_asiento(self, entrada_id):
        """
        Zona del recinto donde está el asiento: la fila 'A' es 'Zona A'.
        - Entrada inexistente → KeyError
        - Esa zona no está en el mapa → None
        """
        self.catalogo.consulta(entrada_id)
        zona = f"Zona {entrada_id.split('-')[0]}"
        return zona if self.recinto.existe(zona) else None

    def ruta_a_asiento(self, entrada_id, desde=PUERTA_PRINCIPAL):
        """
        Zonas a cruzar desde `desde` hasta la zona del asiento (menos tramos).
        - Entrada inexistente o `desde` fuera del mapa → KeyError
        - Zona cerrada, aislada o sin mapa → None
        """
        zona = self.zona_de_asiento(entrada_id)
        if zona is None:
            if not self.recinto.existe(desde):
                raise KeyError(f"Zona no encontrada: {desde}")
            return None
        return self.recinto.camino(desde, zona)

    def cerrar_zona(self, zona):
        """Cierra una zona: nadie entra ni cruza por ella. Inexistente → KeyError."""
        self.recinto.cerrar(zona)

    def abrir_zona(self, zona):
        self.recinto.abrir(zona)


# ---------------------------------------------------------------------------
# Programa principal: python src/sistema.py   (menú)
#                     python src/sistema.py --demo   (recorrido automático)
# ---------------------------------------------------------------------------

def cargar_datos_demo(s):
    s.agregar_evento("E1", "Concierto Rock")
    s.agregar_evento("E2", "Obra de teatro")
    for codigo in ("A-01", "A-02", "A-03"):
        s.agregar_entrada(codigo, "E1", 80.0)
    for codigo in ("B-01", "B-02"):
        s.agregar_entrada(codigo, "E2", 50.0)


def cargar_recinto_demo(s):
    """Mapa de ejemplo: hay un ciclo (Hall, pasillos y zonas B y C) y vecinas A-B."""
    for zona in (PUERTA_PRINCIPAL, "Hall", "Pasillo norte", "Pasillo sur",
                 "Zona A", "Zona B", "Zona C", "Zona D", "Baños", "Salida de emergencia"):
        s.recinto.agregar_zona(zona)
    pasillos = [
        (PUERTA_PRINCIPAL, "Hall"),
        ("Hall", "Pasillo norte"), ("Hall", "Pasillo sur"), ("Hall", "Baños"),
        ("Pasillo norte", "Zona A"), ("Pasillo norte", "Zona B"),
        ("Zona A", "Zona B"),
        ("Zona B", "Zona C"),
        ("Pasillo sur", "Zona C"), ("Pasillo sur", "Zona D"),
        ("Zona C", "Zona D"),
        ("Zona D", "Salida de emergencia"),
    ]
    for a, b in pasillos:
        s.recinto.conectar(a, b)


def _intentar(accion, *args):
    """Ejecuta y muestra el caso límite como mensaje, sin romper el programa."""
    try:
        return accion(*args)
    except (KeyError, ValueError, IndexError) as e:
        print("  ! " + str(e.args[0] if e.args else e))
        return None


def _mostrar_menu():
    print()
    print("=== Venta de entradas ===")
    print("1. Llegar comprador a la cola")
    print("2. Atender al siguiente y venderle una entrada")
    print("3. Buscar entrada por id")
    print("4. Historial de reservas de un comprador")
    print("5. Listar eventos")
    print("6. Ver cuántos esperan en la cola")
    print("7. Ver una fila de asientos en orden (BST)")
    print("8. Ver asientos entre dos códigos (BST)")
    print("9. ¿Existe este asiento? (BST)")
    print("10. Cómo llegar a un asiento (grafo)")
    print("11. Cerrar o abrir una zona del recinto (grafo)")
    print("0. Salir")


def _opcion(s, op, leer):
    if op == "1":
        nombre = leer("Nombre del comprador: ").strip()
        if nombre:
            s.llegar_comprador(nombre)
            print(f"  {nombre} entró a la cola ({len(s.cola)} en espera).")
        else:
            print("  ! El nombre no puede estar vacío.")
    elif op == "2":
        entrada_id = leer("Id de la entrada a vender: ").strip()
        e = _intentar(s.atender_y_vender, entrada_id)
        if e:
            print(f"  Vendida: {e.entrada_id} -> {e.comprador}")
            _mostrar_ruta(s, e.entrada_id)
    elif op == "3":
        entrada_id = leer("Id de la entrada: ").strip()
        e = _intentar(s.buscar_entrada, entrada_id)
        if e:
            print(f"  {e}  precio={e.precio}")
    elif op == "4":
        nombre = leer("Comprador: ").strip()
        reservas = s.historial_de(nombre)
        if not reservas:
            print("  No hay reservas")
        for r in reservas:
            print(f"  {r['entrada_id']} (evento {r['evento_id']})")
    elif op == "5":
        eventos = s.listar_eventos()
        if not eventos:
            print("  No hay eventos")
        for ev in eventos:
            print(f"  {ev.evento_id}: {ev.nombre}")
    elif op == "6":
        print(f"  En espera: {len(s.cola)}")
    elif op == "7":
        fila = leer("Fila (ej. A): ").strip()
        entradas = s.listar_fila(fila)
        if not entradas:
            print("  No hay asientos en esa fila")
        for e in entradas:
            print(f"  {e}")
    elif op == "8":
        desde = leer("Desde (ej. A-01): ").strip()
        hasta = leer("Hasta (ej. A-03): ").strip()
        entradas = s.asientos_entre(desde, hasta)
        if not entradas:
            print("  No hay asientos en ese rango")
        for e in entradas:
            print(f"  {e}")
    elif op == "9":
        codigo = leer("Código de asiento: ").strip()
        print("  Sí existe" if s.existe_asiento(codigo) else "  No existe ese asiento")
    elif op == "10":
        codigo = leer("Código de asiento: ").strip()
        if _intentar(s.buscar_entrada, codigo):
            _mostrar_ruta(s, codigo)
    elif op == "11":
        zona = leer("Zona (ej. Zona B): ").strip()
        if _intentar(s.recinto.vecinos, zona) is not None:
            if s.recinto.esta_cerrada(zona):
                s.abrir_zona(zona)
                print(f"  {zona} reabierta.")
            else:
                s.cerrar_zona(zona)
                print(f"  {zona} cerrada.")
    else:
        print("  ! Opción no válida.")


def _mostrar_ruta(s, entrada_id):
    """Imprime el camino desde la puerta; sin camino es un caso límite, no un error."""
    try:
        ruta = s.ruta_a_asiento(entrada_id)
    except (KeyError, ValueError) as e:
        print("  ! " + str(e.args[0] if e.args else e))
        return
    if ruta:
        print(f"  Ruta ({len(ruta) - 1} tramos): " + " -> ".join(ruta))
    else:
        print("  No hay ruta: la zona está cerrada, aislada o no figura en el mapa")


def menu(s, leer=input):
    while True:
        _mostrar_menu()
        try:
            op = leer("Opción: ").strip()
        except EOFError:
            print()
            return
        if op == "0":
            print("Hasta luego.")
            return
        _opcion(s, op, leer)


def demo(s):
    print("Demo v3: cola (FIFO) + catálogo (hash) + historial (lista) + BST de asientos + grafo del recinto")
    s.llegar_comprador("Ana")
    s.llegar_comprador("Beto")
    print("Llegaron Ana y Beto. Atiende primero a:", s.cola.frente())
    print("Vende A-01:", s.atender_y_vender("A-01"))
    print("Vende A-02:", s.atender_y_vender("A-02"))
    print("Historial de Ana:", s.historial_de("Ana"))
    print("Caso límite, cola vacía:")
    _intentar(s.atender_y_vender, "A-03")
    print("Caso límite, entrada inexistente:")
    _intentar(s.buscar_entrada, "Z-99")
    print("Caso límite, historial vacío:", s.historial_de("Cora") or "No hay reservas")
    print("v2 — fila A en orden (BST):", [e.entrada_id for e in s.listar_fila("A")])
    print("v2 — asientos entre A-02 y B-01:",
          [e.entrada_id for e in s.asientos_entre("A-02", "B-01")])
    print("v2 — ¿existe B-02?", s.existe_asiento("B-02"), "| ¿existe Z-99?", s.existe_asiento("Z-99"))
    print("Caso límite v2, fila sin asientos:", s.listar_fila("Z") or "No hay asientos en esa fila")
    print("v3 — ruta a A-01:", " -> ".join(s.ruta_a_asiento("A-01")))
    print("v3 — ruta a B-02:", " -> ".join(s.ruta_a_asiento("B-02")))
    s.cerrar_zona("Pasillo norte")
    print("v3 — con Pasillo norte cerrado, ruta a A-01:", " -> ".join(s.ruta_a_asiento("A-01")))
    s.cerrar_zona("Zona A")
    print("Caso límite v3, destino al que no se llega (Zona A cerrada):", s.ruta_a_asiento("A-01"))
    s.abrir_zona("Zona A")
    s.abrir_zona("Pasillo norte")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    s = SistemaVentaEntradas()
    cargar_datos_demo(s)
    cargar_recinto_demo(s)
    if "--demo" in argv:
        demo(s)
    else:
        menu(s)


if __name__ == "__main__":
    main()
