import time, os
from generador_clases import GeneradorClases, CURSOS

motor = GeneradorClases()

temas_religion = {
    "primer_ciclo": {"tema": "Dios nos creo por Amor y nos dio un Angel de la Guarda", "objetivo": "Recordar la belleza de la Creacion y la proteccion divina constante.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "segundo_ciclo": {"tema": "Los grandes amigos de Dios: Abraham y Moises", "objetivo": "Repasar la historia de la Antigua Alianza como preparacion para conocer a Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "tercer_ciclo": {"tema": "La caida de Adan y Eva y la Promesa infalible del Salvador", "objetivo": "Comprender el pecado original y la necesidad absoluta de un Redentor.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "cuarto_ciclo": {"tema": "Los Diez Mandamientos como camino de verdadera libertad y santidad", "objetivo": "Repasar el Decalogo a la luz de la Ley Natural y su cumplimiento en Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
}

# Verificar cuales ya existen
from pathlib import Path
OUTPUT_DIR = Path(__file__).parent / "Outputs"

cursos_faltantes = []
for curso_id in CURSOS:
    archivo = OUTPUT_DIR / f"S1_REL_{curso_id}.md"
    if not archivo.exists():
        cursos_faltantes.append(curso_id)

if not cursos_faltantes:
    print("Todos los archivos de Religion ya existen!")
else:
    print(f"Faltan {len(cursos_faltantes)} archivos de Religion: {cursos_faltantes}")
    for curso_id in cursos_faltantes:
        curso_info = CURSOS[curso_id]
        ciclo_key = curso_info["ciclo_key"]
        datos = temas_religion[ciclo_key]
        print(f"\n{curso_info['grado']}:")
        time.sleep(4)
        m = motor.ensamblar_clase("Religion", datos["unidad"], 1, curso_id, datos["tema"], datos["objetivo"])
        motor.guardar_clase(m, "Religion", curso_id, 1)

print("\nSincronizando a GDrive...")
import sync_gdrive
sync_gdrive.sync_to_gdrive()
