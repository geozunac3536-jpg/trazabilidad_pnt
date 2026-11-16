#!/usr/bin/env python3
"""
Regenera los artefactos derivados del repositorio trazabilidad_pnt a partir
del reporte crudo oficial exportado de la Plataforma Nacional de Transparencia.

Uso:
    python3 scripts/actualizar_repo.py 01_FUENTE_PNT/mis_solicitudes_pnt_AAAAMMDD.xls AAAA-MM-DD [VERSION]

Principio de trazabilidad: ningún dato se captura a mano. Todo valor publicado
(folio, institución, fechas, estatus, URL de adjuntos) proviene literalmente de
la exportación oficial de la PNT. La comparación contra el corte anterior usa
01_FUENTE_PNT/estado_previo_index_20260526.csv (extraído del index.html publicado).
"""
import csv, hashlib, html, json, os, re, sys
from collections import Counter, defaultdict
from datetime import date

import pandas as pd

SRC, CORTE = sys.argv[1], sys.argv[2]
VERSION = sys.argv[3] if len(sys.argv) > 3 else "1.1.0"
Y, M, D = CORTE.split("-")
CORTE_MX = f"{D}/{M}/{Y}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

df = pd.read_excel(SRC, engine="xlrd", dtype=str).fillna("")
df["_fr"] = pd.to_datetime(df["Fecha de recepción"], dayfirst=True)
df = df.sort_values(["_fr", "No. de folio"]).reset_index(drop=True)
assert df["No. de folio"].is_unique, "folios duplicados en la fuente"
N = len(df)


def clase(est):
    e = est.lower()
    if e.startswith("terminada"): return "terminada"
    if e.startswith("desechada"): return "desechada"
    if e.startswith("pendiente de acreditación"): return "pendiente"
    if "prórroga" in e: return "prorroga"
    if "información adicional" in e: return "espera"
    if "parcialmente competente" in e: return "parcial"
    if "sin identidad" in e or "prevención" in e: return "prevencion"
    if e.startswith("en proceso"): return "proceso"
    return "otro"


df["_cls"] = df["Estatus"].map(clase)
est_cnt = Counter(df["Estatus"])
cls_cnt = Counter(df["_cls"])
tipo_cnt = Counter(df["Tipo de Solicitud"])
inst_cnt = Counter(df["Institución"])

# ---- evidencia Drive (opcional) ----
ev = defaultdict(int)
EVF = "02_EVIDENCIA_DRIVE/indice_evidencia_drive.csv"
if os.path.exists(EVF):
    for r in csv.DictReader(open(EVF, encoding="utf-8")):
        ev[r["folio"]] += 1

# ---- 1. metadata.json (registro íntegro, JSON válido) ----
cols = [c for c in df.columns if not c.startswith("_")]
json.dump(df[cols].to_dict("records"), open("metadata.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- 2. índice maestro CSV ----
with open("00_INDEX/index_maestro.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["folio", "sujeto_obligado", "autoridad_garante", "tipo_solicitud",
                "fecha_recepcion", "fecha_limite", "estatus_oficial", "clase_estatus",
                "con_respuesta_texto", "url_adjuntos_pnt", "archivos_drive_dedup"])
    for _, r in df.iterrows():
        w.writerow([r["No. de folio"], r["Institución"], r["Autoridad Garante"],
                    r["Tipo de Solicitud"], r["Fecha de recepción"], r["Fecha límite de entrega"],
                    r["Estatus"], r["_cls"], "sí" if r["Respuesta"].strip() else "no",
                    r["Url adjuntos"], ev.get(r["No. de folio"], 0)])

# ---- 3. comparación contra corte previo ----
prev = {}
PF = "01_FUENTE_PNT/estado_previo_index_20260526.csv"
for r in csv.DictReader(open(PF, encoding="utf-8")):
    prev[r["folio"].lstrip("0")] = r
nuevos, cambios = [], []
for _, r in df.iterrows():
    k = r["No. de folio"].lstrip("0")
    if k not in prev:
        nuevos.append(r)
    elif prev[k]["estatus_etiqueta"] != r["Estatus"]:
        cambios.append((r, prev[k]["estatus_etiqueta"]))
retirados = sorted(set(prev) - set(df["No. de folio"].str.lstrip("0")))

L = [f"# Bitácora de cambios — corte {CORTE_MX}", "",
     f"Fuente: `{SRC}` (exportación oficial PNT, {N} folios únicos).",
     f"Base de comparación: `{PF}` ({len(prev)} folios publicados en index.html al 26/05/2026).", "",
     "> Nota metodológica: las etiquetas previas eran resúmenes del index.html (p. ej. «Con prevención», «Parcial»), "
     "no el texto oficial de la PNT. Por eso un cambio de etiqueta puede reflejar normalización y no un cambio real "
     "de estatus. A partir de este corte se publica el texto oficial literal.", "",
     "## Resumen", "",
     f"| Concepto | Cantidad |", "|---|---:|",
     f"| Folios en corte previo | {len(prev)} |",
     f"| Folios en corte actual | {N} |",
     f"| Folios nuevos | {len(nuevos)} |",
     f"| Folios con estatus distinto | {len(cambios)} |",
     f"| Folios del corte previo ausentes en la fuente | {len(retirados)} |", "",
     "## Folios nuevos", "", "| Folio | Sujeto obligado | Recepción | Límite | Estatus oficial |", "|---|---|---|---|---|"]
for r in nuevos:
    L.append(f"| `{r['No. de folio']}` | {r['Institución']} | {r['Fecha de recepción']} | {r['Fecha límite de entrega']} | {r['Estatus']} |")
L += ["", "## Cambios de estatus", "", "| Folio | Sujeto obligado | Etiqueta previa (26/05) | Estatus oficial actual |", "|---|---|---|---|"]
for r, p in cambios:
    L.append(f"| `{r['No. de folio']}` | {r['Institución']} | {p} | {r['Estatus']} |")
if retirados:
    L += ["", "## Ausentes en la fuente actual", ""] + [f"- `{x}`" for x in retirados]
open(f"CAMBIOS_{Y}{M}{D}.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---- 4. index.html (DATA + fecha de corte) ----
data = [[r["No. de folio"], r["Institución"], r["Tipo de Solicitud"], r["Fecha de recepción"],
         r["Fecha límite de entrega"], r["Estatus"], r["_cls"], r["Url adjuntos"]]
        for _, r in df.iterrows()]
h = open("index.html", encoding="utf-8").read()
h = re.sub(r"const DATA = \[.*?\n\];",
           lambda m: "const DATA = [\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in data) + "\n];",
           h, flags=re.S)
h = re.sub(r"📅 Actualizado: [0-9/]+", f"📅 Actualizado: {CORTE_MX}", h)
h = re.sub(r"Repositorio generado automáticamente · [0-9/]+", f"Repositorio generado automáticamente · {CORTE_MX}", h)
h = re.sub(r"const today = \d+;", f"const today = {Y}{M}{D};", h)
stats = (
    f'<div class="stats">\n'
    f'  <div class="stat-card total"><div class="num">{N}</div><div class="lbl">Total folios</div></div>\n'
    + "".join(
        f'  <div class="stat-card {c}"><div class="num">{cls_cnt.get(c,0)}</div><div class="lbl">{lbl}</div></div>\n'
        for c, lbl in [("terminada", "Terminadas"), ("proceso", "En proceso"), ("espera", "Info adicional"),
                       ("parcial", "Parcialmente competente"), ("prevencion", "Sin identidad acreditada"),
                       ("pendiente", "Pendiente acreditación"), ("prorroga", "Prórroga"),
                       ("desechada", "Desechadas")] if cls_cnt.get(c, 0))
    + "</div>")
h = re.sub(r'<div class="stats">.*?\n</div>', lambda m: stats, h, count=1, flags=re.S)
opts = '    <option value="">— Todos los estatus —</option>\n' + "".join(
    f'    <option value="{c}">{lbl}</option>\n' for c, lbl in [
        ("terminada", "Terminada"), ("proceso", "En proceso"), ("espera", "Información adicional"),
        ("parcial", "Parcialmente competente"), ("prevencion", "Sin identidad acreditada"),
        ("pendiente", "Pendiente de acreditación"), ("prorroga", "Prórroga"), ("desechada", "Desechada")]
    if cls_cnt.get(c, 0))
h = re.sub(r'(<select id="filter-status">\n).*?(  </select>)', lambda m: m.group(1) + opts + m.group(2), h, count=1, flags=re.S)
h = re.sub(r'Mostrando \d+ de \d+', f'Mostrando {N} de {N}', h)
if ".badge.desechada" not in h:
    h = h.replace("  .badge.otro ", "  .badge.desechada { background: #e5e7eb; color: #111827; text-decoration: line-through; }\n  .badge.otro ")
    h = h.replace("  .stat-card.espera .num", "  .stat-card.pendiente .num { color: #991b1b; }\n  .stat-card.desechada .num { color: #374151; }\n  .stat-card.espera .num")
open("index.html", "w", encoding="utf-8").write(h)


# ---- 5. concentrado_general.md ----
def tabla_estatus():
    out = ["| Estatus oficial | Folios | % |", "|---|---:|---:|"]
    for e, n in est_cnt.most_common():
        out.append(f"| {e} | {n} | {100*n/N:.1f}% |")
    return out


C = ["# Concentrado General de Solicitudes PNT", "",
     f"Documento autogenerado por `scripts/actualizar_repo.py` desde la exportación oficial PNT del {CORTE_MX}.", "",
     f"**Total de folios únicos:** {N}  ", f"**Información pública:** {tipo_cnt.get('Información pública',0)} · **Datos personales (ARCO):** {tipo_cnt.get('Datos Personales',0)}", "",
     "## Resumen por estatus oficial", ""] + tabla_estatus() + [
     "", "## Sujetos obligados", "", "| Sujeto obligado | Folios |", "|---|---:|"]
C += [f"| {i} | {n} |" for i, n in inst_cnt.most_common()]
C += ["", "## Registro maestro de folios", "", "| Folio | Sujeto obligado | Tipo | Recepción | Límite | Estatus | Archivos Drive |", "|---|---|---|---|---|---|---:|"]
for _, r in df.iterrows():
    C.append(f"| `{r['No. de folio']}` | {r['Institución']} | {r['Tipo de Solicitud']} | {r['Fecha de recepción']} | {r['Fecha límite de entrega']} | {r['Estatus']} | {ev.get(r['No. de folio'],0)} |")
open("concentrado_general.md", "w", encoding="utf-8").write("\n".join(C) + "\n")

# ---- 6. reporte_global.md: se reemplazan solo las secciones cuantitativas (1-4) ----
R = open("reporte_global.md", encoding="utf-8").read()
cab = R.split("## 1. RESUMEN EJECUTIVO")[0]
cab = re.sub(r"\*\*Fecha de Generación:\*\* .*", f"**Fecha de Generación:** {CORTE_MX} (corte de datos PNT)", cab)
tail = R.split("## 5. RELEVANCIA JURÍDICA")[1] if "## 5. RELEVANCIA JURÍDICA" in R else ""
narr = R.split("## 1. RESUMEN EJECUTIVO")[1].split("## 2.")[0]
narr = re.sub(r"universo de \*\*\d+ solicitudes[^*]*\*\*", f"universo de **{N} solicitudes de acceso a la información pública y de datos personales**", narr).strip("\n")
S = [cab.rstrip(), "", "## 1. RESUMEN EJECUTIVO", "", narr.rstrip(), "",
     "## 2. MÉTRICAS E INDICADORES CLAVE", "",
     f"### 📊 Volumen general: **{N} folios**", "",
     "| Métrica | Valor | % |", "| :--- | :---: | :---: |",
     f"| Total de solicitudes | {N} | 100.0% |"]
for t, n in tipo_cnt.most_common():
    S.append(f"| Tipo: {t} | {n} | {100*n/N:.1f}% |")
S += ["", "### 📑 Distribución por estatus oficial", ""] + [f"- **{e}:** {n} ({100*n/N:.1f}%)" for e, n in est_cnt.most_common()]
mes = Counter(df["_fr"].dt.strftime("%Y-%m"))
S += ["", "### 📅 Folios por mes de recepción", "", "| Mes | Folios |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(mes.items())]
S += ["", "## 3. CONCENTRACIÓN POR SUJETO OBLIGADO", "", "| Sujeto obligado | Folios | % |", "| :--- | :---: | :---: |"]
S += [f"| {i} | {n} | {100*n/N:.1f}% |" for i, n in inst_cnt.most_common()]
S += ["", "## 4. INVENTARIO MAESTRO DE FOLIOS", "",
      "Cada folio enlaza al paquete de adjuntos publicado por la propia PNT (URL oficial de descarga).", "",
      "| Folio PNT | Sujeto obligado | Recepción | Límite | Estatus | Adjuntos PNT |", "| :--- | :--- | :---: | :---: | :--- | :---: |"]
for _, r in df.iterrows():
    link = f"[📎 PNT]({r['Url adjuntos']})" if r["Url adjuntos"] else "—"
    S.append(f"| `{r['No. de folio']}` | {r['Institución']} | {r['Fecha de recepción']} | {r['Fecha límite de entrega']} | **{r['Estatus']}** | {link} |")
S += ["", "## 5. RELEVANCIA JURÍDICA" + tail.rstrip()]
open("reporte_global.md", "w", encoding="utf-8").write("\n".join(S) + "\n")

# ---- 7. timeline.md (hechos verificables de la fuente) ----
T = ["# TIMELINE DEL EXPEDIENTE", "", f"Generado desde la exportación oficial PNT del {CORTE_MX}. Una línea por fecha de recepción.", ""]
for fr, g in df.groupby("_fr"):
    T.append(f"- **{fr.strftime('%Y-%m-%d')}** — {len(g)} folio(s): " + ", ".join(f"`{x}`" for x in g["No. de folio"]))
open("timeline.md", "w", encoding="utf-8").write("\n".join(T) + "\n")

# ---- 8. README: bloques de estado ----
RD = open("README.md", encoding="utf-8").read()
RD = re.sub(r"Actualizado: [0-9/]+", f"Actualizado: {CORTE_MX}", RD)
RD = re.sub(r"## 📊 Estado del expediente al [0-9/]+\n.*?\n---\n",
            lambda m: f"## 📊 Estado del expediente al {CORTE_MX}\n\n" + "\n".join(tabla_estatus())
            + f"\n| **TOTAL** | **{N}** | 100% |\n\nCambios respecto del corte 26/05/2026: ver [CAMBIOS_{Y}{M}{D}.md](./CAMBIOS_{Y}{M}{D}.md).\n\n---\n",
            RD, count=1, flags=re.S)
RD = re.sub(r"```\ntrazabilidad_pnt/\n.*?```", lambda m: f"""```
trazabilidad_pnt/
├── index.html                      ← Interfaz principal: {N} folios, filtros por estatus oficial
├── 01_FUENTE_PNT/                  ← Exportación cruda oficial PNT ({CORTE_MX}) + estado previo
├── 00_INDEX/index_maestro.csv      ← Índice maestro derivado (1 fila por folio)
├── 02_EVIDENCIA_DRIVE/             ← Índice deduplicado de archivos crudos por folio (Drive)
├── metadata.json                   ← Registro íntegro de la exportación (JSON válido)
├── concentrado_general.md · reporte_global.md · timeline.md
├── CAMBIOS_{Y}{M}{D}.md               ← Bitácora de folios nuevos y cambios de estatus
├── scripts/actualizar_repo.py      ← Generador reproducible de todo lo anterior
└── SHA.256SUMS.txt · manifest.json ← Integridad
```""", RD, count=1, flags=re.S)
ab = defaultdict(Counter)
for _, r in df.iterrows():
    ab[r["Institución"]][r["_cls"]] += 1
inst_rows = "\n".join(
    f"| {i} | {n} | " + " / ".join(f"{v} {k}" for k, v in ab[i].most_common()) + " |"
    for i, n in inst_cnt.most_common())
RD = re.sub(r"## 🏛️ Instituciones involucradas.*?\n---\n",
            lambda m: "## 🏛️ Instituciones involucradas\n\n| Institución | Folios | Estatus (clase) |\n|---|---:|---|\n"
            + inst_rows + "\n\n---\n", RD, count=1, flags=re.S)
RD = re.sub(r"Última actualización automatizada: .*?\*", f"Última actualización automatizada: {CORTE_MX}.*", RD)
open("README.md", "w", encoding="utf-8").write(RD)

# ---- 9. CITATION.cff ----
cff = open("CITATION.cff", encoding="utf-8").read()
cff = re.sub(r"(?m)^version: .*", f"version: {VERSION}", cff)
cff = re.sub(r"date-released: .*", f"date-released: {CORTE}", cff)
open("CITATION.cff", "w", encoding="utf-8").write(cff)


# ---- 10. integridad: SHA.256SUMS.txt, manifest.json, index_maestro.json ----
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


skip = {"SHA.256SUMS.txt", "manifest.json"}
files = sorted(os.path.relpath(os.path.join(dp, f), ROOT)
               for dp, dn, fn in os.walk(ROOT) if "/.git" not in dp + "/" and not dp.endswith(".git")
               for f in fn)
files = [f for f in files if not f.startswith(".git/") and f not in skip]
json.dump({"repositorio": "trazabilidad_pnt", "version": VERSION, "corte_datos": CORTE,
           "fuente": SRC, "sha256_fuente": sha(SRC), "total_folios": N,
           "por_estatus": dict(est_cnt.most_common()),
           "folios": df["No. de folio"].tolist()},
          open("index_maestro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
files = sorted(set(files) | {"index_maestro.json"})
sums = [(sha(f), f) for f in files]
open("SHA.256SUMS.txt", "w").write("".join(f"{h}  {f}\n" for h, f in sums))
json.dump({"integridad": {"algoritmo": "SHA256", "generado": CORTE,
                          "archivos": [{"ruta": f, "sha256": h} for h, f in sums]}},
          open("manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"OK {N} folios · nuevos {len(nuevos)} · cambios {len(cambios)} · archivos con hash {len(sums)}")
