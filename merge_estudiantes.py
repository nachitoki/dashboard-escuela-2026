import yaml
import os
from pathlib import Path

# Rutas
BASE_DIR = Path(r"C:\Users\Dr Pixel Pc\.gemini\antigravity\brain\5f4bf7f0-5c0d-4876-beba-68002e23f044\Sistema_2026")
ESTUDIANTES_FILE = BASE_DIR / "estudiantes.yml"
LISTAS_FILE = BASE_DIR / "estudiantes_listas.yml"

def merge_estudiantes():
    with open(ESTUDIANTES_FILE, "r", encoding="utf-8") as f:
        estudiantes_data = yaml.safe_load(f)
        
    with open(LISTAS_FILE, "r", encoding="utf-8") as f:
        listas_data = yaml.safe_load(f)
        
    # Fusionar
    for curso, lista in listas_data["listas_estudiantes"].items():
        if curso in estudiantes_data["contexto_estudiantes"]:
            estudiantes_data["contexto_estudiantes"][curso]["lista_nombres"] = lista
        else:
            print(f"⚠️ Curso {curso} no encontrado en estudiantes.yml")
            
    with open(ESTUDIANTES_FILE, "w", encoding="utf-8") as f:
        yaml.dump(estudiantes_data, f, allow_unicode=True, sort_keys=False)
    
    print(f"✅ Fusionado exitosamente en: {ESTUDIANTES_FILE}")

if __name__ == "__main__":
    merge_estudiantes()
