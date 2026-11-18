#!/usr/bin/env python3
"""Capa de recursos de revisión: un expediente por folio, sin repetir.

Entradas (en el repositorio):
  metadata.json                              exportación oficial PNT (fecha de recepción, límite, estatus)
  04_RECURSOS_REVISION/expedientes_base.csv  expediente ↔ folio ↔ autoridad garante ↔ régimen
  04_RECURSOS_REVISION/actuaciones_rr.csv    línea de tiempo verificada contra documentos en Drive

Entrada opcional (fuera del repositorio, contiene datos personales):
  --reporte RUTA.xlsx   reporte de control de litigios; se coteja contra las fuentes primarias
                        y sólo se publica el resultado del cotejo, nunca el archivo.

Salidas:
  04_RECURSOS_REVISION/recursos_revision.csv   una fila por expediente
  04_RECURSOS_REVISION/cotejo_reporte.csv      (sólo si se pasa --reporte)
  04_RECURSOS_REVISION/LEEME.md
  SHA.256SUMS.txt, manifest.json               recalculados

Uso:  python3 scripts/recursos_revision.py [--reporte reporte.xlsx] [--corte AAAA-MM-DD]
"""
import argparse, csv, datetime as dt, hashlib, json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
D = "04_RECURSOS_REVISION"

ap = argparse.ArgumentParser()
ap.add_argument("--reporte")
ap.add_argument("--corte", default=dt.date.today().isoformat())
args = ap.parse_args()
CORTE = args.corte

# Días de descanso obligatorio (art. 74 LFT) dentro del periodo cubierto.
INHABILES = {dt.date(2026, 5, 1), dt.date(2026, 9, 16), dt.date(2026, 11, 16)}


def fecha(s):
    s = (s or "").strip()
    if not s:
        return None
    if re.match(r"\d{2}/\d{2}/\d{4}", s):
        d, m, y = s[:10].split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def habiles(a, b):
    """Días hábiles aproximados entre a (excluido) y b (incluido): lunes a viernes sin art. 74 LFT."""
    if not a or not b:
        return ""
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in INHABILES:
            n += 1
    return n


def iso(d):
    return d.isoformat() if d else ""


meta = json.load(open("metadata.json", encoding="utf-8"))
meta = meta if isinstance(meta, list) else list(meta.values())[0]
pnt = {r["No. de folio"]: r for r in meta}

base = list(csv.DictReader(open(f"{D}/expedientes_base.csv", encoding="utf-8")))
act = list(csv.DictReader(open(f"{D}/actuaciones_rr.csv", encoding="utf-8")))
por_exp = defaultdict(list)
for a in act:
    por_exp[a["expediente"]].append(a)

folios = [b["folio"] for b in base]
assert len(folios) == len(set(folios)), "folio repetido en expedientes_base.csv"
assert {a["expediente"] for a in act} <= {b["expediente"] for b in base}


def primera(ev, *etapas):
    xs = sorted((a for a in ev if a["etapa"] in etapas), key=lambda a: a["fecha"])
    return xs[0] if xs else None


def sentido(desc):
    d = desc.upper()
    out = [k for k in ("SOBRESEE PARCIALMENTE", "CONFIRMA", "REVOCA", "MODIFICA", "DESECHA") if k in d]
    return " + ".join(out)


filas = []
for b in base:
    f, e = b["folio"], b["expediente"]
    r = pnt.get(f, {})
    ev = por_exp[e]
    rec, lim = fecha(r.get("Fecha de recepción")), fecha(r.get("Fecha límite de entrega"))
    i = primera(ev, "interposicion")
    p = primera(ev, "prevencion")
    adm = primera(ev, "admision")
    amp = primera(ev, "ampliacion")
    cie = primera(ev, "cierre_instruccion")
    res = primera(ev, "resolucion")
    noti = [a for a in ev if a["etapa"] == "notificacion" and res and a["fecha"] >= res["fecha"]]
    fi, fa, fr = (fecha(x["fecha"]) if x else None for x in (i, adm, res))
    est_pnt = [a for a in ev if a["etapa"] == "estatus_pnt" and "RESUELTO" in a["descripcion"].upper()]
    if res:
        estado = "Desechado" if "DESECHA" in res["descripcion"].upper() else "Resuelto"
    elif est_pnt:
        estado = "Resuelto en PNT sin documento notificado"
    elif adm or p:
        estado = "En trámite: sin resolución localizada"
    elif i:
        estado = "Sólo consta la interposición"
    else:
        estado = "Sólo citado por el sujeto obligado"
    filas.append({
        "expediente": e, "folio": f,
        "sujeto_obligado": r.get("Institución", ""),
        "tipo_solicitud_pnt": r.get("Tipo de Solicitud", ""),
        "estatus_pnt_al_corte": r.get("Estatus", ""),
        "autoridad_garante": b["autoridad_garante"],
        "regimen_legal_del_recurso": b["regimen_legal_del_recurso"],
        "fecha_recepcion_solicitud": iso(rec),
        "fecha_limite_respuesta": iso(lim),
        "fecha_interposicion_rr": iso(fi),
        "hora_interposicion_rr": i["hora"] if i else "",
        "fecha_prevencion": p["fecha"] if p else "",
        "fecha_admision": iso(fa),
        "fecha_ampliacion": amp["fecha"] if amp else "",
        "fecha_cierre_instruccion": cie["fecha"] if cie else "",
        "fecha_resolucion": iso(fr),
        "sentido_resolucion": sentido(res["descripcion"]) if res else "",
        "fecha_notificacion_resolucion": noti[0]["fecha"] if noti else "",
        "estado_del_recurso": estado,
        "dh_recepcion_a_interposicion": habiles(rec, fi),
        "dh_interposicion_a_resolucion": habiles(fi, fr),
        "dh_admision_a_resolucion": habiles(fa, fr),
        "dn_resolucion_a_notificacion": (fecha(noti[0]["fecha"]) - fr).days if noti else "",
        "actuaciones_documentadas": len(ev),
        "drive_id_acuse_interposicion": i["drive_file_id"] if i else "",
        "drive_id_resolucion": res["drive_file_id"] if res else "",
    })
filas.sort(key=lambda x: (x["fecha_interposicion_rr"], x["expediente"]))
campos = list(filas[0])
with open(f"{D}/recursos_revision.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, campos)
    w.writeheader()
    w.writerows(filas)

# ---------- cotejo del reporte externo ----------
cotejo = []
if args.reporte:
    import openpyxl
    wb = openpyxl.load_workbook(args.reporte, data_only=True)
    sha_rep = hashlib.sha256(open(args.reporte, "rb").read()).hexdigest()
    ver = {x["expediente"]: x for x in filas}
    ver_f = {x["folio"]: x for x in filas}
    split = lambda s: [t.strip() for t in str(s or "").split("/") if t.strip()]

    def add(exp_rep, campo, val_rep, val_ver, fuente):
        cotejo.append({"expediente_en_reporte": exp_rep, "campo": campo,
                       "valor_en_reporte": val_rep, "valor_verificado": val_ver,
                       "fuente_verificada": fuente})

    vistos = set()
    ws = wb["Timestamps y Tiempos Legales"]
    for row in ws.iter_rows(min_row=4, values_only=True):
        if not row[0] or not row[1]:
            continue
        fs, es = split(row[0]), split(row[1])
        inter = split(row[5])
        resol = str(row[10] or "")
        for k, er in enumerate(es):
            fr_rep = fs[k] if k < len(fs) else fs[-1]
            v = ver.get(er) or ver_f.get(fr_rep)
            if not v:
                add(er, "expediente", er, "no localizado en fuentes primarias", "")
                continue
            vistos.add(v["expediente"])
            if er != v["expediente"]:
                add(er, "número de expediente", er, v["expediente"], "acuse de interposición PNT")
            if fr_rep != v["folio"]:
                add(er, "folio de la solicitud", fr_rep, v["folio"], "acuse de interposición PNT")
            fs_rep = str(row[3] or "")
            if fs_rep and fs_rep[:10] != v["fecha_recepcion_solicitud"]:
                add(er, "fecha de la solicitud", fs_rep[:10], v["fecha_recepcion_solicitud"], "exportación oficial PNT")
            ir = inter[k] if k < len(inter) else (inter[0] if inter else "")
            if ir and ir[:10] != v["fecha_interposicion_rr"]:
                add(er, "fecha de interposición", ir[:16], f'{v["fecha_interposicion_rr"]} {v["hora_interposicion_rr"]}'.strip(), "acuse de interposición PNT")
            m = re.match(r"\d{4}-\d{2}-\d{2}", resol)
            if m and m.group(0) != v["fecha_resolucion"]:
                add(er, "fecha de resolución o desechamiento", m.group(0), v["fecha_resolucion"] or "sin resolución localizada", "resolución o acuerdo en Drive")
            if not m and v["fecha_resolucion"]:
                add(er, "fecha de resolución o desechamiento", resol, v["fecha_resolucion"], "resolución o acuerdo en Drive")
    for v in filas:
        if v["expediente"] not in vistos:
            add("(no aparece)", "expediente omitido en el reporte", "", f'{v["expediente"]} / {v["folio"]}', "acuse de interposición PNT")
    with open(f"{D}/cotejo_reporte.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(cotejo[0]))
        w.writeheader()
        w.writerows(cotejo)
    json.dump({"archivo": os.path.basename(args.reporte), "sha256": sha_rep, "cotejado": CORTE,
               "discrepancias": len(cotejo)},
              open(f"{D}/cotejo_reporte_origen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- LEEME ----------
n = len(filas)
cnt = Counter(x["estado_del_recurso"] for x in filas)
sent = Counter(x["sentido_resolucion"] for x in filas if x["sentido_resolucion"])
conf = sum(v for k, v in sent.items() if "CONFIRMA" in k)
dese = sum(v for k, v in sent.items() if "DESECHA" in k)
rev = sum(v for k, v in sent.items() if "REVOCA" in k or "MODIFICA" in k)
pend = [x for x in filas if x["estatus_pnt_al_corte"].startswith("Pendiente de acreditación")]
largos = [x for x in filas if x["dh_admision_a_resolucion"] != "" and x["dh_admision_a_resolucion"] > 40]
dhs = [x["dh_admision_a_resolucion"] for x in filas if x["dh_admision_a_resolucion"] != ""]
con_amp = [x["expediente"] for x in largos if x["fecha_ampliacion"]]
sin_amp = [x["expediente"] for x in largos if not x["fecha_ampliacion"]]


def tabla():
    h = "| Expediente | Folio | Sujeto obligado | Interposición | Admisión / prevención | Resolución | Sentido | DH admisión→resolución |\n|---|---|---|---|---|---|---|---|\n"
    for x in filas:
        so = re.sub(r"^(FED|VER|CMX) - ", "", x["sujeto_obligado"])[:48]
        ap_ = x["fecha_admision"] or (f'prev. {x["fecha_prevencion"]}' if x["fecha_prevencion"] else "—")
        h += (f'| `{x["expediente"]}` | `{x["folio"]}` | {so} | {x["fecha_interposicion_rr"]} | {ap_} | '
              f'{x["fecha_resolucion"] or "—"} | {x["sentido_resolucion"] or x["estado_del_recurso"]} | {x["dh_admision_a_resolucion"]} |\n')
    return h


def linea_pend(x):
    ev = sorted(por_exp[x["expediente"]], key=lambda a: a["fecha"])
    pasos = "; ".join(f'{a["fecha"]}: {a["descripcion"]}' for a in ev)
    return f'- **`{x["folio"]}` — {re.sub(r"^FED - ", "", x["sujeto_obligado"])}** (expediente `{x["expediente"]}`). {pasos}.'


cotejo_txt = ""
if cotejo:
    cc = Counter(c["campo"] for c in cotejo)
    cotejo_txt = (
        "\n## Cotejo del reporte de control de litigios\n\n"
        f"El reporte `02_recursos_de_revision.xlsx` se cotejó campo por campo contra los acuses, acuerdos y resoluciones. "
        f"Se registraron **{len(cotejo)} diferencias** en [`cotejo_reporte.csv`](cotejo_reporte.csv): "
        + ", ".join(f"{v} en «{k}»" for k, v in cc.most_common()) + ". "
        "En el repositorio prevalece siempre el dato de la fuente primaria. El reporte no se publica porque contiene "
        "datos personales; sólo se registra su huella SHA-256 en `cotejo_reporte_origen.json`.\n")

md = f"""# Recursos de revisión — capa procesal del cerco documental

Corte: **{CORTE}**. Un expediente por folio, sin repeticiones: **{n} expedientes / {n} folios**.

Esta carpeta documenta qué ocurrió **después** de la respuesta de cada sujeto obligado: la impugnación, la actuación de la autoridad garante y el tiempo que tomó cada etapa. Los plazos forman parte de la prueba: muestran cuánto tardó cada vía en producir —o no— un pronunciamiento.

## Archivos

| Archivo | Contenido |
|---|---|
| [`recursos_revision.csv`](recursos_revision.csv) | Una fila por expediente: folio, sujeto obligado, garante, régimen legal, fechas clave, sentido y días hábiles |
| [`actuaciones_rr.csv`](actuaciones_rr.csv) | Línea de tiempo: {len(act)} actuaciones con documento y `drive_file_id` |
| [`expedientes_base.csv`](expedientes_base.csv) | Correspondencia expediente ↔ folio ↔ autoridad garante ↔ ley aplicada |
{"| [`cotejo_reporte.csv`](cotejo_reporte.csv) | Diferencias entre el reporte de control y las fuentes primarias |" + chr(10) if cotejo else ""}
Generador: `python3 scripts/recursos_revision.py [--reporte archivo.xlsx] [--corte AAAA-MM-DD]`.

## Estado al corte

- Resueltos de fondo: **{cnt.get("Resuelto", 0)}** (todos en sentido confirmatorio; {conf} con «CONFIRMA», incluidos los sobreseimientos parciales).
- Desechados: **{cnt.get("Desechado", 0)}**.
- En trámite sin resolución localizada en Drive: **{cnt.get("En trámite: sin resolución localizada", 0)}**.
- Sólo consta la interposición: **{cnt.get("Sólo consta la interposición", 0)}**.
- Marcados «RESUELTO SIN CUMPLIMIENTO» en la PNT sin que se haya notificado el documento de resolución: **{cnt.get("Resuelto en PNT sin documento notificado", 0)}**.
- Recursos conocidos sólo porque el sujeto obligado los cita en su correspondencia (sin acuse ni acuerdo del garante localizado): **{cnt.get("Sólo citado por el sujeto obligado", 0)}**.
- Resoluciones que revocan o modifican la respuesta del sujeto obligado: **{rev}**.

{tabla()}
DH = días hábiles aproximados (lunes a viernes, sin los días del art. 74 LFT). No descuentan suspensiones de plazos publicadas por cada garante ni días inhábiles internos; para un cómputo procesal deben verificarse contra el calendario oficial. Los acuses PNT informan que el garante debe resolver en un plazo que no exceda **40 días contados desde la admisión**, ampliable **una sola vez** hasta por 20 días.

## Por qué hay folios en «Pendiente de acreditación de la identidad»

La exportación oficial registra {len(pend)} folios de esta capa con ese estatus. Todos fueron capturados por la PNT como solicitudes de **datos personales**, por lo que su trámite quedó detenido en la fase de acreditación de identidad y no llegó a la respuesta sustantiva por la plataforma. Sus recursos se rigen por la LGPDPPSO:

{chr(10).join(linea_pend(x) for x in pend)}

Los dos expedientes de la STPS se desecharon porque, según la propia autoridad garante de datos personales, la materia es **acceso a información pública**, que no le compete. El expediente de la PRODECON se amplió el 24/07/2026 y el 11/11/2026 la PNT lo pasó en dos minutos a «EN RESOLUCIÓN», «RESUELTO» y «RESUELTO SIN CUMPLIMIENTO», sin notificar el documento de resolución (114 días hábiles aproximados después de la admisión). En esos tres casos el estatus PNT sigue siendo «Pendiente de acreditación» al corte: la vía de datos personales se declara incompetente por tratarse de información pública, y la solicitud permanece clasificada como de datos personales.

El folio del INFONAVIT muestra la otra cara del mismo estatus. La identidad del titular ya se había acreditado en persona ante el propio Instituto (CESI Fortín de las Flores, 11/05/2026, con constancia enviada por correo el 12/05/2026, que además fijó el correo como medio de entrega). Aun así, el 12/10/2026 y el 11/11/2026 la respuesta se condicionó otra vez a una comparecencia presencial con apercibimiento de destrucción a los 60 días, sin decir qué documentos se entregarían. El detalle está en [`05_CERCO_ADICIONAL`](../05_CERCO_ADICIONAL/LEEME.md).

## Lectura de los plazos

- **Admisión → resolución.** Los expedientes con admisión y resolución documentadas consumieron entre {min(dhs)} y {max(dhs)} días hábiles aproximados, es decir, todos rebasaron los 40 días ordinarios. Tienen acuerdo de ampliación localizado: {", ".join(f"`{x}`" for x in con_amp) or "ninguno"}. Sin acuerdo de ampliación localizado en Drive: {", ".join(f"`{x}`" for x in sin_amp) or "ninguno"}. Las resoluciones de `SAT2607042` y `Trans2608173` relacionan tres suspensiones de plazos de Transparencia para el Pueblo publicadas en el DOF (11, 24 y 30 de junio de 2026), que este cómputo aproximado no descuenta.
- **Resolución → notificación.** Cuando el correo de notificación está en Drive, el intervalo se registra en `dn_resolucion_a_notificacion`. El caso más extenso es `STPS2610620`: resolución firmada el 14/08/2026 y notificada por correo el 10/11/2026.
- **Estatus «RESUELTO SIN CUMPLIMIENTO».** `Poder2612894` (09/11/2026) y `PRODE2612313` (11/11/2026) recorrieron tres estatus en avisos automáticos separados por uno o dos minutos. Ese estatus indica que la resolución no impone al sujeto obligado nada que cumplir. En `Poder2612894` la resolución confirmó la respuesta y el informe solicitado sigue sin entregarse; en `PRODE2612313` no se ha notificado el documento. En ambos casos queda cerrada la etapa de cumplimiento sin que el titular haya recibido el documento pedido, de modo que no existe incumplimiento que denunciar ni, en el segundo, una resolución notificada a partir de la cual impugnar.
- **Desechamientos tempranos.** IMSS, FGR y PRS se desecharon en menos de un mes por causales de procedencia (prevención, consulta o ampliación de la solicitud); ninguno llegó al estudio de fondo.
{cotejo_txt}
## Reglas de esta capa

1. Ningún archivo de Drive se movió, renombró ni modificó; sólo se citan por su `drive_file_id`, que es estable y es el que aparece hipervinculado en los escritos presentados.
2. `tipo_fuente = primaria`: el dato consta en el propio acuse, acuerdo, resolución o correo. `citada_en_resolucion`: el dato consta en la relación de antecedentes de la resolución del mismo expediente. `citada_por_sujeto_obligado`: el número de expediente sólo consta en la correspondencia del sujeto obligado; no se localizó acuse de interposición ni acuerdo del garante.
3. Cuando un documento no se localizó, la fecha queda vacía; no se estima ni se completa con otras fuentes.
"""
open(f"{D}/LEEME.md", "w", encoding="utf-8").write(md)


# ---------- sitio web: página de recursos y contador en index.html ----------
import html as _h

DRIVE = "https://drive.google.com/file/d/{}/view"
CLS = {"Resuelto": "res", "Desechado": "des", "En trámite: sin resolución localizada": "tra",
       "Sólo consta la interposición": "int",
       "Resuelto en PNT sin documento notificado": "snd", "Sólo citado por el sujeto obligado": "cit"}


def dmy(s):
    return f"{s[8:10]}/{s[5:7]}/{s[:4]}" if s else "—"


def doc_link(fid, txt):
    return f'<a class="doc" href="{DRIVE.format(fid)}" target="_blank" rel="noopener">{txt}</a>' if fid else ""


filas_html = []
for x in filas:
    ev = sorted(por_exp[x["expediente"]], key=lambda a: a["fecha"])
    pasos = "".join(
        f'<li><b>{dmy(a["fecha"])}</b> · {_h.escape(a["descripcion"])} '
        f'{doc_link(a["drive_file_id"], "📄")}</li>' for a in ev)
    anc = re.sub(r"[^A-Za-z0-9]", "", x["expediente"])
    so = re.sub(r"^(FED|VER|CMX) - ", "", x["sujeto_obligado"])
    filas_html.append(f"""<tr id="{anc}" data-estado="{CLS[x['estado_del_recurso']]}">
<td><span class="exp">{_h.escape(x['expediente'])}</span><br><span class="folio">{x['folio']}</span></td>
<td>{_h.escape(so)}<br><span class="muted">{_h.escape(x['autoridad_garante'])} · {_h.escape(x['regimen_legal_del_recurso'])}</span></td>
<td>{dmy(x['fecha_interposicion_rr'])}</td>
<td>{dmy(x['fecha_resolucion'])}</td>
<td><span class="badge {CLS[x['estado_del_recurso']]}">{_h.escape(x['sentido_resolucion'] or x['estado_del_recurso'])}</span></td>
<td class="num">{x['dh_admision_a_resolucion'] if x['dh_admision_a_resolucion'] != '' else '—'}</td>
<td>{doc_link(x['drive_id_acuse_interposicion'], '📎 Acuse')} {doc_link(x['drive_id_resolucion'], '⚖️ Resolución')}</td>
</tr>
<tr class="det" data-estado="{CLS[x['estado_del_recurso']]}"><td colspan="7"><details><summary>{len(ev)} actuaciones</summary><ul>{pasos}</ul></details></td></tr>""")

page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recursos de revisión — Trazabilidad PNT</title>
<meta name="description" content="{n} recursos de revisión sobre solicitudes PNT: fechas, autoridad garante, sentido de la resolución y plazos.">
<link rel="canonical" href="https://geozunac3536-jpg.github.io/trazabilidad_pnt/recursos_revision.html">
<style>
:root{{--vino:#6e003c;--navy:#00205f;--gold:#b46400;--green:#006432;--gray-bg:#f6f7f9;--border:#d0d5de;--text:#1a1a2e;--muted:#6b7280}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--gray-bg);color:var(--text);font-size:14px}}
header{{background:linear-gradient(135deg,var(--navy) 0%,var(--vino) 100%);color:#fff;padding:24px 28px 18px;border-bottom:4px solid var(--gold)}}
header h1{{font-size:1.35rem}} header .sub{{font-size:.82rem;opacity:.8;margin-top:5px}}
header a{{color:#fff}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;padding:16px 28px;background:#fff;border-bottom:1px solid var(--border)}}
.stat-card{{background:var(--gray-bg);border:1px solid var(--border);border-radius:8px;padding:10px 16px;min-width:105px;text-align:center;cursor:pointer}}
.stat-card.on{{outline:2px solid var(--navy)}}
.stat-card .num{{font-size:1.55rem;font-weight:800;line-height:1}}
.stat-card .lbl{{font-size:.68rem;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:.5px}}
.c-all .num{{color:var(--navy)}} .c-res .num{{color:var(--green)}} .c-des .num{{color:#374151}} .c-tra .num{{color:var(--gold)}} .c-int .num{{color:#0077aa}} .c-snd .num{{color:#9a3412}} .c-cit .num{{color:#5b21b6}} .c-rev .num{{color:var(--vino)}}
.note{{padding:12px 28px;font-size:.82rem;color:var(--muted)}}
.wrap{{padding:0 28px 28px;overflow-x:auto}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--border);border-radius:8px}}
th{{background:var(--navy);color:#fff;font-size:.75rem;text-align:left;padding:9px 10px}}
td{{padding:9px 10px;border-top:1px solid #eef0f4;vertical-align:top}}
tr.det td{{border-top:none;padding-top:0}}
.exp{{font-weight:700;font-family:monospace}} .folio{{font-family:monospace;font-size:.78rem;color:var(--muted)}}
.muted{{font-size:.74rem;color:var(--muted)}} .num{{text-align:center}}
.badge{{display:inline-block;border-radius:10px;padding:2px 9px;font-size:.72rem;font-weight:600}}
.badge.res{{background:#e3f4ea;color:var(--green)}} .badge.des{{background:#eceef2;color:#374151}}
.badge.tra{{background:#fdf0dd;color:var(--gold)}} .badge.int{{background:#e0f2fb;color:#0077aa}} .badge.snd{{background:#fde7dc;color:#9a3412}} .badge.cit{{background:#ede9fe;color:#5b21b6}}
a.doc{{text-decoration:none;font-size:.78rem;white-space:nowrap}}
details summary{{cursor:pointer;font-size:.76rem;color:var(--navy)}} details ul{{margin:6px 0 4px 18px;font-size:.78rem;line-height:1.5}}
footer{{padding:16px 28px;font-size:.75rem;color:var(--muted)}}
@media(max-width:700px){{header,.stats,.note,.wrap,footer{{padding-left:12px;padding-right:12px}}}}
</style>
</head>
<body>
<header>
<h1>⚖️ Recursos de revisión</h1>
<div class="sub">Capa procesal del cerco documental · {n} expedientes, uno por folio · corte {dmy(CORTE)} · <a href="index.html">← volver al índice de folios</a></div>
</header>
<div class="stats">
<div class="stat-card c-all on" data-f=""><div class="num">{n}</div><div class="lbl">Recursos</div></div>
<div class="stat-card c-res" data-f="res"><div class="num">{cnt.get("Resuelto", 0)}</div><div class="lbl">Resueltos (confirman)</div></div>
<div class="stat-card c-des" data-f="des"><div class="num">{cnt.get("Desechado", 0)}</div><div class="lbl">Desechados</div></div>
<div class="stat-card c-tra" data-f="tra"><div class="num">{cnt.get("En trámite: sin resolución localizada", 0)}</div><div class="lbl">En trámite</div></div>
<div class="stat-card c-int" data-f="int"><div class="num">{cnt.get("Sólo consta la interposición", 0)}</div><div class="lbl">Sólo interposición</div></div>
<div class="stat-card c-snd" data-f="snd"><div class="num">{cnt.get("Resuelto en PNT sin documento notificado", 0)}</div><div class="lbl">«Resuelto» sin documento</div></div>
<div class="stat-card c-cit" data-f="cit"><div class="num">{cnt.get("Sólo citado por el sujeto obligado", 0)}</div><div class="lbl">Citado por el SO</div></div>
<div class="stat-card c-rev" data-f="none"><div class="num">{rev}</div><div class="lbl">Revocan o modifican</div></div>
</div>
<p class="note">DH = días hábiles aproximados de la admisión a la resolución (lunes a viernes, sin art.&nbsp;74 LFT ni suspensiones). Los acuses señalan un plazo de 40 días desde la admisión, ampliable una vez hasta por 20. Cada 📄 abre el documento en Drive si está compartido por enlace. Datos y método: <a href="04_RECURSOS_REVISION/LEEME.md">LEEME</a> · <a href="04_RECURSOS_REVISION/recursos_revision.csv">CSV</a> · <a href="04_RECURSOS_REVISION/actuaciones_rr.csv">actuaciones</a>.</p>
<div class="wrap"><table>
<thead><tr><th>Expediente / folio</th><th>Sujeto obligado · garante · ley</th><th>Interpuesto</th><th>Resuelto</th><th>Sentido</th><th>DH</th><th>Documentos</th></tr></thead>
<tbody>
{chr(10).join(filas_html)}
</tbody></table></div>
<footer>Generado con <code>scripts/recursos_revision.py</code> a partir de acuses, acuerdos y resoluciones; los archivos de Drive se citan por su identificador sin moverse ni modificarse.</footer>
<script>
document.querySelectorAll('.stat-card').forEach(c=>c.addEventListener('click',()=>{{
document.querySelectorAll('.stat-card').forEach(x=>x.classList.remove('on'));c.classList.add('on');
const f=c.dataset.f;document.querySelectorAll('tbody tr').forEach(r=>{{r.style.display=(!f||r.dataset.estado===f)?'':'none'}});}}));
if(location.hash){{const t=document.querySelector(location.hash);if(t){{t.style.background='#fff7e0';t.scrollIntoView();}}}}
</script>
</body>
</html>
"""
open("recursos_revision.html", "w", encoding="utf-8").write(page)

# Contador y marcas en index.html (bloques delimitados; se reemplazan en cada corrida)
idx = open("index.html", encoding="utf-8").read()
mapa = {x["folio"]: re.sub(r"[^A-Za-z0-9]", "", x["expediente"]) for x in filas}
etiq = {x["folio"]: x["expediente"] for x in filas}
stat = (f'<!--RR-STAT--><a class="stat-card rr" href="recursos_revision.html" title="Ver los {n} recursos de revisión">'
        f'<div class="num">{n}</div><div class="lbl">Recursos de revisión ›</div></a><!--/RR-STAT-->')
css = ('<!--RR-CSS--><style>.stat-card.rr{text-decoration:none;color:inherit;border-color:var(--vino);background:#fbf3f7}'
       '.stat-card.rr .num{color:var(--vino)}.stat-card.rr:hover{background:#f6e3ec}'
       '.rr-badge{display:inline-block;margin-left:6px;font-size:.68rem;font-weight:600;color:var(--vino);'
       'border:1px solid var(--vino);border-radius:9px;padding:0 6px;text-decoration:none;white-space:nowrap}</style><!--/RR-CSS-->')
js = ("<!--RR-JS--><script>(function(){const RR=" + json.dumps(mapa) + ",L=" + json.dumps(etiq, ensure_ascii=False) + ";"
      "const tb=document.getElementById('tbody');if(!tb)return;"
      "function mark(){tb.querySelectorAll('span.folio').forEach(s=>{const f=s.textContent.trim();"
      "if(RR[f]&&!(s.nextElementSibling&&s.nextElementSibling.classList.contains('rr-badge'))){"
      "const a=document.createElement('a');a.className='rr-badge';a.href='recursos_revision.html#'+RR[f];"
      "a.textContent='⚖️ '+L[f];a.title='Recurso de revisión';s.after(a);}});}"
      "new MutationObserver(mark).observe(tb,{childList:true});mark();})();</script><!--/RR-JS-->")


def bloque(h, tag, nuevo, ancla, antes=True):
    pat = re.compile(rf"<!--{tag}-->.*?<!--/{tag}-->", re.S)
    if pat.search(h):
        return pat.sub(lambda m: nuevo, h)
    i = h.index(ancla)
    return h[:i] + nuevo + "\n" + h[i:] if antes else h[:i + len(ancla)] + "\n" + nuevo + h[i + len(ancla):]


m = re.search(r'<div class="stats">.*?\n</div>', idx, re.S)
if "<!--RR-STAT-->" not in idx:
    fin = m.end() - len("</div>")
    idx = idx[:fin] + "  " + stat + "\n" + idx[fin:]
else:
    idx = bloque(idx, "RR-STAT", stat, "")
idx = bloque(idx, "RR-CSS", css, "</head>")
idx = bloque(idx, "RR-JS", js, "</body>")
open("index.html", "w", encoding="utf-8").write(idx)

# ---------- integridad ----------
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


skip = {"SHA.256SUMS.txt", "manifest.json"}
files = sorted(os.path.relpath(os.path.join(dp, f), ROOT)
               for dp, dn, fn in os.walk(ROOT) if "/.git" not in dp + "/" and not dp.endswith(".git")
               for f in fn)
files = [f for f in files if not f.startswith(".git/") and f not in skip]
sums = [(sha(f), f) for f in files]
open("SHA.256SUMS.txt", "w").write("".join(f"{h}  {f}\n" for h, f in sums))
man = json.load(open("manifest.json", encoding="utf-8"))
man["integridad"].update({"generado": CORTE, "archivos": [{"ruta": f, "sha256": h} for h, f in sums]})
json.dump(man, open("manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"OK {n} expedientes · {len(act)} actuaciones · cotejo {len(cotejo)} · archivos con hash {len(sums)}")
