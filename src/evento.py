"""Evento del dominio (concierto, obra, feria, etc.)."""


class Evento:
    def __init__(self, evento_id, nombre):
        self.evento_id = evento_id
        self.nombre = nombre

    def __repr__(self):
        return f"Evento({self.evento_id!r}, {self.nombre!r})"
