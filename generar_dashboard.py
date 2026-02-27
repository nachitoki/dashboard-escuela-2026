import os
import re
import json
import markdown
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "Outputs"
DASHBOARD_FILE = OUTPUT_DIR / "dashboard.html"

def parse_md_file(filepath):
    """Extrae metadatos y contenido de un archivo .md de planificación"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extraer nombre del archivo
    filename = filepath.name
    parts = filename.replace(".md", "").split("_")
    
    semana = parts[0].replace("S", "") if len(parts) > 0 else "?"
    asignatura_code = parts[1] if len(parts) > 1 else "?"
    curso = parts[2] if len(parts) > 2 else "?"
    
    asignatura = "Patrimonio" if asignatura_code == "PAT" else "Religión" if asignatura_code == "REL" else asignatura_code
    
    # Extraer datos del contenido
    titulo_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    titulo = titulo_match.group(1) if titulo_match else filename
    
    objetivo_match = re.search(r"## 🎯 Objetivo de la Clase\s*\n(.+)", content)
    objetivo = objetivo_match.group(1).strip() if objetivo_match else ""
    
    # MBE checks
    mbe_a = "[x]" in content.split("Dominio A")[1].split("\n")[0] if "Dominio A" in content else False
    mbe_b = "[x]" in content.split("Dominio B")[1].split("\n")[0] if "Dominio B" in content else False
    mbe_c = "[x]" in content.split("Dominio C")[1].split("\n")[0] if "Dominio C" in content else False
    mbe_d = "[x]" in content.split("Dominio D")[1].split("\n")[0] if "Dominio D" in content else False

    # Extraer materiales inteligentemente
    materiales = extraer_materiales(content, asignatura)

    # Convertir MD a HTML básico
    html_content = md_to_html(content)
    
    return {
        "filename": filename,
        "semana": semana,
        "asignatura": asignatura,
        "asignatura_code": asignatura_code,
        "curso": curso,
        "titulo": titulo,
        "objetivo": objetivo,
        "mbe": {"A": mbe_a, "B": mbe_b, "C": mbe_c, "D": mbe_d},
        "materiales": materiales,
        "html": html_content,
        "raw_md": content
    }

def extraer_materiales(content, asignatura):
    """Extrae y deduce materiales necesarios del contenido de la clase"""
    materiales = []
    texto = content.lower()
    
    # Materiales explícitos del campo Materiales:
    mat_match = re.search(r'\*\*Materiales:\*\*(.+)', content)
    if mat_match:
        for item in mat_match.group(1).split(','):
            item = item.strip().rstrip('.')
            if item and item not in ['cuaderno', 'pizarra', 'lápiz']:
                materiales.append({'tipo': 'basico', 'item': item, 'preparar': False})
    
    # Detección inteligente de materiales a preparar
    detecciones = [
        ('fotografía', 'foto', '📷 Fotografías impresas o proyectadas'),
        ('tarjeta', None, '🃏 Tarjetas / fichas impresas'),
        ('guía', None, '📝 Guía de trabajo impresa'),
        ('mapa', 'mapeo', '🗺️ Mapa o plano impreso'),
        ('línea de tiempo', 'timeline', '📏 Línea de tiempo impresa/dibujada'),
        ('lámina', None, '🖼️ Láminas visuales'),
        ('afiche', 'póster', '📋 Cartulinas para afiches'),
        ('video', None, '📺 Video preparado (proyector/parlante)'),
        ('canción', 'canto', '🎵 Audio/letra de canción'),
        ('dibujo', 'colorear', '🖍️ Hojas para dibujar / colorear'),
        ('exposición', 'presentación', '📊 Pauta de exposición'),
        ('debate', None, '🗣️ Pauta de debate estructurado'),
        ('ensayo', None, '📄 Pauta de ensayo'),
        ('rúbrica', 'evaluación', '📊 Rúbrica de evaluación'),
        ('recorte', 'tijera', '✂️ Materiales para recortar/pegar'),
        ('biblia', 'straubinger', '📖 Biblia (Straubinger) disponible'),
    ]
    
    for keywords in detecciones:
        primary = keywords[0]
        secondary = keywords[1]
        label = keywords[2]
        if primary in texto or (secondary and secondary in texto):
            if not any(m['item'] == label for m in materiales):
                materiales.append({'tipo': 'preparar', 'item': label, 'preparar': True})
    
    # Si es Patrimonio, siempre necesita cámara/celular para bitácora
    if asignatura == 'Patrimonio':
        materiales.append({'tipo': 'preparar', 'item': '📸 Cámara/celular para bitácora fotográfica', 'preparar': True})
    
    return materiales

def md_to_html(md_text):
    """Conversión de Markdown a HTML usando extensión nativa"""
    # Protegemos casillas
    md_text = md_text.replace("[x]", "☑").replace("[ ]", "☐")
    
    # Renderizamos usando librería markdown con soporte para listas anidadas
    # y saltos de línea automáticos.
    html = markdown.markdown(md_text, extensions=['extra', 'sane_lists', 'nl2br'])
    
    return html

def generate_dashboard(clases):
    """Genera el HTML del dashboard completo con vista calendario"""
    
    semanas = sorted(set(c["semana"] for c in clases))
    clases_json = json.dumps(clases, ensure_ascii=False, indent=2)
    
    # Fechas de inicio de cada semana de clases 2026
    semana_fechas = {
        "1": "3-7 Mar", "2": "10-14 Mar", "3": "17-21 Mar", "4": "24-28 Mar",
        "5": "31 Mar-4 Abr", "6": "7-11 Abr", "7": "21-25 Abr", "8": "28 Abr-2 May",
        "9": "5-9 May", "10": "12-16 May", "11": "19-23 May", "12": "26-30 May",
        "13": "2-6 Jun", "14": "9-13 Jun", "15": "16-20 Jun", "16": "23-27 Jun",
        "17": "30 Jun-4 Jul", "18": "7-11 Jul", "19": "28 Jul-1 Ago", "20": "4-8 Ago",
        "21": "11-15 Ago", "22": "18-22 Ago", "23": "25-29 Ago", "24": "1-5 Sep",
        "25": "8-12 Sep", "26": "22-26 Sep", "27": "29 Sep-3 Oct", "28": "6-10 Oct",
        "29": "13-17 Oct", "30": "20-24 Oct", "31": "27-31 Oct", "32": "3-7 Nov",
        "33": "10-14 Nov", "34": "17-21 Nov", "35": "24-28 Nov", "36": "1-5 Dic",
    }
    semana_fechas_json = json.dumps(semana_fechas, ensure_ascii=False)

    from datetime import datetime
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Curricular 2026 — Escuela Aonikenk</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #242836;
    --border: #2d3348;
    --text: #e4e4e7;
    --text-muted: #9ca3af;
    --pat-primary: #10b981;
    --pat-bg: #10b98115;
    --rel-primary: #8b5cf6;
    --rel-bg: #8b5cf615;
    --accent: #3b82f6;
    --gold: #f59e0b;
    --danger: #ef4444;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}

.header {{
    background: linear-gradient(135deg, #1a1d27 0%, #242836 100%);
    border-bottom: 1px solid var(--border);
    padding: 1.25rem 2rem;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 0.5rem;
}}
.header h1 {{
    font-size: 1.4rem; font-weight: 700;
    background: linear-gradient(135deg, var(--pat-primary), var(--rel-primary));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.header .subtitle {{ color: var(--text-muted); font-size: 0.8rem; margin-top: 0.15rem; }}

.stats-bar {{
    display: flex; gap: 0.75rem; padding: 0.75rem 2rem;
    border-bottom: 1px solid var(--border); background: var(--surface);
    overflow-x: auto;
}}
.stat-card {{
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.75rem 1.25rem; flex: 1; text-align: center; min-width: 100px;
}}
.stat-card .number {{ font-size: 1.75rem; font-weight: 700; }}
.stat-card .label {{ color: var(--text-muted); font-size: 0.75rem; margin-top: 0.15rem; }}

/* View Toggle */
.view-toggle {{
    display: flex; gap: 0; padding: 0 2rem;
    border-bottom: 1px solid var(--border); background: var(--surface);
}}
.view-tab {{
    padding: 0.75rem 1.5rem; border: none; background: none;
    color: var(--text-muted); cursor: pointer; font-family: inherit;
    font-size: 0.85rem; font-weight: 500; border-bottom: 2px solid transparent;
    transition: all 0.2s;
}}
.view-tab:hover {{ color: var(--text); }}
.view-tab.active {{ color: var(--accent); border-bottom-color: var(--accent); }}

/* Filters */
.filters {{
    display: flex; gap: 0.5rem; padding: 0.75rem 2rem;
    flex-wrap: wrap; border-bottom: 1px solid var(--border);
}}
.filter-btn {{
    padding: 0.4rem 1rem; border-radius: 20px;
    border: 1px solid var(--border); background: var(--surface2);
    color: var(--text-muted); cursor: pointer; font-size: 0.8rem;
    font-family: inherit; transition: all 0.2s;
}}
.filter-btn:hover {{ border-color: var(--accent); color: var(--text); }}
.filter-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}
.filter-btn.pat-active {{ background: var(--pat-primary); color: white; border-color: var(--pat-primary); }}
.filter-btn.rel-active {{ background: var(--rel-primary); color: white; border-color: var(--rel-primary); }}

/* Grid View */
.grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1rem; padding: 1.25rem 2rem;
}}
.card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; overflow: hidden; transition: all 0.3s; cursor: pointer;
}}
.card:hover {{ transform: translateY(-2px); border-color: var(--accent); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }}
.card.pat {{ border-left: 4px solid var(--pat-primary); }}
.card.rel {{ border-left: 4px solid var(--rel-primary); }}
.card-header {{ padding: 1rem 1.25rem 0; display: flex; justify-content: space-between; align-items: flex-start; }}
.card-badge {{
    font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 20px;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}}
.card.pat .card-badge {{ background: var(--pat-bg); color: var(--pat-primary); }}
.card.rel .card-badge {{ background: var(--rel-bg); color: var(--rel-primary); }}
.card-title {{ font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem; padding: 0 1.25rem; }}
.card-objetivo {{ font-size: 0.78rem; color: var(--text-muted); margin-top: 0.35rem; padding: 0 1.25rem; line-height: 1.4; }}
.card-footer {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.75rem 1.25rem; border-top: 1px solid var(--border); margin-top: 0.75rem;
}}
.mbe-dots {{ display: flex; gap: 0.3rem; }}
.mbe-dot {{
    width: 22px; height: 22px; border-radius: 5px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 700;
    border: 1px solid var(--border); color: var(--text-muted);
}}
.mbe-dot.active {{ background: var(--pat-primary); color: white; border-color: var(--pat-primary); }}
.card-week {{ color: var(--text-muted); font-size: 0.7rem; }}

/* Calendar View */
.calendar {{ padding: 1.25rem 2rem; }}
.cal-month {{
    margin-bottom: 1.5rem;
}}
.cal-month-title {{
    font-size: 1rem; font-weight: 700; color: var(--gold);
    margin-bottom: 0.75rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 0.5rem;
}}
.cal-week {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; margin-bottom: 0.5rem;
    transition: all 0.2s; cursor: pointer;
}}
.cal-week:hover {{ border-color: var(--accent); }}
.cal-week.expanded {{ border-color: var(--accent); }}
.cal-week-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.85rem 1.25rem; gap: 1rem;
}}
.cal-week-label {{
    display: flex; align-items: center; gap: 0.75rem; min-width: 180px;
}}
.cal-week-num {{
    background: var(--accent); color: white; font-weight: 700;
    font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 6px;
}}
.cal-week-date {{ color: var(--text-muted); font-size: 0.8rem; }}
.cal-week-dots {{ display: flex; gap: 0.35rem; flex-wrap: wrap; justify-content: center; flex: 1; }}
.cal-dot {{
    width: 28px; height: 28px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.55rem; font-weight: 700; cursor: pointer;
    transition: all 0.15s; position: relative;
}}
.cal-dot.pat {{ background: var(--pat-bg); color: var(--pat-primary); border: 1px solid var(--pat-primary)30; }}
.cal-dot.rel {{ background: var(--rel-bg); color: var(--rel-primary); border: 1px solid var(--rel-primary)30; }}
.cal-dot:hover {{ transform: scale(1.15); }}
.cal-dot.empty {{ background: var(--surface2); color: var(--text-muted); border: 1px dashed var(--border); opacity: 0.4; }}
.cal-week-count {{ color: var(--text-muted); font-size: 0.75rem; min-width: 60px; text-align: right; }}
.cal-week-arrow {{ color: var(--text-muted); font-size: 0.8rem; transition: transform 0.2s; }}
.cal-week.expanded .cal-week-arrow {{ transform: rotate(90deg); }}

.cal-week-body {{
    display: none; padding: 0 1.25rem 1rem;
    border-top: 1px solid var(--border);
}}
.cal-week.expanded .cal-week-body {{ display: block; }}
.cal-week-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 0.75rem; padding-top: 0.75rem;
}}
.cal-mini-card {{
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.75rem 1rem; cursor: pointer;
    transition: all 0.2s;
}}
.cal-mini-card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
.cal-mini-card.pat {{ border-left: 3px solid var(--pat-primary); }}
.cal-mini-card.rel {{ border-left: 3px solid var(--rel-primary); }}
.cal-mini-title {{ font-size: 0.8rem; font-weight: 600; }}
.cal-mini-sub {{ font-size: 0.7rem; color: var(--text-muted); margin-top: 0.2rem; }}

/* Modal */
.modal-overlay {
    display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.85); z-index: 1000;
    justify-content: center; align-items: center; padding: 1.5rem;
    backdrop-filter: blur(5px);
}
.modal-overlay.active { display: flex; }
.modal {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 20px; max-width: 950px; width: 100%;
    max-height: 90vh; overflow-y: auto; padding: 2.5rem; position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
.modal h1 { font-size: 1.6rem; margin-bottom: 1rem; color: var(--text); border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
.modal h2 { font-size: 1.3rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--accent); display: flex; align-items: center; gap: 0.5rem; }
.modal h3 { 
    font-size: 1.1rem; margin-top: 1.8rem; margin-bottom: 1rem; 
    color: var(--gold); background: rgba(245, 158, 11, 0.1); 
    padding: 0.5rem 1rem; border-radius: 8px; border-left: 4px solid var(--gold);
}
.modal h4 { font-size: 1rem; margin-top: 1.2rem; color: var(--pat-primary); }
.modal p { line-height: 1.75; margin-top: 1rem; margin-bottom: 1.2rem; font-size: 1.05rem; }
.modal li { margin-left: 1.5rem; line-height: 1.75; margin-bottom: 0.8rem; font-size: 1.05rem; }
.modal ul, .modal ol { margin-top: 0.8rem; margin-bottom: 1.5rem; }
.modal li > ul, .modal li > ol { margin-top: 0.5rem; margin-bottom: 0.5rem; }
.modal hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; opacity: 0.5; }
.modal blockquote { 
    border-left: 4px solid var(--rel-primary); padding: 1rem 1.5rem; 
    margin: 1.5rem 0; background: rgba(139, 92, 246, 0.05);
    color: var(--text); font-style: italic; border-radius: 0 8px 8px 0;
}
.modal strong { color: var(--text); font-weight: 600; }

/* Diferenciación de Secciones */
.modal h3:contains("INICIO"), .modal h3:contains("Inicio") { border-left-color: var(--accent); background: rgba(59, 130, 246, 0.1); color: var(--accent); }
.modal h3:contains("DESARROLLO"), .modal h3:contains("Desarrollo") { border-left-color: var(--gold); background: rgba(245, 158, 11, 0.1); color: var(--gold); }
.modal h3:contains("CIERRE"), .modal h3:contains("Cierre") { border-left-color: var(--pat-primary); background: rgba(16, 185, 129, 0.1); color: var(--pat-primary); }
.modal-close {{
    position: sticky; top: 0; float: right;
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); width: 36px; height: 36px;
    border-radius: 50%; cursor: pointer; font-size: 1.2rem;
    display: flex; align-items: center; justify-content: center; z-index: 10;
}}
.modal-actions {{
    display: flex; gap: 0.75rem; flex-wrap: wrap;
    margin-top: 1.5rem; padding-top: 1rem;
    border-top: 1px solid var(--border);
}}
.btn {{
    padding: 0.5rem 1.25rem; border-radius: 10px;
    border: 1px solid var(--border); background: var(--surface2);
    color: var(--text); cursor: pointer; font-family: inherit;
    font-size: 0.8rem; transition: all 0.2s;
}}
.btn:hover {{ background: var(--accent); border-color: var(--accent); color: white; }}
.btn-print {{ background: var(--pat-primary); border-color: var(--pat-primary); color: white; }}

/* Material Tracker */
.materials {{ padding: 1.25rem 2rem; }}
.mat-week {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; margin-bottom: 1rem; overflow: hidden;
}}
.mat-week-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.25rem; cursor: pointer;
}}
.mat-week-header:hover {{ background: var(--surface2); }}
.mat-week-title {{ font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 0.75rem; }}
.mat-week-badge {{
    font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 12px;
    font-weight: 700;
}}
.mat-week-badge.urgent {{ background: #ef444430; color: var(--danger); }}
.mat-week-badge.soon {{ background: #f59e0b30; color: var(--gold); }}
.mat-week-badge.planned {{ background: #3b82f630; color: var(--accent); }}
.mat-progress {{ display: flex; align-items: center; gap: 0.5rem; }}
.mat-progress-bar {{
    width: 100px; height: 6px; background: var(--surface2);
    border-radius: 3px; overflow: hidden;
}}
.mat-progress-fill {{ height: 100%; border-radius: 3px; transition: width 0.3s; background: var(--pat-primary); }}
.mat-progress-text {{ color: var(--text-muted); font-size: 0.75rem; }}
.mat-week-body {{ padding: 0 1.25rem 1rem; }}
.mat-clase {{
    margin-bottom: 0.75rem; padding: 0.75rem; background: var(--surface2);
    border-radius: 8px; border-left: 3px solid var(--border);
}}
.mat-clase.pat {{ border-left-color: var(--pat-primary); }}
.mat-clase.rel {{ border-left-color: var(--rel-primary); }}
.mat-clase-title {{ font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem; }}
.mat-item {{
    display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0;
    font-size: 0.8rem; cursor: pointer; transition: opacity 0.2s;
}}
.mat-item:hover {{ opacity: 0.8; }}
.mat-item.done {{ text-decoration: line-through; opacity: 0.5; }}
.mat-checkbox {{
    width: 18px; height: 18px; border-radius: 4px;
    border: 2px solid var(--border); cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; flex-shrink: 0; transition: all 0.2s;
}}
.mat-checkbox.checked {{ background: var(--pat-primary); border-color: var(--pat-primary); color: white; }}
.mat-summary {{
    display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;
}}
.mat-summary-card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 1rem 1.5rem; flex: 1; min-width: 150px; text-align: center;
}}
.mat-summary-num {{ font-size: 1.75rem; font-weight: 700; }}
.mat-summary-label {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem; }}

@media (max-width: 700px) {{
    .header {{ padding: 1rem; }}
    .header h1 {{ font-size: 1.1rem; }}
    .stats-bar {{ padding: 0.5rem 1rem; gap: 0.5rem; }}
    .stat-card {{ padding: 0.5rem 0.75rem; }}
    .stat-card .number {{ font-size: 1.3rem; }}
    .filters {{ padding: 0.5rem 1rem; }}
    .grid {{ padding: 1rem; grid-template-columns: 1fr; }}
    .calendar {{ padding: 1rem; }}
    .materials {{ padding: 1rem; }}
    .cal-week-header {{ flex-wrap: wrap; padding: 0.75rem; }}
    .cal-week-dots {{ justify-content: flex-start; }}
    .cal-week-grid {{ grid-template-columns: 1fr; }}
    .modal {{ padding: 1.25rem; }}
}}

@media print {{
    body {{ background: white; color: black; }}
    .header,.stats-bar,.view-toggle,.filters,.grid,.calendar,.materials,.modal-close,.modal-actions {{ display: none !important; }}
    .modal-overlay {{ position: static; background: none; display: block !important; padding: 0; }}
    .modal {{ max-height: none; border: none; padding: 1rem; box-shadow: none; background: white; color: black; max-width: 100%; }}
    .modal h1 {{ color: black; }} .modal h2 {{ color: #1a5276; }}
    .modal h3 {{ color: #7d6608; }} .modal blockquote {{ color: #555; }}
}}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>📚 Dashboard Curricular 2026</h1>
        <div class="subtitle">Escuela Aonikenk — Generado por Antigravity</div>
    </div>
    <div style="color: var(--text-muted); font-size: 0.75rem;">
        Actualizado: {timestamp}
    </div>
</div>

<div class="stats-bar" id="statsBar"></div>
<div class="view-toggle">
    <button class="view-tab" id="tabCal" onclick="switchView('calendar')">📅 Calendario</button>
    <button class="view-tab active" id="tabGrid" onclick="switchView('grid')">🔲 Tarjetas</button>
    <button class="view-tab" id="tabMat" onclick="switchView('materials')">📦 Material</button>
</div>
<div class="filters" id="filtersBar"></div>
<div class="grid" id="grid"></div>
<div class="calendar" id="calendar" style="display:none"></div>
<div class="materials" id="materials" style="display:none"></div>

<div class="modal-overlay" id="modalOverlay" onclick="if(event.target===this)closeModal()">
    <div class="modal" id="modalContent"></div>
</div>

<script>
const CLASES = {clases_json};
const SEMANA_FECHAS = {semana_fechas_json};
const MESES_SEMANAS = {{
    "Marzo": ["1","2","3","4"],
    "Abril": ["5","6","7","8"],
    "Mayo": ["9","10","11","12"],
    "Junio": ["13","14","15","16"],
    "Julio": ["17","18"],
    "Agosto": ["19","20","21","22","23"],
    "Septiembre": ["24","25","26","27"],
    "Octubre": ["28","29","30","31"],
    "Noviembre": ["32","33","34","35"],
    "Diciembre": ["36"]
}};
const CURSOS = ["1basico","2basico","3basico","4basico","5basico","6basico","7basico","8basico"];

let activeView = 'grid';
let activeFilters = {{ asignatura: 'all', curso: 'all' }};

function init() {{ renderStats(); renderFilters(); renderGrid(); renderCalendar(); renderMaterials(); }}

// localStorage helper for material tracking
function getMatState() {{ try {{ return JSON.parse(localStorage.getItem('matState2026') || '{{}}'); }} catch(e) {{ return {{}}; }} }}
function setMatState(s) {{ localStorage.setItem('matState2026', JSON.stringify(s)); }}
function toggleMat(key) {{
    const s = getMatState();
    s[key] = !s[key];
    setMatState(s);
    renderMaterials();
}}

function switchView(v) {{
    activeView = v;
    document.getElementById('grid').style.display = v==='grid' ? 'grid' : 'none';
    document.getElementById('calendar').style.display = v==='calendar' ? 'block' : 'none';
    document.getElementById('materials').style.display = v==='materials' ? 'block' : 'none';
    document.getElementById('tabGrid').className = 'view-tab' + (v==='grid' ? ' active' : '');
    document.getElementById('tabCal').className = 'view-tab' + (v==='calendar' ? ' active' : '');
    document.getElementById('tabMat').className = 'view-tab' + (v==='materials' ? ' active' : '');
    if (v==='materials') renderMaterials();
}}

function renderStats() {{
    const valid = CLASES.filter(c => !c.curso.includes('ciclo'));
    const total = valid.length;
    const pat = valid.filter(c => c.asignatura === 'Patrimonio').length;
    const rel = valid.filter(c => c.asignatura === 'Religión' || c.asignatura === 'Religion').length;
    const semanas = new Set(valid.map(c => c.semana)).size;
    document.getElementById('statsBar').innerHTML = `
        <div class="stat-card"><div class="number" style="color:var(--accent)">${{total}}</div><div class="label">Planificaciones</div></div>
        <div class="stat-card"><div class="number" style="color:var(--pat-primary)">${{pat}}</div><div class="label">Patrimonio</div></div>
        <div class="stat-card"><div class="number" style="color:var(--rel-primary)">${{rel}}</div><div class="label">Religión</div></div>
        <div class="stat-card"><div class="number" style="color:var(--gold)">${{semanas}}</div><div class="label">Semanas</div></div>
    `;
}}

function renderFilters() {{
    const cursos = [...new Set(CLASES.map(c => c.curso))].filter(c => !c.includes('ciclo')).sort();
    let html = `
        <button class="filter-btn active" onclick="setFilter('asignatura','all',this)">Todas</button>
        <button class="filter-btn" onclick="setFilter('asignatura','Patrimonio',this)" data-type="pat">📗 Patrimonio</button>
        <button class="filter-btn" onclick="setFilter('asignatura','Religion',this)" data-type="rel">📕 Religión</button>
        <span style="width:1px;background:var(--border);margin:0 0.25rem"></span>
    `;
    cursos.forEach(c => {{
        html += `<button class="filter-btn" onclick="setFilter('curso','${{c}}',this)">${{c.replace('basico','°')}}</button>`;
    }});
    document.getElementById('filtersBar').innerHTML = html;
}}

function setFilter(key, value, btn) {{
    activeFilters[key] = value;
    if (key === 'asignatura') {{
        document.querySelectorAll('.filter-btn').forEach(b => {{
            if (b.textContent.includes('Todas') || b.textContent.includes('Patrimonio') || b.textContent.includes('Religión'))
                b.className = 'filter-btn';
        }});
        if (value === 'Patrimonio') btn.className = 'filter-btn pat-active';
        else if (value === 'Religion') btn.className = 'filter-btn rel-active';
        else btn.className = 'filter-btn active';
    }} else {{
        document.querySelectorAll('.filter-btn').forEach(b => {{
            if (!b.dataset.type && !['Todas','Patrimonio','Religión'].some(t => b.textContent.includes(t)))
                b.className = 'filter-btn';
        }});
        btn.className = 'filter-btn active';
    }}
    renderGrid(); renderCalendar();
}}

function getFiltered() {{
    let f = CLASES.filter(c => !c.curso.includes('ciclo'));
    if (activeFilters.asignatura !== 'all')
        f = f.filter(c => c.asignatura === activeFilters.asignatura || c.asignatura.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'') === activeFilters.asignatura);
    if (activeFilters.curso !== 'all')
        f = f.filter(c => c.curso === activeFilters.curso);
    return f;
}}

function renderGrid() {{
    const filtered = getFiltered();
    document.getElementById('grid').innerHTML = filtered.map(c => `
        <div class="card ${{c.asignatura_code==='PAT'?'pat':'rel'}}" onclick="openModal(${{CLASES.indexOf(c)}})">
            <div class="card-header">
                <span class="card-badge">${{c.asignatura}}</span>
                <span style="color:var(--text-muted);font-size:0.75rem">${{c.curso.replace('basico','° Básico')}}</span>
            </div>
            <div class="card-title">${{c.titulo.substring(0,75)}}</div>
            <div class="card-objetivo">${{c.objetivo.substring(0,100)}}${{c.objetivo.length>100?'...':''}}</div>
            <div class="card-footer">
                <div class="mbe-dots">
                    <div class="mbe-dot ${{c.mbe.A?'active':''}}">A</div>
                    <div class="mbe-dot ${{c.mbe.B?'active':''}}">B</div>
                    <div class="mbe-dot ${{c.mbe.C?'active':''}}">C</div>
                    <div class="mbe-dot ${{c.mbe.D?'active':''}}">D</div>
                </div>
                <span class="card-week">S${{c.semana}}</span>
            </div>
        </div>
    `).join('') || '<p style="color:var(--text-muted);padding:2rem;text-align:center">Sin planificaciones para este filtro.</p>';
}}

function renderCalendar() {{
    const filtered = getFiltered();
    let html = '';
    for (const [mes, semNums] of Object.entries(MESES_SEMANAS)) {{
        const semanasConClases = semNums.filter(s => filtered.some(c => c.semana === s));
        const semanasVacias = semNums.filter(s => !filtered.some(c => c.semana === s));
        
        html += `<div class="cal-month">
            <div class="cal-month-title">📅 ${{mes}} <span style="font-weight:400;font-size:0.8rem;color:var(--text-muted)">${{semanasConClases.length}}/${{semNums.length}} semanas</span></div>`;
        
        for (const sn of semNums) {{
            const weekClases = filtered.filter(c => c.semana === sn);
            const hasContent = weekClases.length > 0;
            const fecha = SEMANA_FECHAS[sn] || '';
            
            html += `<div class="cal-week ${{hasContent?'':''}}" onclick="this.classList.toggle('expanded')">
                <div class="cal-week-header">
                    <div class="cal-week-label">
                        <span class="cal-week-num" style="${{!hasContent?'opacity:0.3;background:var(--border)':''}}">S${{sn}}</span>
                        <span class="cal-week-date">${{fecha}}</span>
                    </div>
                    <div class="cal-week-dots">`;
            
            if (hasContent) {{
                weekClases.forEach(c => {{
                    const tipo = c.asignatura_code === 'PAT' ? 'pat' : 'rel';
                    const label = c.curso.replace('basico','°');
                    html += `<div class="cal-dot ${{tipo}}" onclick="event.stopPropagation();openModal(${{CLASES.indexOf(c)}})" title="${{c.asignatura}} ${{c.curso.replace('basico','° Básico')}}">${{label}}</div>`;
                }});
            }} else {{
                html += '<span style="color:var(--text-muted);font-size:0.7rem;opacity:0.5">Sin planificar</span>';
            }}
            
            html += `</div>
                    <span class="cal-week-count">${{hasContent ? weekClases.length + ' clases' : ''}}</span>
                    <span class="cal-week-arrow">${{hasContent ? '▸' : ''}}</span>
                </div>`;
            
            if (hasContent) {{
                html += `<div class="cal-week-body"><div class="cal-week-grid">`;
                weekClases.forEach(c => {{
                    const tipo = c.asignatura_code === 'PAT' ? 'pat' : 'rel';
                    html += `<div class="cal-mini-card ${{tipo}}" onclick="event.stopPropagation();openModal(${{CLASES.indexOf(c)}})">
                        <div class="cal-mini-title">${{c.curso.replace('basico','° Básico')}} — ${{c.asignatura}}</div>
                        <div class="cal-mini-sub">${{c.titulo.substring(0,60)}}</div>
                    </div>`;
                }});
                html += `</div></div>`;
            }}
            
            html += `</div>`;
        }}
        html += `</div>`;
    }}
    document.getElementById('calendar').innerHTML = html;
}}

function openModal(idx) {{
    const c = CLASES[idx];
    document.getElementById('modalContent').innerHTML = `
        <button class="modal-close" onclick="closeModal()">✕</button>
        ${{c.html}}
        <div class="modal-actions">
            <button class="btn btn-print" onclick="window.print()">🖨️ Imprimir / PDF</button>
            <button class="btn" onclick="copyToClipboard(${{idx}})">📋 Copiar texto</button>
            <button class="btn" onclick="closeModal()">Cerrar</button>
        </div>
    `;
    document.getElementById('modalOverlay').classList.add('active');
}}
function closeModal() {{ document.getElementById('modalOverlay').classList.remove('active'); }}
function copyToClipboard(idx) {{
    navigator.clipboard.writeText(CLASES[idx].raw_md).then(() => alert('¡Texto copiado!'));
}}
document.addEventListener('keydown', e => {{ if (e.key==='Escape') closeModal(); }});

function renderMaterials() {{
    const valid = CLASES.filter(c => !c.curso.includes('ciclo'));
    const semanas = [...new Set(valid.map(c => c.semana))].sort((a,b) => parseInt(a)-parseInt(b));
    const state = getMatState();
    let totalItems = 0, doneItems = 0;
    const weekData = semanas.map(sn => {{
        const clases = valid.filter(c => c.semana === sn);
        let items = 0, done = 0;
        clases.forEach(c => {{
            const mats = c.materiales.filter(m => m.preparar);
            mats.forEach(m => {{
                const key = c.filename + '_' + m.item;
                items++;
                if (state[key]) done++;
            }});
        }});
        totalItems += items; doneItems += done;
        return {{ sn, clases, items, done }};
    }});
    const pendiente = totalItems - doneItems;
    let html = '<div class="mat-summary">';
    html += '<div class="mat-summary-card"><div class="mat-summary-num" style="color:var(--danger)">' + pendiente + '</div><div class="mat-summary-label">Pendientes</div></div>';
    html += '<div class="mat-summary-card"><div class="mat-summary-num" style="color:var(--pat-primary)">' + doneItems + '</div><div class="mat-summary-label">Listos</div></div>';
    html += '<div class="mat-summary-card"><div class="mat-summary-num" style="color:var(--gold)">' + totalItems + '</div><div class="mat-summary-label">Total</div></div>';
    html += '<div class="mat-summary-card"><div class="mat-summary-num" style="color:var(--accent)">' + (totalItems > 0 ? Math.round(doneItems/totalItems*100) : 0) + '%</div><div class="mat-summary-label">Avance</div></div>';
    html += '</div>';
    for (const wd of weekData) {{
        const fecha = SEMANA_FECHAS[wd.sn] || '';
        const pct = wd.items > 0 ? Math.round(wd.done/wd.items*100) : 100;
        const urgency = parseInt(wd.sn) <= 1 ? 'urgent' : parseInt(wd.sn) <= 2 ? 'soon' : 'planned';
        const urgLabel = urgency === 'urgent' ? 'ESTA SEMANA' : urgency === 'soon' ? 'Proxima' : 'Semana ' + wd.sn;
        if (wd.items === 0) continue;
        html += '<div class="mat-week">';
        html += '<div class="mat-week-header" onclick="var b=this.parentElement.querySelector(\\'.mat-week-body\\');b.style.display=b.style.display===\\'none\\'?\\'block\\':\\'none\\'">';
        html += '<div class="mat-week-title">Semana ' + wd.sn + ' <span style="font-weight:400;color:var(--text-muted)">(' + fecha + ')</span> ';
        html += '<span class="mat-week-badge ' + urgency + '">' + urgLabel + '</span></div>';
        html += '<div class="mat-progress"><div class="mat-progress-bar"><div class="mat-progress-fill" style="width:' + pct + '%;' + (pct===100?'background:var(--pat-primary)':'background:var(--gold)') + '"></div></div>';
        html += '<span class="mat-progress-text">' + wd.done + '/' + wd.items + '</span></div></div>';
        html += '<div class="mat-week-body">';
        for (const c of wd.clases) {{
            const mats = c.materiales.filter(m => m.preparar);
            if (mats.length === 0) continue;
            const tipo = c.asignatura_code === 'PAT' ? 'pat' : 'rel';
            html += '<div class="mat-clase ' + tipo + '"><div class="mat-clase-title">' + c.curso.replace('basico',' Basico') + ' - ' + c.asignatura + '</div>';
            for (const m of mats) {{
                const key = c.filename + '_' + m.item;
                const checked = state[key] ? true : false;
                const safeKey = key.replace(/[^a-zA-Z0-9_.]/g, '');
                html += '<div class="mat-item ' + (checked?'done':'') + '" onclick="toggleMat(\\\'' + safeKey + '\\\')">';
                html += '<div class="mat-checkbox ' + (checked?'checked':'') + '">' + (checked?'\\u2713':'') + '</div>';
                html += '<span>' + m.item + '</span></div>';
            }}
            html += '</div>';
        }}
        html += '</div></div>';
    }}
    if (totalItems === 0) {{
        html += '<p style="text-align:center;color:var(--text-muted);padding:2rem">No hay materiales detectados.</p>';
    }}
    document.getElementById('materials').innerHTML = html;
}}

init();
</script>
</body>
</html>"""
    return html

def main():
    print("📊 Generando Dashboard Curricular...")
    
    md_files = list(OUTPUT_DIR.glob("*.md"))
    if not md_files:
        print("No se encontraron archivos .md en Outputs/")
        return
    
    clases = []
    for f in sorted(md_files):
        try:
            clase = parse_md_file(f)
            clases.append(clase)
            print(f"  ✅ {f.name}")
        except Exception as e:
            print(f"  ⚠️ Error parsing {f.name}: {e}")
    
    html = generate_dashboard(clases)
    
    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n🎉 Dashboard generado: {DASHBOARD_FILE}")
    print(f"   Abre en Chrome: file:///{DASHBOARD_FILE.as_posix()}")

if __name__ == "__main__":
    main()
