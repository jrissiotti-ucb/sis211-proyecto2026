"""Entrada / asiento identificada por entrada_id."""


class Entrada:
    def __init__(self, entrada_id, evento_id, precio=0.0):
        self.entrada_id = entrada_id
        self.evento_id = evento_id
        self.precio = float(precio)
        self.vendida = False
        self.comprador = None

    def __repr__(self):
        estado = "vendida" if self.vendida else "disponible"
        return f"Entrada({self.entrada_id!r}, evento={self.evento_id!r}, {estado})"
