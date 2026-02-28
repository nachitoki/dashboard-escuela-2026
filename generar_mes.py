import time
import os
from generador_clases import GeneradorClases, CURSOS

motor = GeneradorClases()

# Planificación Mensual de Marzo (4 semanas)
# Estructura: ciclo -> asignatura -> lista de 4 semanas [tema, objetivo]
PLAN_MARZO = {
    "primer_ciclo": {
        "Patrimonio": [
            ["Yo y mi familia: ¿De dónde vengo?", "Reconocer a los miembros de la familia como primer entorno patrimonial."],
            ["Mi casa: Mi primer territorio", "Identificar espacios significativos en el hogar."],
            ["El camino a la escuela: Paisajes cotidianos", "Observar elementos del entorno en el trayecto diario."],
            ["Mi escuela Aonikenk: Nuestra casa común", "Identificar la escuela como espacio de pertenencia."]
        ],
        "Religión": [
            ["Dios nos creó por Amor", "Reconocer la vida como un regalo divino."],
            ["El jardín de la Creación", "Identificar la naturaleza como obra de Dios."],
            ["Mi Ángel de la Guarda", "Comprender la protección divina constante."],
            ["La gran familia de Dios", "Valorar la comunidad cristiana."]
        ]
    },
    "segundo_ciclo": {
        "Patrimonio": [
            ["La memoria de nuestra escuela Aonikenk", "Identificar el espacio escolar como lugar de encuentro y memoria."],
            ["Héroes y leyendas de nuestro barrio", "Conocer relatos locales significativos."],
            ["Objetos con historia: Mi tesoro familiar", "Valorar el patrimonio material doméstico."],
            ["Mapeando mi comunidad", "Crear un mapa básico de hitos locales."]
        ],
        "Religión": [
            ["Los grandes amigos de Dios: Abraham", "Conocer la fe del padre de los creyentes."],
            ["Moisés y la liberación", "Identificar a Dios como libertador de su pueblo."],
            ["La Alianza en el Sinaí", "Comprender el compromiso entre Dios y el hombre."],
            ["Preparando el camino a Jesús", "Relacionar el AT con el cumplimiento en Cristo."]
        ]
    },
    # Tercer y Cuarto ciclo seguirán el mismo patrón...
    "tercer_ciclo": {
        "Patrimonio": [
            ["El barrio que habitamos y sus relatos", "Mapear los hitos locales y espacios comunitarios."],
            ["Arquitectura local: Estilos y transformaciones", "Observar la evolución del entorno construido."],
            ["Oficios tradicionales de la zona", "Identificar saberes locales en riesgo de desaparecer."],
            ["Archivos y fotos: El pasado en el presente", "Analizar fuentes primarias de la historia local."]
        ],
        "Religión": [
            ["La caída y la Promesa de Salvador", "Comprender el pecado original y la esperanza."],
            ["Profetas: La voz de Dios en el mundo", "Identificar el rol de los profetas."],
            ["Juan el Bautista: El precursor", "Conocer la figura que anuncia al Mesías."],
            ["La Anunciación: El 'Sí' de María", "Valorar la obediencia de fe en la Virgen."]
        ]
    },
    "cuarto_ciclo": {
        "Patrimonio": [
            ["Identidad local: Raíces profundas", "Analizar críticamente el concepto de territorio."],
            ["Conflictos y acuerdos en nuestra historia", "Debatir sobre hitos históricos locales."],
            ["Patrimonio Inmaterial: Lenguaje y costumbres", "Valorar expresiones culturales vivas."],
            ["Gestión del Patrimonio: ¿Cómo protegemos lo nuestro?", "Identificar roles ciudadanos en la conservación."]
        ],
        "Religión": [
            ["Los Mandamientos: Camino de libertad", "Repasar el Decálogo como camino de vida."],
            ["Justicia y Caridad en los profetas", "Relacionar la fe con el compromiso social."],
            ["La Ley Natural y la Ley Divina", "Discernir fundamentos éticos universales."],
            ["Cristo: Plenitud de la Ley y la Libertad", "Comprender la Gracia como motor de santidad."]
        ]
    }
}

def generar_vertical(mes_nombre="Marzo"):
    print("=" * 60)
    print(f"  GENERACIÓN VERTICAL - MES DE {mes_nombre.upper()}")
    print("=" * 60)

    for curso_id, curso_info in CURSOS.items():
        ciclo = curso_info["ciclo_key"]
        print(f"\n🚀 PROCESANDO CURSO: {curso_info['grado']} ({ciclo})")
        print("-" * 50)
        
        for semana_idx in range(4):
            semana = semana_idx + 1
            print(f"  Semana {semana}:")
            
            # Patrimonio
            pat_tema, pat_obj = PLAN_MARZO[ciclo]["Patrimonio"][semana_idx]
            print(f"    📗 Patrimonio: {pat_tema}")
            m_pat = motor.ensamblar_clase("Patrimonio", "Unidad 1: Identidad y Territorio", semana, curso_id, pat_tema, pat_obj)
            motor.guardar_clase(m_pat, "Patrimonio", curso_id, semana)
            
            # Religión
            rel_tema, rel_obj = PLAN_MARZO[ciclo]["Religión"][semana_idx]
            print(f"    📕 Religión: {rel_tema}")
            m_rel = motor.ensamblar_clase("Religión", "Unidad 0/1", semana, curso_id, rel_tema, rel_obj)
            motor.guardar_clase(m_rel, "Religión", curso_id, semana)
            
            time.sleep(2) # Respetar tasa de la API

    print("\n✅ Generación Vertical Completada.")

if __name__ == "__main__":
    generar_vertical()
