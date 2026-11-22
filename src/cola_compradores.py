"""
Cola FIFO de compradores en espera.
Familia: cola — entra al fondo (append), sale el frente (pop(0)).
"""


class ColaCompradores:
    def __init__(self):
        self._datos = []

    def encolar(self, comprador):
        """El comprador entra al fondo de la fila."""
        self._datos.append(comprador)

    def atender(self):
        """Atiende al primero. Cola vacía → IndexError."""
        if not self._datos:
            raise IndexError("No hay compradores en espera")
        return self._datos.pop(0)

    def frente(self):
        """Mira el siguiente sin sacarlo. Vacía → IndexError."""
        if not self._datos:
            raise IndexError("No hay compradores en espera")
        return self._datos[0]

    def en_espera(self):
        """Copia de los compradores en espera, del frente al fondo."""
        return list(self._datos)

    def esta_vacia(self):
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"ColaCompradores({self._datos!r})"
