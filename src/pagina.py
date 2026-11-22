"""
Página de la interfaz web (HTML, CSS y JavaScript en un solo texto).
La sirve src/interfaz.py; no hay archivos estáticos aparte.
"""

PAGINA = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Taquilla · Venta de entradas</title>
<style>
:root{
  --paper:#f2efe9; --panel:#fffdf9; --ink:#16181b; --ink2:#454a52; --mute:#868b93;
  --line:#e2ddd2; --line2:#cfc9bc; --accent:#b23d27; --accent-d:#8f2f1d; --accent-t:#f7e6e1;
  --route:#0a6b67; --route-t:#dcefed; --ok:#2e6b4c; --ok-t:#e1efe7; --warn-t:#fbece7;
  --side:#14171b; --side2:#1e2228; --side-ink:#c6c9ce;
  --serif:Georgia,"Iowan Old Style","Palatino Linotype",serif;
  --sans:"Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.45 var(--sans);-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}
.shell{display:grid;grid-template-columns:240px 1fr;min-height:100%}
/* ---- barra lateral ---- */
.side{background:var(--side);color:var(--side-ink);display:flex;flex-direction:column;padding:22px 14px;position:sticky;top:0;height:100vh}
.brand{display:flex;align-items:center;gap:11px;padding:2px 8px 22px}
.mark{width:34px;height:34px;border-radius:8px;background:var(--accent);position:relative;flex:none}
.mark:before,.mark:after{content:"";position:absolute;top:50%;width:9px;height:9px;margin-top:-4.5px;background:var(--side);border-radius:50%}
.mark:before{left:-4.5px}.mark:after{right:-4.5px}
.mark i{position:absolute;left:50%;top:7px;bottom:7px;border-left:2px dashed rgba(255,255,255,.7)}
.brand b{display:block;color:#fff;font:600 19px var(--serif);letter-spacing:.2px}
.brand small{color:#8c9097;font-size:11.5px;letter-spacing:.3px}
.nav{display:flex;flex-direction:column;gap:3px}
.nav button{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:7px;cursor:pointer;color:var(--side-ink);position:relative;transition:background .15s,color .15s}
.nav button:hover{background:var(--side2);color:#fff}
.nav button:focus-visible{outline:2px solid #fff;outline-offset:1px}
.nav button.on{background:var(--side2);color:#fff}
.nav button.on:before{content:"";position:absolute;left:-14px;top:9px;bottom:9px;width:3px;border-radius:0 3px 3px 0;background:var(--accent)}
.nav svg{width:18px;height:18px;flex:none;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.nav .n{margin-left:auto;font-size:11.5px;background:#2b3038;color:#d9dce0;border-radius:10px;padding:1px 8px}
.side .foot{margin-top:auto;padding:14px 10px 4px;border-top:1px solid #262a31;font-size:12px;color:#7d828a;line-height:1.6}
.side .foot b{color:#aeb2b8;font-weight:600}
/* ---- contenido ---- */
.main{padding:30px 38px 48px;max-width:1320px;width:100%}
.top{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:24px;flex-wrap:wrap}
.top h1{margin:0;font:600 30px/1.15 var(--serif);letter-spacing:-.2px}
.top p{margin:6px 0 0;color:var(--ink2);max-width:62ch}
.seg{display:inline-flex;background:#e8e3d8;border-radius:9px;padding:3px}
.seg button{all:unset;cursor:pointer;padding:7px 15px;border-radius:7px;color:var(--ink2);font-weight:500;transition:background .15s}
.seg button:hover{color:var(--ink)}
.seg button.on{background:var(--panel);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.12)}
.seg button:focus-visible{outline:2px solid var(--ink)}
.seg small{color:var(--mute);margin-left:6px;font-weight:400}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:22px;align-items:start}
.grid.map{grid-template-columns:minmax(0,1fr) 340px}
.stack{display:flex;flex-direction:column;gap:22px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:22px}
.card h2{margin:0 0 4px;font:600 12px var(--sans);letter-spacing:1.1px;text-transform:uppercase;color:var(--mute)}
.card .sub{color:var(--ink2);margin:0 0 16px}
.row{display:flex;align-items:center;gap:10px}
.between{justify-content:space-between}
.btn{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:9px 16px;border-radius:8px;background:var(--ink);color:#fff;font-weight:600;transition:background .15s,transform .05s}
.btn:hover{background:#2c3036}.btn:active{transform:translateY(1px)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn.acc{background:var(--accent)}.btn.acc:hover{background:var(--accent-d)}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line2)}.btn.ghost:hover{background:#f0ece3}
.btn.sm{padding:5px 11px;font-size:12.5px}
.btn[disabled]{opacity:.4;cursor:not-allowed;pointer-events:none}
.btn.block{width:100%}
input[type=text],select{width:100%;padding:9px 12px;border:1px solid var(--line2);border-radius:8px;background:#fff;outline:none;transition:border-color .15s,box-shadow .15s}
input[type=text]:focus,select:focus{border-color:var(--ink);box-shadow:0 0 0 3px rgba(22,24,27,.08)}
label.f{display:block;font-size:12px;font-weight:600;color:var(--ink2);margin:0 0 5px}
.chip{display:inline-block;font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:20px;background:#ece8de;color:var(--ink2)}
.chip.ok{background:var(--ok-t);color:var(--ok)}.chip.sold{background:#e9e5dc;color:#7a7f86}
.chip.warn{background:var(--warn-t);color:var(--accent-d)}.chip.route{background:var(--route-t);color:var(--route)}
/* ---- asientos ---- */
.stage{margin:0 auto 24px;width:70%;text-align:center;padding:8px;border-radius:0 0 40px 40px;background:linear-gradient(#ebe6da,#f4f0e7);border:1px solid var(--line);border-top:3px solid var(--ink);font-size:11px;letter-spacing:3px;color:var(--mute);font-weight:600}
.fila{display:flex;align-items:center;gap:16px;margin-bottom:14px}
.fila .lab{width:128px;flex:none}
.fila .lab b{display:block;font:600 17px var(--serif)}
.fila .lab span{font-size:12px;color:var(--mute)}
.fila .lab em{font-style:normal;font-size:12px;color:var(--ink2)}
.seats{display:flex;flex-wrap:wrap;gap:7px}
.seat{all:unset;box-sizing:border-box;width:38px;height:36px;border-radius:7px 7px 11px 11px;border:1.5px solid var(--line2);background:#fff;text-align:center;line-height:33px;font-size:12px;font-weight:600;cursor:pointer;font-variant-numeric:tabular-nums;transition:border-color .12s,background .12s,transform .08s}
.seat:hover{border-color:var(--ink);transform:translateY(-1px)}
.seat:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.seat.sold{background:repeating-linear-gradient(135deg,#ebe7dd 0 4px,#e2ddd1 4px 8px);color:#9a9ea5;border-color:#d8d3c7}
.seat.sel{background:var(--ink);border-color:var(--ink);color:#fff}
.legend{display:flex;gap:18px;margin-top:22px;padding-top:16px;border-top:1px solid var(--line);color:var(--ink2);font-size:12.5px;flex-wrap:wrap}
.legend i{display:inline-block;width:14px;height:13px;border-radius:4px 4px 6px 6px;border:1.5px solid var(--line2);background:#fff;vertical-align:-2px;margin-right:6px}
.legend i.s{background:repeating-linear-gradient(135deg,#ebe7dd 0 3px,#e2ddd1 3px 6px)}.legend i.k{background:var(--ink);border-color:var(--ink)}
/* ---- cola ---- */
.cola{list-style:none;margin:0 0 16px;padding:0}
.cola li{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--line)}
.cola li:last-child{border-bottom:0}
.cola .pos{width:26px;height:26px;border-radius:50%;background:#ece8de;color:var(--ink2);font-weight:600;font-size:12px;display:grid;place-items:center;flex:none}
.cola li.first .pos{background:var(--accent);color:#fff}
.cola li.first{font-weight:600}
.cola .tag{margin-left:auto}
.vacio{color:var(--mute);padding:14px 0 18px}
.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0 0 16px}
.kv dt{color:var(--mute)}.kv dd{margin:0;font-weight:600;text-align:right}
.price{font:600 30px var(--serif)}
.path{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:6px 0 0}
.path span{background:var(--route-t);color:var(--route);padding:3px 10px;border-radius:6px;font-size:12.5px;font-weight:600}
.path em{font-style:normal;color:var(--route);opacity:.55}
.aviso{background:var(--warn-t);color:var(--accent-d);border-radius:8px;padding:10px 13px;font-size:13px}
/* ---- entrada emitida ---- */
.ticket{display:grid;grid-template-columns:1fr 104px;background:#fffefb;border:1px solid var(--line2);border-radius:12px;position:relative;overflow:hidden;box-shadow:0 10px 24px -14px rgba(22,24,27,.35)}
.ticket:before,.ticket:after{content:"";position:absolute;right:96px;width:16px;height:16px;border-radius:50%;background:var(--paper);border:1px solid var(--line2)}
.ticket:before{top:-9px}.ticket:after{bottom:-9px}
.t-main{padding:20px 22px;border-right:2px dashed var(--line2)}
.t-k{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--accent);font-weight:700}
.t-seat{font:600 46px/1.05 var(--serif);margin:6px 0 2px;letter-spacing:-1px}
.t-meta{color:var(--ink2);font-size:13px;display:flex;gap:6px 14px;flex-wrap:wrap}
.t-route{margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}
.t-route small{display:block;color:var(--mute);font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:600}
.t-stub{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:14px}
.bars{width:56px;height:96px;background:repeating-linear-gradient(90deg,var(--ink) 0 2px,transparent 2px 4px,var(--ink) 4px 5px,transparent 5px 8px,var(--ink) 8px 11px,transparent 11px 12px);-webkit-mask:linear-gradient(#000,#000);opacity:.9}
.t-stub small{font-size:10.5px;color:var(--mute);letter-spacing:1px;writing-mode:vertical-rl;transform:rotate(180deg)}
/* ---- mapa del recinto ---- */
.map-wrap{background:#faf8f3;border:1px solid var(--line);border-radius:10px;padding:6px}
svg.mapa{display:block;width:100%;height:auto}
.mapa .edge{stroke:var(--line2);stroke-width:2.5;stroke-linecap:round}
.mapa .edge.off{stroke-dasharray:3 6;opacity:.6}
.mapa .edge.on{stroke:var(--route);stroke-width:5}
.mapa .nodo rect{fill:#fff;stroke:var(--line2);stroke-width:1.5}
.mapa .nodo.asientos rect{fill:#f3efe6;stroke:#bcb5a4}
.mapa .nodo.on rect{stroke:var(--route);stroke-width:2.5;fill:var(--route-t)}
.mapa .nodo.off rect{fill:url(#rayas);stroke:#c3bdaf;stroke-dasharray:4 3}
.mapa text{font-family:var(--sans);text-anchor:middle;fill:var(--ink)}
.mapa .t1{font-size:13px;font-weight:600}.mapa .t2{font-size:10.5px;fill:var(--mute)}
.mapa .nodo.off text{fill:#9a9ea5}
.mapa .paso circle{fill:var(--route)}.mapa .paso text{fill:#fff;font-size:11px;font-weight:700}
.zonas{display:flex;flex-direction:column}
.zonas div{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line)}
.zonas div:last-child{border-bottom:0}
.steps{list-style:none;margin:12px 0 0;padding:0;position:relative}
.steps li{position:relative;padding:0 0 12px 30px;font-weight:600}
.steps li:before{content:"";position:absolute;left:8px;top:18px;bottom:-2px;border-left:2px solid var(--route);opacity:.35}
.steps li:last-child:before{display:none}
.steps li i{position:absolute;left:0;top:1px;width:18px;height:18px;border-radius:50%;background:var(--route);color:#fff;font:700 10.5px/18px var(--sans);text-align:center;font-style:normal}
.big{font:600 42px/1 var(--serif);color:var(--route)}
/* ---- tablas ---- */
table{width:100%;border-collapse:collapse}
th{font:600 11.5px var(--sans);letter-spacing:1px;text-transform:uppercase;color:var(--mute);text-align:left;padding:0 12px 10px}
td{padding:11px 12px;border-top:1px solid var(--line)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr:hover td{background:#faf7f0}
.code{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-weight:600}
.filtros{display:grid;grid-template-columns:repeat(4,1fr) auto;gap:12px;align-items:end;margin-bottom:18px}
.toast{position:fixed;right:22px;bottom:22px;display:flex;flex-direction:column;gap:10px;z-index:10}
.toast div{background:var(--ink);color:#fff;padding:12px 16px;border-radius:9px;box-shadow:0 10px 30px -10px rgba(0,0,0,.5);max-width:340px;border-left:4px solid var(--ok);animation:sube .2s ease-out}
.toast div.err{border-left-color:var(--accent)}
@keyframes sube{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (max-width:1080px){
  .shell{grid-template-columns:1fr}
  .side{position:static;height:auto;flex-direction:row;align-items:center;padding:12px 16px;gap:16px;overflow-x:auto}
  .brand{padding:0}.nav{flex-direction:row}.nav button.on:before{display:none}.side .foot{display:none}
  .grid,.grid.map{grid-template-columns:1fr}.main{padding:22px 18px 40px}
  .filtros{grid-template-columns:1fr 1fr}
}
</style>
</head>
<body>
<div class="shell">
  <aside class="side">
    <div class="brand"><span class="mark"><i></i></span><div><b>Taquilla</b><small>Venta de entradas</small></div></div>
    <nav class="nav" id="nav"></nav>
    <div class="foot"><b>SIS-211 · v3</b><br>Cola · hash · lista · BST · grafo</div>
  </aside>
  <main class="main" id="app"></main>
</div>
<div class="toast" id="toast"></div>
<script>
"use strict";
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const bs = n => "Bs " + Number(n).toLocaleString("es-BO", {minimumFractionDigits: 0, maximumFractionDigits: 2});

const S = {
  d: null, vista: "taquilla", evento: "E1", sel: null, prev: null, emitida: null,
  mapa: {desde: "Puerta principal", hacia: "Zona A", res: null},
  aq: {res: null, fila: "", desde: "", hasta: "", codigo: "", existe: null},
  hist: {q: "", res: null},
};

async function api(url, body) {
  const r = await fetch(url, body ? {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)} : undefined);
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || "Error");
  return data;
}
function aviso(msg, err) {
  const d = document.createElement("div");
  if (err) d.className = "err";
  d.textContent = msg;
  $("#toast").appendChild(d);
  setTimeout(() => d.remove(), 3600);
}
async function intentar(fn) { try { return await fn(); } catch (e) { aviso(e.message, true); } }

const ICONOS = {
  taquilla: '<path d="M3 9a2 2 0 0 0 0 6v3h18v-3a2 2 0 0 0 0-6V6H3z"/><path d="M14 6v12" stroke-dasharray="2 2.5"/>',
  recinto: '<circle cx="6" cy="6" r="2.2"/><circle cx="18" cy="8" r="2.2"/><circle cx="12" cy="18" r="2.2"/><path d="M8 7l8 1M7 8l4 8M17 10l-4 6"/>',
  asientos: '<path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/>',
  historial: '<path d="M4 6h16M4 12h16M4 18h10"/>',
};
const VISTAS = [
  ["taquilla", "Taquilla"], ["recinto", "Recinto"], ["asientos", "Asientos"], ["historial", "Historial"],
];

/* ------------------------------------------------------------------ mapa */
function mapaSVG(ruta) {
  const R = S.d.recinto, pos = {};
  R.zonas.forEach(z => pos[z.id] = z);
  const tramos = new Set();
  if (ruta) for (let i = 0; i < ruta.length - 1; i++) { tramos.add(ruta[i] + "|" + ruta[i + 1]); tramos.add(ruta[i + 1] + "|" + ruta[i]); }
  let normal = "", activo = "", nodos = "";
  R.pasillos.forEach(([a, b]) => {
    const A = pos[a], B = pos[b];
    const linea = c => `<line class="edge ${c}" x1="${A.x}" y1="${A.y}" x2="${B.x}" y2="${B.y}"/>`;
    if (tramos.has(a + "|" + b)) activo += linea("on");
    else normal += linea(A.cerrada || B.cerrada ? "off" : "");
  });
  R.zonas.forEach(z => {
    const w = Math.max(z.asientos ? 112 : 118, z.id.length * 7.6 + 30), h = 48, i = ruta ? ruta.indexOf(z.id) : -1;
    const cls = ["nodo", z.asientos ? "asientos" : "", i >= 0 ? "on" : "", z.cerrada ? "off" : ""].join(" ");
    nodos += `<g class="${cls}"><rect x="${z.x - w / 2}" y="${z.y - h / 2}" width="${w}" height="${h}" rx="9"/>
      <text class="t1" x="${z.x}" y="${z.y - 2}">${esc(z.id)}</text>
      <text class="t2" x="${z.x}" y="${z.y + 15}">${z.cerrada ? "cerrada" : esc(z.detalle)}</text></g>`;
    if (i >= 0) nodos += `<g class="paso"><circle cx="${z.x - w / 2 + 2}" cy="${z.y - h / 2 + 2}" r="10"/><text x="${z.x - w / 2 + 2}" y="${z.y - h / 2 + 6}">${i + 1}</text></g>`;
  });
  return `<svg class="mapa" viewBox="0 0 810 450" role="img" aria-label="Mapa del recinto">
    <defs><pattern id="rayas" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#f1eee6"/><line x1="0" y1="0" x2="0" y2="8" stroke="#d9d4c7" stroke-width="3"/></pattern></defs>
    ${normal}${activo}${nodos}</svg>`;
}
function camino(ruta) { return ruta.map(z => `<span>${esc(z)}</span>`).join("<em>→</em>"); }

/* -------------------------------------------------------------- taquilla */
function vistaTaquilla() {
  const d = S.d, ev = d.eventos.find(e => e.id === S.evento);
  const ent = d.entradas.filter(e => e.evento === S.evento);
  const filas = [...new Set(ent.map(e => e.fila))];
  const detalle = z => (d.recinto.zonas.find(x => x.id === z) || {}).detalle || "";
  const mapaAsientos = filas.map(f => {
    const zona = "Zona " + f, seats = ent.filter(e => e.fila === f);
    return `<div class="fila"><div class="lab"><b>Fila ${esc(f)}</b><span>${esc(zona)}</span><br><em>${esc(detalle(zona))} · ${bs(seats[0].precio)}</em></div>
      <div class="seats">${seats.map(e => `<button class="seat ${e.vendida ? "sold" : ""} ${S.sel === e.id ? "sel" : ""}" data-a="asiento" data-id="${e.id}" title="${e.id}${e.vendida ? " · vendida a " + esc(e.comprador) : ""}">${e.id.slice(-2)}</button>`).join("")}</div></div>`;
  }).join("");

  const sig = d.cola[0];
  const cola = d.cola.length
    ? `<ol class="cola">${d.cola.map((n, i) => `<li class="${i ? "" : "first"}"><span class="pos">${i + 1}</span>${esc(n)}${i ? "" : '<span class="tag chip warn">Siguiente</span>'}</li>`).join("")}</ol>`
    : `<p class="vacio">No hay compradores en espera.</p>`;

  let seleccion = "";
  if (S.sel) {
    const e = d.entradas.find(x => x.id === S.sel), p = S.prev;
    const ruta = !p ? "" : p.ruta
      ? `<label class="f">Ruta desde la puerta · ${p.tramos} tramos</label><div class="path">${camino(p.ruta)}</div>`
      : `<div class="aviso">Sin ruta: la zona de este asiento está cerrada o no se alcanza por pasillos abiertos.</div>`;
    seleccion = `<div class="card"><h2>Asiento seleccionado</h2>
      <div class="row between" style="margin:8px 0 14px"><span class="price">${esc(e.id)}</span><span class="chip ${e.vendida ? "sold" : "ok"}">${e.vendida ? "Vendida" : "Disponible"}</span></div>
      <dl class="kv"><dt>Zona</dt><dd>${esc(e.zona || "Sin zona en el mapa")}</dd><dt>Precio</dt><dd>${bs(e.precio)}</dd>${e.vendida ? `<dt>Comprador</dt><dd>${esc(e.comprador)}</dd>` : ""}</dl>
      ${e.vendida ? "" : ruta + `<div style="margin-top:18px"><button class="btn acc block" data-a="vender" ${sig ? "" : "disabled"}>${sig ? "Vender a " + esc(sig) : "Sin compradores en cola"}</button></div>`}</div>`;
  }

  let emitida = "";
  if (S.emitida) {
    const {entrada: e, ruta: r} = S.emitida, evn = (d.eventos.find(x => x.id === e.evento) || {}).nombre;
    emitida = `<div class="ticket"><div class="t-main">
      <div class="t-k">Entrada emitida · ${esc(evn)}</div><div class="t-seat">${esc(e.id)}</div>
      <div class="t-meta"><span>${esc(e.comprador)}</span><span>${esc(e.zona)}</span><span>${bs(e.precio)}</span></div>
      <div class="t-route"><small>Cómo llegar</small>${r.ruta ? `<div class="path">${camino(r.ruta)}</div>
        <div style="margin-top:10px"><button class="btn ghost sm" data-a="vermapa">Ver en el mapa</button></div>`
        : `<div class="aviso" style="margin-top:8px">Sin ruta: la zona está cerrada o aislada. Avisar al comprador en boletería.</div>`}</div></div>
      <div class="t-stub"><div class="bars"></div><small>${esc(e.id)} · ${esc(e.evento)}</small></div></div>`;
  }

  return `<div class="top"><div><h1>Taquilla</h1><p>Atiende en orden de llegada, elige el asiento y entrega la ruta para llegar a él.</p></div>
    <div class="seg" role="tablist">${d.eventos.map(e => `<button class="${e.id === S.evento ? "on" : ""}" data-a="evento" data-id="${e.id}">${esc(e.nombre)}<small>${e.libres}/${e.total}</small></button>`).join("")}</div></div>
    <div class="grid"><div class="card"><h2>${esc(ev.nombre)}</h2><p class="sub">${ev.libres} de ${ev.total} asientos disponibles</p>
      <div class="stage">ESCENARIO</div>${mapaAsientos}
      <div class="legend"><span><i></i>Disponible</span><span><i class="s"></i>Vendida</span><span><i class="k"></i>Seleccionada</span></div></div>
    <div class="stack">${emitida}
      <div class="card"><h2>Cola de espera</h2><p class="sub">${d.cola.length} ${d.cola.length === 1 ? "persona" : "personas"} · se atiende al primero que llegó</p>${cola}
        <div class="row"><input type="text" id="nuevo" placeholder="Nombre del comprador" data-enter="comprador" autocomplete="off"><button class="btn" data-a="comprador">Agregar</button></div></div>
      ${seleccion}</div></div>`;
}

/* --------------------------------------------------------------- recinto */
function vistaRecinto() {
  const R = S.d.recinto, m = S.mapa, res = m.res;
  const opts = sel => R.zonas.map(z => `<option ${z.id === sel ? "selected" : ""}>${esc(z.id)}</option>`).join("");
  const hacia = R.zonas.find(z => z.id === m.hacia);
  let resultado = "";
  if (res && res.ruta) {
    resultado = `<div class="big">${res.tramos}</div><div style="color:var(--ink2)">${res.tramos === 1 ? "tramo" : "tramos"} entre ${esc(m.desde)} y ${esc(m.hacia)}</div>
      <ol class="steps">${res.ruta.map((z, i) => `<li><i>${i + 1}</i>${esc(z)}</li>`).join("")}</ol>`;
  } else if (res) {
    const motivo = (hacia && hacia.cerrada) || (R.zonas.find(z => z.id === m.desde) || {}).cerrada
      ? "Una de las dos zonas está cerrada." : "Con los pasillos abiertos no hay forma de llegar.";
    resultado = `<div class="aviso"><b>No se llega a ${esc(m.hacia)}.</b><br>${motivo}</div>`;
  }
  const cerradas = R.zonas.filter(z => z.cerrada).length;
  return `<div class="top"><div><h1>Recinto</h1><p>Zonas y pasillos como un grafo. Se busca el recorrido con menos tramos; si cierras una zona, el mapa busca otro camino.</p></div>
    <span class="chip">${R.zonas.length} zonas · ${R.pasillos.length} pasillos${cerradas ? " · " + cerradas + " cerrada" + (cerradas > 1 ? "s" : "") : ""}</span></div>
    <div class="grid map"><div class="card"><div class="map-wrap">${mapaSVG(res && res.ruta)}</div></div>
    <div class="stack"><div class="card"><h2>Recorrido</h2>
      <div style="margin:10px 0 12px"><label class="f">Desde</label><select data-f="desde">${opts(m.desde)}</select></div>
      <div style="margin-bottom:18px"><label class="f">Hasta</label><select data-f="hacia">${opts(m.hacia)}</select></div>${resultado}</div>
    <div class="card"><h2>Estado de las zonas</h2><p class="sub">Cerrar una zona la quita del mapa de recorridos.</p>
      <div class="zonas">${R.zonas.map(z => `<div><span>${esc(z.id)}</span><span class="row">${z.cerrada ? '<span class="chip warn">Cerrada</span>' : ""}<button class="btn ghost sm" data-a="zona" data-id="${esc(z.id)}" data-c="${z.cerrada ? 0 : 1}">${z.cerrada ? "Abrir" : "Cerrar"}</button></span></div>`).join("")}</div></div></div></div>`;
}

/* --------------------------------------------------------------- asientos */
function filaTabla(e) {
  return `<tr><td class="code">${esc(e.id)}</td><td>${esc((S.d.eventos.find(x => x.id === e.evento) || {}).nombre)}</td><td>${esc(e.zona || "—")}</td>
    <td class="num">${bs(e.precio)}</td><td><span class="chip ${e.vendida ? "sold" : "ok"}">${e.vendida ? "Vendida" : "Disponible"}</span></td><td>${esc(e.comprador || "—")}</td></tr>`;
}
function vistaAsientos() {
  const a = S.aq, filas = [...new Set(S.d.entradas.map(e => e.fila))];
  const lista = a.res ? a.res.entradas : S.d.entradas;
  let existe = "";
  if (a.existe) existe = a.existe.existe ? `<span class="chip ok">${esc(a.existe.codigo)} existe</span>` : `<span class="chip warn">${esc(a.existe.codigo)}: no existe ese asiento</span>`;
  return `<div class="top"><div><h1>Asientos</h1><p>Consultas ordenadas por código: una fila entera, un rango entre dos códigos o saber si un asiento existe.</p></div></div>
    <div class="card"><div class="filtros">
      <div><label class="f">Fila</label><select id="q-fila"><option value="">Todas</option>${filas.map(f => `<option ${a.fila === f ? "selected" : ""}>${esc(f)}</option>`).join("")}</select></div>
      <div><label class="f">Desde</label><input type="text" id="q-desde" placeholder="A-02" value="${esc(a.desde)}" data-enter="consultar"></div>
      <div><label class="f">Hasta</label><input type="text" id="q-hasta" placeholder="B-03" value="${esc(a.hasta)}" data-enter="consultar"></div>
      <div><label class="f">¿Existe el código?</label><input type="text" id="q-codigo" placeholder="C-04" value="${esc(a.codigo)}" data-enter="consultar"></div>
      <div class="row"><button class="btn" data-a="consultar">Consultar</button><button class="btn ghost" data-a="limpiar">Limpiar</button></div></div>
      ${existe ? `<div style="margin-bottom:14px">${existe}</div>` : ""}
      ${lista.length ? `<table><thead><tr><th>Código</th><th>Evento</th><th>Zona</th><th class="num">Precio</th><th>Estado</th><th>Comprador</th></tr></thead><tbody>${lista.map(filaTabla).join("")}</tbody></table>`
        : `<p class="vacio">No hay asientos en esa fila o ese rango.</p>`}</div>`;
}

/* --------------------------------------------------------------- historial */
function vistaHistorial() {
  const h = S.hist, r = h.res || [];
  return `<div class="top"><div><h1>Historial</h1><p>Reservas en el orden en que se hicieron. Filtra por comprador para ver solo las suyas.</p></div></div>
    <div class="card"><div class="row" style="margin-bottom:18px;max-width:520px"><input type="text" id="h-q" placeholder="Nombre del comprador (vacío = todos)" value="${esc(h.q)}" data-enter="historial" autocomplete="off"><button class="btn" data-a="historial">Buscar</button></div>
    ${r.length ? `<table><thead><tr><th class="num">N.º</th><th>Comprador</th><th>Entrada</th><th>Zona</th><th>Evento</th></tr></thead><tbody>${r.map((x, i) => `<tr><td class="num">${i + 1}</td><td>${esc(x.comprador)}</td><td class="code">${esc(x.entrada_id)}</td><td>${esc(x.zona || "—")}</td><td>${esc((S.d.eventos.find(e => e.id === x.evento_id) || {}).nombre)}</td></tr>`).join("")}</tbody></table>`
      : `<p class="vacio">No hay reservas${h.q ? " para " + esc(h.q) : ""}.</p>`}</div>`;
}

/* ------------------------------------------------------------------ vista */
function render() {
  $("#nav").innerHTML = VISTAS.map(([id, nombre]) => `<button class="${id === S.vista ? "on" : ""}" data-a="vista" data-id="${id}"><svg viewBox="0 0 24 24">${ICONOS[id]}</svg>${nombre}${id === "taquilla" && S.d.cola.length ? `<span class="n">${S.d.cola.length}</span>` : ""}</button>`).join("");
  $("#app").innerHTML = {taquilla: vistaTaquilla, recinto: vistaRecinto, asientos: vistaAsientos, historial: vistaHistorial}[S.vista]();
}
async function refrescar() { S.d = await api("/api/estado"); }
async function irA(v) {
  S.vista = v;
  if (v === "recinto") await actualizarRuta();
  if (v === "historial") await buscarHistorial();
  if (v === "asientos" && !S.aq.res) await consultar(true);
  render();
}
async function actualizarRuta() {
  S.mapa.res = await api(`/api/ruta?desde=${encodeURIComponent(S.mapa.desde)}&hacia=${encodeURIComponent(S.mapa.hacia)}`);
}
async function consultar(silencioso) {
  const a = S.aq;
  if (!silencioso) { a.fila = $("#q-fila").value; a.desde = $("#q-desde").value.trim(); a.hasta = $("#q-hasta").value.trim(); a.codigo = $("#q-codigo").value.trim(); }
  a.existe = null; a.res = null;
  if (a.codigo) a.existe = await api("/api/asientos?codigo=" + encodeURIComponent(a.codigo));
  const q = `/api/asientos?fila=${encodeURIComponent(a.fila)}&desde=${encodeURIComponent(a.desde)}&hasta=${encodeURIComponent(a.hasta)}`;
  a.res = await api(q);
}
async function buscarHistorial() {
  const el = $("#h-q");
  if (el) S.hist.q = el.value.trim();
  S.hist.res = (await api("/api/historial?comprador=" + encodeURIComponent(S.hist.q))).reservas;
}

const ACCIONES = {
  async vista(t) { await irA(t.dataset.id); },
  async evento(t) { S.evento = t.dataset.id; S.sel = null; S.prev = null; render(); },
  async asiento(t) {
    S.sel = t.dataset.id; S.prev = null; render();
    S.prev = await api("/api/ruta?entrada=" + encodeURIComponent(S.sel)); render();
  },
  async comprador() {
    await api("/api/comprador", {nombre: $("#nuevo").value});
    await refrescar(); render(); $("#nuevo").focus();
  },
  async vender() {
    S.emitida = await api("/api/vender", {entrada_id: S.sel});
    S.sel = null; S.prev = null; await refrescar(); render();
    aviso("Entrada " + S.emitida.entrada.id + " vendida a " + S.emitida.entrada.comprador);
  },
  async vermapa() {
    S.mapa.desde = S.emitida.ruta.desde; S.mapa.hacia = S.emitida.ruta.hacia; await irA("recinto");
  },
  async zona(t) {
    await api("/api/zona", {zona: t.dataset.id, cerrada: t.dataset.c === "1"});
    await refrescar(); await actualizarRuta(); render();
  },
  async consultar() { await consultar(false); render(); },
  async limpiar() { S.aq = {res: null, fila: "", desde: "", hasta: "", codigo: "", existe: null}; await consultar(true); render(); },
  async historial() { await buscarHistorial(); render(); },
};
document.addEventListener("click", e => {
  const t = e.target.closest("[data-a]");
  if (t && ACCIONES[t.dataset.a]) intentar(() => ACCIONES[t.dataset.a](t));
});
document.addEventListener("keydown", e => {
  if (e.key === "Enter" && e.target.dataset && e.target.dataset.enter) intentar(() => ACCIONES[e.target.dataset.enter](e.target));
});
document.addEventListener("change", e => {
  const f = e.target.dataset && e.target.dataset.f;
  if (f) intentar(async () => { S.mapa[f] = e.target.value; await actualizarRuta(); render(); });
});
intentar(async () => { await refrescar(); render(); });
</script>
</body>
</html>
'''
