"""
Historial de reservas en orden de compra.
Familia: lista.
"""


class HistorialReservas:
    def __init__(self):
        self._reservas = []

    def registrar(self, comprador, entrada_id, evento_id):
        """Agrega una reserva al final (orden cronológico)."""
        self._reservas.append(
            {"comprador": comprador, "entrada_id": entrada_id, "evento_id": evento_id}
        )

    def de_usuario(self, comprador):
        """
        Reservas de ese comprador, en el orden en que se hicieron.
        Sin compras → lista vacía.
        """
        return [r for r in self._reservas if r["comprador"] == comprador]

    def todas(self):
        return list(self._reservas)

    def esta_vacio(self):
        return len(self._reservas) == 0

    def __len__(self):
        return len(self._reservas)

    def __repr__(self):
        return f"HistorialReservas({len(self._reservas)} reservas)"
