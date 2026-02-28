import time
import os
import sys

# Asegurar que el directorio actual esté en el path para importar generador_clases
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generador_clases import GeneradorClases, CURSOS

# Clase especializada con los datos de NotebookLM
class FabricaSemana1(GeneradorClases):
    def __init__(self):
        super().__init__()
        # Inyectamos el contexto de NotebookLM obtenido en la sesión
        self.context_pat = {
            "primer_ciclo": "Historia sobre el esfuerzo de las familias de Puerto Ibáñez en 1920 (ladrillos de barro y greda).",
            "segundo_ciclo": "Fundación de la Escuela Aonikenk en 1920 por los padres para evitar que sus hijos se fueran del pueblo. Ladrillos artesanales y madera de troncos.",
            "tercer_cuarto": "Significado de 'Aonikenk' = Gente del Sur (Tehuelches). Conexión profunda con el territorio patagónico y la historia de los gigantes del sur."
        }
        self.context_rel = {
            "primer_ciclo": "OA 1 (Dios nos crea a su imagen - Gen 1,26-27). Foco en el Amor como motor de la vida.",
            "segundo_ciclo": "OA 5 (Personajes que responden al Amor de Dios). Abraham como modelo de respuesta fiel y obediencia.",
            "tercer_cuarto": "OA 8 (La Libertad cristiana). Los Mandamientos no como reglas, sino como camino liberador para elegir el bien."
        }

    def generar_material_pro(self, asignatura, curso_id):
        curso_info = CURSOS[curso_id]
        ciclo = curso_info["ciclo_key"]
        grado = curso_info["grado"]
        
        # Seleccionar contexto
        if asignatura == "Patrimonio":
            if ciclo == "primer_ciclo": ctx = self.context_pat["primer_ciclo"]
            elif ciclo == "segundo_ciclo": ctx = self.context_pat["segundo_ciclo"]
            else: ctx = self.context_pat["tercer_cuarto"]
        else: # Religión
            if ciclo == "primer_ciclo": ctx = self.context_rel["primer_ciclo"]
            elif ciclo == "segundo_ciclo": ctx = self.context_rel["segundo_ciclo"]
            else: ctx = self.context_rel["tercer_cuarto"]

        prompt = f"""
        Actúa como el experto pedagogo del ROADMAP y tus System Prompts.
        
        ASIGNATURA: {asignatura}
        CURSO: {grado}
        SEMANA: 1 (Inicio de Clases)
        
        CONTEXTO DE INVESTIGACIÓN (NotebookLM):
        {ctx}
        
        TAREA: Genera el material didáctico 'ALTA INVERSIÓN' para esta clase.
        DEBE INCLUIR:
        1. **Un Relato o Texto Motivador** (basado en el contexto de NotebookLM).
        2. **Una Ficha de Trabajo / Actividad** (acorde a {curso_info['diferenciador']}). Especialmente: Matriz de Análisis Patrimonial para Patrimonio, o Preguntas de Reflexión para Religión.
        3. **Instrumento de Evaluación** (Rúbrica simple o Lista de cotejo).
        
        Usa un lenguaje cálido pero profesional.
        """
        
        if not self.client:
            return f"**[MOCK MATERIAL]** {asignatura} s1 {grado}\nContexto: {ctx}"

        try:
            print(f"  🏭 Fabricando Material ({asignatura}) para {grado}...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'temperature': 0.5}
            )
            return response.text
        except Exception as e:
            return f"Error: {e}"

def fabricar():
    fab = FabricaSemana1()
    
    clases_semana_1 = [
        ("Religion", "4basico"),
        ("Patrimonio", "3basico"),
        ("Religion", "5basico"),
        ("Patrimonio", "1basico"),
        ("Patrimonio", "2basico"),
        ("Religion", "7basico"),
        ("Patrimonio", "5basico"),
        ("Religion", "8basico"),
        ("Religion", "6basico")
    ]
    
    os.makedirs(os.path.join("Outputs", "Materiales"), exist_ok=True)
    
    print("="*60)
    print("🚀 FÁBRICA DE MATERIAL - SEMANA 1 (4 AL 6 MARZO)")
    print("="*60)

    for asig, curso_id in clases_semana_1:
        material = fab.generar_material_pro(asig, curso_id)
        
        # Guardar en archivo físico
        filename = f"MAT_S1_{asig[:3].upper()}_{curso_id}.md"
        filepath = os.path.join("Outputs", "Materiales", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Material Didáctico — {asig} ({CURSOS[curso_id]['grado']})\n")
            f.write(f"**Semana:** 1 (4-6 Marzo) | **Estado:** ALTA INVERSIÓN\n\n")
            f.write(material)
            
        print(f"  ✅ Generado: {filename}")
        time.sleep(1)

    print("\n✅ Fábrica de Semana 1 completada.")

if __name__ == "__main__":
    fabricar()
