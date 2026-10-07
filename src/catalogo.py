"""
Catálogo de entrada_id de asiento/entrada → Entrada.
Familia: tabla hash (dict).
"""

from .entrada import Entrada


class CatalogoEntradas:
    def __init__(self):
        self._por_entrada_id = {}

    def alta(self, entrada):
        """Registra o actualiza una entrada por su entrada_id."""
        self._por_entrada_id[entrada.entrada_id] = entrada

    def consulta(self, entrada_id):
        """Devuelve la Entrada. Si no está → KeyError."""
        if entrada_id not in self._por_entrada_id:
            raise KeyError(f"Entrada no encontrada: {entrada_id}")
        return self._por_entrada_id[entrada_id]

    def contiene(self, entrada_id):
        return entrada_id in self._por_entrada_id

    def vender(self, entrada_id, comprador):
        """
        Marca la entrada como vendida.
        - entrada_id inexistente → KeyError
        - Ya vendida → ValueError (duplicado)
        """
        entrada = self.consulta(entrada_id)
        if entrada.vendida:
            raise ValueError(f"Entrada ya vendida: {entrada_id}")
        entrada.vendida = True
        entrada.comprador = comprador
        return entrada

    def __len__(self):
        return len(self._por_entrada_id)

    def __repr__(self):
        return f"CatalogoEntradas({len(self._por_entrada_id)} entradas)"
