import json
import random
import re
import streamlit as st
from groq import Groq

# ==============================================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==============================================================
st.set_page_config(
    page_title="Alquimia Lírica Pro",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==============================================================
# 2. BANCO DE HISTORIAS HUMANAS COTIDIANAS (SEMILLAS ANCLA)
# ==============================================================
IDEAS_COTIDIANAS = [
    ("Descubrí que me mentías al revisar fotos viejas donde ya mirabas a otra persona.", 75),
    ("El silencio incómodo en el auto cuando ambos sabemos que esto ya se terminó.", 50),
    ("Te perdono no porque lo merezcas, sino porque mi paz mental no es negociable.", 350),
    ("La ansiedad de ver tu nombre en 'en línea' sabiendo que ya no es a mí a quien le escribes.", 100),
    ("Fui yo quien arruinó la relación por miedo a que descubrieras quién soy de verdad.", 30),
    ("Tiradera elegante: tu traición no me destruyó, me volvió exitoso e inalcanzable.", 150),
    ("Verte en brazos de otro y tragarme las ganas de gritar en medio de la fiesta.", 125),
    ("Toqué fondo en el piso de mi cuarto y entendí que nadie vendría a salvarme excepto yo.", 200),
    ("La culpa de haber sido quien empacó las maletas sin darte una última explicación.", 30),
    ("Un amor cotidiano y sano: bailar descalzos en la cocina mientras se calienta el café.", 500),
    ("Borrar tu número de memoria para no llamarte ebrio a las tres de la mañana.", 125),
    ("La felicidad explosiva de caminar por la calle sabiendo que por fin dejé de extrañarte.", 540),
    ("La calma absoluta de mirar la lluvia sabiendo que las heridas ya cerraron.", 600),
    ("Estar rodeado de gente en una discoteca y sentirme en el vacío más absoluto.", 50),
    ("Agradecerte el tiempo juntos, desearte lo mejor y cerrar la puerta con una sonrisa.", 350),
]

# ==============================================================
# 3. MAPA DE CONCIENCIA DE HAWKINS (EMOCIÓN Y VIRALIDAD)
# ==============================================================
HAWKINS_SCALE = {
    20: {
        "nombre": "Vergüenza (20)",
        "emocion": "Humillación / Desprecio",
        "viralidad": "84%",
        "color": "#7f1d1d",
        "psicologia": "Vulnerabilidad extrema, confesar lo innombrable, catarsis de lo oculto."
    },
    30: {
        "nombre": "Culpa (30)",
        "emocion": "Remordimiento / Castigo",
        "viralidad": "89%",
        "color": "#991b1b",
        "psicologia": "Baladas desgarradoras de arrepentimiento, deudas morales y perdón tardío."
    },
    50: {
        "nombre": "Apatía (50)",
        "emocion": "Desesperanza / Indiferencia",
        "viralidad": "80%",
        "color": "#9a3412",
        "psicologia": "Nihilismo urbano, canciones 'sad', vacío existencial compartido."
    },
    75: {
        "nombre": "Pena / Duelo (75)",
        "emocion": "Tristeza / Pérdida",
        "viralidad": "94%",
        "color": "#c2410c",
        "psicologia": "Duelo universal, despedidas inevitables (Efecto Adele)."
    },
    100: {
        "nombre": "Miedo (100)",
        "emocion": "Ansiedad / Amenaza",
        "viralidad": "91%",
        "color": "#b45309",
        "psicologia": "Paranoia, terror al abandono, la zozobra de quedarse solo."
    },
    125: {
        "nombre": "Deseo / Apego (125)",
        "emocion": "Lujuria / Obsesión",
        "viralidad": "97%",
        "color": "#a16207",
        "psicologia": "Amor tóxico, sensualidad insaciable, adicción a una persona (Trap / Urbano)."
    },
    150: {
        "nombre": "Ira / Rabia (150)",
        "emocion": "Resentimiento / Venganza",
        "viralidad": "99%",
        "color": "#dc2626",
        "psicologia": "Tiraderas viscerales, despecho furioso, cobrar traiciones (Efecto Shakira / BZRP)."
    },
    175: {
        "nombre": "Orgullo (175)",
        "emocion": "Superioridad / Egolatría",
        "viralidad": "95%",
        "color": "#e11d48",
        "psicologia": "Flexing, presumir logros, 'nadie creía en mí' (Hip Hop / Corridos)."
    },
    200: {
        "nombre": "Coraje (200) [Umbral]",
        "emocion": "Valentía / Determinación",
        "viralidad": "93%",
        "color": "#16a34a",
        "psicologia": "Himnos de superación personal, levantarse tras la caída (Efecto Rocky)."
    },
    250: {
        "nombre": "Neutralidad (250)",
        "emocion": "Confianza / Desapego",
        "viralidad": "82%",
        "color": "#0d9488",
        "psicologia": "Cero drama, fluir con la vida, madurez emocional despreocupada."
    },
    310: {
        "nombre": "Voluntad (310)",
        "emocion": "Optimismo / Enfoque",
        "viralidad": "88%",
        "color": "#0284c7",
        "psicologia": "Mentalidad imparable, disciplina de hierro, fe en el proceso."
    },
    350: {
        "nombre": "Aceptación (350)",
        "emocion": "Perdón / Trascendencia",
        "viralidad": "92%",
        "color": "#2563eb",
        "psicologia": "Cierre de ciclos en paz, soltar rencores, reconciliación íntima."
    },
    400: {
        "nombre": "Razón / Sabiduría (400)",
        "emocion": "Claridad / Discernimiento",
        "viralidad": "85%",
        "color": "#4f46e5",
        "psicologia": "Rap consciente, metáforas reflexivas, disección psicológica de las relaciones."
    },
    500: {
        "nombre": "Amor Incondicional (500)",
        "emocion": "Compasión / Reverencia",
        "viralidad": "96%",
        "color": "#7c3aed",
        "psicologia": "Himnos atemporales de amor que erizan la piel (Coldplay, Bob Marley)."
    },
    540: {
        "nombre": "Alegría Serena (540)",
        "emocion": "Éxtasis / Celebración",
        "viralidad": "97%",
        "color": "#c026d3",
        "psicologia": "Euforia de vivir, fiesta contagiosa, liberación pura ('Happy', Funk)."
    },
    600: {
        "nombre": "Paz / Unidad (600)",
        "emocion": "Serenidad / Trascendencia",
        "viralidad": "78%",
        "color": "#059669",
        "psicologia": "Trascendencia, silencio sonoro, trance pacífico y unificación espiritual."
    }
}

# ==============================================================
# 4. GESTIÓN DE SESIÓN Y MEMORIA PERSISTENTE
# ==============================================================
ESTADOS_INICIALES = {
    "texto_input": "",
    "historia_base": "",
    "slider_hawkins": 500,
    "analisis_hawkins": None,
    "letra_trans_es": None,
    "letra_trans_en": None,
    "guia_produccion": None
}
for key, val in ESTADOS_INICIALES.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Clave de API por defecto desde secrets
api_key_default = ""
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key_default = st.secrets["GROQ_API_KEY"].strip()
except Exception:
    pass

# ==============================================================
# 5. MOTOR GROQ OPTIMIZADO (DETECCIÓN DINÁMICA SIN CACHÉ CORRUPTA)
# ==============================================================
def get_groq_client(api_key: str):
    return Groq(api_key=api_key.strip())

def resolver_modelos_groq(client):
    """Consulta en tiempo real los modelos disponibles para tu API Key"""
    try:
        todos = [m.id for m in client.models.list().data]
        chat_models = [
            m for m in todos 
            if not any(x in m.lower() for x in ["whisper", "guard", "audio", "orpheus", "embed", "tts", "stt", "vision", "safeguard"])
        ]
        preferentes = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
        disponibles = [p for p in preferentes if p in chat_models]
        if disponibles:
            return disponibles
        elif chat_models:
            return chat_models
    except Exception:
        pass
    return ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]

def llamar_groq_dinamico(client, mensajes, temperature=0.6, json_mode=False):
    modelos = resolver_modelos_groq(client)
    kwargs = {
        "messages": mensajes,
        "temperature": temperature,
        "max_tokens": 4096,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    ultimo_err = None
    for mod in modelos:
        try:
            kwargs["model"] = mod
            res = client.chat.completions.create(**kwargs)
            return res.choices[0].message.content, mod
        except Exception as e:
            ultimo_err = e
            continue
    raise Exception(f"Falla con los modelos disponibles ({modelos}): {ultimo_err}")

def parsear_json_limpio(texto: str) -> dict:
    t = texto.strip()
    if t.startswith("```json"):
        t = t[7:]
    elif t.startswith("```"):
        t = t[3:]
    if t.endswith("```"):
        t = t[:-3]
    return json.loads(t.strip())

# ==============================================================
# 6. MODULADOR HAWKINS EN VIVO (TRANSMUTADOR DE SEMILLA)
# ==============================================================
def transmutar_semilla_rapida(texto_base: str, frecuencia_num: int, api_key: str) -> str:
    """Reescribe la frase del cajón según la frecuencia de Hawkins seleccionada"""
    if not api_key.strip() or not texto_base.strip():
        return texto_base
    try:
        client = get_groq_client(api_key)
        frec_info = HAWKINS_SCALE.get(frecuencia_num, HAWKINS_SCALE[500])
        prompt = f"""Reescribe esta premisa para reflejar de forma directa y emocional la frecuencia de {frec_info['nombre']} (Emoción: {frec_info['emocion']}).
Conserva la situación y personajes, pero adapta la actitud y sentimiento al nivel indicado.
Responde ÚNICAMENTE con la frase reescrita en 1 o 2 oraciones cotidianas y directas, sin comillas ni explicaciones adicionales.

PREMISA BASE:
"{texto_base}" """

        res, _ = llamar_groq_dinamico(
            client,
            [{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return res.strip().replace('"', '').replace('\n', ' ')
    except Exception:
        return texto_base

# ==============================================================
# 7. COMPOSICIÓN MUSICAL ROBUSTA CON REGEX
# ==============================================================
def calibrar_hawkins_json(letra_o_idea: str, api_key: str) -> dict:
    client = get_groq_client(api_key)
    prompt = f"""Eres un analista experto en psicología musical y en el Mapa de Conciencia de David R. Hawkins (Power vs. Force).
Analiza el siguiente texto de canción o temática:
\"\"\"{letra_o_idea}\"\"\"

Responde OBLIGATORIAMENTE en un objeto JSON con estas llaves exactas:
{{
    "frecuencia": "Nombre de la emoción y puntaje Hawkins (ej: Ira / Resentimiento (150 puntos))",
    "viralidad": "Porcentaje 0-100% y explicación concisa de por qué conecta psicológicamente con las masas",
    "patron": "1 frase que sintetiza la herida emocional, el apego o conflicto del texto",
    "elevacion": "Frecuencia sugerida para transmutar la canción hacia un estado superior",
    "clave": "Concepto central para lograr la redención o soberanía emocional"
}}"""

    res, _ = llamar_groq_dinamico(
        client,
        [{"role": "system", "content": "Responde estrictamente en JSON válido."},
         {"role": "user", "content": prompt}],
        temperature=0.2,
        json_mode=True
    )
    return parsear_json_limpio(res)

def componer_cancion_dual(
    texto_base: str,
    frecuencia_num: int,
    modo_estilo: str,
    estructura_tipo: str,
    perspectiva_pov: str,
    rima_esquema: str,
    genero_ritmo: str,
    rango_silabas: tuple,
    api_key: str
):
    client = get_groq_client(api_key)
    frec_info = HAWKINS_SCALE.get(frecuencia_num, HAWKINS_SCALE[500])
    min_sil, max_sil = rango_silabas

    if "Simple" in modo_estilo:
        estilo_instruccion = (
            "ESTILO LÍRICO SIMPLE (COLOQUIAL / POP URBANO DIRECTO):\n"
            "- Usa lenguaje común, callejero, de conversación real o audio de WhatsApp.\n"
            "- Cero palabras pretenciosas o rebuscadas. Frases contundentes y memorables.\n"
            "- Imágenes directas que cualquier persona comprende de inmediato."
        )
    else:
        estilo_instruccion = (
            "ESTILO LÍRICO DESCRIPTIVO (POÉTICO / CINEMATOGRÁFICO):\n"
            "- Desarrolla imágenes sensoriales ricas: texturas, olores, temperaturas, objetos físicos tangibles.\n"
            "- Metáforas cinematográficas profundas y elegancia lírica.\n"
            "- Construye una atmósfera visual densa que erice la piel sin perder el ritmo cantable."
        )

    if "Simple" in estructura_tipo:
        estructura_instruccion = (
            "ARQUITECTURA MUSICAL SIMPLE:\n"
            "[Verse 1]\n\n[Chorus]\n\n[Verse 2]\n\n[Chorus]\n\n[Bridge]\n\n[Chorus]\n\n[Outro]\n"
            "(Separa rigurosamente cada bloque con doble salto de línea)."
        )
    else:
        estructura_instruccion = (
            "ARQUITECTURA MUSICAL AVANZADA (HITMAKER POP FORMAT):\n"
            "[Verse 1]: Escena inicial y conflicto.\n\n"
            "[Pre-Chorus]: Tensión creciente de 2 a 4 versos que anticipan el estallido.\n\n"
            "[Chorus]: El clímax armónico, gancho memorable y contundente.\n\n"
            "[Post-Chorus]: Gancho rítmico con palabra clave del coro repetida + arreglo vocal de 2 líneas con ad-libs entre paréntesis.\n\n"
            "[Verse 2]: Evolución lírica de la historia.\n\n"
            "[Pre-Chorus]: Cohesión melódica (mismo motivo y frases clave del primer Pre-Coro).\n\n"
            "[Chorus]: Gancho central repetido.\n\n"
            "[Bridge]: Quiebre armónico y de tempo, máxima vulnerabilidad o revelación.\n\n"
            "[Chorus Final]: Explosión catártica con ad-libs vocales sugeridos entre paréntesis.\n\n"
            "[Outro]: Desvanecimiento lírico o remate contundente.\n"
            "(Separa rigurosamente cada bloque con doble salto de línea)."
        )

    prompt = f"""Eres un galardonado compositor musical, letrista de élite y productor discográfico.

MISIÓN:
Compón una canción completa con impacto radial basada en las siguientes coordenadas técnicas:
- TEMA O HISTORIA BASE: "{texto_base}"
- FRECUENCIA DE HAWKINS OBJETIVO: {frec_info['nombre']} (Emoción: {frec_info['emocion']}).
- GÉNERO Y CADENCIA RÍTMICA: {genero_ritmo}.
- PERSPECTIVA NARRATIVA (POV): {perspectiva_pov}.
- ESQUEMA DE RIMA: {rima_esquema}.

REGLAS DE ORO OBLIGATORIAS:
1. CONTROL MÉTRICO DE SÍLABAS (ISOSILABISMO):
   - Cada verso (línea) DEBE tener rigurosamente entre {min_sil} y {max_sil} sílabas métricas reales (tomando en cuenta sinalefas naturales del español).
   - Prohibido hacer versos cortos recortados (menos de {min_sil} sílabas) o versos largos en prosa (más de {max_sil} sílabas).
   - Toda la canción debe mantener una cadencia musical simétrica que encaje perfectamente en el compás rítmico.

2. PROHIBICIÓN ABSOLUTA DE RIMA IDÉNTICA O EPÍFORA:
   - Está TERMINANTEMENTE PROHIBIDO terminar dos o más versos con la misma palabra (como repetir la palabra '{frec_info['emocion'].split()[0]}' o cualquier otra al final de las líneas).
   - Cada verso DEBE terminar en una palabra diferente con rimas consonantes o asonantes ricas en español (ejemplo: canción / perdón, herida / vida, olvido / herido).
   - La frecuencia de Hawkins es la ATMÓSFERA EMOCIONAL y psicológica del texto, NUNCA una palabra que debas escribir al final de las líneas.

{estilo_instruccion}

{estructura_instruccion}

REQUISITOS DE FORMATO OBLIGATORIOS:
Devuelve ÚNICAMENTE los 3 bloques separados por estos títulos exactos:
===ESPAÑOL===
[Aquí la letra completa en español]
===INGLES===
[Aquí la adaptación cantable al inglés con rima equivalente]
===PRODUCCION===
[BPM, Escala musical, Instrumentos y notas de interpretación]"""

    salida_cruda, mod_usado = llamar_groq_dinamico(
        client,
        [{"role": "user", "content": prompt}],
        temperature=0.6
    )

    # EXTRACCIÓN ROBUSTA MEDIANTE REGEX
    patron_es = re.search(r'===\s*ESPA?Ñ?OL\s*===\s*(.*?)(?====\s*INGL[EÉ]S\s*===|\Z)', salida_cruda, re.DOTALL | re.IGNORECASE)
    patron_en = re.search(r'===\s*INGL[EÉ]S\s*===\s*(.*?)(?====\s*PRODUCCI[OÓ]N\s*===|\Z)', salida_cruda, re.DOTALL | re.IGNORECASE)
    patron_prod = re.search(r'===\s*PRODUCCI[OÓ]N\s*===\s*(.*)', salida_cruda, re.DOTALL | re.IGNORECASE)

    es_txt = patron_es.group(1).strip() if patron_es else salida_cruda.strip()
    en_txt = patron_en.group(1).strip() if patron_en else "Versión en inglés integrada en la generación principal."
    prod_txt = patron_prod.group(1).strip() if patron_prod else f"Estilo sugerido: {genero_ritmo} | Métrica: {min_sil}-{max_sil} sílabas"

    return es_txt, en_txt, prod_txt, mod_usado

# ==============================================================
# 8. BARRA LATERAL (CONFIGURACIÓN & RESET)
# ==============================================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    groq_api_key_input = st.text_input(
        "Groq API Key:",
        value=api_key_default,
        type="password",
        placeholder="gsk_..."
    )
    
    api_key_activa = groq_api_key_input.strip() or api_key_default

    if api_key_activa:
        st.success("🟢 API Key activa")
    else:
        st.warning("Pega tu clave gratis de console.groq.com")

    st.markdown("---")
    st.markdown("### 📘 Sobre Hawkins en la Música")
    st.caption(
        "Las frecuencias bajas (<200) conectan por catarsis y desahogo masivo. "
        "Las frecuencias altas (200-600) crean himnos atemporales de redención y trascendencia."
    )

    if st.button("🗑️ Limpiar todo el taller"):
        for k, v in ESTADOS_INICIALES.items():
            st.session_state[k] = v
        st.rerun()

# ==============================================================
# 9. PANEL PRINCIPAL: EL LIENZO DE COMPOSICIÓN & ANÁLISIS
# ==============================================================
st.title("🎵 Alquimia Lírica Pro")
st.caption("Composición musical de élite, resonancia viral de Hawkins y métrica silábica")

col_top_a, col_top_b = st.columns([2, 1])
with col_top_a:
    st.markdown("#### ✍️ Lienzo de Creación")
with col_top_b:
    if st.button("🎲 Sorpréndeme con una Idea", help="Genera una historia humana y sincroniza la emoción con Hawkins"):
        idea_sel, frec_sel = random.choice(IDEAS_COTIDIANAS)
        st.session_state["historia_base"] = idea_sel
        st.session_state["slider_hawkins"] = frec_sel
        
        if api_key_activa:
            with st.spinner("Creando semilla emocional..."):
                frase_mutada = transmutar_semilla_rapida(idea_sel, frec_sel, api_key_activa)
                st.session_state["texto_input"] = frase_mutada
        else:
            st.session_state["texto_input"] = idea_sel
        st.rerun()

# CAJÓN PRINCIPAL MULTIFUNCIÓN (Sin callbacks que bloqueen el botón)
texto_actual = st.text_area(
    "Pega aquí una letra existente (para analizar) O escribe tu idea / historia cotidiana:",
    value=st.session_state["texto_input"],
    height=130,
    placeholder="Ej: Empaqué mis cosas y salí sin decir nada... o pega los versos de una canción completa..."
)
st.session_state["texto_input"] = texto_actual
if texto_actual.strip() and not st.session_state["historia_base"]:
    st.session_state["historia_base"] = texto_actual.strip()

# ==============================================================
# 10. CONTROLES DE COMPOSICIÓN & CONFIGURADOR DE SÍLABAS
# ==============================================================
st.markdown("##### 🎛️ Dirección Artística & Estructura")
col_estilo, col_estruct, col_pov = st.columns(3)

with col_estilo:
    modo_estilo_sel = st.selectbox(
        "Estilo Lírico:",
        options=["Simple (Cotidiano / Pop Directo)", "Descriptivo (Poético / Cinematográfico)"],
        index=0
    )

with col_estruct:
    estructura_sel = st.selectbox(
        "Arquitectura Musical:",
        options=["Avanzada Hitmaker (Con Pre/Post-Coro)", "Simple (Verso - Coro - Puente)"],
        index=0
    )

with col_pov:
    narrativa_pov_sel = st.selectbox(
        "Perspectiva (Punto de Vista):",
        options=[
            "1ª Persona ('Yo' - Íntimo / Confesional)",
            "2ª Persona ('Tú' - Confrontación / Carta abierta)",
            "3ª Persona ('Él / Ella' - Crónica / Testigo)",
            "Mixto / Diálogo ('Tú y Yo' - Conversacional)",
            "Omnisciente ('Voz Universal' - Filosófico)"
        ],
        index=0
    )

col_silabas, col_ajustes = st.columns([1, 1])

with col_silabas:
    rango_silabas_sel = st.slider(
        "📏 Métrica por verso (Rango de sílabas):",
        min_value=5,
        max_value=16,
        value=(7, 12),
        step=1,
        help="Fuerza a cada línea a mantenerse entre este mínimo y máximo de sílabas para una cuadratura musical perfecta."
    )

with col_ajustes:
    rima_sel = st.selectbox(
        "Esquema de Rima:",
        options=["ABAB (Alterna pop / Dinámica)", "AABB (Pareado clásico)", "ABCB (Balada tradicional)", "AAAA (Monorrima contundente)"],
        index=0
    )

with st.expander("🎼 Género Musical y Cadencia"):
    genero_sel = st.selectbox(
        "Estilo Instrumental Sugerido:",
        options=[
            "Pop Urbano / Reggaetón Comercial",
            "Balada Acústica / Pop Emocional",
            "Indie Rock / Pop Alternativo",
            "Trap / Hip Hop Consciente",
            "R&B Contemporáneo / Soul",
            "Corrido Tumbado / Regional"
        ],
        index=0
    )

# ==============================================================
# 11. ESCALA DE VIBRACIÓN HAWKINS INTERACTIVA (MODULADOR EN VIVO)
# ==============================================================
st.markdown("---")
st.markdown("##### 🎚️ Nivel de Resonancia Hawkins (Modulador de Emoción)")

frec_seleccionada = st.select_slider(
    "Mueve el slider para modular la emoción en tiempo real:",
    options=list(HAWKINS_SCALE.keys()),
    value=st.session_state["slider_hawkins"],
    format_func=lambda x: HAWKINS_SCALE[x]["nombre"]
)

# Sincronización limpia al mover el slider sin romper los botones
if frec_seleccionada != st.session_state["slider_hawkins"]:
    st.session_state["slider_hawkins"] = frec_seleccionada
    base = st.session_state["historia_base"].strip() or st.session_state["texto_input"].strip()
    if base and api_key_activa:
        with st.spinner("Modulando emoción de la historia..."):
            frase_adaptada = transmutar_semilla_rapida(base, frec_seleccionada, api_key_activa)
            st.session_state["texto_input"] = frase_adaptada
            st.rerun()

info_frec = HAWKINS_SCALE[frec_seleccionada]

st.markdown(
    f"""<div style="background-color: #0b1120; border-left: 6px solid {info_frec['color']}; padding: 12px 16px; border-radius: 8px; margin-bottom: 12px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
    <h4 style="margin: 0; color: #ffffff;">{info_frec['nombre']}</h4>
    <span style="background-color: {info_frec['color']}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 13px; font-weight: bold;">
        🔥 Viralidad estimada: {info_frec['viralidad']}
    </span>
</div>
<p style="margin: 4px 0; color: #94a3b8; font-size: 13px;"><b>Campo Emocional:</b> {info_frec['emocion']}</p>
<p style="margin: 0; color: #38bdf8; font-size: 13px;"><b>Conexión Psicológica:</b> {info_frec['psicologia']}</p>
</div>""",
    unsafe_allow_html=True
)

# ==============================================================
# 12. BOTONES MAESTROS DE ACCIÓN
# ==============================================================
col_btn_cal, col_btn_comp = st.columns([1, 1])

with col_btn_cal:
    btn_analizar = st.button("🔍 Analizar / Calibrar Letra", use_container_width=True)

with col_btn_comp:
    btn_componer = st.button("✨ Componer / Transmutar Canción", type="primary", use_container_width=True)

# LÓGICA DE ACCIÓN 1: ANALIZAR LETRA
if btn_analizar:
    texto_a_evaluar = st.session_state["texto_input"].strip()
    if not api_key_activa:
        st.error("⚠️ Falta la Groq API Key. Ingrésala en la barra lateral izquierda.")
    elif not texto_a_evaluar:
        st.warning("Escribe o pega una letra en el cajón superior para calibrarla.")
    else:
        with st.spinner("Calibrando frecuencia y potencial viral con Groq..."):
            try:
                diag = calibrar_hawkins_json(texto_a_evaluar, api_key_activa)
                st.session_state["analisis_hawkins"] = diag
            except Exception as e:
                st.error(f"Error al analizar la letra: {e}")

# LÓGICA DE ACCIÓN 2: COMPONER CANCIÓN
if btn_componer:
    texto_base = st.session_state["texto_input"].strip()
    if not api_key_activa:
        st.error("⚠️ Falta la Groq API Key. Ingrésala en la barra lateral izquierda.")
    elif not texto_base:
        st.warning("Escribe una idea en el cajón o haz clic en '🎲 Sorpréndeme con una Idea'.")
    else:
        with st.spinner(f"Componiendo ({modo_estilo_sel}, métrica de {rango_silabas_sel[0]}-{rango_silabas_sel[1]} sílabas)..."):
            try:
                es_letra, en_letra, guia_prod, modelo_usado = componer_cancion_dual(
                    texto_base=texto_base,
                    frecuencia_num=frec_seleccionada,
                    modo_estilo=modo_estilo_sel,
                    estructura_tipo=estructura_sel,
                    perspectiva_pov=narrativa_pov_sel,
                    rima_esquema=rima_sel,
                    genero_ritmo=genero_sel,
                    rango_silabas=rango_silabas_sel,
                    api_key=api_key_activa
                )
                st.session_state["letra_trans_es"] = es_letra
                st.session_state["letra_trans_en"] = en_letra
                st.session_state["guia_produccion"] = guia_prod
                st.toast(f"¡Composición completada con éxito usando {modelo_usado}!")
            except Exception as e:
                st.error(f"Error en el motor de composición: {e}")

# ==============================================================
# 13. MUESTRA DE RESULTADOS: DIAGNÓSTICO HAWKINS
# ==============================================================
if st.session_state.get("analisis_hawkins"):
    diag = st.session_state["analisis_hawkins"]
    st.markdown("---")
    st.markdown(
        f"""<div style="background: linear-gradient(135deg, #090d16 0%, #1e1b4b 60%, #311042 100%); border-left: 6px solid #fb7185; padding: 18px 22px; border-radius: 12px; margin: 15px 0;">
<h4 style="margin: 0 0 10px 0; color: #fb7185;">📊 Diagnóstico de la Letra: <span style="color: #ffffff; text-decoration: underline;">{diag.get('frecuencia')}</span></h4>
<p style="margin: 5px 0; color: #38bdf8; font-size: 14px;"><b>🔥 Potencial Viral:</b> {diag.get('viralidad')}</p>
<p style="margin: 5px 0; color: #e2e8f0; font-size: 14px;"><b>⚠️ Conflicto / Patrón Detectado:</b> {diag.get('patron')}</p>
<p style="margin: 5px 0; color: #34d399; font-size: 14px;"><b>✨ Frecuencia de Elevación Recomendada:</b> {diag.get('elevacion')}</p>
<p style="margin: 5px 0; color: #c084fc; font-size: 14px;"><b>🔑 Clave de Transmutación Poética:</b> {diag.get('clave')}</p>
</div>""",
        unsafe_allow_html=True
    )

# ==============================================================
# 14. MUESTRA DE RESULTADOS: CANCIONES GENERADAS (DUAL TAB)
# ==============================================================
if st.session_state.get("letra_trans_es"):
    st.markdown("---")
    st.success(f"🎉 ¡Canción compuesta con éxito! Métrica estricta de {rango_silabas_sel[0]} a {rango_silabas_sel[1]} sílabas.")

    tab_es, tab_en, tab_prod = st.tabs([
        "🇪🇸 Versión en Español (Lírica Ritmada)",
        "🇺🇸 English Trans-Adaptation (Rhymed & Singable)",
        "🎛️ Guía de Producción & Metatags"
    ])

    with tab_es:
        st.caption("Usa el icono en la esquina superior derecha del recuadro para copiar:")
        st.code(st.session_state["letra_trans_es"], language="markdown")

    with tab_en:
        st.caption("Adaptación cantable en inglés que conserva la métrica silábica y el esquema de rima:")
        st.code(st.session_state.get("letra_trans_en", ""), language="markdown")

    with tab_prod:
        st.caption("Metatags y guía técnica de producción (BPM, tonalidad y notas para el vocalista):")
        st.code(st.session_state.get("guia_produccion", ""), language="yaml")
