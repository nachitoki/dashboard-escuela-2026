import pandas as pd
import os
import yaml
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(r"e:\Mi unidad\2026 Clases\Planificaciones\INSTRUMENTOS RECTORES ESCUELA AONIKENK 2026")
LISTAS_DIR = BASE_DIR / "Listas de curso"
OUTPUT_FILE = Path(os.getcwd()) / "estudiantes_listas.yml"

def limpiar_nombre(nombre):
    if pd.isna(nombre):
        return None
    # Limpiar espacios y posibles números al inicio (como en listas de asistencia)
    return str(nombre).strip()

def extraer_listas():
    resultados = {}
    archivos = [f"{i}°.xlsx" for i in range(1, 9)]
    
    for archivo in archivos:
        path = LISTAS_DIR / archivo
        if not path.exists():
            print(f"⚠️ No se encontró: {archivo}")
            continue
            
        print(f"Reading {archivo}...")
        try:
            # Leemos sin encabezado para detectar la columna de nombres manualmente
            df = pd.read_excel(path, header=None)
            
            # Buscamos la columna que tenga más texto (probablemente los nombres)
            # O simplemente tomamos la columna 1 o 2 (índice 0 o 1) que suele ser el nombre completo
            # Intentamos detectar:
            nombres = []
            for col in df.columns:
                # Si la columna tiene strings largos, es probable que sea la de nombres
                sample = df[col].dropna().head(10).astype(str)
                if sample.str.len().mean() > 10:
                    nombres = df[col].dropna().apply(limpiar_nombre).tolist()
                    # Filtramos filas que parezcan encabezados o metadatos
                    blacklist = ["NOMBRE", "LISTA", "RELIGIÓN", "BÁSICA", "CARRILLO", "BELTRÁN", "CARVAJAL", "IGNACIO", "1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°"]
                    nombres = [n for n in nombres if not any(word in n.upper() for word in blacklist) and len(n) > 5]
                    break
            
            if nombres:
                curso_key = archivo.replace(".xlsx", "").replace("°", "_basico")
                resultados[curso_key] = nombres
                print(f"✅ Extraídos {len(nombres)} estudiantes de {archivo}")
            else:
                print(f"❌ No se detectaron nombres en {archivo}")
                
        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump({"listas_estudiantes": resultados}, f, allow_unicode=True, sort_keys=False)
    print(f"\n📁 Archivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    extraer_listas()
