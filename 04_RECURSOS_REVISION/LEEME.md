# Recursos de revisión — capa procesal del cerco documental

Corte: **2026-11-17**. Un expediente por folio, sin repeticiones: **18 expedientes / 18 folios**.

Esta carpeta documenta qué ocurrió **después** de la respuesta de cada sujeto obligado: la impugnación, la actuación de la autoridad garante y el tiempo que tomó cada etapa. Los plazos forman parte de la prueba: muestran cuánto tardó cada vía en producir —o no— un pronunciamiento.

## Archivos

| Archivo | Contenido |
|---|---|
| [`recursos_revision.csv`](recursos_revision.csv) | Una fila por expediente: folio, sujeto obligado, garante, régimen legal, fechas clave, sentido y días hábiles |
| [`actuaciones_rr.csv`](actuaciones_rr.csv) | Línea de tiempo: 75 actuaciones con documento y `drive_file_id` |
| [`expedientes_base.csv`](expedientes_base.csv) | Correspondencia expediente ↔ folio ↔ autoridad garante ↔ ley aplicada |
| [`cotejo_reporte.csv`](cotejo_reporte.csv) | Diferencias entre el reporte de control y las fuentes primarias |

Generador: `python3 scripts/recursos_revision.py [--reporte archivo.xlsx] [--corte AAAA-MM-DD]`.

## Estado al corte

- Resueltos de fondo: **9** (todos en sentido confirmatorio; 9 con «CONFIRMA», incluidos los sobreseimientos parciales).
- Desechados: **5**.
- En trámite sin resolución localizada en Drive: **2**.
- Sólo consta la interposición: **2**.
- Resoluciones que revocan o modifican la respuesta del sujeto obligado: **0**.

| Expediente | Folio | Sujeto obligado | Interposición | Admisión / prevención | Resolución | Sentido | DH admisión→resolución |
|---|---|---|---|---|---|---|---|
| `FGR2607067` | `450024600096126` | Fiscalía General de la República | 2026-04-20 | prev. 2026-04-27 | 2026-05-12 | DESECHA |  |
| `IMSS2607051` | `340018001223026` | Instituto Mexicano del Seguro Social (IMSS) | 2026-04-20 | prev. 2026-04-27 | 2026-05-08 | DESECHA |  |
| `SAT2607042` | `340027700062326` | Servicio de Administración Tributaria (SAT) | 2026-04-20 | 2026-04-27 | 2026-07-24 | CONFIRMA | 63 |
| `ATDT2607389` | `343204900019026` | Agencia de Transformación Digital y Telecomunica | 2026-04-22 | 2026-04-29 | 2026-07-28 | CONFIRMA | 63 |
| `GN2607409` | `342259800048026` | S.D.N-Guardia Nacional | 2026-04-22 | 2026-04-29 | 2026-07-28 | SOBRESEE PARCIALMENTE + CONFIRMA | 63 |
| `Trans2608173` | `343224900038026` | Transparencia para el Pueblo | 2026-04-29 | 2026-05-07 | 2026-07-24 | CONFIRMA | 56 |
| `OPR2608391` | `341000100043626` | Oficina de la Presidencia de la República | 2026-05-04 | 2026-05-12 | 2026-08-06 | CONFIRMA | 62 |
| `S/N-INFOCDMX` | `090165926000296` | Instituto de Transparencia, Acceso a la Informac | 2026-05-08 | — | — | Sólo consta la interposición |  |
| `SAT2609690` | `340027700068926` | Servicio de Administración Tributaria (SAT) | 2026-05-12 | 2026-05-19 | 2026-08-13 | SOBRESEE PARCIALMENTE + CONFIRMA | 62 |
| `PRS2610007` | `340024000011226` | Prevención y Reinserción Social | 2026-05-14 | — | 2026-05-21 | DESECHA |  |
| `STPS2610620` | `340027100027726` | Secretaría del Trabajo y Previsión Social (STPS) | 2026-05-20 | prev. 2026-05-27 | 2026-08-14 | DESECHA |  |
| `CD2610732` | `400030200057126` | Cámara de Diputados (CD) | 2026-05-21 | — | — | Sólo consta la interposición |  |
| `STPS2611014` | `340027100027826` | Secretaría del Trabajo y Previsión Social (STPS) | 2026-05-25 | — | 2026-06-10 | DESECHA |  |
| `PRODE2612313` | `340024200005926` | Procuraduría de la Defensa del Contribuyente (PR | 2026-05-29 | 2026-06-03 | — | En trámite: sin resolución localizada |  |
| `Poder2612894` | `771277626000139` | Poder Judicial del Estado de Veracruz | 2026-06-04 | — | 2026-11-04 | CONFIRMA |  |
| `CNPRD2613106` | `340006100001726` | Centro Nacional de Prevención de Desastres (CENA | 2026-06-05 | 2026-06-12 | 2026-09-07 | CONFIRMA | 61 |
| `GN2617625` | `342259800058926` | S.D.N-Guardia Nacional | 2026-07-08 | 2026-07-24 | 2026-10-16 | CONFIRMA | 59 |
| `STPS2620966` | `340027100052926` | Secretaría del Trabajo y Previsión Social (STPS) | 2026-08-13 | 2026-08-19 | — | En trámite: sin resolución localizada |  |

DH = días hábiles aproximados (lunes a viernes, sin los días del art. 74 LFT). No descuentan suspensiones de plazos publicadas por cada garante ni días inhábiles internos; para un cómputo procesal deben verificarse contra el calendario oficial. Los acuses PNT informan que el garante debe resolver en un plazo que no exceda **40 días contados desde la admisión**, ampliable **una sola vez** hasta por 20 días.

## Por qué hay folios en «Pendiente de acreditación de la identidad»

La exportación oficial registra 3 folios de esta capa con ese estatus. Los tres fueron capturados por la PNT como solicitudes de **datos personales**, por lo que su trámite quedó detenido en la fase de acreditación de identidad y no llegó a la respuesta sustantiva. Sus recursos se tramitaron bajo la LGPDPPSO ante la Unidad de Protección de Datos Personales de la SABG:

- **`340027100027726` — Secretaría del Trabajo y Previsión Social (STPS)** (expediente `STPS2610620`). 2026-05-20: Interposición del recurso de revisión (LGPDPPSO; garante: Unidad de Protección de Datos Personales SABG); 2026-05-27: Acuerdo de prevención al recurrente; 2026-06-01: Desahogo de la prevención por correo; el recurrente expresa que su intención es el acceso a información pública; 2026-08-14: Resolución: DESECHA POR IMPROCEDENTE; la Unidad de Protección de Datos Personales no es competente para recursos de acceso a información pública; 2026-11-10: Notificación de la resolución por correo electrónico.
- **`340027100027826` — Secretaría del Trabajo y Previsión Social (STPS)** (expediente `STPS2611014`). 2026-05-15: Respuesta de 5 fojas puesta a disposición en ventanilla (CDMX) o por correo certificado previo pago; en ambos casos con identificación oficial y acreditación de personalidad; 2026-05-25: Interposición del recurso de revisión (LGPDPPSO; garante: Unidad de Protección de Datos Personales SABG); 2026-06-10: Resolución: DESECHA POR IMPROCEDENTE; la Secretaría no es competente para recursos relativos a solicitudes de acceso a información pública.
- **`340024200005926` — Procuraduría de la Defensa del Contribuyente (PRODECON)** (expediente `PRODE2612313`). 2026-05-29: Interposición del recurso de revisión (LGPDPPSO; garante: Unidad de Protección de Datos Personales SABG); 2026-06-03: Acuerdo de admisión; 2026-07-24: Acuerdo de ampliación del plazo para resolver (art. 100 LGPDPPSO).

Los dos expedientes de la STPS se desecharon porque, según la propia autoridad garante de datos personales, la materia es **acceso a información pública**, que no le compete. El expediente de la PRODECON se amplió y no tiene resolución localizada. En los tres casos el estatus PNT sigue siendo «Pendiente de acreditación» al corte: la vía de datos personales se declara incompetente por tratarse de información pública, y la solicitud permanece clasificada como de datos personales.

## Lectura de los plazos

- **Admisión → resolución.** Los expedientes con admisión y resolución documentadas consumieron entre 56 y 63 días hábiles aproximados, es decir, todos rebasaron los 40 días ordinarios. Tienen acuerdo de ampliación localizado: `SAT2607042`, `ATDT2607389`, `Trans2608173`, `OPR2608391`, `CNPRD2613106`. Sin acuerdo de ampliación localizado en Drive: `GN2607409`, `SAT2609690`, `GN2617625`. Las resoluciones de `SAT2607042` y `Trans2608173` relacionan tres suspensiones de plazos de Transparencia para el Pueblo publicadas en el DOF (11, 24 y 30 de junio de 2026), que este cómputo aproximado no descuenta.
- **Resolución → notificación.** Cuando el correo de notificación está en Drive, el intervalo se registra en `dn_resolucion_a_notificacion`. El caso más extenso es `STPS2610620`: resolución firmada el 14/08/2026 y notificada por correo el 10/11/2026.
- **Desechamientos tempranos.** IMSS, FGR y PRS se desecharon en menos de un mes por causales de procedencia (prevención, consulta o ampliación de la solicitud); ninguno llegó al estudio de fondo.

## Cotejo del reporte de control de litigios

El reporte `02_recursos_de_revision.xlsx` se cotejó campo por campo contra los acuses, acuerdos y resoluciones. Se registraron **48 diferencias** en [`cotejo_reporte.csv`](cotejo_reporte.csv): 16 en «fecha de la solicitud», 15 en «fecha de resolución o desechamiento», 11 en «fecha de interposición», 3 en «folio de la solicitud», 2 en «número de expediente», 1 en «expediente omitido en el reporte». En el repositorio prevalece siempre el dato de la fuente primaria. El reporte no se publica porque contiene datos personales; sólo se registra su huella SHA-256 en `cotejo_reporte_origen.json`.

## Reglas de esta capa

1. Ningún archivo de Drive se movió, renombró ni modificó; sólo se citan por su `drive_file_id`, que es estable y es el que aparece hipervinculado en los escritos presentados.
2. `tipo_fuente = primaria`: el dato consta en el propio acuse, acuerdo, resolución o correo. `citada_en_resolucion`: el dato consta en la relación de antecedentes de la resolución del mismo expediente.
3. Cuando un documento no se localizó, la fecha queda vacía; no se estima ni se completa con otras fuentes.
