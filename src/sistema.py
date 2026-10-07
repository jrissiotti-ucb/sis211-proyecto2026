"""
Orquesta cola (FIFO), catálogo (hash) e historial (lista).
Aquí se combinan los tres flujos del mapa v1.
"""

from .evento import Evento
from .entrada import Entrada
from .cola_compradores import ColaCompradores
from .catalogo import CatalogoEntradas
from .historial import HistorialReservas


class SistemaVentaEntradas:
    def __init__(self):
        self.eventos = {}
        self.catalogo = CatalogoEntradas()
        self.cola = ColaCompradores()
        self.historial = HistorialReservas()

    def agregar_evento(self, evento_id, nombre):
        self.eventos[evento_id] = Evento(evento_id, nombre)

    def listar_eventos(self):
        """Lista de eventos en orden de inserción."""
        return list(self.eventos.values())

    def agregar_entrada(self, entrada_id, evento_id, precio=0.0):
        if evento_id not in self.eventos:
            raise KeyError(f"Evento no encontrado: {evento_id}")
        entrada = Entrada(entrada_id, evento_id, precio)
        self.catalogo.alta(entrada)
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
        """Atiende al frente de la cola y le vende esa entrada."""
        comprador = self.atender_siguiente()
        return self.vender_a(entrada_id, comprador)

    def historial_de(self, comprador):
        """Reservas del usuario (lista). Vacío → []."""
        return self.historial.de_usuario(comprador)
