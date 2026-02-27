import time
from generador_clases import GeneradorClases, CURSOS

motor = GeneradorClases()

# Tema raíz compartido por ciclo, pero la IA diferenciará por curso
temas_patrimonio = {
    "primer_ciclo": {"tema": "Yo y mi familia: ¿De dónde vengo?", "objetivo": "Reconocer a los miembros de la familia como primer entorno patrimonial.", "unidad": "Unidad 1: Identidad y Territorio"},
    "segundo_ciclo": {"tema": "La memoria de nuestra escuela Aonikenk", "objetivo": "Identificar el espacio escolar como lugar de encuentro y memoria.", "unidad": "Unidad 1: Identidad y Territorio"},
    "tercer_ciclo": {"tema": "El barrio que habitamos y sus relatos", "objetivo": "Mapear los hitos locales y espacios comunitarios de importancia histórica.", "unidad": "Unidad 1: Identidad y Territorio"},
    "cuarto_ciclo": {"tema": "Identidad local: Raíces profundas de nuestra ciudad", "objetivo": "Analizar críticamente el concepto de territorio y pertenencia cultural.", "unidad": "Unidad 1: Identidad y Territorio"},
}

temas_religion = {
    "primer_ciclo": {"tema": "Dios nos creó por Amor y nos dio un Ángel de la Guarda", "objetivo": "Recordar la belleza de la Creación y la protección divina constante.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "segundo_ciclo": {"tema": "Los grandes amigos de Dios: Abraham y Moisés", "objetivo": "Repasar la historia de la Antigua Alianza como preparación para conocer a Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "tercer_ciclo": {"tema": "La caída de Adán y Eva y la Promesa infalible del Salvador", "objetivo": "Comprender el pecado original y la necesidad absoluta de un Redentor.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
    "cuarto_ciclo": {"tema": "Los Diez Mandamientos como camino de verdadera libertad y santidad", "objetivo": "Repasar el Decálogo a la luz de la Ley Natural y su cumplimiento en Cristo.", "unidad": "Unidad 0: Fundamentos (Resumen)"},
}

SEMANA = 1

print("=" * 60)
print("  FÁBRICA DE PLANIFICACIONES - SEMANA 1 (MARZO)")
print("  16 archivos: 8 cursos × 2 asignaturas")
print("=" * 60)

# Generar Patrimonio (8 cursos)
print("\n📗 PATRIMONIO (Unidad 1: Identidad y Territorio)")
print("-" * 50)
for curso_id, curso_info in CURSOS.items():
    ciclo_key = curso_info["ciclo_key"]
    datos = temas_patrimonio[ciclo_key]
    print(f"\n🔸 {curso_info['grado']}:")
    time.sleep(3)
    m = motor.ensamblar_clase("Patrimonio", datos["unidad"], SEMANA, curso_id, datos["tema"], datos["objetivo"])
    motor.guardar_clase(m, "Patrimonio", curso_id, SEMANA)

# Generar Religión (8 cursos)
print("\n\n📕 RELIGIÓN (Unidad 0: Fundamentos)")
print("-" * 50)
for curso_id, curso_info in CURSOS.items():
    ciclo_key = curso_info["ciclo_key"]
    datos = temas_religion[ciclo_key]
    print(f"\n🔸 {curso_info['grado']}:")
    time.sleep(4)  # Rate limit
    m = motor.ensamblar_clase("Religión", datos["unidad"], SEMANA, curso_id, datos["tema"], datos["objetivo"])
    motor.guardar_clase(m, "Religión", curso_id, SEMANA)

print("\n" + "=" * 60)
print("  ✅ GENERACIÓN COMPLETADA: 16 archivos")
print("=" * 60)
