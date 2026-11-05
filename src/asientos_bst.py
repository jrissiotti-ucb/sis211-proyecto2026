"""
BST de asientos, ordenado por entrada_id (v2).
Familia: árbol binario de búsqueda.

Flujo nuevo: listar los asientos de una fila en orden de código, listar los
que caen entre dos códigos, o saber si un código de asiento existe.
Lo uso porque la tabla hash de v1 encuentra un id pero no lo lista en orden ni
devuelve un rango; el BST sí (recorrido inorden), y el rango no recorre las
ramas que no pueden tener resultados.

Todos los recorridos son iterativos (con pila propia), así que funcionan
aunque el árbol quede muy profundo (por ejemplo, ids insertados ya ordenados).
"""


class NodoAsiento:
    def __init__(self, codigo):
        self.codigo = codigo
        self.izq = None
        self.der = None


class ArbolAsientos:
    def __init__(self):
        self.raiz = None
        self._tamano = 0

    def esta_vacio(self):
        return self.raiz is None

    def __len__(self):
        return self._tamano

    def insertar(self, codigo):
        """Inserta el código. Devuelve False si ya estaba (sin duplicados)."""
        nuevo = NodoAsiento(codigo)
        if self.raiz is None:
            self.raiz = nuevo
            self._tamano += 1
            return True
        actual = self.raiz
        while True:
            if codigo == actual.codigo:
                return False
            if codigo < actual.codigo:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
        self._tamano += 1
        return True

    def existe(self, codigo):
        actual = self.raiz
        while actual is not None:
            if codigo == actual.codigo:
                return True
            actual = actual.izq if codigo < actual.codigo else actual.der
        return False

    def listar_en_orden(self):
        """Todos los códigos de menor a mayor. Árbol vacío → []."""
        salida = []
        pila = []
        actual = self.raiz
        while actual is not None or pila:
            if actual is not None:
                pila.append(actual)
                actual = actual.izq
            else:
                nodo = pila.pop()
                salida.append(nodo.codigo)
                actual = nodo.der
        return salida

    def rango(self, desde, hasta):
        """
        Códigos con desde <= código <= hasta, en orden.
        Ninguno en el rango (o desde > hasta) → [].
        """
        salida = []
        if desde > hasta:
            return salida
        pila = []
        actual = self.raiz
        while actual is not None or pila:
            if actual is not None:
                pila.append(actual)
                # solo hay algo útil a la izquierda si desde < este código
                actual = actual.izq if desde < actual.codigo else None
            else:
                nodo = pila.pop()
                if nodo.codigo > hasta:
                    break  # el resto del inorden es aún mayor
                if nodo.codigo >= desde:
                    salida.append(nodo.codigo)
                actual = nodo.der
        return salida

    def con_prefijo(self, prefijo):
        """Códigos que empiezan con el prefijo (ej. 'A-'), en orden."""
        return self.rango(prefijo, prefijo + "\uffff")
