import os
import yaml
import docx
import re
from pathlib import Path

try:
    from google import genai
except ImportError:
    print("Por favor instala: pip install google-genai python-docx")
    exit(1)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "Outputs" / "Generadas_2026"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Contexto Extraído desde NotebookLM (Caché local para evitar llamadas extra al MCP)
CONTEXTO_REGLAS_NOTEBOOKLM = """
[CONTEXTO DE NOTEBOOKLM - PROGRAMAS DE RELIGIÓN Y PATRIMONIO AONIKENK 2026]
EJES CURRICULARES (1° a 8° BÁSICO):
- Naturaleza y cultura: El ser humano cuida la 'casa común'. (Especialmente en Patrimonio: Huerto local, identidad).
- Persona y sociedad: Promover convivencia, dignidad y bien común.
- Espiritualidad: Búsqueda de sentido, mensaje de Jesucristo.
ENFOQUE DIDÁCTICO:
- Aprendizaje Tridimensional: Integrar conocimientos, habilidades y actitudes.
- Pedagogía de Jesús como modelo: Encuentro personal, diálogo abierto.
- Razón religiosa y cordial: Superar lo meramente cognitivo. Sentido de la realidad.
- En Patrimonio: Fomentar el orgullo por la cultura tehuelche/aonikenk, historia local de la escuela y saberes ancestrales de la región.
VALORES: Dignidad humana, Cuidado de la Casa Común, Inclusión, Fraternidad.
"""

class GeneradorAonikenk:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️ ADVERTENCIA: No se encontró GEMINI_API_KEY. Operando en modo Mock/Simulación.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

        self.cargar_prompts()

    def cargar_prompts(self):
        workflows_dir = BASE_DIR / ".agents" / "workflows"
        with open(workflows_dir / "prompt_maestro_planificaciones.md", "r", encoding="utf-8") as f:
            self.prompt_planificacion = f.read()
        
        with open(workflows_dir / "prompt_maestro_fichas.md", "r", encoding="utf-8") as f:
            self.prompt_fichas = f.read()

        with open(BASE_DIR / "ROADMAP.yml", "r", encoding="utf-8") as f:
            self.roadmap = yaml.safe_load(f)

    def guardar_docx(self, markdown_text, filename):
        doc = docx.Document()
        for line in markdown_text.split('\n'):
            if line.startswith('# '):
                doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:], level=3)
            elif line.startswith('- '):
                doc.add_paragraph(line[2:], style='List Bullet')
            elif line.startswith('> '):
                doc.add_paragraph(line[2:], style='Quote')
            elif re.match(r'^\d+\.\s', line):
                doc.add_paragraph(line[line.find(' ')+1:], style='List Number')
            else:
                if line.strip():
                    doc.add_paragraph(line.strip())
        doc.save(filename)
        print(f"📄 Guardado DOCX: {filename.name}")

    def guardar_archivos(self, asignatura, curso, semana, contenido_plan, contenido_ficha):
        # Crear estructura de carpetas tipo Google Drive
        ruta_curso = OUTPUT_DIR / asignatura / f"{curso}_{asignatura}" / f"{curso}_{asignatura}_Clase{semana}"
        os.makedirs(ruta_curso, exist_ok=True)

        # Guardar Planificacion
        base_name_plan = f"Clase {semana} {asignatura} {curso} - 2026"
        with open(ruta_curso / f"{base_name_plan}.md", "w", encoding="utf-8") as f:
            f.write(contenido_plan)
        self.guardar_docx(contenido_plan, ruta_curso / f"{base_name_plan}.docx")

        # Guardar Ficha si existe
        if contenido_ficha and len(contenido_ficha.strip()) > 50:
            base_name_ficha = f"Guia {semana} {asignatura} {curso} - 2026"
            with open(ruta_curso / f"{base_name_ficha}.md", "w", encoding="utf-8") as f:
                f.write(contenido_ficha)
            self.guardar_docx(contenido_ficha, ruta_curso / f"{base_name_ficha}.docx")

    def generar_clase(self, asignatura, curso, semana, tema_especifico):
        print(f"\n🚀 Generando Clase: {asignatura} | {curso} | Semana {semana}")
        
        system_instructions_plan = f"{CONTEXTO_REGLAS_NOTEBOOKLM}\n{self.prompt_planificacion}"
        system_instructions_ficha = f"{CONTEXTO_REGLAS_NOTEBOOKLM}\n{self.prompt_fichas}"

        prompt_usuario = f"""
        Debes planificar la Semana {semana} de la asignatura de {asignatura} para el curso {curso}.
        Tema central para esta semana: {tema_especifico}
        Recuerda aplicar obligatoriamente la regla del Objetivo (Taxonomía + Qué + Cómo) y adecuar la didáctica para la edad de los niños.
        """

        if not self.client:
            print("SIMULACIÓN: Retornando texto mock...")
            plan_final = f"# {asignatura} - Clase {semana}\n**Curso:** {curso}\n## 🎯 Objetivo de la Clase\nComprender {tema_especifico} mediante dibujo."
            ficha_final = f"# 📚 Ficha de Aprendizaje - {curso}\n**Asignatura:** {asignatura}\n\n## 🚀 ¡Manos a la obra!\n_dibuja el texto."
            self.guardar_archivos(asignatura, curso, semana, plan_final, ficha_final)
            return

        print("🧠 IA Planificando la Clase (Modo Pedagógico)...")
        try:
            plan_response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_usuario,
                config={"system_instruction": system_instructions_plan, "temperature": 0.3}
            )
            plan_final = plan_response.text
            
            # Condicional de Ficha según Regla 3 de la propuesta
            texto_minusculas = plan_final.lower()
            if "guía" in texto_minusculas or "ficha" in texto_minusculas or "fotocopia" in texto_minusculas:
                print("✍️ IA Diseñando la Guía Escolar (Modo Copywriter)...")
                ficha_prompt = f"Usando la siguiente planificación, crea la Ficha de Trabajo Estudiantil respetando tus instrucciones maestras:\n{plan_final}"
                ficha_response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=ficha_prompt,
                    config={"system_instruction": system_instructions_ficha, "temperature": 0.6}
                )
                ficha_final = ficha_response.text
            else:
                ficha_final = None

        except Exception as e:
            print(f"❌ Error en API: {e}")
            return

        self.guardar_archivos(asignatura, curso, semana, plan_final, ficha_final)
        print("✅ Generación completada con éxito.")

if __name__ == "__main__":
    generador = GeneradorAonikenk()
    
    # Pruebas Rápidas de la Fase 3
    print("Iniciando Modo Arquitecto - Fábrica de Clases Aonikenk 2026")
    generador.generar_clase("Religión", "2° Básico", "2", "Repaso de Moisés y liberación (Unidad 0)")
