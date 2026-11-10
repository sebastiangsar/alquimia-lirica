import json
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Configuración de página al inicio absoluto
st.set_page_config(page_title="Alquimia Lírica (Hawkins)", page_icon="🎵", layout="centered")

st.title("🎵 Alquimia Lírica")
st.caption("Estructura musical, resonancia viral de Hawkins y transmutación poética rítmica")

# Memoria de sesión limpia y persistente
claves_estado = [
    "letra_esc_orig", "letra_esc_es", "analisis_hawkins", 
    "letra_trans_en", "letra_trans_es"
]
for k in claves_estado:
    if k not in st.session_state:
        st.session_state[k] = None

# Manejo seguro de la API Key
GROQ_API_KEY = ""
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# ==============================================================
# MAPA COMPLETO DE HAWKINS: VIRALIDAD + TEMAS BAJOS Y ALTOS
# ==============================================================
HAWKINS_SCALE = {
    20: {
        "nombre": "Vergüenza (20)",
        "emocion": "Humillación / Desprecio",
        "viralidad": "84%",
        "tipo_viral": "Exposición, vulnerabilidad extrema ('Storytime de lo peor que me pasó').",
        "color": "#7f1d1d",
        "temas_baja": ["El secreto que me avergüenza y nadie sabe", "Sintiéndome la burla de todos", "Escondiéndome del mundo"],
        "temas_alta": ["Perdonarme por haberme fallado", "La humillación que forjó mi carácter", "Digno de existir sin pedir permiso"]
    },
    30: {
        "nombre": "Culpa (30)",
        "emocion": "Remordimiento / Castigo",
        "viralidad": "89%",
        "tipo_viral": "Baladas desgarradoras de arrepentimiento y deudas morales.",
        "color": "#991b1b",
        "temas_baja": ["Fui yo quien arruinó todo", "Cargando con la culpa que me asfixia", "Demasiado tarde para pedir perdón"],
        "temas_alta": ["Soltar la cruz que no me corresponde", "Me perdono por no haber sabido más", "De la culpa nace mi redención"]
    },
    50: {
        "nombre": "Apatía (50)",
        "emocion": "Desesperanza / Indiferencia",
        "viralidad": "80%",
        "tipo_viral": "Canciones 'sad', nihilismo y vacío existencial compartido.",
        "color": "#9a3412",
        "temas_baja": ["Ya nada me importa ni me duele", "El cansancio crónico de existir", "Viendo los días pasar sin sentido"],
        "temas_alta": ["Una chispa en medio de la niebla", "Elegir sentir aunque dé miedo", "Despertar del coma emocional"]
    },
    75: {
        "nombre": "Pena / Duelo (75)",
        "emocion": "Tristeza / Pérdida",
        "viralidad": "94%",
        "tipo_viral": "Duelo compartido, despedidas inevitables (Efecto Adele / Sam Smith).",
        "color": "#c2410c",
        "temas_baja": ["Extrañarte me está matando", "Nuestra casa vacía sin tu voz", "Llorando en la madrugada por ti"],
        "temas_alta": ["Aprender a honrar lo que fue", "Agradecerte el tiempo compartido", "Llevarte en el alma sin dolor"]
    },
    100: {
        "nombre": "Miedo (100)",
        "emocion": "Ansiedad / Amenaza",
        "viralidad": "91%",
        "tipo_viral": "Paranoia, miedo al rechazo, temor a quedarse solo.",
        "color": "#b45309",
        "temas_baja": ["Pánico a que me dejes solo", "La ansiedad que me paraliza el pecho", "Corriendo de mis propios demonios"],
        "temas_alta": ["Abrazar el miedo y avanzar temblando", "La tormenta no me puede quebrar", "Confiar en lo desconocido"]
    },
    125: {
        "nombre": "Deseo / Apego (125)",
        "emocion": "Anhelo / Lujuria / Obsesión",
        "viralidad": "97%",
        "tipo_viral": "Reggaeton, sensualidad insaciable, amor prohibido, ambición (Trap/Urbano).",
        "color": "#a16207",
        "temas_baja": ["Obsesión carnal que me domina", "Tenerte aunque seas un veneno", "Quererlo todo y nunca estar lleno"],
        "temas_alta": ["Atracción consciente y magnética", "Canalizar la pasión en creación pura", "Amor que nutre sin encadenar"]
    },
    150: {
        "nombre": "Ira / Rabia (150)",
        "emocion": "Resentimiento / Venganza",
        "viralidad": "99%",
        "tipo_viral": "Tiraderas brutales, despecho furioso, sed de venganza (Efecto Shakira / BZRP).",
        "color": "#dc2626",
        "temas_baja": ["Tiradera sin piedad contra mi ex", "Que te duela el doble de lo que me dolió", "Ardiendo de furia contra la traición"],
        "temas_alta": ["Convertir la rabia en disciplina de fuego", "Mi mejor venganza es mi éxito rotundo", "Poner límites inquebrantables"]
    },
    175: {
        "nombre": "Orgullo (175)",
        "emocion": "Superioridad / Egolatría",
        "viralidad": "95%",
        "tipo_viral": "Flexing, presumir riqueza y fama, 'nadie creía en mí' (Hip Hop / Corridos).",
        "color": "#e11d48",
        "temas_baja": ["Mírame en la cima y tú abajo", "No necesito de nadie para ganar", "Soy mejor que todos ustedes"],
        "temas_alta": ["Orgullo sano de mis raíces", "Honrar las cicatrices de la victoria", "Celebrar el triunfo con humildad"]
    },
    200: {
        "nombre": "Coraje (200) [Umbral]",
        "emocion": "Valentía / Determinación",
        "viralidad": "93%",
        "tipo_viral": "Himnos de batalla deportiva, levantarse de las cenizas (Efecto Rocky).",
        "color": "#16a34a",
        "temas_baja": ["Gritar aunque me tiemble la voz", "Luchar acorralado contra el mundo", "Dejar la sangre en el intento"],
        "temas_alta": ["Me caigo diez veces y me paro once", "El momento exacto de dar el salto", "Arquitecto de mi propio destino"]
    },
    250: {
        "nombre": "Neutralidad (250)",
        "emocion": "Confianza / Desapego",
        "viralidad": "82%",
        "tipo_viral": "Filosofía 'cero drama', fluir con lo que venga, desapego tranquilo.",
        "color": "#0d9488",
        "temas_baja": ["Me cansé de pelear por tonterías", "Que cada quien haga lo suyo", "Poco me importa lo que opinen"],
        "temas_alta": ["La dulce calma de no reaccionar", "Fluyendo en armonía con el río", "Tranquilidad por encima de la razón"]
    },
    310: {
        "nombre": "Voluntad (310)",
        "emocion": "Optimismo / Disciplina",
        "viralidad": "88%",
        "tipo_viral": "Motivación imparable, disciplina de hierro, mentalidad de crecimiento.",
        "color": "#0284c7",
        "temas_baja": ["Forzar la máquina hasta el límite", "No dormir hasta conseguir la meta", "La obsesión de ganar a toda costa"],
        "temas_alta": ["Disciplina diaria con amor al arte", "Construyendo un legado paso a paso", "Optimismo inquebrantable ante el reto"]
    },
    350: {
        "nombre": "Aceptación (350)",
        "emocion": "Perdón / Trascendencia",
        "viralidad": "92%",
        "tipo_viral": "Cierre de ciclos en paz, reconciliación profunda, sanar el pasado.",
        "color": "#2563eb",
        "temas_baja": ["Aceptar la derrota y soltar", "Reconocer que se terminó el juego", "Firmar la tregua con mi dolor"],
        "temas_alta": ["Te perdono y me libero para siempre", "Cerrar la puerta con gratitud genuina", "Aceptar quién fui para amar quién soy"]
    },
    400: {
        "nombre": "Razón / Sabiduría (400)",
        "emocion": "Claridad / Discernimiento",
        "viralidad": "85%",
        "tipo_viral": "Rap consciente, metáforas filosóficas, juegos de palabras profundos.",
        "color": "#4f46e5",
        "temas_baja": ["Diseccionando la falsedad de la sociedad", "La trampa mental de las masas", "Análisis frío del desamor"],
        "temas_alta": ["Comprender el orden oculto del caos", "Sabiduría destilada en rima pura", "La mente serena que todo lo ve"]
    },
    500: {
        "nombre": "Amor Incondicional (500)",
        "emocion": "Compasión / Reverencia",
        "viralidad": "96%",
        "tipo_viral": "Himnos eternos de amor que erizan la piel (Coldplay, Bob Marley).",
        "color": "#7c3aed",
        "temas_baja": ["Amor que duele de tan inmenso", "Darlo todo sin esperar rescate", "Amar en medio de la tormenta"],
        "temas_alta": ["Amor que no pide nada a cambio", "Sanar al mundo con la mirada", "Encontrarte en los ojos de todos"]
    },
    540: {
        "nombre": "Alegría Serena (540)",
        "emocion": "Éxtasis / Celebración",
        "viralidad": "97%",
        "tipo_viral": "Fiesta contagiosa, felicidad pura de vivir ('Happy', funk, baile sin motivo).",
        "color": "#c026d3",
        "temas_baja": ["Bailar para olvidar las penas", "Locura de euforia desmedida", "Gritar hasta que se vaya el dolor"],
        "temas_alta": ["El milagro glorioso de estar vivos", "Bailar bajo la lluvia sin motivo", "La risa que despierta corazones"]
    },
    600: {
        "nombre": "Paz / Unidad (600)",
        "emocion": "Serenidad / Trascendencia",
        "viralidad": "78%",
        "tipo_viral": "Música contemplativa, silencio sonoro, trance pacífico.",
        "color": "#059669",
        "temas_baja": ["El silencio después de la catástrofe", "Aislarse del ruido del mundo", "La calma de la rendición"],
        "temas_alta": ["El océano de paz dentro del pecho", "Ser uno con el latido cósmico", "La luz infinita que nunca se apaga"]
    }
}

# ==============================================================
# MOTOR GROQ CON ANTI-BUCLE Y REINTENTO DINÁMICO
# ==============================================================
def llamar_groq_seguro(client, mensajes, temperature=0.6, anti_bucle=True):
    candidatos = []
    try:
        modelos_api = [m.id for m in client.models.list().data]
        chat_models = [
            m for m in modelos_api 
            if not any(x in m.lower() for x in ["whisper", "guard", "audio", "orpheus", "embed", "tts", "stt"])
        ]
        candidatos = chat_models
    except Exception:
        pass

    if not candidatos:
        candidatos = [
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-120b", "openai/gpt-oss-20b", 
            "qwen/qwen3.8-27b", "llama-3.1-8b-instant"
        ]

    kwargs = {
        "messages": mensajes,
        "temperature": temperature,
    }
    
    if anti_bucle:
        kwargs["frequency_penalty"] = 0.5
        kwargs["presence_penalty"] = 0.4

    ultimo_error = None
    for mod in candidatos:
        try:
            kwargs["model"] = mod
            res = client.chat.completions.create(**kwargs)
            return res.choices[0].message.content
        except Exception as e:
            ultimo_error = e
            continue

    raise Exception(f"No se pudo conectar con los modelos de Groq: {ultimo_error}")

# BARRA LATERAL
with st.sidebar:
    st.header("⚙️ Configuración")
    if not GROQ_API_KEY:
        GROQ_API_KEY = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
    st.caption("Obtén tu clave gratis en console.groq.com")
    
    if st.button("Limpiar todo"):
        for k in claves_estado:
            st.session_state[k] = None
        st.rerun()

def boton_copiar(texto, id_btn="copiar"):
    if not texto:
        return
    texto_json = json.dumps(texto)
    html_code = f"""
    <button id="{id_btn}" onclick="copiar_{id_btn}()" style="
        background-color: #10b981;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        font-size: 14px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    ">📋 Copiar</button>
    <span id="msg_{id_btn}" style="margin-left: 10px; color: #10b981; font-weight: bold; display: none;">✅ ¡Copiado!</span>

    <script>
    function copiar_{id_btn}() {{
        const text = {texto_json};
        navigator.clipboard.writeText(text).then(() => {{
            const msg = document.getElementById('msg_{id_btn}');
            msg.style.display = 'inline';
            setTimeout(() => {{ msg.style.display = 'none'; }}, 2500);
        }}).catch(err => {{
            alert('Error al copiar: ' + err);
        }});
    }}
    </script>
    """
    components.html(html_code, height=45)

def estructurar_letra_musical(letra_cruda, api_key):
    """Estructura la letra original y genera una adaptación al español que RIME con sentido poético"""
    client = Groq(api_key=api_key)
    instruccion = (
        "Eres un productor y letrista musical de élite. Organiza este texto lírico en bloques musicales formales:\n"
        "[Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Bridge], [Chorus], [Outro].\n"
        "Separa cada bloque con doble salto de línea (\\n\\n). Cada verso en una línea individual."
    )
    letra_orig = llamar_groq_seguro(
        client, 
        [{"role": "system", "content": instruccion}, {"role": "user", "content": letra_cruda}], 
        temperature=0.3
    )

    instruccion_es = (
        "Eres un adaptador lírico y letrista profesional. NO hagas una traducción literal palabra por palabra.\n"
        "Tu misión es hacer una ADAPTACIÓN POÉTICA Y MUSICAL AL ESPAÑOL:\n"
        "1. Adapta las frases para que RIMEN de forma natural y mantengan la métrica y ritmo para cantar.\n"
        "2. Mantén intacto el sentido emocional, el mensaje y las imágenes de la canción original.\n"
        "3. Conserva las etiquetas musicales entre corchetes [Verso 1], [Coro], etc., separadas por doble salto de línea."
    )
    letra_es = llamar_groq_seguro(
        client, 
        [{"role": "system", "content": instruccion_es}, {"role": "user", "content": letra_orig}], 
        temperature=0.4
    )
    return letra_orig, letra_es

def calibrar_hawkins_estructurado(letra_texto, api_key):
    """Analiza directamente la letra del primer cuadro en la escala de Hawkins y su viralidad"""
    client = Groq(api_key=api_key)
    prompt = f"""Eres un analista de psicología musical y del Mapa de Conciencia de David R. Hawkins (Power vs. Force).
Analiza a fondo el texto de la siguiente canción:
\"\"\"{letra_texto}\"\"\"

Determina:
1. Frecuencia vibracional dominante en la escala Hawkins (20 a 600 puntos).
2. Grado de Viralidad y Conexión Emocional (0 a 100%) y el motivo psicológico (por qué conecta con la gente, desahogo, despecho, etc.).
3. Frecuencia Opuesta de Elevación sugerida.
4. Clave de Transmutación (concepto central para elevar el mensaje).

Responde exactamente con líneas que comiencen con estas etiquetas:
FRECUENCIA: [Emoción y puntos]
VIRALIDAD: [Porcentaje 0-100% y explicación breve del fenómeno de conexión/catarsis]
PATRON: [1 frase explicando el dolor, rencor o apego del texto]
ELEVACION: [Nivel de alta frecuencia hacia donde elevar]
CLAVE: [Concepto central de redención o soberanía]"""

    contenido = llamar_groq_seguro(client, [{"role": "user", "content": prompt}], temperature=0.2, anti_bucle=False)
    lineas = contenido.split("\n")
    datos = {
        "frecuencia": "Culpa (30 puntos)", 
        "viralidad": "92% - Muy Alta (Conexión por Catarsis Colectiva)",
        "patron": "Carga de apego o remordimiento en la narrativa.",
        "elevacion": "Aceptación (350) / Amor Incondicional (500)", 
        "clave": "Perdón y soberanía personal"
    }
    for l in lineas:
        if l.startswith("FRECUENCIA:"):
            datos["frecuencia"] = l.replace("FRECUENCIA:", "").strip()
        elif l.startswith("VIRALIDAD:"):
            datos["viralidad"] = l.replace("VIRALIDAD:", "").strip()
        elif l.startswith("PATRON:"):
            datos["patron"] = l.replace("PATRON:", "").strip()
        elif l.startswith("ELEVACION:"):
            datos["elevacion"] = l.replace("ELEVACION:", "").strip()
        elif l.startswith("CLAVE:"):
            datos["clave"] = l.replace("CLAVE:", "").strip()
    return datos

def transmutar_letra_poetica_avanzada(letra_base, frec_num, rima_tipo, modo, tema, api_key):
    """Compone en Español con rima y copywriting, y genera la adaptación en Inglés garantizada con rima métrica"""
    client = Groq(api_key=api_key)
    frec_info = HAWKINS_SCALE.get(frec_num, HAWKINS_SCALE[500])

    if modo == "misma":
        enfoque_prompt = (
            "ENFOQUE: REESCRIBIR LA MISMA HISTORIA EN ESTA FRECUENCIA.\n"
            "- Conserva la situación, la herida y los personajes del tema original.\n"
            f"- Transmútalo hacia el estado vibracional de: {frec_info['nombre']} ({frec_info['emocion']})."
        )
    else:
        enfoque_prompt = (
            f"ENFOQUE: COMPONER CANCIÓN DESDE CERO SOBRE ESTA TEMÁTICA: \"{tema}\".\n"
            f"- Toda la narrativa debe vibrar en el campo de: {frec_info['nombre']} ({frec_info['emocion']})."
        )

    # FASE 1: Componer la letra en ESPAÑOL con rima estricta y copywriting emocional
    prompt_es = f"""Eres un letrista y compositor de élite galardonado.
Tu maestría radica en escribir letras que conmueven profundamente usando LENGUAJE SIMPLE, VISUAL Y COTIDIANO.

{enfoque_prompt}

DIRECTRICES LÍRICAS OBLIGATORIAS:
1. PALABRAS SIMPLES Y HUMANAS: Cero palabras rebuscadas de diccionario. Usa frases reales y coloquiales.
2. IMÁGENES MENTALES SENSORIALES: Incluye objetos reales, miradas, el frío, el teléfono, las calles, lugares concretos. Crea una película en la mente del oyente.
3. ESQUEMA DE RIMA OBLIGATORIO: {rima_tipo}. Cada estrofa debe rimar de forma limpia y musical.
4. ESTRUCTURA: [Verso 1], [Pre-Coro], [Coro], [Verso 2], [Puente], [Coro Final], [Outro].
   Separa cada bloque con doble salto de línea (\\n\\n).

LETRA DE REFERENCIA:
\"\"\"{letra_base}\"\"\"

Devuelve ÚNICAMENTE la letra en Español con sus bloques musicales.
"""
    letra_es = llamar_groq_seguro(client, [{"role": "user", "content": prompt_es}], temperature=0.6, anti_bucle=True)

    # FASE 2: Adaptación poética al INGLÉS (NO LITERAL, adaptando para que rime y mantenga sentido y métrica)
    prompt_en = f"""You are a master lyrical adapter and hit songwriter in English.
Take the following Spanish song lyrics and create a professional, radio-ready ENGLISH LYRICAL ADAPTATION.

CRITICAL RULES (TRANS-ADAPTATION, NOT LITERAL TRANSLATION):
1. DO NOT translate literally word-for-word. Adapt the lyrics into natural, catchy, modern English idioms.
2. PRESERVE THE EMOTIONAL MESSAGE: Keep the exact narrative, emotional impact, and visual imagery.
3. RHYME SCHEME REQUIREMENT: Enforce the rhyme scheme: {rima_tipo} across all stanzas in English. The lines MUST naturally rhyme.
4. SINGABILITY: Match the syllable count and rhythmic cadence so it can be sung over the same musical beat.
5. Keep the exact section tags [Verse 1], [Chorus], etc. separated by double newlines (\\n\\n).

SPANISH SOURCE LYRICS:
\"\"\"{letra_es}\"\"\"

Output ONLY the English song lyrics.
"""
    letra_en = llamar_groq_seguro(client, [{"role": "user", "content": prompt_en}], temperature=0.6, anti_bucle=True)

    return letra_es, letra_en

# ==============================================================
# FASE 1: ENTRADA LIMPIA (EL PRIMER CAJÓN)
# ==============================================================
letra_manual = st.text_area(
    "Pega aquí la letra de la canción:",
    height=170,
    placeholder="Pega aquí los versos de la canción que quieres analizar o transformar..."
)

col_btn_esc, col_btn_cal = st.columns([1, 1])

with col_btn_esc:
    btn_escanear = st.button("Escanear", type="primary", key="btn_escanear")

with col_btn_cal:
    btn_calibrar_directo = st.button("Calibrar", key="btn_calibrar_directo")

# 1. BOTÓN: ESCANEAR (Estructura y traducción poética que rima)
if btn_escanear:
    if not GROQ_API_KEY.strip():
        st.error("Ingresa tu Groq API Key en la barra lateral.")
    elif not letra_manual.strip():
        st.warning("Pega la letra de la canción antes de escanear.")
    else:
        with st.spinner("Estructurando bloques musicales y creando traducción adaptada con rima..."):
            try:
                orig, es = estructurar_letra_musical(letra_manual.strip(), GROQ_API_KEY)
                st.session_state.letra_esc_orig = orig
                st.session_state.letra_esc_es = es
            except Exception as e:
                st.error(f"Error al estructurar: {e}")

# 2. BOTÓN: CALIBRAR (Analiza directamente la letra del primer cajón)
if btn_calibrar_directo:
    texto_a_calibrar = letra_manual.strip() or st.session_state.letra_esc_orig
    if not GROQ_API_KEY.strip():
        st.error("Ingresa tu Groq API Key en la barra lateral.")
    elif not texto_a_calibrar:
        st.warning("Pega una letra en el primer cajón para poder calibrar su frecuencia.")
    else:
        with st.spinner("Analizando la letra del primer cajón en la escala Hawkins y midiendo viralidad..."):
            try:
                st.session_state.analisis_hawkins = calibrar_hawkins_estructurado(texto_a_calibrar, GROQ_API_KEY)
            except Exception as e:
                st.error(f"Error al calibrar: {e}")

# ==============================================================
# FASE 2: MUESTRA RESULTADOS CUANDO SE ESCANEA O CALIBRA
# ==============================================================
# Mostrar estructura si existe
if st.session_state.letra_esc_orig:
    st.markdown("---")
    st.markdown("#### 🎼 Letra Estructurada")
    tab_l_orig, tab_l_es = st.tabs(["🌐 Original", "🇪🇸 Adaptación en Español (Con Rima)"])
    with tab_l_orig:
        boton_copiar(st.session_state.letra_esc_orig, id_btn="cp_esc_orig")
        st.text_area("Original", value=st.session_state.letra_esc_orig, height=180)
    with tab_l_es:
        boton_copiar(st.session_state.letra_esc_es, id_btn="cp_esc_es")
        st.text_area("Español Adaptado", value=st.session_state.letra_esc_es, height=180)

# Mostrar tarjeta de diagnóstico si se calibró
if st.session_state.analisis_hawkins:
    h = st.session_state.analisis_hawkins
    frec_str = h.get("frecuencia", "")

    st.markdown("---")
    st.markdown(f"""<div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%); border-left: 6px solid #f43f5e; padding: 18px 22px; border-radius: 12px; margin: 15px 0;">
<h4 style="margin: 0 0 10px 0; color: #fb7185; font-size: 18px;">📊 Diagnóstico de la Letra: <span style="color: #ffffff; text-decoration: underline;">{frec_str}</span></h4>
<p style="margin: 6px 0; color: #38bdf8; font-size: 15px;"><b>🔥 Potencial Viral / Conexión Emocional:</b> <span style="color: #ffffff; font-weight: bold;">{h.get('viralidad')}</span></p>
<p style="margin: 6px 0; color: #e2e8f0; font-size: 14px;"><b>⚠️ Patrón Psicológico Detectado:</b> {h.get('patron')}</p>
<p style="margin: 6px 0; color: #34d399; font-size: 15px;"><b>✨ Frecuencia de Elevación recomendada:</b> {h.get('elevacion')}</p>
<p style="margin: 6px 0; color: #c084fc; font-size: 14px;"><b>🔑 Clave de Transmutación:</b> {h.get('clave')}</p>
</div>""", unsafe_allow_html=True)

# ==============================================================
# FASE 3: SLIDER Y PANEL DE TRANSMUTACIÓN
# (Solo visible si ya hay letra ingresada en el cajón o escaneada)
# ==============================================================
hay_letra = bool(letra_manual.strip() or st.session_state.letra_esc_orig)

if hay_letra:
    st.markdown("---")
    st.markdown("### 🎚️ Escala de Vibración & Conexión Viral (Hawkins)")
    st.caption("Desliza para elegir la frecuencia destino y descubrir los temas de alta o baja vibración:")

    frec_seleccionada = st.select_slider(
        "Nivel de Frecuencia Hawkins:",
        options=list(HAWKINS_SCALE.keys()),
        value=500,
        format_func=lambda x: HAWKINS_SCALE[x]["nombre"]
    )

    info_frec = HAWKINS_SCALE[frec_seleccionada]

    st.markdown(
        f"""<div style="background-color: #0b1120; border-left: 6px solid {info_frec['color']}; padding: 14px 18px; border-radius: 8px; margin-bottom: 12px;">
<h3 style="margin: 0; color: #ffffff;">{info_frec['nombre']} <span style="background-color: {info_frec['color']}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 13px; margin-left: 8px;">🔥 Viralidad: {info_frec['viralidad']}</span></h3>
<p style="margin: 6px 0 2px 0; color: #cbd5e1; font-size: 14px;"><b>Campo Emocional:</b> {info_frec['emocion']}</p>
<p style="margin: 0; color: #38bdf8; font-size: 13px;"><b>Psicología de Conexión:</b> {info_frec['tipo_viral']}</p>
</div>""",
        unsafe_allow_html=True
    )

    col_baja, col_alta = st.columns(2)

    with col_baja:
        st.markdown(
            f"""<div style="background-color: rgba(220, 38, 38, 0.12); border: 1px solid rgba(220, 38, 38, 0.4); padding: 12px; border-radius: 8px; min-height: 140px;">
<b style="color: #f87171; font-size: 14px;">🔥 3 Temas de Baja Vibración (Catarsis):</b>
<ul style="margin: 8px 0 0 0; padding-left: 18px; color: #fecaca; font-size: 13px;">
<li>{info_frec['temas_baja'][0]}</li>
<li>{info_frec['temas_baja'][1]}</li>
<li>{info_frec['temas_baja'][2]}</li>
</ul>
</div>""",
            unsafe_allow_html=True
        )

    with col_alta:
        st.markdown(
            f"""<div style="background-color: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); padding: 12px; border-radius: 8px; min-height: 140px;">
<b style="color: #34d399; font-size: 14px;">✨ 3 Temas de Alta Vibración (Elevación):</b>
<ul style="margin: 8px 0 0 0; padding-left: 18px; color: #a7f3d0; font-size: 13px;">
<li>{info_frec['temas_alta'][0]}</li>
<li>{info_frec['temas_alta'][1]}</li>
<li>{info_frec['temas_alta'][2]}</li>
</ul>
</div>""",
            unsafe_allow_html=True
        )

    # ==============================================================
    # CONFIGURACIÓN Y TRANSMUTACIÓN
    # ==============================================================
    st.markdown("---")
    st.markdown("### ✨ Configurar y Componer Letra")

    col_rima, col_modo = st.columns([1, 1])

    with col_rima:
        tipo_rima_elegida = st.selectbox(
            "Estructura de Rima:",
            options=["AABB (Pareado clásico)", "ABAB (Alterna pop)", "AAAA (Monorrima contundente)", "ABCB (Balada tradicional)"],
            index=1
        )

    with col_modo:
        modo_elegido = st.radio(
            "Enfoque de Composición:",
            options=[
                "Elevar la misma historia original",
                "Elegir tema de Baja Vibración (Catarsis)",
                "Elegir tema de Alta Vibración (Elevación)",
                "Tema libre personalizado"
            ],
            index=0
        )

    tema_para_enviar = ""
    if modo_elegido == "Elegir tema de Baja Vibración (Catarsis)":
        tema_para_enviar = st.selectbox("Selecciona el tema de baja vibración:", options=info_frec['temas_baja'])
    elif modo_elegido == "Elegir tema de Alta Vibración (Elevación)":
        tema_para_enviar = st.selectbox("Selecciona el tema de alta vibración:", options=info_frec['temas_alta'])
    elif modo_elegido == "Tema libre personalizado":
        tema_para_enviar = st.text_input("Escribe tu temática:", placeholder="Ej: Triunfo personal, Paz mental, Un amor sano...")

    st.markdown(" ")

    # 3. BOTÓN: TRANSMUTAR
    if st.button("Transmutar", type="primary", key="btn_transmutar"):
        if not GROQ_API_KEY.strip():
            st.error("Por favor ingresa tu Groq API Key en la barra lateral.")
        elif modo_elegido == "Tema libre personalizado" and not tema_para_enviar.strip():
            st.warning("Por favor escribe la temática que deseas.")
        else:
            letra_base_final = st.session_state.letra_esc_orig or letra_manual.strip()
            modo_codigo = "misma" if modo_elegido == "Elevar la misma historia original" else "nuevo"
            
            with st.spinner("Componiendo en Español con rima y creando adaptación lírica al Inglés..."):
                try:
                    es_txt, en_txt = transmutar_letra_poetica_avanzada(
                        letra_base=letra_base_final,
                        frec_num=frec_seleccionada,
                        rima_tipo=tipo_rima_elegida,
                        modo=modo_codigo,
                        tema=tema_para_enviar.strip(),
                        api_key=GROQ_API_KEY
                    )
                    st.session_state.letra_trans_es = es_txt
                    st.session_state.letra_trans_en = en_txt
                except Exception as e:
                    st.error(f"Error de conexión con Groq: {e}")

    # CUADRO CON AMBAS VERSIONES CON RIMA (ESPAÑOL E INGLÉS)
    if st.session_state.letra_trans_es and st.session_state.letra_trans_en:
        st.markdown("---")
        st.markdown("""<div style="background-color: #064e3b; border-left: 6px solid #10b981; padding: 14px 20px; border-radius: 8px; margin: 15px 0;">
<h4 style="margin: 0; color: #a7f3d0;">🎉 ¡Letra compuesta con éxito! Rima musical adaptada en Español e Inglés</h4>
</div>""", unsafe_allow_html=True)

        tab_t_es, tab_t_en = st.tabs(["🇪🇸 Versión en Español (Lírica Ritmada)", "🇺🇸 English Version (Rhymed Trans-adaptation)"])
        with tab_t_es:
            boton_copiar(st.session_state.letra_trans_es, id_btn="cp_t_es")
            st.text_area("Español (Párrafos limpios)", value=st.session_state.letra_trans_es, height=350)
        with tab_t_en:
            boton_copiar(st.session_state.letra_trans_en, id_btn="cp_t_en")
            st.text_area("Inglés (Poetic & Rhymed)", value=st.session_state.letra_trans_en, height=350)
