import os
import shutil
from pathlib import Path

# Paths
LOCAL_OUTPUTS_DIR = r"C:\Users\Dr Pixel Pc\.gemini\antigravity\brain\5f4bf7f0-5c0d-4876-beba-68002e23f044\Sistema_2026\Outputs"
GDRIVE_DIR = r"e:\Mi unidad\2026 Clases\Planificaciones\INSTRUMENTOS RECTORES ESCUELA AONIKENK 2026\Outputs_Sistema"

def sync_to_gdrive():
    try:
        if not os.path.exists(LOCAL_OUTPUTS_DIR):
            print(f"Directorio local no existe: {LOCAL_OUTPUTS_DIR}")
            return
            
        os.makedirs(GDRIVE_DIR, exist_ok=True)
        
        count = 0
        for root, dirs, files in os.walk(LOCAL_OUTPUTS_DIR):
            for file in files:
                local_path = os.path.join(root, file)
                # Calcular ruta relativa para mantener estructura
                rel_path = os.path.relpath(local_path, LOCAL_OUTPUTS_DIR)
                target_path = os.path.join(GDRIVE_DIR, rel_path)
                
                # Crear directorios si es necesario
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Copiar archivo (sobreescribe)
                shutil.copy2(local_path, target_path)
                print(f"Copiado: {rel_path} a GDrive")
                count += 1
                
        print(f"\n✅ Sincronización exitosa: {count} archivos copiados a GDrive.")
        print(f"Ruta GDrive: {GDRIVE_DIR}")
        
    except Exception as e:
        print(f"❌ Error sincronizando: {e}")

if __name__ == "__main__":
    sync_to_gdrive()
