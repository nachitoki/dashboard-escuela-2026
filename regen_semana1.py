"""Regenera TODAS las clases de Semana 1 con el motor mejorado (materiales contextuales)"""
import time, os
from generador_clases import GeneradorClases, CURSOS

motor = GeneradorClases()

temas_patrimonio = {
    "primer_ciclo": {"tema": "Yo y mi familia en la Patagonia", "objetivo": "Reconocer la propia identidad y la de su familia dentro del territorio patagonico.", "unidad": "Unidad 1: Identidad y Territorio"},
    "segundo_ciclo": {"tema": "La memoria de nuestra escuela Aonikenk", "objetivo": "Identificar el espacio escolar como lugar de encuentro y memoria.", "unidad": "Unidad 1: Identidad y Territorio"},
    "tercer_ciclo": {"tema": "El barrio y sus relatos: voces de la comunidad", "objetivo": "Investigar relatos orales del entorno cercano para valorar la memoria comunitaria.", "unidad": "Unidad 1: Identidad y Territorio"},
    "cuarto_ciclo": {"tema": "Raices profundas: quienes habitaron antes que nosotros", "objetivo": "Analizar las raices culturales y territoriales de la identidad local.", "unidad": "Unidad 1: Identidad y Territorio"},
}

temas_religion = {
    "primer_ciclo": {"tema": "Dios nos creo por Amor y nos dio un Angel de la Guarda", "objetivo": "Recordar la belleza de la Creacion y la proteccion divina constante.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "segundo_ciclo": {"tema": "Los grandes amigos de Dios: Abraham y Moises", "objetivo": "Repasar la historia de la Antigua Alianza como preparacion para conocer a Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "tercer_ciclo": {"tema": "La caida de Adan y Eva y la Promesa infalible del Salvador", "objetivo": "Comprender el pecado original y la necesidad absoluta de un Redentor.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "cuarto_ciclo": {"tema": "Los Diez Mandamientos como camino de verdadera libertad y santidad", "objetivo": "Repasar el Decalogo a la luz de la Ley Natural y su cumplimiento en Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
}

total = len(CURSOS) * 2
count = 0

for curso_id in CURSOS:
    curso_info = CURSOS[curso_id]
    ciclo_key = curso_info["ciclo_key"]
    
    # Patrimonio
    datos_pat = temas_patrimonio[ciclo_key]
    count += 1
    print(f"\n[{count}/{total}] Patrimonio - {curso_info['grado']}:")
    time.sleep(3)
    m = motor.ensamblar_clase("Patrimonio", datos_pat["unidad"], 1, curso_id, datos_pat["tema"], datos_pat["objetivo"])
    motor.guardar_clase(m, "Patrimonio", curso_id, 1)
    
    # Religion
    datos_rel = temas_religion[ciclo_key]
    count += 1
    print(f"\n[{count}/{total}] Religion - {curso_info['grado']}:")
    time.sleep(3)
    m2 = motor.ensamblar_clase("Religion", datos_rel["unidad"], 1, curso_id, datos_rel["tema"], datos_rel["objetivo"])
    motor.guardar_clase(m2, "Religion", curso_id, 1)

print(f"\n{'='*50}")
print(f"OK {total} planificaciones regeneradas con materiales contextuales")

# Regenerar dashboard y sincronizar
print("\nRegenerando dashboard...")
import subprocess
subprocess.run(["py", "generar_dashboard.py"], check=True)

print("\nSincronizando a GDrive...")
import sync_gdrive
sync_gdrive.sync_to_gdrive()

print("\nPublicando en GitHub...")
os.chdir("Outputs")
os.system('git add -A && git commit -m "S1 completa con materiales contextuales" && git push')
print("\nTODO LISTO!")
