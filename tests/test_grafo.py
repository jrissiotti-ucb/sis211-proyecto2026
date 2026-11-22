"""
Casos límite v3 — grafo del recinto.

Ejecutar desde la raíz del repo:
  python tests/test_grafo.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.recinto_grafo import GrafoRecinto
from src.sistema import SistemaVentaEntradas, cargar_recinto_demo, PUERTA_PRINCIPAL


def armar_cuadrado():
    """0-1, 0-2, 1-3, 2-3: dos recorridos del mismo largo de 0 a 3 (un ciclo)."""
    g = GrafoRecinto()
    for z in ("0", "1", "2", "3"):
        g.agregar_zona(z)
    for a, b in (("0", "1"), ("0", "2"), ("1", "3"), ("2", "3")):
        g.conectar(a, b)
    return g


def armar_sistema():
    s = SistemaVentaEntradas()
    s.agregar_evento("E1", "Concierto")
    for c in ("A-01", "B-01", "C-01", "Z-01"):
        s.agregar_entrada(c, "E1", 10.0)
    cargar_recinto_demo(s)
    return s


def test_grafo_vacio():
    g = GrafoRecinto()
    assert g.esta_vacio() and len(g) == 0 and g.zonas() == [] and g.pasillos() == []
    try:
        g.camino("A", "B")
        assert False
    except KeyError:
        pass


def test_pasillo_repetido_no_duplica():
    g = armar_cuadrado()
    g.conectar("0", "1")
    g.conectar("1", "0")
    assert g.vecinos("0") == ["1", "2"] and len(g.pasillos()) == 4


def test_errores_de_construccion():
    g = armar_cuadrado()
    for accion in (lambda: g.agregar_zona("0"), lambda: g.conectar("0", "0")):
        try:
            accion()
            assert False
        except ValueError:
            pass
    try:
        g.conectar("0", "9")
        assert False
    except KeyError:
        pass


def test_camino_y_empate():
    g = armar_cuadrado()
    assert g.camino("0", "3") == ["0", "1", "3"]  # empate: gana el que el BFS halla primero
    assert g.camino("0", "0") == ["0"] and g.distancia("0", "0") == 0
    assert g.distancia("0", "3") == 2
    assert g.bfs("0") == ["0", "1", "2", "3"]


def test_destino_al_que_no_se_llega():
    g = armar_cuadrado()
    g.agregar_zona("aislada")
    assert g.camino("0", "aislada") is None and g.distancia("0", "aislada") == -1
    g.cerrar("1")
    g.cerrar("2")
    assert g.camino("0", "3") is None  # los dos pasillos están cerrados
    assert g.bfs("0") == ["0"]
    g.abrir("1")
    assert g.camino("0", "3") == ["0", "1", "3"]


def test_cerrada_no_se_cruza_y_busca_otro_camino():
    g = armar_cuadrado()
    g.cerrar("1")
    assert g.camino("0", "3") == ["0", "2", "3"]
    assert g.camino("0", "1") is None and g.camino("1", "0") is None
    assert g.bfs("1") == []


def test_sistema_ruta_a_asiento():
    s = armar_sistema()
    assert s.ruta_a_asiento("A-01") == [PUERTA_PRINCIPAL, "Hall", "Pasillo norte", "Zona A"]
    s.cerrar_zona("Pasillo norte")
    assert s.ruta_a_asiento("A-01")[-1] == "Zona A"
    assert "Pasillo norte" not in s.ruta_a_asiento("A-01")
    s.cerrar_zona("Zona A")
    assert s.ruta_a_asiento("A-01") is None  # caso límite: destino al que no se llega


def test_sistema_limites():
    s = armar_sistema()
    assert s.ruta_a_asiento("Z-01") is None  # fila sin zona en el mapa
    try:
        s.ruta_a_asiento("X-99")
        assert False
    except KeyError:
        pass
    try:
        s.ruta_a_asiento("A-01", desde="Azotea")
        assert False
    except KeyError:
        pass
    vacio = SistemaVentaEntradas()
    assert vacio.recinto.esta_vacio()


def test_v1_y_v2_siguen_igual():
    s = armar_sistema()
    s.llegar_comprador("Ana")
    assert s.atender_y_vender("A-01").comprador == "Ana"
    assert [e.entrada_id for e in s.listar_fila("A")] == ["A-01"]
    assert s.ruta_a_asiento("A-01") is not None


if __name__ == "__main__":
    test_grafo_vacio()
    test_pasillo_repetido_no_duplica()
    test_errores_de_construccion()
    test_camino_y_empate()
    test_destino_al_que_no_se_llega()
    test_cerrada_no_se_cruza_y_busca_otro_camino()
    test_sistema_ruta_a_asiento()
    test_sistema_limites()
    test_v1_y_v2_siguen_igual()
    print("OK — todos los tests del grafo del recinto pasaron.")
