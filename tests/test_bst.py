"""
Casos límite v2 — BST de asientos.

Ejecutar desde la raíz del repo:
  python tests/test_bst.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.asientos_bst import ArbolAsientos
from src.sistema import SistemaVentaEntradas


def armar_arbol():
    a = ArbolAsientos()
    for c in ["B-02", "A-03", "A-01", "B-01", "A-02", "C-01"]:
        a.insertar(c)
    return a


def armar_sistema():
    s = SistemaVentaEntradas()
    s.agregar_evento("E1", "Concierto")
    for c in ["B-02", "A-03", "A-01", "B-01", "A-02"]:  # a propósito desordenado
        s.agregar_entrada(c, "E1", 10.0)
    return s


def verificar_balance(nodo):
    if nodo is None:
        return 0
    altura_izquierda = verificar_balance(nodo.izq)
    altura_derecha = verificar_balance(nodo.der)
    assert abs(altura_izquierda - altura_derecha) <= 1
    assert nodo.altura == 1 + max(altura_izquierda, altura_derecha)
    return nodo.altura


def test_arbol_vacio():
    a = ArbolAsientos()
    assert a.esta_vacio() and len(a) == 0
    assert a.listar_en_orden() == [] and a.rango("A", "Z") == []
    assert a.existe("A-01") is False


def test_no_encontrado():
    assert armar_arbol().existe("Z-99") is False


def test_inorden_y_fila():
    a = armar_arbol()
    assert a.listar_en_orden() == ["A-01", "A-02", "A-03", "B-01", "B-02", "C-01"]
    assert a.con_prefijo("A-") == ["A-01", "A-02", "A-03"]


def test_rango():
    a = armar_arbol()
    assert a.rango("A-02", "B-01") == ["A-02", "A-03", "B-01"]
    assert a.rango("D-01", "D-99") == []          # ninguno en el rango
    assert a.rango("B-01", "A-01") == []          # rango invertido
    assert a.con_prefijo("Z-") == []              # fila inexistente


def test_duplicado():
    a = armar_arbol()
    assert a.insertar("A-01") is False and len(a) == 6


def test_rotaciones_avl():
    for codigos in (("C", "B", "A"), ("A", "B", "C"),
                    ("C", "A", "B"), ("A", "C", "B")):
        a = ArbolAsientos()
        for codigo in codigos:
            a.insertar(codigo)
        assert a.raiz.codigo == "B"
        assert a.listar_en_orden() == ["A", "B", "C"]
        verificar_balance(a.raiz)


def test_inserciones_ordenadas_se_autobalancean():
    a = ArbolAsientos()
    for i in range(3000):            # inserción ordenada: debe conservar balance AVL
        a.insertar(f"A-{i:05d}")
    assert len(a.listar_en_orden()) == 3000
    assert len(a.rango("A-00010", "A-00019")) == 10
    assert verificar_balance(a.raiz) <= 20


def test_sistema_fila_en_orden():
    s = armar_sistema()
    assert [e.entrada_id for e in s.listar_fila("A")] == ["A-01", "A-02", "A-03"]
    assert [e.entrada_id for e in s.listar_asientos()] == [
        "A-01", "A-02", "A-03", "B-01", "B-02"]


def test_sistema_limites():
    s = armar_sistema()
    assert s.existe_asiento("A-01") is True
    assert s.existe_asiento("Z-99") is False
    assert s.listar_fila("Z") == []
    assert s.asientos_entre("X-01", "X-09") == []
    vacio = SistemaVentaEntradas()
    assert vacio.listar_asientos() == [] and vacio.listar_fila("A") == []


def test_v1_sigue_igual():
    s = armar_sistema()
    s.llegar_comprador("Ana")
    e = s.atender_y_vender("A-02")
    assert e.comprador == "Ana"
    assert [x.vendida for x in s.listar_fila("A")] == [False, True, False]


if __name__ == "__main__":
    test_arbol_vacio()
    test_no_encontrado()
    test_inorden_y_fila()
    test_rango()
    test_duplicado()
    test_rotaciones_avl()
    test_inserciones_ordenadas_se_autobalancean()
    test_sistema_fila_en_orden()
    test_sistema_limites()
    test_v1_sigue_igual()
    print("OK — todos los tests del BST de asientos pasaron.")
