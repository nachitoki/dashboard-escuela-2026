"""POC: Genera UNA clase con el motor actualizado para ver las secciones de materiales"""
import time, os
from generador_clases import GeneradorClases, CURSOS

motor = GeneradorClases()

# Probar con 3° Básico Patrimonio (tiene tarjetas y fotos)
curso_id = "3basico"
curso_info = CURSOS[curso_id]
tema = "La memoria de nuestra escuela Aonikenk"
objetivo = "Identificar el espacio escolar como lugar de encuentro y memoria."
unidad = "Unidad 1: Identidad y Territorio"

print("=== TEST: Generando 3° Básico Patrimonio con materiales contextuales ===")
m = motor.ensamblar_clase("Patrimonio", unidad, 1, curso_id, tema, objetivo)
motor.guardar_clase(m, "Patrimonio", curso_id, 1)

print("\n=== TEST: Generando 3° Básico Religión con fichas bíblicas ===")
time.sleep(4)
m2 = motor.ensamblar_clase("Religión", "Unidad 0: Fundamentos (Resumen)", 1, curso_id,
    "Los grandes amigos de Dios: Abraham y Moisés",
    "Repasar la historia de la Antigua Alianza como preparación para conocer a Cristo.")
motor.guardar_clase(m2, "Religion", curso_id, 1)

print("\n✅ Archivos generados. Revisa las nuevas secciones al final de cada .md")
