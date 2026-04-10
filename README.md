# trip-osint

Sistema OSINT modular para ingestión, normalización, enriquecimiento y análisis de señales relacionadas con movilidad, seguridad, clima y política.

## Pipeline

1. Ingest → `data/raw/`
2. Normalize → `data/processed/`
3. Enrich → `data/processed/`
4. KPIs → `data/kpis/`

## Ejecución

python3 src/ingest/ingest_rss.py  
python3 src/normalize/normalize_events.py  
python3 src/enrich/enrich_events.py  
python3 src/kpis/kpi_activity.py  

