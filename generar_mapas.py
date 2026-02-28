import yaml
import os

def generar_mapas():
    # Cargar datos
    with open("patrimonio_unidades.yml", "r", encoding="utf-8") as f:
        pat_data = yaml.safe_load(f)["patrimonio_anual"]
    
    with open("religion_unidades.yml", "r", encoding="utf-8") as f:
        rel_data = yaml.safe_load(f)["religion_anual"]

    # Carpeta de salida
    os.makedirs("Outputs", exist_ok=True)

    # 1. Mapa de Patrimonio
    md_pat = f"""# 🗺️ Mapa Curricular: {pat_data['asignatura']} 2026
**Enfoque:** {pat_data['enfoque']}

```mermaid
graph TD
    subgraph "Lógica Anual de Patrimonio"
"""
    
    prev_id = None
    for u_key, u in pat_data["unidades"].items():
        uid = u["id"]
        label = f"{uid.upper()}: {u['titulo']}<br/>({u['meses']})<br/><i>{u['pregunta_esencial']}</i>"
        md_pat += f'    {uid}["{label}"]\n'
        if prev_id:
            md_pat += f'    {prev_id} --> {uid}\n'
        prev_id = uid
        
    md_pat += "end\n```\n\n### Hitos y Productos\n"
    for u_key, u in pat_data["unidades"].items():
        md_pat += f"- **{u['titulo']}**: {u['producto_esperado']} (Hito: {u['hito_vinculado']})\n"

    with open("Outputs/mapa_patrimonio.md", "w", encoding="utf-8") as f:
        f.write(md_pat)

    # 2. Mapa de Religión (Diferenciado por Ciclos)
    md_rel = f"""# 🗺️ Mapa Curricular: {rel_data['asignatura']} 2026
**Enfoque:** {rel_data['enfoque']}

```mermaid
graph LR
"""
    for ciclo, data in rel_data["ciclos"].items():
        ciclo_label = ciclo.replace("_", " ").title()
        md_rel += f'    subgraph "{ciclo_label}"\n'
        prev_id = None
        for u in data["unidades"]:
            uid = u["id"]
            label = f"{u['titulo']}<br/>({u['mes']})"
            md_rel += f'        {uid}["{label}"]\n'
            if prev_id:
                md_rel += f'        {prev_id} --> {uid}\n'
            prev_id = uid
        md_rel += "    end\n"
        
    md_rel += "```\n"

    with open("Outputs/mapa_religion.md", "w", encoding="utf-8") as f:
        f.write(md_rel)

    print("✅ Mapas conceptuales generados en Outputs/mapa_patrimonio.md y Outputs/mapa_religion.md")

if __name__ == "__main__":
    generar_mapas()
