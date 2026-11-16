# Índice de evidencia cruda en Google Drive (deduplicado)

`indice_evidencia_drive.csv` relaciona cada folio PNT con los archivos del Drive del titular cuyo **nombre contiene el número de folio original**.

## Método

1. Búsqueda en Drive por título que contiene cada uno de los 121 folios de la exportación oficial (4 lotes de ~30 folios, carpetas `*_pnt`, `*oleada*`, `respuestas_pnt`, `folios_pnt`, etc.).
2. Deduplicación: dos archivos son la misma evidencia si coinciden en **nombre normalizado** (sin sufijos de copia ` (n)`) y **tamaño en bytes**. Se conserva un ID representativo y se reporta el número de copias detectadas.
3. No se descargó ni se publicó el contenido de los archivos: los IDs de Drive son privados y solo sirven al titular para localizar el original.

## Cobertura (corte 16/11/2026)

- Archivos revisados (copias incluidas): 1,540 · evidencias únicas tras deduplicar: 459.
- Folios con al menos un archivo localizado: 121 de 121.
- **Límite:** se recorrieron las primeras 4 páginas (400 resultados) de cada lote; Drive aún reportaba páginas adicionales. El índice es suficiente para vincular cada folio con su evidencia, pero no es un inventario exhaustivo de todas las copias.
- Archivos cuyo nombre no contiene el folio (p. ej. oficios nombrados solo por número interno) no quedan vinculados por este método.
