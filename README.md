# Trazabilidad PNT — Expediente CAOG840906RG3
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20331856.svg)](https://doi.org/10.5281/zenodo.20331856)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20405451.svg)](https://doi.org/10.5281/zenodo.20405451)
> **Repositorio de trazabilidad pública** de solicitudes de acceso a la información y datos personales interpuestas ante instituciones del Estado Mexicano en el marco del caso **Narcea / Tucán / R-Control**.

🔗 **Sitio en vivo:** [https://geozunac3536-jpg.github.io/trazabilidad_pnt/](https://geozunac3536-jpg.github.io/trazabilidad_pnt/)

# 🗂️ Trazabilidad PNT — Matriz de Solicitudes Institucionales

> **Expediente de Transparencia y Protección de Derechos**  
> Titular: Genaro Carrasco Ozuna · RFC: CAOG840906RG3 · CURP: CAOG840906HVZRZN08  
> ORCID: [0009-0005-6358-9910](https://orcid.org/0009-0005-6358-9910) · Actualizado: 16/11/2026

---

## 📊 Estado del expediente al 16/11/2026

| Estatus oficial | Folios | % |
|---|---:|---:|
| Terminada | 98 | 81.0% |
| Pendiente de acreditación de la identidad | 9 | 7.4% |
| En proceso | 8 | 6.6% |
| Desechada por falta de respuesta del ciudadano | 3 | 2.5% |
| En proceso, parcialmente competente | 1 | 0.8% |
| En proceso, información adicional | 1 | 0.8% |
| En proceso, sin identidad acreditada | 1 | 0.8% |
| **TOTAL** | **121** | 100% |

Cambios respecto del corte 26/05/2026: ver [CAMBIOS_20261116.md](./CAMBIOS_20261116.md).

---

## ⚖️ Recursos de revisión

La carpeta [`04_RECURSOS_REVISION/`](./04_RECURSOS_REVISION/LEEME.md) registra los **18 recursos de revisión** interpuestos sobre folios del cerco, uno por folio y sin repeticiones. Para cada uno consta la autoridad garante, la ley aplicada, las fechas de interposición, admisión o prevención, ampliación, cierre y resolución, el sentido de la resolución y los días transcurridos entre etapas. Cada fecha remite al acuse, acuerdo o resolución correspondiente mediante su identificador estable de Drive.

---

## 🔍 Visualización interactiva

👉 **[Ver índice completo (index.html)](./index.html)** — tabla filtrable y ordenable con enlaces directos a cada respuesta PNT.

---

## 📁 Estructura del repositorio

```
trazabilidad_pnt/
├── index.html                      ← Interfaz principal: 121 folios, filtros por estatus oficial
├── 01_FUENTE_PNT/                  ← Exportación cruda oficial PNT (16/11/2026) + estado previo
├── 00_INDEX/index_maestro.csv      ← Índice maestro derivado (1 fila por folio)
├── 02_EVIDENCIA_DRIVE/             ← Índice deduplicado de archivos crudos por folio (Drive)
├── 04_RECURSOS_REVISION/           ← 18 recursos de revisión: un expediente por folio, actuaciones y plazos
├── metadata.json                   ← Registro íntegro de la exportación (JSON válido)
├── concentrado_general.md · reporte_global.md · timeline.md
├── CAMBIOS_20261116.md               ← Bitácora de folios nuevos y cambios de estatus
├── scripts/actualizar_repo.py      ← Generador reproducible de todo lo anterior
└── SHA.256SUMS.txt · manifest.json ← Integridad
```

---

## 🏛️ Instituciones involucradas

| Institución | Folios | Estatus (clase) |
|---|---:|---|
| FED - Instituto del Fondo Nacional de la Vivienda para los Trabajadores (INFONAVIT) | 6 | 5 pendiente / 1 terminada |
| FED - Secretaría de Infraestructura, Comunicaciones y Transportes (SICT) | 5 | 3 terminada / 2 proceso |
| FED - Servicio de Administración Tributaria (SAT) | 5 | 5 terminada |
| FED - Consejo Nacional para Prevenir la Discriminación (CONAPRED) | 5 | 5 terminada |
| FED - S.D.N-Guardia Nacional | 5 | 4 terminada / 1 proceso |
| FED - Secretaría del Trabajo y Previsión Social (STPS) | 4 | 2 pendiente / 2 terminada |
| FED - Transparencia para el Pueblo | 4 | 4 terminada |
| FED - Agencia de Transformación Digital y Telecomunicaciones (ATDT) | 4 | 4 terminada |
| FED - Secretaría de Gobernación (SEGOB) | 4 | 3 terminada / 1 proceso |
| FED - Procuraduría de la Defensa del Contribuyente (PRODECON) | 3 | 1 terminada / 1 pendiente / 1 desechada |
| FED - Fiscalía General de la República | 3 | 2 terminada / 1 prevencion |
| FED - Secretaría Anticorrupción y  Buen Gobierno (buen gobierno) | 3 | 3 terminada |
| FED - Oficina de la Presidencia de la República | 3 | 3 terminada |
| FED - Centro Federal de Conciliación y Registro Laboral (CFCRL) | 3 | 1 terminada / 1 proceso / 1 espera |
| FED - Comisión Nacional de los Derechos Humanos (CNDH) | 3 | 3 terminada |
| FED - Instituto Nacional de Estadística y Geografía (INEGI) | 3 | 2 terminada / 1 desechada |
| FED - Cámara de Diputados (CD) | 3 | 3 terminada |
| FED - Instituto Mexicano del Seguro Social (IMSS) | 2 | 2 terminada |
| FED - Suprema Corte de Justicia de la Nación (SCJN) | 2 | 2 terminada |
| FED - Secretaría de Relaciones Exteriores (SRE) | 2 | 2 terminada |
| FED - Prevención y Reinserción Social | 2 | 2 terminada |
| FED - Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros (CONDUSEF) | 2 | 2 terminada |
| FED - Instituto Nacional de Ciencias Penales (INACIPE) | 2 | 2 terminada |
| FED - Secretaría de Hacienda y Crédito Público (SHCP) | 2 | 2 terminada |
| FED - Senado de la República | 2 | 2 terminada |
| FED - Secretaría de Economía (SE) | 2 | 1 terminada / 1 proceso |
| FED - Agencia Nacional de Aduanas de México (ANAM) | 2 | 1 terminada / 1 proceso |
| CMX - Instituto de Transparencia, Acceso a la Información Pública, Protección de Datos Personales y Rendición de Cuentas de la Ciudad de México | 1 | 1 terminada |
| FED - SICT-Instituto Mexicano del Transporte (*IMT) | 1 | 1 terminada |
| FED - Fondo para el Desarrollo de Recursos Humanos (FIDERH) | 1 | 1 terminada |
| VER - Poder Judicial del Estado de Veracruz | 1 | 1 terminada |
| FED - Comisión Ejecutiva de Atención a Víctimas (CEAV) | 1 | 1 pendiente |
| FED - CEAV-Fondo de ayuda, asistencia y reparación integral | 1 | 1 terminada |
| FED - Centro Nacional de Inteligencia | 1 | 1 terminada |
| FED - Centro Nacional de Metrología (CENAM) | 1 | 1 terminada |
| FED - Centro Nacional de Prevención de Desastres (CENAPRED) | 1 | 1 terminada |
| FED - Instituto Mexicano de la Propiedad Industrial (IMPI) | 1 | 1 terminada |
| FED - Instituto Politécnico Nacional (IPN) | 1 | 1 terminada |
| FED - CULTURA-Instituto Nacional del Derecho de Autor (INDAUTOR*) | 1 | 1 terminada |
| FED - INFOTEC Centro de Investigación e Innovación en Tecnologías de la Información y Comunicación (INFOTEC) | 1 | 1 terminada |
| FED - Auditoría Superior de la Federación (ASF) | 1 | 1 terminada |
| FED - Universidad Nacional Autónoma de México (UNAM) | 1 | 1 terminada |
| FED - Consejería Jurídica del Ejecutivo Federal (CJEF) | 1 | 1 terminada |
| FED - Procuraduría Federal de la Defensa del Trabajo (PROFEDET) | 1 | 1 terminada |
| FED - Instituto Nacional Electoral (INE) | 1 | 1 desechada |
| FED - Banco de México (BANXICO) | 1 | 1 terminada |
| FED - Consejo de la Judicatura Federal (CJF) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Altamira, S.A. de C.V. (ASIPONA ALTAMIRA) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Coatzacoalcos, S.A. de C.V. (ASIPONA COATZACOALCOS) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Dos Bocas, S.A. de C.V. (ASIPONA DOS BOCAS) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Ensenada, S.A. de C.V. (ASIPONA ENSENADA) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Guaymas, S.A. de C.V. (ASIPONA GUAYMAS) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Lázaro Cárdenas, S.A. de C.V. (ASIPONA LÁZARO CÁRDENAS | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Mazatlán, S.A. de C.V. (ASIPONA MAZATLÁN) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Progreso, S.A. de C.V. (ASIPONA PROGRESO) | 1 | 1 parcial |
| FED - Administración del Sistema Portuario Nacional Puerto Chiapas, S.A. de C.V. (ASIPONA CHIAPAS) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Salina Cruz, S.A. de C.V. (ASIPONA SALINA CRUZ) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Topolobampo, S.A. de C.V. (ASIPONA TOPOLOBAMPO) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Tuxpan, S.A. de C.V. (ASIPONA TUXPAN) | 1 | 1 terminada |
| FED - Administración del Sistema Portuario Nacional Veracruz, S.A. de C.V. (ASIPONA VERACRUZ) | 1 | 1 terminada |
| FED - Archivo General de la Nación (AGN) | 1 | 1 terminada |
| FED - Secretaría de Seguridad y Protección Ciudadana | 1 | 1 proceso |

---


---

## 🔒 Datos personales y licencia

Este repositorio contiene datos personales del titular, publicados por él mismo con fines de trazabilidad documental. La licencia ([CC BY-NC-SA 4.0](./LICENSE)) cubre solo derechos de autor; **no** licencia derechos de privacidad ni de la personalidad. Ver [AVISO_DATOS_PERSONALES.md](./AVISO_DATOS_PERSONALES.md).

---

## 📐 Marco jurídico

Este repositorio documenta la estrategia de transparencia institucional orientada a certificar la ausencia de habilitación legal de **Recurso Confiable S.A. de C.V. (R-Control, RFC: RCO970529F57)** para operar como sistema de evaluación laboral vinculante en el sector de autotransporte federal, en el contexto del expediente **FGR/CEDAC/0021/2026** y la demanda civil ante Tlalnepantla de Baz (daño reclamado: $31,150,480.81 MXN).

Fundamento constitucional: Arts. 1°, 5°, 6°, 14, 16, 22 CPEUM; Arts. 11 y 22 CADH.

---

## 🔬 Proyecto científico vinculado

**GeoSigma TCDS** — Sistema de predicción sísmica  
PWA: [geo-sigma-pulse.base44.app](https://geo-sigma-pulse.base44.app)  
Web of Science ResearcherID: OSH-8541-2025

---

*Repositorio generado y mantenido por el titular en ejercicio de sus derechos de transparencia.*  
*Última actualización automatizada: 16/11/2026.*
## Sustento Científico e Indexación Global
Este repositorio contiene la infraestructura técnica y los datos de trazabilidad que complementan las siguientes publicaciones de investigación:
- **DOI 10.5281/zenodo.20331856:** Modelación matemática de la persistencia de falsos positivos y limitaciones de los derechos ARCO.
- **DOI 10.5281/zenodo.20405451:** Gobernanza algorítmica, vacío de soberanía digital y el estándar de responsabilidad objetiva.
- **Perfil Académico e Indexación de Jurisprudencia:** [Consultar en Google Scholar](https://scholar.google.com/)
