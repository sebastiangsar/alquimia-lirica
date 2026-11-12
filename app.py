import json
import random
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
# 2. BANCO DE IDEAS HUMANAS COTIDIANAS (SORPRÉNDEME)
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
        "psicologia": "Vulnerabilidad extrema, confesar lo innombrable, catarsis de lo oculto.",
        "temas_baja": ["El error que nadie me perdona", "Esconderme de la mirada de todos", "Sintiéndome una farsa"],
        "temas_alta": ["Digno de existir sin pedir permiso", "La humillación que forjó mi temple", "Perdonar mis caídas"]
    },
    30: {
        "nombre": "Culpa (30)",
        "emocion": "Remordimiento / Castigo",
        "viralidad": "89%",
        "color": "#991b1b",
        "psicologia": "Baladas desgarradoras de arrepentimiento, deudas morales y perdón tardío.",
        "temas_baja": ["Fui yo quien rompió todo", "La culpa me asfixia en la noche", "Demasiado tarde para pedir perdón"],
        "temas_alta": ["Soltar cruces ajenas", "Comprender mi error y sanar", "De la culpa nace mi redención"]
    },
    50: {
        "nombre": "Apatía (50)",
        "emocion": "Desesperanza / Indiferencia",
        "viralidad": "80%",
        "color": "#9a3412",
        "psicologia": "Nihilismo urbano, canciones 'sad', vacío existencial compartido.",
        "temas_baja": ["Ya nada duele ni importa", "El cansancio crónico de existir", "Días grises en automático"],
        "temas_alta": ["Una chispa en medio de la niebla", "Elegir sentir aunque arda", "Despertar del coma emocional"]
    },
    75: {
        "nombre": "Pena / Duelo (75)",
        "emocion": "Tristeza / Pérdida",
        "viralidad": "94%",
        "color": "#c2410c",
        "psicologia": "Duelo universal, despedidas inevitables (Efecto Adele).",
        "temas_baja": ["Tu lado de la cama está frío", "Extrañarte me está matando", "Nuestra foto en la pared vacía"],
        "temas_alta": ["Honrar lo que fuimos", "Llevarte en el alma sin dolor", "Agradecer tu paso por mi vida"]
    },
    100: {
        "nombre": "Miedo (100)",
        "emocion": "Ansiedad / Amenaza",
        "viralidad": "91%",
        "color": "#b45309",
        "psicologia": "Paranoia, terror a quedarse solo, el pánico al abandono o al rechazo.",
        "temas_baja": ["Pánico a que te vayas", "La ansiedad que me oprime el pecho", "Corriendo de mis monstruos"],
        "temas_alta": ["Avanzar aunque me tiemblen las piernas", "La tormenta no me romperá", "Confiar en el destino"]
    },
    125: {
        "nombre": "Deseo / Apego (125)",
        "emocion": "Lujuria / Obsesión",
        "viralidad": "97%",
        "color": "#a16207",
        "psicologia": "Amor tóxico, sensualidad insaciable, adicción a una persona (Trap / Urbano).",
        "temas_baja": ["Obsesión carnal que me quema", "Tenerte aunque seas veneno", "Deseo que no me deja dormir"],
        "temas_alta": ["Pasión consciente y magnética", "Atracción libre sin cadenas", "Canalizar el fuego en arte"]
    },
    150: {
        "nombre": "Ira / Rabia (150)",
        "emocion": "Resentimiento / Venganza",
        "viralidad": "99%",
        "color": "#dc2626",
        "psicologia": "Tiraderas viscerales, despecho furioso, cobrar traiciones (Efecto Shakira / BZRP).",
        "temas_baja": ["Que te duela el doble de lo que me dolió", "Ardiendo de furia por tu traición", "Tiradera sin piedad"],
        "temas_alta": ["Mi éxito rotundo es mi respuesta", "Límites de acero inquebrantables", "Furia transmutada en disciplina"]
    },
    175: {
        "nombre": "Orgullo (175)",
        "emocion": "Superioridad / Egolatría",
        "viralidad": "95%",
        "color": "#e11d48",
        "psicologia": "Flexing, presumir logros, 'nadie creía en mí' (Hip Hop / Corridos).",
        "temas_baja": ["Mírame en la cima y tú abajo", "No necesito de nadie", "Soy intocable"],
        "temas_alta": ["Orgullo noble de mis raíces", "Honrar las cicatrices ganadas", "Triunfo con humildad real"]
    },
    200: {
        "nombre": "Coraje (200) [Umbral]",
        "emocion": "Valentía / Determinación",
        "viralidad": "93%",
        "color": "#16a34a",
        "psicologia": "Himnos de superación personal, levantarse tras la caída (Efecto Rocky).",
        "temas_baja": ["Luchar acorralado contra todos", "Dejar la piel en el intento", "Gritar con la voz rota"],
        "temas_alta": ["Me caigo diez veces, me levanto once", "El momento exacto de saltar", "Dueño de mi destino"]
    },
    250: {
        "nombre": "Neutralidad (250)",
        "emocion": "Confianza / Desapego",
        "viralidad": "82%",
        "color": "#0d9488",
        "psicologia": "Cero drama, fluir con la vida, madurez emocional despreocupada.",
        "temas_baja": ["Me cansé de discusiones inútiles", "Que cada quien haga su vida", "Ya no me importa qué digan"],
        "temas_alta": ["La paz de no engancharse", "Fluyendo en el río de la vida", "Tranquilidad por sobre la razón"]
    },
    310: {
        "nombre": "Voluntad (310)",
        "emocion": "Optimismo / Enfoque",
        "viralidad": "88%",
        "color": "#0284c7",
        "psicologia": "Mentalidad imparable, disciplina de hierro, fe en el proceso.",
        "temas_baja": ["Forzar el cuerpo hasta el límite", "Trabajar sin descanso ni tregua", "Ganar a como dé lugar"],
        "temas_alta": ["Construyendo un legado paso a paso", "Optimismo inquebrantable", "Amor por el camino recorrido"]
    },
    350: {
        "nombre": "Aceptación (350)",
        "emocion": "Perdón / Trascendencia",
        "viralidad": "92%",
        "color": "#2563eb",
        "psicologia": "Cierre de ciclos en paz, soltar rencores, reconciliación íntima.",
        "temas_baja": ["Aceptar que esto se terminó", "Firmar la tregua con mi pasado", "Reconocer la derrota con calma"],
        "temas_alta": ["Te perdono y me libero de ti", "Cerrar la puerta con gratitud", "Amar lo que fue y bendecir lo que viene"]
    },
    400: {
        "nombre": "Razón / Sabiduría (400)",
        "emocion": "Claridad / Discernimiento",
        "viralidad": "85%",
        "color": "#4f46e5",
        "psicologia": "Rap consciente, metáforas filosóficas, disección psicológica de las relaciones.",
        "temas_baja": ["Diseccionando tus contradicciones", "La trampa mental de las masas", "Análisis frío del adiós"],
        "temas_alta": ["Comprender el orden oculto", "Sabiduría destilada en rima", "Claridad mental absoluta"]
    },
    500: {
        "nombre": "Amor Incondicional (500)",
        "emocion": "Compasión / Reverencia",
        "viralidad": "96%",
        "color": "#7c3aed",
        "psicologia": "Himnos atemporales de amor que erizan la piel (Coldplay, Bob Marley).",
        "temas_baja": ["Amarte duele de tan inmenso", "Darlo todo sin esperar rescate", "Cuidarte en medio del caos"],
        "temas_alta": ["Amor que no pide nada a cambio", "Sanar con solo mirarte", "Tu felicidad es mi alegría"]
    },
    540: {
        "nombre": "Alegría Serena (540)",
        "emocion": "Éxtasis / Celebración",
        "viralidad": "97%",
        "color": "#c026d3",
        "psicologia": "Euforia de vivir, fiesta contagiosa, liberación pura ('Happy', Funk).",
        "temas_baja": ["Bailar para no llorar", "Locura de una noche eterna", "Gritar hasta que se apague la pena"],
        "temas_alta": ["El milagro de seguir con vida", "Bailar bajo la lluvia sin motivo", "Risa que contagia el mundo"]
    },
    600: {
        "nombre": "Paz / Unidad (600)",
        "emocion": "Serenidad / Trascendencia",
        "viralidad": "78%",
        "color": "#059669",
        "psicologia": "Trascendencia, silencio sonoro, trance pacífico y unificación espiritual.",
        "temas_baja": ["La quietud tras la tormenta", "Desconectado del ruido del mundo", "Rendición pacífica"],
        "temas_alta": ["Océano de calma en el pecho", "Un latido común con el universo", "Luz que nunca se extingue"]
    }
}

# ==============================================================
# 4. GESTIÓN DE SESIÓN Y MEMORIA PERSISTENTE
# ==============================================================
ESTADOS_INICIALES = {
    "texto_input": "",
    "slider_hawkins": 500,
    "analisis_hawkins": None,
    "letra_trans_es": None,
    "letra_trans_en": None,
    "guia_produccion": None
}
for key, val in ESTADOS_INICIALES.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Manejo de API Key (Secrets o Manual)
api_key_default = ""
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key_default = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# ==============================================================
# 5. MOTOR GROQ OPTIMIZADO CON LIMPIEZA DE LLAVE
# ==============================================================
@st.cache_resource
def get_groq_client(api_key: str):
    # .strip() elimina espacios accidentales al copiar la clave
    return Groq(api_key=api_key.strip())

def llamar_groq_robusto(client, mensajes, temperature=0.6, json_mode=False):
    """Ejecuta llamadas con modelos de alta gama sin sobrecargar peticiones"""
    modelos = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
    kwargs = {
        "messages": mensajes,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    ultimo_err = None
    for mod in modelos:
        try:
            kwargs["model"] = mod
            res = client.chat.completions.create(**kwargs)
            return res.choices[0].message.content
        except Exception as e:
            ultimo_err = e
            continue
    raise Exception(f"Falla de conexión con Groq: {ultimo_err}")

# ==============================================================
# 6. FUNCIONES DE PROCESAMIENTO MUSICAL
# ==============================================================
def calibrar_hawkins_json(letra_o_idea: str, api_key: str) -> dict:
    """Diagnóstico psicológico y de viralidad en formato JSON estructurado"""
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

    res = llamar_groq_robusto(
        client,
        [{"role": "system", "content": "Responde estrictamente en JSON válido."},
         {"role": "user", "content": prompt}],
        temperature=0.2,
        json_mode=True
    )
    return json.loads(res)

def componer_cancion_dual(
    texto_base: str,
    frecuencia_num: int,
    modo_estilo: str,
    estructura_tipo: str,
    perspectiva_pov: str,
    rima_esquema: str,
    genero_ritmo: str,
    api_key: str
):
    """Compone la letra en Español y su trans-adaptación rimada en Inglés en una sola ejecución armónica"""
    client = get_groq_client(api_key)
    frec_info = HAWKINS_SCALE.get(frecuencia_num, HAWKINS_SCALE[500])

    if "Simple" in modo_estilo:
        estilo_instruccion = (
            "ESTILO LÍRICO SIMPLE (COLOQUIAL / POP URBANO DIRECTO):\n"
            "- Usa lenguaje común, cotidiano, de calle o de conversación real.\n"
            "- Cero palabras pretenciosas o rebuscadas. Frases cortas, contundentes y memorables.\n"
            "- Imágenes directas que cualquier persona comprende al primer segundo de escucha."
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
            "[Verse 1]: Establece la escena y el conflicto.\n\n"
            "[Pre-Chorus]: Tensión creciente de 2 a 4 versos que anticipan la explosión.\n\n"
            "[Chorus]: El clímax armónico, gancho memorable y contundente.\n\n"
            "[Post-Chorus]: Gancho rítmico con palabra clave del coro repetida + arreglo vocal de 2 líneas con ad-libs entre paréntesis.\n\n"
            "[Verse 2]: Evolución de la historia, detalles adicionales.\n\n"
            "[Pre-Chorus]: Cohesión melódica (mismo motivo y frases clave del primer Pre-Coro para fijación radial).\n\n"
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
- ESQUEMA DE RIMA OBLIGATORIO: {rima_esquema}.

{estilo_instruccion}

{estructura_instruccion}

REQUISITOS DE SALIDA:
1. Genera primero la versión completa en ESPAÑOL.
2. Genera después la ADAPTACIÓN LÍRICA AL INGLÉS (NO traducción literal; trans-adaptación cantable que rime con el mismo esquema {rima_esquema} y conserve la métrica para cantarse sobre la misma base instrumental).
3. Redacta una GUÍA DE PRODUCCIÓN corta para Suno/Udio/Productor (BPM, Tonalidad, Instrumentos clave y Prompt de estilo).

Separa OBLIGATORIAMENTE las secciones con estos delimitadores exactos:
===ESPANOL===
[Aquí toda la letra en español]
===INGLES===
[Aquí toda la letra adaptada en inglés]
===PRODUCCION===
[BPM, Escala musical, Prompt de estilo para IA musical y notas para el cantante]"""

    salida_cruda = llamar_groq_robusto(
        client,
        [{"role": "user", "content": prompt}],
        temperature=0.6
    )

    es_txt, en_txt, prod_txt = "", "", ""
    if "===ESPANOL===" in salida_cruda and "===INGLES===" in salida_cruda:
        partes = salida_cruda.split("===INGLES===")
        es_txt = partes[0].replace("===ESPANOL===", "").strip()
        
        resto = partes[1]
        if "===PRODUCCION===" in resto:
            partes_en_prod = resto.split("===PRODUCCION===")
            en_txt = partes_en_prod[0].strip()
            prod_txt = partes_en_prod[1].strip()
        else:
            en_txt = resto.strip()
            prod_txt = f"Estilo sugerido: {genero_ritmo} | Frecuencia: {frec_info['nombre']}"
    else:
        es_txt = salida_cruda.strip()
        en_txt = "Generación en inglés integrada en la versión principal."
        prod_txt = f"Estilo: {genero_ritmo}"

    return es_txt, en_txt, prod_txt

# ==============================================================
# 7. BARRA LATERAL (CONFIGURACIÓN & RESET)
# ==============================================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    groq_api_key_input = st.text_input(
        "Groq API Key:",
        value=api_key_default,
        type="password",
        placeholder="gsk_..."
    )
    
    if groq_api_key_input.strip():
        GROQ_API_KEY = groq_api_key_input.strip()
        st.success("🟢 API Key cargada correctamente")
    else:
        GROQ_API_KEY = ""
        st.warning("Pega tu clave gratis de console.groq.com")

    st.markdown("---")
    st.markdown("### 📘 Sobre Hawkins en la Música")
    st.caption(
        "Las canciones por debajo de 200 puntos (Ira, Culpa, Deseo) conectan por **catarsis colectiva** (despecho, rabia). "
        "Las canciones de 200 a 600 (Coraje, Aceptación, Amor) se convierten en **himnos atemporales de sanación y empoderamiento**."
    )

    if st.button("🗑️ Limpiar todo el taller"):
        st.cache_resource.clear()
        for k, v in ESTADOS_INICIALES.items():
            st.session_state[k] = v
        st.rerun()

# ==============================================================
# 8. PANEL PRINCIPAL: EL LIENZO DE COMPOSICIÓN & ANÁLISIS
# ==============================================================
st.title("🎵 Alquimia Lírica Pro")
st.caption("Composición musical de élite, resonancia viral de Hawkins y trans-adaptación rítmica")

def inyectar_idea_aleatoria():
    idea_sel, frec_sel = random.choice(IDEAS_COTIDIANAS)
    st.session_state["texto_input"] = idea_sel
    st.session_state["slider_hawkins"] = frec_sel

col_top_a, col_top_b = st.columns([2, 1])
with col_top_a:
    st.markdown("#### ✍️ Lienzo de Creación")
with col_top_b:
    st.button("🎲 Sorpréndeme con una Idea", on_click=inyectar_idea_aleatoria, help="Genera un conflicto humano cotidiano y adapta la frecuencia automáticamente")

# CAJÓN MULTIFUNCIÓN ÚNICO
texto_usuario = st.text_area(
    "Pega aquí una letra existente (para analizar) O escribe tu idea / historia cotidiana:",
    value=st.session_state["texto_input"],
    height=140,
    placeholder="Ej: Descubrí que salías con alguien más y te vi en el café de la esquina... o pega los versos de una canción completa..."
)
st.session_state["texto_input"] = texto_usuario

# ==============================================================
# 9. CONTROLES DE COMPOSICIÓN (EN 3 COLUMNAS LIMPIAS)
# ==============================================================
st.markdown("##### 🎛️ Dirección Artística & Estructura")
col_estilo, col_estruct, col_pov = st.columns(3)

with col_estilo:
    modo_estilo_sel = st.selectbox(
        "Estilo Lírico:",
        options=["Simple (Cotidiano / Pop Directo)", "Descriptivo (Poético / Cinematográfico)"],
        index=0,
        help="Simple usa palabras coloquiales. Descriptivo crea imágenes sensoriales poéticas."
    )

with col_estruct:
    estructura_sel = st.selectbox(
        "Arquitectura Musical:",
        options=["Simple (Verso - Coro - Puente)", "Avanzada Hitmaker (Con Pre/Post-Coro)"],
        index=1,
        help="Avanzada incluye Pre-Coro de tensión y Post-Coro con ad-libs para máxima recordación."
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
        index=0,
        help="Define quién habla y a quién se dirige la narrativa de la canción."
    )

with st.expander("⚙️ Ajustes Opcionales de Producción (Rima & Ritmo)"):
    col_sub_rima, col_sub_ritmo = st.columns(2)
    with col_sub_rima:
        rima_sel = st.selectbox(
            "Esquema de Rima:",
            options=["ABAB (Alterna pop / Dinámica)", "AABB (Pareado clásico)", "ABCB (Balada tradicional)", "AAAA (Monorrima contundente)"],
            index=0
        )
    with col_sub_ritmo:
        genero_sel = st.selectbox(
            "Género / Cadencia:",
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
# 10. ESCALA DE VIBRACIÓN HAWKINS INTERACTIVA
# ==============================================================
st.markdown("---")
st.markdown("##### 🎚️ Nivel de Resonancia Hawkins")

frec_seleccionada = st.select_slider(
    "Selecciona la emoción / vibración destino:",
    options=list(HAWKINS_SCALE.keys()),
    value=st.session_state["slider_hawkins"],
    format_func=lambda x: HAWKINS_SCALE[x]["nombre"],
    key="slider_hawkins"
)

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
# 11. BOTONES MAESTROS DE ACCIÓN
# ==============================================================
col_btn_cal, col_btn_comp = st.columns([1, 1])

with col_btn_cal:
    btn_analizar = st.button("🔍 Analizar / Calibrar Letra", use_container_width=True)

with col_btn_comp:
    btn_componer = st.button("✨ Componer / Transmutar Canción", type="primary", use_container_width=True)

# LÓGICA DE ACCIÓN 1: ANALIZAR LETRA EXISTENTE
if btn_analizar:
    texto_a_evaluar = st.session_state["texto_input"].strip()
    if not GROQ_API_KEY:
        st.error("⚠️ Falta la Groq API Key. Ingrésala en la barra lateral izquierda.")
    elif not texto_a_evaluar:
        st.warning("Escribe o pega una letra en el cajón superior para calibrarla.")
    else:
        with st.spinner("Calibrando frecuencia, patrón psicológico y potencial viral..."):
            try:
                diag = calibrar_hawkins_json(texto_a_evaluar, GROQ_API_KEY)
                st.session_state.analisis_hawkins = diag
            except Exception as e:
                if "401" in str(e) or "invalid_api_key" in str(e):
                    st.error("Error 401: La API Key de Groq es inválida o expiró. Verifica tu clave en console.groq.com/keys.")
                else:
                    st.error(f"Error al analizar la letra: {e}")

# LÓGICA DE ACCIÓN 2: COMPONER CANCIÓN
if btn_componer:
    texto_base = st.session_state["texto_input"].strip()
    if not GROQ_API_KEY:
        st.error("⚠️ Falta la Groq API Key. Ingrésala en la barra lateral izquierda.")
    elif not texto_base:
        st.warning("Escribe una idea en el cajón o haz clic en '🎲 Sorpréndeme con una Idea'.")
    else:
        with st.spinner(f"Componiendo en Español ({modo_estilo_sel}) y adaptando al Inglés con rima cantable..."):
            try:
                es_letra, en_letra, guia_prod = componer_cancion_dual(
                    texto_base=texto_base,
                    frecuencia_num=frec_seleccionada,
                    modo_estilo=modo_estilo_sel,
                    estructura_tipo=estructura_sel,
                    perspectiva_pov=narrativa_pov_sel,
                    rima_esquema=rima_sel,
                    genero_ritmo=genero_sel,
                    api_key=GROQ_API_KEY
                )
                st.session_state.letra_trans_es = es_letra
                st.session_state.letra_trans_en = en_letra
                st.session_state.guia_produccion = guia_prod
            except Exception as e:
                if "401" in str(e) or "invalid_api_key" in str(e):
                    st.error("Error 401: La API Key de Groq es inválida o expiró. Verifica tu clave en console.groq.com/keys.")
                else:
                    st.error(f"Error en el motor de composición: {e}")

# ==============================================================
# 12. MUESTRA DE RESULTADOS: DIAGNÓSTICO HAWKINS
# ==============================================================
if st.session_state.analisis_hawkins:
    diag = st.session_state.analisis_hawkins
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
# 13. MUESTRA DE RESULTADOS: CANCIONES GENERADAS (DUAL TAB)
# ==============================================================
if st.session_state.letra_trans_es and st.session_state.letra_trans_en:
    st.markdown("---")
    st.success("🎉 ¡Obra compuesta con éxito! Las dos versiones conservan la métrica para cantarse sobre la misma base instrumental.")

    tab_es, tab_en, tab_prod = st.tabs([
        "🇪🇸 Versión en Español (Lírica Ritmada)",
        "🇺🇸 English Trans-Adaptation (Rhymed & Singable)",
        "🎛️ Guía de Producción & Metatags"
    ])

    with tab_es:
        st.caption("Usa el icono de la esquina superior derecha del bloque para copiar:")
        st.code(st.session_state.letra_trans_es, language="markdown")

    with tab_en:
        st.caption("Adaptación cantable en inglés con rima equivalente y métrica silábica:")
        st.code(st.session_state.letra_trans_en, language="markdown")

    with tab_prod:
        st.caption("Ficha técnica recomendada para vocalistas, productores o generadores de audio IA (Suno / Udio):")
        st.code(st.session_state.guia_produccion, language="yaml")
