# Trazabilidad PNT — Expediente CAOG840906RG3
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20331856.svg)](https://doi.org/10.5281/zenodo.20331856)
> **Repositorio de trazabilidad pública** de solicitudes de acceso a la información y datos personales interpuestas ante instituciones del Estado Mexicano en el marco del caso **Narcea / Tucán / R-Control**.

🔗 **Sitio en vivo:** [https://geozunac3536-jpg.github.io/trazabilidad_pnt/](https://geozunac3536-jpg.github.io/trazabilidad_pnt/)

---

## Contexto del caso

Desde el **15 de diciembre de 2025**, la anotación adversa de **Recurso Confiable S.A. de C.V. (R-Control)** — identificador `006-033202305-SV1966111caog840906202958` — ha bloqueado al operador federal de autotransporte de carga **Genaro Carrasco Ozuna (RFC: CAOG840906RG3)** del mercado laboral en el sector, con al menos 6 empresas que han negado contratación documentada.

La estrategia jurídica multi-institucional se articula bajo la teoría del **Nexo Causal Único Interdominio (NCU)**: un único nodo causal (la relación laboral con Narcea/Tucán) que genera violaciones simultáneas en dominios laboral, fiscal, penal, constitucional, datos personales y derechos humanos.

**Empresas demandadas:**
| RFC | Razón Social |
|-----|-------------|
| `TNA910502JI5` | Transportes Narcea S.A. de C.V. |
| `CTU1307205L1` | Correcaminos Tucán S.A. de C.V. |
| `RCO970529F57` | Recurso Confiable S.A. de C.V. (R-Control) |

---

## Estadísticas del repositorio

| Indicador | Valor |
|-----------|-------|
| **Total de folios PNT** | 52 |
| Solicitudes de Información Pública | 43 |
| Solicitudes de Datos Personales | 9 |
| Terminadas | 19 |
| En proceso | 16 |
| Pendientes de acreditación de identidad | 5 |
| En proceso con prevención | 3 |
| En proceso parcialmente competente | 3 |
| En proceso con prórroga | 2 |

---

## Estructura del repositorio

```
trazabilidad_pnt/
├── index.html          # Dashboard interactivo (GitHub Pages)
├── data.js             # Datos de todos los folios (JSON embebido)
└── README.md           # Este archivo
```

### `index.html`
Dashboard web con:
- **Tabla filtrable** por texto libre, tipo de solicitud y estatus
- **Indicadores de alerta** para folios con plazo límite vencido
- **Vínculos directos** a los adjuntos PDF de cada respuesta en la PNT
- **Contadores en tiempo real** de estatus agregados

### `data.js`
Array `FOLIOS` con 52 objetos. Cada objeto contiene:

```js
{
  folio:            "340027700068926",
  tipo:             "Información pública",
  institucion:      "Servicio de Administración Tributaria (SAT)",
  fecha_recepcion:  "17/04/2026",
  fecha_limite:     "19/05/2026",
  estatus:          "Terminada",
  url:              "https://servicios.plataformadetransparencia.org.mx/..."
}
```

---

## Instituciones cubiertas

<details>
<summary>Ver listado completo (click para expandir)</summary>

| Institución | Folios |
|------------|--------|
| INFONAVIT | 4 |
| CONAPRED | 3 |
| Fiscalía General de la República (FGR) | 3 |
| ATDT (Agencia de Transformación Digital) | 2 |
| Servicio de Administración Tributaria (SAT) | 2 |
| Transparencia para el Pueblo | 2 |
| INEGI | 2 |
| PRODECON | 2 |
| SSPC-Guardia Nacional | 2 |
| Cámara de Diputados | 1 |
| Auditoría Superior de la Federación (ASF) | 1 |
| CEAV (Comisión Ejecutiva de Atención a Víctimas) | 1 |
| CEAV-FAARI | 1 |
| CENAPRED | 1 |
| Centro Nacional de Inteligencia | 1 |
| CENAM | 1 |
| CFCRL (Centro Federal de Conciliación y Registro Laboral) | 1 |
| CJEF (Consejería Jurídica del Ejecutivo Federal) | 1 |
| CNDH | 1 |
| CONDUSEF | 1 |
| FIDERH (OIC Banxico) | 1 |
| IMPI | 1 |
| IMSS | 1 |
| INACIPE | 1 |
| INDAUTOR | 1 |
| INFOTEC | 1 |
| IPN | 1 |
| Oficina de la Presidencia | 1 |
| Poder Judicial Veracruz | 1 |
| SCJN | 1 |
| SEGOB | 1 |
| SICT | 1 |
| SICT-IMT | 1 |
| SRE | 1 |
| STPS (×2 datos personales) | 2 |
| UNAM | 1 |
| INFOCDMX (local CDMX) | 1 |

</details>

---

## Folios críticos con seguimiento activo

| Folio PNT | Institución | Estatus | Observación |
|-----------|------------|---------|-------------|
| `340027700068926` | SAT (RR SAT2609690) | Terminada | Recurso de Revisión activo; instructor: ricardo.vivas@transparencia.gob.mx |
| `342259800048026` | SSPC-Guardia Nacional | Terminada | RR GN2607409; ventana de manifestación activa |
| `343204900019026` | ATDT | Terminada | RR ATDT2607389; instructor: mario.sanchez@transparencia.gob.mx |
| `340024000011226` | Prevención y Reinserción Social | Terminada | RR PRS2610007; 40+20 días activos |
| `340031000129926` | INFONAVIT | Pendiente ID | Respuesta PNT 340031000129926; vence **29/05/2026** |
| `340031000137326` | INFONAVIT | En proceso c/prevención | ARCO+ crédito hipotecario; prevención desahogada |
| `340007600009126` | CEAV | En proceso c/prevención | Prevención desahogada; respuesta de fondo pendiente |

---

## Infraestructura legal complementaria

Este repositorio PNT es un componente del **Estado Mayor Jurídico** activo. Las rutas terminales en desarrollo son:

1. **LFRPE** — Demanda de responsabilidad patrimonial ante TFJA  
2. **Amparo Indirecto V3** — Con medidas cautelares: congelamiento de cuentas Narcea + depuración base de datos R-Control  
3. **CIDH** — Petición que enmarca el caso como servidumbre corporativa moderna en autotransporte federal mexicano  

**Daño cuantificado al 21/05/2026:**  
`M(D) = 2,336,978.36 + [(D − 98) × 2,413.15 MXN]` · Total reclamado: **$31,150,480.81 MXN**

---

## Licencia y autoría

Repositorio de uso personal e institucional. Los documentos vinculados pertenecen a las instituciones públicas correspondientes (PNT) y son de libre acceso conforme a la Ley General de Transparencia y Acceso a la Información Pública.

**Titular:** Genaro Carrasco Ozuna · RFC: CAOG840906RG3 · ORCID: [0009-0005-6358-9910](https://orcid.org/0009-0005-6358-9910)  
**Contacto:** geozunac3536@gmail.com  
**Última actualización:** 21/05/2026
