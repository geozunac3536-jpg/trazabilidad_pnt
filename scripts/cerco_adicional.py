#!/usr/bin/env python3
"""Genera la sección adicional del cerco documental: vías fuera de la PNT o
dirigidas a particulares (ARCO directo, quejas, entregas condicionadas).

Uso: python3 scripts/cerco_adicional.py [--corte AAAA-MM-DD]
Lee 05_CERCO_ADICIONAL/procedimientos.csv y actuaciones.csv; escribe
05_CERCO_ADICIONAL/LEEME.md, cerco_adicional.html e inserta un contador en
index.html (bloques <!--CA-...--> reemplazables). Ejecutar antes de
scripts/recursos_revision.py, que recalcula las huellas de integridad.
"""
import argparse
import csv
import html
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
D = "05_CERCO_ADICIONAL"
ap = argparse.ArgumentParser()
ap.add_argument("--corte", default="2026-11-18")
CORTE = ap.parse_args().corte

procs = list(csv.DictReader(open(f"{D}/procedimientos.csv", encoding="utf-8")))
acts = list(csv.DictReader(open(f"{D}/actuaciones.csv", encoding="utf-8")))
ids = [p["id"] for p in procs]
assert len(ids) == len(set(ids)), "id repetido en procedimientos.csv"
assert {a["id"] for a in acts} <= set(ids), "actuación sin procedimiento"
por = defaultdict(list)
for a in acts:
    por[a["id"]].append(a)
for k in por:
    por[k].sort(key=lambda a: (a["fecha"], a["hora"]))


def dmy(s):
    return f"{s[8:10]}/{s[5:7]}/{s[:4]}" if s else "—"


ETQ = {"primaria": "", "citada_en_documento": " *(citada)*",
       "manifestacion_del_titular": " *(manifestación del titular)*",
       "consulta_no_oficial": " *(consulta no oficial)*"}
n, na = len(procs), len(acts)
part = [p for p in procs if p["naturaleza"].startswith("Particular")]

secc = []
for p in procs:
    filas = "\n".join(
        f'| {dmy(a["fecha"])} {a["hora"]} | {a["emisor"]} | {a["descripcion"]}{ETQ.get(a["tipo_fuente"], "")} | {a["fuente"]} |'
        for a in por[p["id"]])
    secc.append(f"""### {p["id"]} — {p["contraparte"]}

- **Vía:** {p["via"]}
- **Referencia:** {p["referencia"]}
- **Estado al corte:** {p["estado_al_corte"]}
- **Plazo / vencimiento:** {p["vencimiento_o_plazo"]}

| Fecha / hora | Emisor | Actuación | Fuente |
|---|---|---|---|
{filas}

**Lectura.** {p["lectura"]}
""")

md = f"""# Sección adicional del cerco documental

Corte: **{CORTE}**. {n} vías · {na} actuaciones fechadas.

La matriz PNT y los recursos de revisión ([`04_RECURSOS_REVISION`](../04_RECURSOS_REVISION/LEEME.md)) registran lo que ocurre dentro de la plataforma. Esta sección registra lo que ocurre fuera de ella o la rodea:

- el ejercicio del derecho de acceso **directamente ante los particulares** responsables del tratamiento ({len(part)} empresas);
- las **quejas** que no producen expediente ni resolución;
- las **entregas condicionadas** a comparecencia;
- los **estatus de cierre** que no van acompañados de un documento.

## Resumen

| Vía | Contraparte | Estado al corte | Plazo / vencimiento |
|---|---|---|---|
""" + "\n".join(f'| `{p["id"]}` | {p["contraparte"]} | {p["estado_al_corte"]} | {p["vencimiento_o_plazo"]} |' for p in procs) + """

## Detalle por vía

""" + "\n".join(secc) + """
## Reglas de esta sección

1. `tipo_fuente = primaria`: el dato consta en el correo, acuse, acuerdo o resolución.
2. `citada_en_documento`: el dato lo refiere otro documento del mismo trámite.
3. `manifestacion_del_titular`: hecho narrado por el titular que no tiene soporte escrito de la contraparte. Se registra para que pueda contrastarse con lo que la contraparte exhiba.
4. `consulta_no_oficial`: resultado de un servicio no oficial. Debe verificarse en la fuente oficial antes de usarse como prueba.
5. Las horas están en tiempo del centro de México. Los días hábiles son aproximados (lunes a viernes, sin los días del art. 74 LFT).
6. No se publican direcciones de correo ni datos de contacto de personas físicas. Tampoco números de cuenta, de servicio ni de juicios del orden familiar.
7. Ningún archivo de Drive se movió, renombró ni modificó.

Generador: `python3 scripts/cerco_adicional.py [--corte AAAA-MM-DD]`.
"""
open(f"{D}/LEEME.md", "w", encoding="utf-8").write(md)

# ---------- página ----------
ICO = {"manifestacion_del_titular": "🗣️", "citada_en_documento": "↪", "consulta_no_oficial": "⚠️"}
tarjetas = []
for p in procs:
    li = "".join(
        f'<li class="{a["tipo_fuente"]}"><b>{dmy(a["fecha"])}{" " + a["hora"] if a["hora"] else ""}</b> · '
        f'<span class="em">{html.escape(a["emisor"])}</span> — {html.escape(a["descripcion"])} '
        f'{ICO.get(a["tipo_fuente"], "")}<span class="src"> [{html.escape(a["fuente"])}]</span></li>'
        for a in por[p["id"]])
    tarjetas.append(f"""<section class="card" id="{p['id']}">
<h2>{html.escape(p['contraparte'])} <span class="tag">{p['id']}</span></h2>
<p class="via">{html.escape(p['via'])} · {html.escape(p['referencia'])}</p>
<div class="estado"><b>Estado al corte:</b> {html.escape(p['estado_al_corte'])}<br><b>Plazo:</b> {html.escape(p['vencimiento_o_plazo'])}</div>
<details open><summary>{len(por[p['id']])} actuaciones</summary><ul>{li}</ul></details>
<p class="lectura"><b>Lectura:</b> {html.escape(p['lectura'])}</p>
</section>""")

nav = " · ".join(f'<a href="#{p["id"]}">{p["id"]}</a>' for p in procs)
page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sección adicional del cerco documental — Trazabilidad PNT</title>
<meta name="description" content="{n} vías fuera de la PNT: acceso a datos ante particulares, quejas, entregas condicionadas y estatus de cierre sin documento.">
<link rel="canonical" href="https://geozunac3536-jpg.github.io/trazabilidad_pnt/cerco_adicional.html">
<style>
:root{{--vino:#6e003c;--navy:#00205f;--gold:#b46400;--gray-bg:#f6f7f9;--border:#d0d5de;--text:#1a1a2e;--muted:#6b7280}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--gray-bg);color:var(--text);font-size:14px;line-height:1.45}}
header{{background:linear-gradient(135deg,var(--navy) 0%,var(--vino) 100%);color:#fff;padding:24px 28px 18px;border-bottom:4px solid var(--gold)}}
header h1{{font-size:1.35rem}} header .sub{{font-size:.82rem;opacity:.85;margin-top:5px}} header a{{color:#fff}}
nav{{padding:10px 28px;background:#fff;border-bottom:1px solid var(--border);font-size:.78rem}} nav a{{color:var(--navy)}}
.note{{padding:12px 28px;font-size:.82rem;color:var(--muted)}}
main{{padding:0 28px 28px;display:grid;gap:14px}}
.card{{background:#fff;border:1px solid var(--border);border-left:4px solid var(--vino);border-radius:8px;padding:14px 16px}}
.card h2{{font-size:1rem;color:var(--navy)}} .tag{{font-family:monospace;font-size:.72rem;color:var(--vino);border:1px solid var(--vino);border-radius:9px;padding:0 6px;margin-left:6px}}
.via{{font-size:.78rem;color:var(--muted);margin:4px 0 8px}}
.estado{{background:#fdf0dd;border-radius:6px;padding:8px 10px;font-size:.82rem}}
details summary{{cursor:pointer;font-size:.78rem;color:var(--navy);margin-top:8px}}
details ul{{margin:6px 0 4px 18px;font-size:.8rem}} li{{margin-bottom:4px}}
li.manifestacion_del_titular{{background:#f3f0ff}} li.consulta_no_oficial{{background:#fff7e0}}
.em{{font-weight:600}} .src{{color:var(--muted);font-size:.72rem}}
.lectura{{margin-top:8px;font-size:.84rem;border-top:1px dashed var(--border);padding-top:8px}}
footer{{padding:16px 28px;font-size:.75rem;color:var(--muted)}}
@media(max-width:700px){{header,nav,.note,main,footer{{padding-left:12px;padding-right:12px}}}}
</style>
</head>
<body>
<header>
<h1>🧭 Sección adicional del cerco documental</h1>
<div class="sub">{n} vías · {na} actuaciones · corte {dmy(CORTE)} · <a href="index.html">← índice de folios</a> · <a href="recursos_revision.html">recursos de revisión</a></div>
</header>
<nav>{nav}</nav>
<p class="note">Acceso a datos ante particulares, quejas sin expediente, entregas condicionadas a comparecencia y estatus de cierre sin documento. Marcas: 🗣️ manifestación del titular · ↪ dato citado en otro documento · ⚠️ consulta no oficial. Horas del centro de México. Datos: <a href="05_CERCO_ADICIONAL/LEEME.md">LEEME</a> · <a href="05_CERCO_ADICIONAL/procedimientos.csv">procedimientos</a> · <a href="05_CERCO_ADICIONAL/actuaciones.csv">actuaciones</a>.</p>
<main>
{chr(10).join(tarjetas)}
</main>
<footer>Generado con <code>scripts/cerco_adicional.py</code>. No se publican correos ni datos de contacto de personas físicas.</footer>
</body>
</html>
"""
open("cerco_adicional.html", "w", encoding="utf-8").write(page)

# ---------- contador en index.html ----------
idx = open("index.html", encoding="utf-8").read()
stat = (f'<!--CA-STAT--><a class="stat-card ca" href="cerco_adicional.html" title="Vías fuera de la PNT">'
        f'<div class="num">{n}</div><div class="lbl">Cerco adicional ›</div></a><!--/CA-STAT-->')
css = ('<!--CA-CSS--><style>.stat-card.ca{text-decoration:none;color:inherit;border-color:var(--navy);background:#eef2fa}'
       '.stat-card.ca .num{color:var(--navy)}.stat-card.ca:hover{background:#dfe6f5}</style><!--/CA-CSS-->')
pat = lambda t: re.compile(rf"<!--{t}-->.*?<!--/{t}-->", re.S)
if pat("CA-STAT").search(idx):
    idx = pat("CA-STAT").sub(lambda m: stat, idx)
else:
    i = idx.index("<!--/RR-STAT-->") + len("<!--/RR-STAT-->")
    idx = idx[:i] + "\n  " + stat + idx[i:]
if pat("CA-CSS").search(idx):
    idx = pat("CA-CSS").sub(lambda m: css, idx)
else:
    i = idx.index("</head>")
    idx = idx[:i] + css + "\n" + idx[i:]
open("index.html", "w", encoding="utf-8").write(idx)
print(f"OK {n} vías · {na} actuaciones")
