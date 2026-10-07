"""
Casos límite v1 — venta de entradas para eventos.

Ejecutar desde la raíz del repo:
  python tests/test_limites.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cola_compradores import ColaCompradores
from src.catalogo import CatalogoEntradas
from src.entrada import Entrada
from src.historial import HistorialReservas
from src.sistema import SistemaVentaEntradas


def test_cola_vacia():
    cola = ColaCompradores()
    try:
        cola.atender()
        assert False, "Debía lanzar IndexError"
    except IndexError as e:
        assert "No hay compradores en espera" in str(e)


def test_entrada_inexistente():
    catalogo = CatalogoEntradas()
    try:
        catalogo.consulta("A-99")
        assert False, "Debía lanzar KeyError"
    except KeyError as e:
        assert "Entrada no encontrada" in str(e)


def test_historial_vacio():
    hist = HistorialReservas()
    assert hist.de_usuario("Ana") == []
    assert hist.esta_vacio() is True


def test_entrada_duplicada():
    cat = CatalogoEntradas()
    cat.alta(Entrada("A-01", "EVT-1", 50.0))
    cat.vender("A-01", "Ana")
    try:
        cat.vender("A-01", "Beto")
        assert False, "Debía lanzar ValueError"
    except ValueError as e:
        assert "ya vendida" in str(e).lower()


def test_flujo_completo_fifo():
    s = SistemaVentaEntradas()
    s.agregar_evento("EVT-1", "Concierto Rock")
    s.agregar_entrada("A-01", "EVT-1", 80.0)
    s.agregar_entrada("A-02", "EVT-1", 80.0)

    s.llegar_comprador("Ana")
    s.llegar_comprador("Beto")

    e1 = s.atender_y_vender("A-01")
    assert e1.comprador == "Ana"
    assert e1.vendida is True

    e2 = s.atender_y_vender("A-02")
    assert e2.comprador == "Beto"

    assert s.historial_de("Ana") == [
        {"comprador": "Ana", "entrada_id": "A-01", "evento_id": "EVT-1"}
    ]
    assert len(s.historial_de("Cora")) == 0


def test_listar_eventos():
    s = SistemaVentaEntradas()
    s.agregar_evento("E1", "Obra")
    s.agregar_evento("E2", "Feria")
    nombres = [ev.nombre for ev in s.listar_eventos()]
    assert nombres == ["Obra", "Feria"]


def test_caso_limite():
    test_cola_vacia()
    test_entrada_inexistente()
    test_historial_vacio()
    test_entrada_duplicada()


if __name__ == "__main__":
    test_cola_vacia()
    test_entrada_inexistente()
    test_historial_vacio()
    test_entrada_duplicada()
    test_flujo_completo_fifo()
    test_listar_eventos()
    test_caso_limite()
    print("OK — todos los tests de límites y flujo pasaron.")
