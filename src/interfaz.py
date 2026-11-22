"""
Interfaz web local del sistema de venta de entradas (v3).

Servidor mínimo con la biblioteca estándar: no hay que instalar nada.
Las clases del dominio no cambian; la interfaz solo las llama.

Desde la raíz del repo:
  python src/interfaz.py            # abre el navegador en http://127.0.0.1:8765
  python src/interfaz.py --puerto 9000 --sin-navegador
"""

import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.sistema import SistemaVentaEntradas, cargar_recinto_demo, PUERTA_PRINCIPAL
    from src.pagina import PAGINA
else:
    from .sistema import SistemaVentaEntradas, cargar_recinto_demo, PUERTA_PRINCIPAL
    from .pagina import PAGINA

ERRORES_DE_DOMINIO = (KeyError, ValueError, IndexError)

# Cómo se dibuja el mapa del recinto (solo presentación): zona -> (x, y, detalle)
DISENO_MAPA = {
    PUERTA_PRINCIPAL: (74, 225, "Acceso"),
    "Hall": (222, 225, "Distribuidor"),
    "Baños": (222, 372, "Servicios"),
    "Pasillo norte": (392, 112, "Circulación"),
    "Pasillo sur": (392, 338, "Circulación"),
    "Zona A": (580, 62, "Platea"),
    "Zona B": (580, 168, "Preferencial"),
    "Zona C": (580, 282, "VIP"),
    "Zona D": (580, 388, "Balcón"),
    "Salida de emergencia": (730, 388, "Solo salida"),
}


def cargar_datos_interfaz(s):
    """Datos de ejemplo más completos que los del menú, para ver el mapa de asientos."""
    s.agregar_evento("E1", "Concierto Rock")
    s.agregar_evento("E2", "Obra de teatro")
    tarifas = (("A", "E1", 8, 120.0), ("B", "E1", 8, 180.0), ("C", "E1", 6, 320.0),
               ("D", "E2", 10, 90.0))
    for fila, evento, cantidad, precio in tarifas:
        for n in range(1, cantidad + 1):
            s.agregar_entrada(f"{fila}-{n:02d}", evento, precio)
    for nombre in ("Camila Rojas", "Diego Vargas"):
        s.llegar_comprador(nombre)
    s.atender_y_vender("A-03")
    s.atender_y_vender("A-04")
    for nombre in ("Lucía Mamani", "Mateo Quispe", "Valeria Choque"):
        s.llegar_comprador(nombre)


class Aplicacion:
    """Une el sistema con la interfaz. Cada método devuelve datos listos para JSON."""

    def __init__(self, sistema=None):
        if sistema is None:
            sistema = SistemaVentaEntradas()
            cargar_datos_interfaz(sistema)
            cargar_recinto_demo(sistema)
        self.s = sistema
        self._cerrojo = threading.Lock()

    # --- lectura ----------------------------------------------------------

    def _entrada(self, e):
        return {
            "id": e.entrada_id,
            "evento": e.evento_id,
            "fila": e.entrada_id.split("-")[0],
            "precio": e.precio,
            "vendida": e.vendida,
            "comprador": e.comprador,
            "zona": self.s.zona_de_asiento(e.entrada_id),
        }

    def estado(self):
        entradas = [self._entrada(e) for e in self.s.listar_asientos()]  # BST: en orden
        eventos = []
        for ev in self.s.listar_eventos():
            propias = [e for e in entradas if e["evento"] == ev.evento_id]
            eventos.append({
                "id": ev.evento_id,
                "nombre": ev.nombre,
                "total": len(propias),
                "libres": len([e for e in propias if not e["vendida"]]),
            })
        r = self.s.recinto
        zonas = []
        for z in r.zonas():
            x, y, detalle = DISENO_MAPA.get(z, (400, 225, ""))
            zonas.append({"id": z, "x": x, "y": y, "detalle": detalle,
                          "asientos": z.startswith("Zona "), "cerrada": r.esta_cerrada(z)})
        return {
            "eventos": eventos,
            "entradas": entradas,
            "cola": self.s.cola.en_espera(),
            "reservas": len(self.s.historial),
            "recinto": {"zonas": zonas, "pasillos": r.pasillos(), "puerta": PUERTA_PRINCIPAL},
        }

    def ruta(self, entrada=None, desde=None, hacia=None):
        desde = desde or PUERTA_PRINCIPAL
        if entrada:
            ruta = self.s.ruta_a_asiento(entrada, desde)
            hacia = self.s.zona_de_asiento(entrada)
        else:
            ruta = self.s.recinto.camino(desde, hacia)
        return {"desde": desde, "hacia": hacia, "ruta": ruta,
                "tramos": None if ruta is None else len(ruta) - 1}

    def asientos(self, fila="", desde="", hasta="", codigo=""):
        if codigo:
            return {"existe": self.s.existe_asiento(codigo), "codigo": codigo}
        if desde or hasta:
            if not (desde and hasta):
                raise ValueError("Indica los dos códigos del rango")
            lista = self.s.asientos_entre(desde, hasta)
        elif fila:
            lista = self.s.listar_fila(fila)
        else:
            lista = self.s.listar_asientos()
        return {"entradas": [self._entrada(e) for e in lista]}

    def historial(self, comprador=""):
        if comprador:
            reservas = self.s.historial_de(comprador)
        else:
            reservas = self.s.historial.todas()
        con_zona = [
            {**r, "zona": self.s.zona_de_asiento(r["entrada_id"])}
            for r in reservas
        ]
        return {"reservas": con_zona}

    # --- acciones ---------------------------------------------------------

    def llegar(self, nombre):
        nombre = (nombre or "").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        self.s.llegar_comprador(nombre)
        return {"cola": self.s.cola.en_espera()}

    def vender(self, entrada_id):
        e = self.s.atender_y_vender(entrada_id)
        return {"entrada": self._entrada(e), "ruta": self.ruta(entrada=entrada_id)}

    def zona(self, zona, cerrada):
        if cerrada:
            self.s.cerrar_zona(zona)
        else:
            self.s.abrir_zona(zona)
        return {"zona": zona, "cerrada": bool(cerrada)}

    # --- despacho ---------------------------------------------------------

    def atender(self, metodo, ruta, consulta, cuerpo):
        """Devuelve (código, datos). Los casos límite del dominio salen como 400."""
        q = {k: v[0] for k, v in consulta.items()}
        with self._cerrojo:
            try:
                if metodo == "GET" and ruta == "/api/estado":
                    return 200, self.estado()
                if metodo == "GET" and ruta == "/api/ruta":
                    return 200, self.ruta(q.get("entrada"), q.get("desde"), q.get("hacia"))
                if metodo == "GET" and ruta == "/api/asientos":
                    return 200, self.asientos(q.get("fila", ""), q.get("desde", ""),
                                              q.get("hasta", ""), q.get("codigo", ""))
                if metodo == "GET" and ruta == "/api/historial":
                    return 200, self.historial(q.get("comprador", ""))
                if metodo == "POST" and ruta == "/api/comprador":
                    return 200, self.llegar(cuerpo.get("nombre"))
                if metodo == "POST" and ruta == "/api/vender":
                    return 200, self.vender(cuerpo.get("entrada_id", ""))
                if metodo == "POST" and ruta == "/api/zona":
                    return 200, self.zona(cuerpo.get("zona", ""), cuerpo.get("cerrada"))
            except ERRORES_DE_DOMINIO as e:
                return 400, {"error": str(e.args[0] if e.args else e)}
        return 404, {"error": "No existe esa ruta"}


def crear_manejador(app):
    class Manejador(BaseHTTPRequestHandler):
        def _responder(self, codigo, datos, tipo="application/json; charset=utf-8"):
            cuerpo = datos if isinstance(datos, bytes) else json.dumps(datos).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(cuerpo)

        def _atender(self, metodo):
            url = urlparse(self.path)
            if metodo == "GET" and url.path in ("/", "/index.html"):
                return self._responder(200, PAGINA.encode("utf-8"), "text/html; charset=utf-8")
            cuerpo = {}
            if metodo == "POST":
                largo = int(self.headers.get("Content-Length") or 0)
                try:
                    cuerpo = json.loads(self.rfile.read(largo) or b"{}")
                except ValueError:
                    return self._responder(400, {"error": "Datos no válidos"})
            codigo, datos = app.atender(metodo, url.path, parse_qs(url.query), cuerpo)
            self._responder(codigo, datos)

        def do_GET(self):
            self._atender("GET")

        def do_POST(self):
            self._atender("POST")

        def log_message(self, *args):
            pass  # sin ruido en la terminal

    return Manejador


def servir(puerto=8765, abrir_navegador=True, app=None):
    app = app or Aplicacion()
    servidor = None
    for p in range(puerto, puerto + 20):
        try:
            servidor = ThreadingHTTPServer(("127.0.0.1", p), crear_manejador(app))
            break
        except OSError:
            continue
    if servidor is None:
        raise SystemExit("No hay un puerto libre cerca de %d" % puerto)
    url = "http://127.0.0.1:%d" % servidor.server_address[1]
    print("Interfaz lista en", url, "(Ctrl+C para cerrar)")
    if abrir_navegador:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nHasta luego.")
    finally:
        servidor.server_close()


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    puerto = 8765
    if "--puerto" in argv:
        puerto = int(argv[argv.index("--puerto") + 1])
    servir(puerto, abrir_navegador="--sin-navegador" not in argv)


if __name__ == "__main__":
    main()
