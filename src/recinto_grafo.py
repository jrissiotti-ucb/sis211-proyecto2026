"""
Mapa del recinto como grafo no dirigido (v3).
Familia: grafo (lista de adyacencia) + recorrido en amplitud (BFS).

Flujo nuevo: después de vender una entrada, decir al comprador cómo llegar
desde una puerta hasta la zona de su asiento, pasando por la menor cantidad
de tramos (cada tramo vale 1; no se miden minutos).

Lo uso porque las zonas del recinto se conectan entre sí de varias maneras:
hay pasillos que forman un ciclo y zonas vecinas que se comunican entre pares.
Eso no es un árbol: el BST de v2 solo ordena códigos y no puede decir por dónde
se llega de una zona a otra. Con el grafo, el BFS encuentra el camino con menos
tramos y, si se cierra una zona, busca otro recorrido por el resto del mapa.

La cola del BFS es una lista (append / pop(0)), igual que ColaCompradores.
"""


class GrafoRecinto:
    def __init__(self):
        self._vecinos = {}      # zona -> lista de zonas conectadas (orden de alta)
        self._cerradas = set()  # zonas cerradas: no se entra ni se cruzan

    # --- construcción -----------------------------------------------------

    def agregar_zona(self, zona):
        """Agrega una zona. Repetida → ValueError (no se pisa)."""
        if zona in self._vecinos:
            raise ValueError(f"Zona ya existe: {zona}")
        self._vecinos[zona] = []

    def conectar(self, a, b):
        """
        Pasillo entre dos zonas, en las dos direcciones.
        - Zona inexistente → KeyError
        - Una zona con ella misma → ValueError
        - Pasillo repetido → no duplica al vecino
        """
        self._exigir(a)
        self._exigir(b)
        if a == b:
            raise ValueError("Un pasillo une dos zonas distintas")
        if b not in self._vecinos[a]:
            self._vecinos[a].append(b)
        if a not in self._vecinos[b]:
            self._vecinos[b].append(a)

    # --- consulta ---------------------------------------------------------

    def zonas(self):
        return list(self._vecinos)

    def pasillos(self):
        """Lista de pares (a, b), cada pasillo una sola vez."""
        vistos = []
        for a, lista in self._vecinos.items():
            for b in lista:
                if (b, a) not in vistos:
                    vistos.append((a, b))
        return vistos

    def vecinos(self, zona):
        self._exigir(zona)
        return list(self._vecinos[zona])

    def existe(self, zona):
        return zona in self._vecinos

    def esta_vacio(self):
        return len(self._vecinos) == 0

    def __len__(self):
        return len(self._vecinos)

    # --- cierres ----------------------------------------------------------

    def cerrar(self, zona):
        self._exigir(zona)
        self._cerradas.add(zona)

    def abrir(self, zona):
        self._exigir(zona)
        self._cerradas.discard(zona)

    def esta_cerrada(self, zona):
        return zona in self._cerradas

    def cerradas(self):
        return [z for z in self._vecinos if z in self._cerradas]

    # --- recorridos (BFS) -------------------------------------------------

    def bfs(self, inicio):
        """
        Zonas alcanzables desde inicio, en orden de amplitud.
        Inicio cerrado → []. Inicio inexistente → KeyError.
        """
        self._exigir(inicio)
        if inicio in self._cerradas:
            return []
        visitadas = [inicio]
        cola = [inicio]
        while cola:
            actual = cola.pop(0)
            for v in self._vecinos[actual]:
                if v not in visitadas and v not in self._cerradas:
                    visitadas.append(v)
                    cola.append(v)
        return visitadas

    def camino(self, inicio, destino):
        """
        Zonas del recorrido con menos tramos, de inicio a destino inclusive.
        Si hay empate, el que el BFS encuentra primero (orden de alta).
        Sin recorrido posible (zona cerrada o aislada) → None.
        Zona inexistente → KeyError.
        """
        self._exigir(inicio)
        self._exigir(destino)
        if inicio in self._cerradas or destino in self._cerradas:
            return None
        cola = [[inicio]]
        vistas = [inicio]
        while cola:
            ruta = cola.pop(0)
            actual = ruta[-1]
            if actual == destino:
                return ruta
            for v in self._vecinos[actual]:
                if v not in vistas and v not in self._cerradas:
                    vistas.append(v)
                    cola.append(ruta + [v])
        return None

    def distancia(self, inicio, destino):
        """Tramos del camino más corto. Misma zona → 0. Sin camino → -1."""
        ruta = self.camino(inicio, destino)
        return -1 if ruta is None else len(ruta) - 1

    def _exigir(self, zona):
        if zona not in self._vecinos:
            raise KeyError(f"Zona no encontrada: {zona}")

    def __repr__(self):
        return f"GrafoRecinto({len(self._vecinos)} zonas, {len(self.pasillos())} pasillos)"
