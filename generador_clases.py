import os
import yaml
from pathlib import Path

# Required: pip install google-genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Por favor, instala: pip install google-genai")
    exit(1)

# Rutas
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "Outputs"
MATERIALES_DIR = OUTPUT_DIR / "Materiales"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MATERIALES_DIR, exist_ok=True)

# Mapeo de cursos a ciclos con sus características específicas
CURSOS = {
    "1basico": {"grado": "1° Básico", "edad": "6-7 años", "ciclo_key": "primer_ciclo",
                "diferenciador": "Actividades concretas: dibujar, colorear, cantar, escuchar cuentos. Frases muy cortas. Vocabulario simple."},
    "2basico": {"grado": "2° Básico", "edad": "7-8 años", "ciclo_key": "primer_ciclo",
                "diferenciador": "Ya lee y escribe oraciones cortas. Puede copiar del pizarrón. Actividades con escritura guiada y narración oral más extensa."},
    "3basico": {"grado": "3° Básico", "edad": "8-9 años", "ciclo_key": "segundo_ciclo",
                "diferenciador": "Inicio de trabajo grupal simple (parejas). Lectura de textos cortos. Preguntas dirigidas con opciones."},
    "4basico": {"grado": "4° Básico", "edad": "9-10 años", "ciclo_key": "segundo_ciclo",
                "diferenciador": "Trabajo en equipos de 3-4. Mapas conceptuales simples. Redacción de párrafos cortos. Mayor autonomía lectora."},
    "5basico": {"grado": "5° Básico", "edad": "10-11 años", "ciclo_key": "tercer_ciclo",
                "diferenciador": "Investigación guiada con preguntas. Exposiciones breves. Inicio de pensamiento abstracto. Trabajo con líneas de tiempo."},
    "6basico": {"grado": "6° Básico", "edad": "11-12 años", "ciclo_key": "tercer_ciclo",
                "diferenciador": "Investigación con mayor autonomía. Debates simples. Redacción de textos argumentativos básicos. Co-evaluación entre pares."},
    "7basico": {"grado": "7° Básico", "edad": "12-13 años", "ciclo_key": "cuarto_ciclo",
                "diferenciador": "Pensamiento crítico inicial. Análisis de fuentes. Ensayos cortos. Debates estructurados. Conexión con actualidad."},
    "8basico": {"grado": "8° Básico", "edad": "13-14 años", "ciclo_key": "cuarto_ciclo",
                "diferenciador": "Pensamiento hipotético-deductivo. Ensayos argumentativos. Proyectos autónomos. Filosofía y ética aplicada. Preparación para Media."},
}

class GeneradorClases:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️ ADVERTENCIA: No se encontró GEMINI_API_KEY en las variables de entorno.")
            print("El motor funcionará en modo 'MOCK' (simulación) para estructuras, sin IA.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            
        self.cargar_configuraciones()

    def cargar_configuraciones(self):
        with open(BASE_DIR / "config_anual.yml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)["config"]
            
        with open(BASE_DIR / "ciclos.yml", "r", encoding="utf-8") as f:
            self.ciclos = yaml.safe_load(f)["ciclos"]
            
        with open(BASE_DIR / "prompt_religion_tradicional.md", "r", encoding="utf-8") as f:
            self.prompt_sistema = f.read()
            
        with open(BASE_DIR / "plantilla_clase.md", "r", encoding="utf-8") as f:
            self.plantilla_base = f.read()

        with open(BASE_DIR / "personas.yml", "r", encoding="utf-8") as f:
            self.personas = yaml.safe_load(f)["personas"]

        # Memoria Central (Roadmap)
        with open(BASE_DIR / "ROADMAP.yml", "r", encoding="utf-8") as f:
            self.roadmap = f.read()

    def generar_actividad_religion_gemini(self, tema, curso_info):
        """Llama a Gemini 2.5 para crear el Desarrollo de la clase tipo Disputatio"""
        grado = curso_info["grado"]
        edad = curso_info["edad"]
        diferenciador = curso_info["diferenciador"]
        
        if not self.client:
            return f"**[MOCK]** Desarrollo generado por IA para: {tema}\nCurso: {grado}\nEstructura: Videtur quod... Sed contra... Respondeo..."

        prompt_usuario = f"""
        Actúa como instruye tu System Prompt.
        
        TEMA DE LA CLASE: {tema}
        CURSO ESPECÍFICO: {grado} ({edad}).
        CARACTERÍSTICAS DEL CURSO: {diferenciador}
        TIEMPO DE LA ACTIVIDAD: 50 minutos.

        CONTEXTO ESTRATÉGICO (ROADMAP):
        {self.roadmap}
        
        Genera SOLO el contenido de la sección 'Desarrollo' aplicando el modelo de la Disputatio (Videtur quod, Sed contra, Respondeo). 
        
        IMPORTANTE: Adecua TOTALMENTE el lenguaje, las actividades y la profundidad al nivel específico de {grado} ({edad}).
        - Las explicaciones deben ser comprensibles para un niño de {edad}.
        - Las actividades prácticas deben corresponder a lo que un alumno de {grado} puede hacer: {diferenciador}
        - Mantén la profundidad escolástica pero tradúcela al nivel cognitivo real del curso.
        """
        
        try:
            print(f"  🧠 Gemini → {grado}: {tema}...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=self.prompt_sistema,
                    temperature=0.3,
                ),
            )
            result = response.text
            return result if result else f"[Contenido filtrado por seguridad. Tema: {tema} para {grado}]"
        except Exception as e:
            print(f"  ❌ Error con Gemini API: {e}")
            return f"Error en generación: {e}"

    def generar_actividad_patrimonio_gemini(self, tema, curso_info):
        """Genera actividad de Patrimonio diferenciada por curso"""
        grado = curso_info["grado"]
        edad = curso_info["edad"]
        diferenciador = curso_info["diferenciador"]
        
        if not self.client:
            return f"**Actividad de Patrimonio para {grado}:** {tema}\n\nActividad ABP diferenciada para {edad}: {diferenciador}"

        prompt_usuario = f"""
        Eres un pedagogo experto en Aprendizaje Basado en Proyectos (ABP) y patrimonio cultural local.
        
        TEMA DE LA CLASE: {tema}
        CURSO ESPECÍFICO: {grado} ({edad}).
        CARACTERÍSTICAS DEL CURSO: {diferenciador}
        TIEMPO DE LA ACTIVIDAD: 50 minutos.
        CONTEXTO ESTRATÉGICO (ROADMAP):
        {self.roadmap}
        CONTEXTO GEOGRÁFICO: Escuela rural en la Patagonia chilena. Identidad Aonikenk. 
        
        Genera SOLO el contenido de la sección 'Desarrollo' con metodología ABP.
        
        Estructura tu respuesta así:
        1. **Exploración inicial** (10 min): Actividad de observación o pregunta detonante.
        2. **Investigación / Creación** (25 min): Actividad central diferenciada para {grado}.
        3. **Puesta en común** (15 min): Socialización del trabajo.
        
        IMPORTANTE: Las actividades deben ser realizables por un alumno de {edad}: {diferenciador}
        """
        
        try:
            print(f"  🧠 Gemini → {grado}: {tema}...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                ),
            )
            result = response.text
            return result if result else f"[Contenido filtrado. Tema: {tema} para {grado}]"
        except Exception as e:
            print(f"  ❌ Error con Gemini API: {e}")
            return f"Error en generación: {e}"

    def generar_materiales(self, actividad_desarrollo, asignatura, tema, curso_info):
        """Genera lista de materiales con contexto + fichas auto-generadas"""
        grado = curso_info["grado"]
        if not self.client:
            return "", "Biblia (Straubinger), cuaderno, pizarra."
        
        prompt = f"""
        Eres un asistente pedagógico. Analiza esta actividad de clase y genera DOS secciones:

        ACTIVIDAD DE LA CLASE:
        {actividad_desarrollo[:2000]}
        
        ASIGNATURA: {asignatura}
        TEMA: {tema}
        CURSO: {grado}

        SECCIÓN 1 - TAREAS DEL DOCENTE (cosas que el profesor debe hacer antes de la clase):
        Lista específica y contextualizada. NO digas "fotografías" a secas. Di exactamente QUÉ fotografías y cuántas.
        Formato: una línea por tarea, comenzando con emoji + descripción concreta.
        Ejemplo: 📷 Imprimir 3 fotografías antiguas de la escuela Aonikenk (se pueden buscar en el archivo escolar)
        Ejemplo: 🖨️ Fotocopiar 15 guías de trabajo (la guía se encuentra adjunta en esta planificación)
        Ejemplo: 📱 Asegurar cámara o celular con batería para bitácora fotográfica

        SECCIÓN 2 - MATERIAL AUTO-GENERADO (fichas, rúbricas, pautas que se adjuntan):
        Si la actividad menciona tarjetas, fichas, guías, rúbricas o pasajes bíblicos, GENERA EL CONTENIDO COMPLETO listo para imprimir.
        {'Para pasajes bíblicos, cita el texto completo de la traducción de Mons. Straubinger.' if asignatura.lower() == 'religión' else ''}
        Formatea cada ficha/material como un bloque claro con título, contenido y formato imprimible.
        Si la actividad usa tarjetas, genera las tarjetas exactas con su contenido.
        Si la actividad necesita una rúbrica de evaluación, genera la rúbrica completa.
        Si no hay materiales que auto-generar, escribe: "No se requiere material adicional."

        RESPONDE EXACTAMENTE EN ESTE FORMATO:
        ---TAREAS_DOCENTE---
        (lista de tareas)
        ---MATERIAL_GENERADO---
        (fichas/rúbricas/pautas completas)
        """
        
        try:
            print(f"  📦 Materiales → {grado}...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2),
            )
            result = response.text if response.text else ""
            
            # Parsear las dos secciones
            tareas = ""
            material_generado = ""
            if "---TAREAS_DOCENTE---" in result and "---MATERIAL_GENERADO---" in result:
                parts = result.split("---MATERIAL_GENERADO---")
                tareas = parts[0].replace("---TAREAS_DOCENTE---", "").strip()
                material_generado = parts[1].strip()
            else:
                tareas = result
            
            return tareas, material_generado
        except Exception as e:
            print(f"  ⚠️ Error en materiales: {e}")
            return "", ""

    def ensamblar_clase(self, asignatura, unidad, semana, curso_id, tema, objetivo):
        curso_info = CURSOS[curso_id]
        ciclo_key = curso_info["ciclo_key"]
        ciclo_data = self.ciclos[ciclo_key]
        grado = curso_info["grado"]
        
        # 1. Generar contenido adaptado por curso
        if asignatura.lower() == "religión":
            actividad_desarrollo = self.generar_actividad_religion_gemini(tema, curso_info)
            mbe_A, mbe_B, mbe_C, mbe_D = "x", "x", "x", " " 
        else:
            actividad_desarrollo = self.generar_actividad_patrimonio_gemini(tema, curso_info)
            mbe_A, mbe_B, mbe_C, mbe_D = "x", " ", "x", "x"

        # 2. Generar materiales con contexto
        import time
        time.sleep(2)  # Rate limit
        tareas_docente, material_generado = self.generar_materiales(
            actividad_desarrollo, asignatura, tema, curso_info
        )

        # 3. Reemplazar tags en la plantilla
        clase_md = self.plantilla_base
        clase_md = clase_md.replace("{{asignatura}}", f"{asignatura.capitalize()} — {grado}")
        clase_md = clase_md.replace("{{nombre_unidad}}", unidad)
        clase_md = clase_md.replace("{{ciclo_nombre}}", f"{grado} ({ciclo_data['nombre']})")
        clase_md = clase_md.replace("{{numero_semana}}", str(semana))
        clase_md = clase_md.replace("{{pregunta_esencial}}", f"¿Cómo comprendemos el misterio de {tema}?")
        clase_md = clase_md.replace("{{objetivo_clase}}", objetivo)
        
        clase_md = clase_md.replace("{{actividad_inicio}}", "Oración inicial (ciclo litúrgico) y recuerdo de la clase anterior.")
        clase_md = clase_md.replace("{{pregunta_inicio}}", f"¿Qué sabemos sobre {tema}?")
        
        clase_md = clase_md.replace("{{actividad_desarrollo}}", actividad_desarrollo)
        clase_md = clase_md.replace("{{tipo_agrupacion}}", "Individual y plenario.")
        clase_md = clase_md.replace("{{materiales_necesarios}}", "Ver sección Materiales abajo.")
        
        clase_md = clase_md.replace("{{actividad_cierre}}", "Síntesis en la pizarra de la verdad enseñada.")
        clase_md = clase_md.replace("{{instruccion_evidencia}}", ciclo_data["evidencia_bitacora"][0] if isinstance(ciclo_data["evidencia_bitacora"], list) else ciclo_data["evidencia_bitacora"])
        clase_md = clase_md.replace("{{tipo_evaluacion}}", "Formativa (participación y bitácora)")
        
        clase_md = clase_md.replace("{{mbe_A}}", mbe_A)
        clase_md = clase_md.replace("{{mbe_B}}", mbe_B)
        clase_md = clase_md.replace("{{mbe_C}}", mbe_C)
        clase_md = clase_md.replace("{{mbe_D}}", mbe_D)

        # 4. Añadir secciones de materiales al final
        if tareas_docente:
            clase_md += f"\n\n---\n\n## ✋ Tareas del Docente (preparar antes de la clase)\n\n{tareas_docente}\n"
        
        if material_generado and "No se requiere" not in material_generado:
            clase_md += f"\n\n---\n\n## 🖨️ Material Auto-Generado (listo para imprimir)\n\n{material_generado}\n"

        return clase_md

    def guardar_clase(self, contenido, asignatura, curso_id, semana):
        nombre_base = f"S{semana}_{asignatura[:3].upper()}_{curso_id}"
        nombre_archivo = f"{nombre_base}.md"
        ruta = OUTPUT_DIR / nombre_archivo
        
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"  ✅ Guardado: {nombre_archivo}")

        # Si hay material generado, guardarlo aparte también
        if "## 🖨️ Material Auto-Generado" in contenido:
            try:
                partes = contenido.split("## 🖨️ Material Auto-Generado")
                material_only = partes[1].strip()
                
                # Crear encabezado para el archivo de material
                header_material = f"# MATERIAL DE TRABAJO - {asignatura.upper()}\n"
                header_material += f"**Curso:** {CURSOS[curso_id]['grado']} | **Semana:** {semana}\n"
                header_material += f"**Tema:** {nombre_base}\n\n---\n\n"
                
                ruta_mat = MATERIALES_DIR / f"MAT_{nombre_base}.md"
                with open(ruta_mat, "w", encoding="utf-8") as fmat:
                    fmat.write(header_material + material_only)
                print(f"  📦 Material guardado: MAT_{nombre_base}.md")
            except Exception as e:
                print(f"  ⚠️ Error guardando material separado: {e}")

if __name__ == "__main__":
    print("--- MOTOR DE GENERACIÓN 2026 (por curso) ---")
    print("Usa lote_marzo.py para generar en lote.")
