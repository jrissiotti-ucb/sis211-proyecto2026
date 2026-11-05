"""
Orquesta cola (FIFO), catálogo (hash) e historial (lista) [v1]
y el BST de asientos [v2].
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
else:
    from .evento import Evento
    from .entrada import Entrada
    from .cola_compradores import ColaCompradores
    from .catalogo import CatalogoEntradas
    from .historial import HistorialReservas
    from .asientos_bst import ArbolAsientos


class SistemaVentaEntradas:
    def __init__(self):
        self.eventos = {}
        self.catalogo = CatalogoEntradas()
        self.cola = ColaCompradores()
        self.historial = HistorialReservas()
        self.asientos = ArbolAsientos()  # v2: índice ordenado por entrada_id

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
            print(f"  Vendida: {e.entrada_id} → {e.comprador}")
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
    else:
        print("  ! Opción no válida.")


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
    print("Demo v2: cola (FIFO) + catálogo (hash) + historial (lista) + BST de asientos")
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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    s = SistemaVentaEntradas()
    cargar_datos_demo(s)
    if "--demo" in argv:
        demo(s)
    else:
        menu(s)


if __name__ == "__main__":
    main()
