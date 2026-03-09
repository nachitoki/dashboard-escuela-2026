import os
import yaml
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(r"C:\Users\Dr Pixel Pc\.gemini\antigravity\brain\5f4bf7f0-5c0d-4876-beba-68002e23f044\Sistema_2026")
ROOT_PLANIFICACIONES = Path(r"e:\Mi unidad\2026 Clases\Planificaciones\INSTRUMENTOS RECTORES ESCUELA AONIKENK 2026\Cursos")

def scan_course_folders():
    discrepancias = []
    
    # Cargar registro
    reg_path = BASE_DIR / "registro_clases.yml"
    if not reg_path.exists():
        print(f"Error: {reg_path} no existe")
        return []
        
    with open(reg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        registro = data.get("registro_clases", [])
        
    for item in registro:
        curso = item["curso"]
        asignatura = item["asignatura"]
        semana = item["semana"]
        estado = item["estado"]
        
        # Normalizar nombres para carpetas
        curso_clean = curso.replace(" Básico", "").replace("°", "°")
        folder_search = ROOT_PLANIFICACIONES / asignatura / f"{curso_clean}_{asignatura}"
        
        if folder_search.exists():
            found_files = []
            for root, dirs, files in os.walk(folder_search):
                for f_name in files:
                    if f_name.lower().endswith(('.md', '.docx')):
                        patterns = [f"Semana{semana}", f"S{semana}", f"Clase {semana}", f"Clase{semana}"]
                        if any(p in f_name for p in patterns):
                            found_files.append(f_name)
            
            if found_files:
                discrepancias.append({
                    "id": item["id"],
                    "estado_actual": estado,
                    "archivos_detectados": found_files,
                    "ruta": str(folder_search)
                })

    return discrepancias

if __name__ == "__main__":
    print("\n--- INFORME DE SINCRONIZACIÓN: REGISTRO VS ARCHIVOS ---")
    results = scan_course_folders()
    for res in results:
        status_icon = "✅" if res['estado_actual'] == "Hecho" else "⚠️"
        print(f"{status_icon} ID: {res['id']} | Registro: {res['estado_actual']}")
        print(f"   Archivos: {', '.join(res['archivos_detectados'])}")
        print(f"   Ruta: {res['ruta']}\n")
