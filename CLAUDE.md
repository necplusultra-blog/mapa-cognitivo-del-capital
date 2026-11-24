# Instrucciones para Claude

- Este repositorio es parte del proyecto doctoral de Pablo Jiménez Cea. El plan, el estado y la bitácora viven en la carpeta del Project de claude.ai «sismografo-del-capital/», archivo «00 Plan, estado y bitácora (retomar aquí).md». Léelo antes de trabajar y actualízalo al cerrar cada sesión.
- Todo se escribe en español: código comentado, mensajes de commit y textos del sitio.
- Las decisiones teóricas (qué trabajo es productivo, qué entra en K, periodización) son de Pablo. No las cambies sin su indicación; regístralas en la sección «Decisiones» del plan.
- Lo que muestra el sitio es manifestación fenoménica, no demostración categorial: evita formulaciones que sugieran «medir la distancia a un tope».
- Verifica localmente con `python run.py --sin-descarga` y renderiza el sitio antes de hacer push.
- Los textos del sitio se editan en `contenido/` (Markdown; guía en `contenido/LEEME.md`), no en `site/*.html`, que se genera con `python -m sismografo.paginas` (también lo hace `run.py`). El marco de las páginas está en `plantillas/`; el estilo, en `site/style.css`.
- Cada gráfico debe tener su desplegable «¿Cómo se calcula?» actualizado cuando cambie el método.
