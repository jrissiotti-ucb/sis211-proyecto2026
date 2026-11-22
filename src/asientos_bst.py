"""
BST AVL de asientos, ordenado por entrada_id (v2).
Familia: árbol binario de búsqueda autobalanceado.

Flujo nuevo: listar los asientos de una fila en orden de código, listar los
que caen entre dos códigos, o saber si un código de asiento existe.
Lo uso porque la tabla hash de v1 encuentra un id pero no lo lista en orden ni
devuelve un rango; el BST sí (recorrido inorden), y el rango no recorre las
ramas que no pueden tener resultados.

Las inserciones mantienen el balance AVL, incluso si los ids llegan ordenados.
Los recorridos son iterativos (con pila propia).
"""


class NodoAsiento:
    def __init__(self, codigo):
        self.codigo = codigo
        self.izq = None
        self.der = None
        self.altura = 1


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
        self.raiz, agregado = self._insertar(self.raiz, codigo)
        if agregado:
            self._tamano += 1
        return agregado

    def _insertar(self, nodo, codigo):
        if nodo is None:
            return NodoAsiento(codigo), True
        if codigo == nodo.codigo:
            return nodo, False

        if codigo < nodo.codigo:
            nodo.izq, agregado = self._insertar(nodo.izq, codigo)
        else:
            nodo.der, agregado = self._insertar(nodo.der, codigo)
        if not agregado:
            return nodo, False

        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        balance = self._altura(nodo.izq) - self._altura(nodo.der)

        if balance > 1:
            if codigo > nodo.izq.codigo:
                nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo), True
        if balance < -1:
            if codigo < nodo.der.codigo:
                nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo), True
        return nodo, True

    @staticmethod
    def _altura(nodo):
        return 0 if nodo is None else nodo.altura

    def _rotar_derecha(self, nodo):
        nueva_raiz = nodo.izq
        nodo.izq = nueva_raiz.der
        nueva_raiz.der = nodo
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        nueva_raiz.altura = 1 + max(
            self._altura(nueva_raiz.izq), self._altura(nueva_raiz.der)
        )
        return nueva_raiz

    def _rotar_izquierda(self, nodo):
        nueva_raiz = nodo.der
        nodo.der = nueva_raiz.izq
        nueva_raiz.izq = nodo
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        nueva_raiz.altura = 1 + max(
            self._altura(nueva_raiz.izq), self._altura(nueva_raiz.der)
        )
        return nueva_raiz

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
