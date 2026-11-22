"""
Pruebas de la interfaz web (v3): la capa que une el sistema con la página.

Ejecutar desde la raíz del repo:
  python tests/test_interfaz.py
"""

import json
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.interfaz import Aplicacion, crear_manejador


def pedir(app, metodo, ruta, consulta=None, cuerpo=None):
    return app.atender(metodo, ruta, consulta or {}, cuerpo or {})


def test_estado_inicial():
    codigo, d = pedir(Aplicacion(), "GET", "/api/estado")
    codigos = [e["id"] for e in d["entradas"]]
    assert codigo == 200 and codigos == sorted(codigos)  # salen en orden (BST)
    assert d["cola"][0] == "Lucía Mamani" and len(d["recinto"]["zonas"]) == 10


def test_vender_devuelve_ruta():
    app = Aplicacion()
    codigo, d = pedir(app, "POST", "/api/vender", cuerpo={"entrada_id": "C-01"})
    assert codigo == 200 and d["entrada"]["comprador"] == "Lucía Mamani"
    assert d["ruta"]["ruta"][0] == "Puerta principal" and d["ruta"]["ruta"][-1] == "Zona C"


def test_limites_son_400_y_no_rompen():
    app = Aplicacion()
    assert pedir(app, "POST", "/api/vender", cuerpo={"entrada_id": "Z-99"})[0] == 400
    assert pedir(app, "POST", "/api/vender", cuerpo={"entrada_id": "A-03"})[0] == 400  # ya vendida
    assert pedir(app, "POST", "/api/comprador", cuerpo={"nombre": "  "})[0] == 400
    assert pedir(app, "GET", "/api/ruta", {"hacia": ["Zona X"]})[0] == 400
    assert pedir(app, "GET", "/api/nada")[0] == 404


def test_zona_cerrada_sin_ruta():
    app = Aplicacion()
    pedir(app, "POST", "/api/zona", cuerpo={"zona": "Zona B", "cerrada": True})
    _, r = pedir(app, "GET", "/api/ruta", {"hacia": ["Zona B"]})
    assert r["ruta"] is None and r["tramos"] is None
    _, r = pedir(app, "GET", "/api/ruta", {"entrada": ["B-01"]})
    assert r["ruta"] is None
    pedir(app, "POST", "/api/zona", cuerpo={"zona": "Zona B", "cerrada": False})
    assert pedir(app, "GET", "/api/ruta", {"hacia": ["Zona B"]})[1]["tramos"] == 3


def test_consultas_de_asientos_e_historial():
    app = Aplicacion()
    _, d = pedir(app, "GET", "/api/asientos", {"desde": ["A-02"], "hasta": ["A-04"]})
    assert [e["id"] for e in d["entradas"]] == ["A-02", "A-03", "A-04"]
    assert pedir(app, "GET", "/api/asientos", {"fila": ["Q"]})[1]["entradas"] == []
    assert pedir(app, "GET", "/api/asientos", {"codigo": ["Z-99"]})[1]["existe"] is False
    reservas = pedir(app, "GET", "/api/historial")[1]["reservas"]
    assert len(reservas) == 2 and reservas[0]["zona"] == "Zona A"
    assert "zona" not in app.s.historial.todas()[0]
    assert pedir(app, "GET", "/api/historial", {"comprador": ["Nadie"]})[1]["reservas"] == []


def test_servidor_http_real():
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), crear_manejador(Aplicacion()))
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()
    base = "http://127.0.0.1:%d" % servidor.server_address[1]
    try:
        pagina = urllib.request.urlopen(base + "/").read().decode("utf-8")
        assert "<title>Taquilla" in pagina
        estado = json.loads(urllib.request.urlopen(base + "/api/estado").read())
        assert len(estado["entradas"]) == 32
    finally:
        servidor.shutdown()
        servidor.server_close()


if __name__ == "__main__":
    test_estado_inicial()
    test_vender_devuelve_ruta()
    test_limites_son_400_y_no_rompen()
    test_zona_cerrada_sin_ruta()
    test_consultas_de_asientos_e_historial()
    test_servidor_http_real()
    print("OK — todos los tests de la interfaz pasaron.")
