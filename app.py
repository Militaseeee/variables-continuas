# ================================================================
# app.py — FRONTEND: Interfaz visual de la aplicación
#
# Este archivo construye todo lo que el usuario ve y toca:
#   · La configuración de la página
#   · Los estilos (CSS) que dan el look oscuro
#   · Los componentes visuales: header, tarjetas, pestañas, botones
#
# La matemática vive en calculos.py.
# Si quieres cambiar colores, textos o layout → edita este archivo.
# Si quieres cambiar cómo se calcula algo    → edita calculos.py.
# ================================================================

import streamlit as st
import matplotlib.pyplot as plt

# Importa todas las funciones matemáticas y de gráfico desde el backend
from calculos import (
    calcular_normal,
    calcular_t,
    calcular_chi2,
    calcular_f,
    crear_grafico,
)


# ================================================================
# BLOQUE 1 — CONFIGURACIÓN DE LA PÁGINA
#
# Lo primero que ejecuta Streamlit. Define el título de la pestaña
# del navegador, el ícono, y que el layout sea "wide" (ancho
# completo) en lugar del modo centrado por defecto.
# La barra lateral empieza colapsada para que no moleste.
# ================================================================

st.set_page_config(
    page_title="Distribuciones Continuas | Bioestadística",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ================================================================
# BLOQUE 2 — ESTILOS CSS (apariencia visual)
#
# st.markdown con unsafe_allow_html=True permite inyectar CSS puro.
# Aquí se define la paleta de colores del tema oscuro:
#
#   #020817  → fondo de la página (azul medianoche)
#   #0D1628  → fondo de tarjetas y containers
#   #1E3055  → color de los bordes
#   #60A5FA  → azul brillante (acento principal)
#   #E2E8F0  → texto claro (casi blanco)
#   #94A3B8  → texto suave (gris azulado)
#
# Cada bloque de CSS lleva un comentario que dice qué elemento afecta.
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Fuente global ─────────────────────────────────────── */
*, *::before, *::after,
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMarkdownContainer"],
button, input, label, p, span, div {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif !important;
}

/* ── Fondo de la página ────────────────────────────────── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background-color: #020817 !important; }

/* ── Ocultar elementos de Streamlit que no necesitamos ─── */
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer         { visibility: hidden !important; }
.block-container          { padding: 0.5rem 2.4rem 2rem !important; }

/* ── Campos de número (inputs) ─────────────────────────── */
input[type="number"],
[data-testid="stNumberInput"] input {
    background-color: #0D1628 !important;
    color: #E2E8F0 !important;
    border: 1px solid #1E3055 !important;
    border-radius: 8px !important;
}
input[type="number"]:focus {
    border-color: #60A5FA !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.18) !important;
}

/* ── Etiquetas y subtextos ─────────────────────────────── */
label, [data-testid="stWidgetLabel"] p,
[data-testid="stCaptionContainer"] p {
    color: #94A3B8 !important;
}

/* ── Radio buttons ─────────────────────────────────────── */
[data-testid="stRadio"] label { color: #CBD5E1 !important; font-size: 0.93rem; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: #CBD5E1 !important; }

/* ── Slider ────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div { background: #1E3055 !important; }
[data-testid="stSlider"] [role="slider"] { background: #60A5FA !important; }

/* ── Pestañas (tabs) ───────────────────────────────────── */
[data-testid="stTabs"] > div:first-child {
    background: #0D1628;
    border-radius: 12px;
    padding: 16px;
    border-bottom: 1px solid #1E3055;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #64748B !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    transition: color .2s;
}
button[data-baseweb="tab"]:hover { color: #93C5FD !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    background: #020817 !important;
    color: #60A5FA !important;
    border-bottom: 3px solid #60A5FA !important;
}
[data-testid="stTabPanel"] {
    background: #020817 !important;
    border: 1px solid #1E3055;
    border-radius: 12px;
    margin-top: 8px;
    padding: 24px 28px !important;
}

/* ── Containers con borde ──────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"],
.st-emotion-cache-130yy1s {
    background: #0D1628 !important;
    border: 1px solid #1E3055 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ── Expanders ─────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #0D1628 !important;
    border: 1px solid #1E3055 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary p { color: #94A3B8 !important; }
[data-testid="stExpander"] summary svg { fill: #64748B !important; }

/* ── Alertas (st.success, st.warning, st.info) ─────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    background: #0D1628 !important;
}

/* ── Línea divisoria ───────────────────────────────────── */
hr { border-color: #1E3055 !important; }


/* ================================================================
   COMPONENTES HTML PERSONALIZADOS
   Los bloques siguientes definen clases CSS que se usan con
   st.markdown(..., unsafe_allow_html=True) en el código de abajo.
   ================================================================ */

/* ── .hdr → Bloque de encabezado principal ─────────────── */
.hdr {
    background: linear-gradient(135deg, #020817 0%, #0B1932 45%, #152545 100%);
    border: 1px solid #1E3055;
    border-radius: 16px;
    padding: 16px;
    margin: 0 0 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(96,165,250,0.1);
    position: relative;
    overflow: hidden;
}
.hdr::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(96,165,250,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.hdr h1 {
    color: #E2E8F0 !important;
    font-size: 2rem;
    margin: 0 0 5px !important;
    padding: 0 !important;
    font-weight: 800;
    letter-spacing: 0.4px;
}
.hdr .sub { color: #94A3B8; font-size: .97rem; margin: 0; }
.hdr .aut { color: #475569; font-size: .83rem; margin: 5px 0 0;
            border-top: 1px solid #1E3055; padding-top: 6px; }

/* ── .ficha → Tarjeta informativa dentro de cada pestaña ── */
.ficha {
    background: #0D1628;
    border: 1px solid #1E3055;
    border-left: 4px solid #3B82F6;
    border-radius: 10px;
    padding: 16px;
    font-size: .89rem;
    color: #94A3B8;
    line-height: 1.6;
    margin-bottom: 14px;
}
.ficha strong { color: #CBD5E1; }

/* ── .ck-* → Tarjetas de concepto (sección "¿Qué es?") ─── */
.ck-azul, .ck-morado, .ck-verde {
    background: #0D1628;
    border: 1px solid #1E3055;
    border-radius: 10px;
    padding: 16px;
    font-size: .89rem;
    color: #94A3B8;
    line-height: 1.6;
    min-height: 170px;
    box-sizing: border-box;
}
.ck-azul   { border-left: 4px solid #3B82F6; }
.ck-morado { border-left: 4px solid #A78BFA; }
.ck-verde  { border-left: 4px solid #34D399; }
.ck-azul strong, .ck-morado strong, .ck-verde strong { color: #CBD5E1; }

/* ── .ficha-lbl → Etiqueta pequeña en mayúsculas ──────── */
.ficha-lbl {
    display: block;
    color: #60A5FA;
    font-weight: 700;
    font-size: .8rem;
    text-transform: uppercase;
    letter-spacing: .6px;
    margin-bottom: 6px;
}

/* ── Iguala la altura de las columnas de concepto ─────── */
[data-testid="stHorizontalBlock"] { align-items: stretch !important; }
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] [data-testid="stMarkdownContainer"] {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] [data-testid="stMarkdownContainer"] > div {
    flex: 1 !important;
}

/* ── .burbuja + .paso-lbl → Numerito circular de paso ─── */
.paso-wrap { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.burbuja {
    background: linear-gradient(135deg, #1D4ED8, #2563EB);
    color: white;
    min-width: 28px; height: 28px;
    border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: .85rem;
    box-shadow: 0 0 12px rgba(59,130,246,0.45);
    flex-shrink: 0;
}
.paso-lbl { font-weight: 700; font-size: .98rem; color: #CBD5E1; }

/* ── .res-card → Tarjeta verde con el resultado numérico ─ */
.res-card {
    background: linear-gradient(145deg, #051E17, #092E22);
    border: 1px solid #14532D;
    border-radius: 14px;
    padding: 24px 18px 18px;
    text-align: center;
    margin-bottom: 14px;
    box-shadow: 0 0 28px rgba(52,211,153,0.12);
}
.res-label { font-size:.74rem; color:#4ADE80; text-transform:uppercase;
             letter-spacing:.8px; margin-bottom:6px; }
.res-num   { font-size:3.4rem; font-weight:900; color:#34D399;
             line-height:1; letter-spacing:-1px; }
.res-pct   { font-size:1.3rem; font-weight:700; color:#6EE7B7; margin-top:4px; }

/* ── .interp → Caja azul con la interpretación en texto ─ */
.interp {
    background: #0B1932;
    border-left: 5px solid #3B82F6;
    border-radius: 10px;
    padding: 15px 20px;
    font-size: .93rem;
    color: #CBD5E1;
    line-height: 1.65;
    margin-bottom: 14px;
}

/* ── .paso-exp → Caja gris por cada paso matemático ───── */
.paso-exp {
    background: #020817;
    border: 1px solid #1E3055;
    border-radius: 10px;
    padding: 13px 17px;
    margin-bottom: 9px;
    font-size: .88rem;
    color: #94A3B8;
    line-height: 1.65;
}
.paso-exp strong, .paso-exp b { color: #CBD5E1; }
.paso-exp > p:first-child { margin-top: 0 !important; }

/* ── Botón principal ───────────────────────────────────── */
div.stButton > button[kind="primary"],
button.stBaseButton-primary {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 11px 28px !important;
    font-size: 1rem !important; font-weight: 700 !important; width: 100%;
    box-shadow: 0 4px 18px rgba(37,99,235,0.45) !important;
    transition: all .2s !important;
    letter-spacing: 0.3px !important;
}
div.stButton > button[kind="primary"]:hover,
button.stBaseButton-primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(37,99,235,0.6) !important;
}
</style>
""", unsafe_allow_html=True)


# ================================================================
# BLOQUE 3 — FUNCIONES DE PRESENTACIÓN
#
# Estas funciones arman los componentes visuales reutilizables.
# No calculan nada matemático: solo reciben datos y los muestran.
#
# mostrar_panel() → muestra el resultado, la interpretación y
#                   los pasos después de hacer un cálculo.
# paso_header()   → dibuja el numerito circular (① ② ③) con
#                   el texto del paso al lado.
# ================================================================

def mostrar_panel(res, interp, pasos, es_valor=False, parte="todo"):
    """Muestra la tarjeta de resultado, la interpretación y los pasos.
    parte='resultado' → solo número + interpretación
    parte='pasos'     → solo explicación paso a paso
    parte='todo'      → ambos (comportamiento original)
    """
    if parte in ("todo", "resultado"):
        if es_valor:
            st.markdown(f"""
            <div class="res-card">
                <div class="res-label">VALOR ENCONTRADO</div>
                <div class="res-num">{res:.4f}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-card">
                <div class="res-label">PROBABILIDAD CALCULADA</div>
                <div class="res-num">{res:.4f}</div>
                <div class="res-pct">{res*100:.2f} %</div>
            </div>""", unsafe_allow_html=True)
        if parte == "todo":
            st.markdown(f'<div class="interp">💬 &nbsp;{interp}</div>', unsafe_allow_html=True)

    if parte in ("todo", "pasos"):
        st.markdown(
            '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
            'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
            '📐 &nbsp;Explicación paso a paso</p>',
            unsafe_allow_html=True,
        )
        for paso in pasos:
            st.markdown(f'<div class="paso-exp">{paso}</div>', unsafe_allow_html=True)


def paso_header(n, texto):
    """Dibuja el círculo numerado con el título del paso."""
    st.markdown(
        f'<div class="paso-wrap">'
        f'<div class="burbuja">{n}</div>'
        f'<div class="paso-lbl">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ================================================================
# BLOQUE 4 — ENCABEZADO PRINCIPAL
#
# Lo primero visible en la página: título, descripción y autora.
# Usa la clase CSS .hdr definida arriba.
# ================================================================

st.markdown("""
<div class="hdr">
  <h1>📊 Distribuciones Continuas en Bioestadística</h1>
  <p class="sub">Visualiza, calcula e interpreta distribuciones de probabilidad continuas paso a paso.</p>
  <p class="aut">Autora: Alejandra Acosta &nbsp;·&nbsp; Bioestadística &nbsp;·&nbsp; Tema 4 — Distribuciones continuas</p>
</div>
""", unsafe_allow_html=True)


# ================================================================
# BLOQUE 5 — TARJETAS DE CONCEPTO (siempre visibles)
#
# Tres tarjetas horizontales que explican:
#   1. ¿Qué es una distribución continua?  (azul)
#   2. Regla clave: área ≠ altura          (morado)
#   3. ¿Cuándo usar cada distribución?     (verde)
#
# st.columns(3) divide la fila en 3 columnas iguales.
# Cada tarjeta usa HTML con una clase CSS distinta.
# ================================================================

st.markdown(
    '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
    'letter-spacing:.6px;text-transform:uppercase;margin:0 0 12px;">'
    '📌 &nbsp;¿Qué es una distribución continua?</p>',
    unsafe_allow_html=True,
)

ck1, ck2, ck3 = st.columns(3, gap="small")

with ck1:
    st.markdown(
        '<div class="ck-azul">'
        '<strong>🌊 ¿Qué es?</strong><br><br>'
        'Describe cómo se distribuye la probabilidad en una variable que puede tomar '
        '<strong>cualquier valor en un rango</strong>: '
        'estatura, peso, glucosa, presión arterial.'
        '</div>',
        unsafe_allow_html=True,
    )

with ck2:
    st.markdown(
        '<div class="ck-morado">'
        '<strong>⚡ Regla clave</strong><br><br>'
        'La probabilidad <strong>NO</strong> es la altura de la curva — '
        'es el <strong>área bajo la curva</strong>. '
        'El área total siempre suma <strong>1 (= 100%)</strong>.<br>'
        '<span style="color:#6D5A8A;font-size:.82rem;margin-top:4px;display:block;">'
        'P(X = valor exacto) = 0</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with ck3:
    st.markdown(
        '<div class="ck-verde">'
        '<strong>🗂️ ¿Cuándo usar cada una?</strong><br><br>'
        '<span style="color:#E2E8F0;font-weight:700;">📈 Normal</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>datos simétricos, n grande</span><br>'
        '<span style="color:#E2E8F0;font-weight:700;">📉 t Student</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>muestra pequeña (n &lt; 30)</span><br>'
        '<span style="color:#E2E8F0;font-weight:700;">📊 χ²</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>tablas de independencia</span><br>'
        '<span style="color:#E2E8F0;font-weight:700;">📋 F Fisher</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>comparar 3+ grupos (ANOVA)</span>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)


# ================================================================
# BLOQUE 6 — PESTAÑAS DE CADA DISTRIBUCIÓN
#
# st.tabs() crea 4 pestañas. Cada pestaña contiene:
#   · Columna izquierda (L): controles de entrada (parámetros,
#     tipo de cálculo, valores)
#   · Columna derecha  (R): gráfica + resultado + pasos
#
# El estado entre interacciones se guarda en st.session_state,
# que es como la "memoria" de la app mientras la página está abierta.
# ================================================================

tab_n, tab_t, tab_c, tab_f = st.tabs([
    "📈  Normal",
    "📉  t de Student",
    "📊  Chi-cuadrado  χ²",
    "📋  F de Fisher",
])


# ── PESTAÑA: NORMAL ─────────────────────────────────────────────
with tab_n:
    L, R = st.columns([1, 1.4], gap="large")

    # -- Controles de entrada ------------------------------------
    with L:
        with st.container(border=True):
            paso_header(1, "Parámetros")
            c1, c2 = st.columns(2)
            media_n = c1.number_input("Media (μ)", value=0.0, step=0.5, format="%.2f", key="media_n")
            sigma_n = c2.number_input("Desviación estándar (σ)", value=1.0,
                                      min_value=0.01, step=0.1, format="%.2f", key="sigma_n")
            st.caption(f"El 95% de los datos caerá entre {media_n-2*sigma_n:.2f} y {media_n+2*sigma_n:.2f}")

        with st.container(border=True):
            paso_header(2, "¿Qué quieres calcular?")
            tipo_n = st.radio("", [
                "📉  P(X ≤ a)  — proporción POR DEBAJO de un valor",
                "📈  P(X ≥ a)  — proporción POR ENCIMA de un valor",
                "📊  P(a ≤ X ≤ b)  — proporción ENTRE dos valores",
                "🎯  Percentil → ¿qué valor separa el p% inferior?",
            ], key="tipo_n", label_visibility="collapsed")

        with st.container(border=True):
            paso_header(3, "Valores y cálculo")
            if "DEBAJO" in tipo_n:
                va = st.number_input("Valor límite (a)", value=float(media_n),
                                     step=0.1, format="%.4f", key="nn_a")
                if st.button("Calcular probabilidad", type="primary", key="btn_ni"):
                    r, ps, it, ev = calcular_normal(media_n, sigma_n, 'izquierda', va)
                    st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=ev,
                                                 ts_n="izquierda", la_n=va, lb_n=None,
                                                 ultima_dist="n"))
                    st.rerun()
            elif "ENCIMA" in tipo_n:
                va = st.number_input("Valor límite (a)", value=float(media_n),
                                     step=0.1, format="%.4f", key="nn_ad")
                if st.button("Calcular probabilidad", type="primary", key="btn_nd"):
                    r, ps, it, ev = calcular_normal(media_n, sigma_n, 'derecha', va)
                    st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=ev,
                                                 ts_n="derecha", la_n=va, lb_n=None,
                                                 ultima_dist="n"))
                    st.rerun()
            elif "ENTRE" in tipo_n:
                c1, c2 = st.columns(2)
                va = c1.number_input("Límite inferior (a)", value=float(media_n - sigma_n),
                                     step=0.1, format="%.4f", key="nn_ae")
                vb = c2.number_input("Límite superior (b)", value=float(media_n + sigma_n),
                                     step=0.1, format="%.4f", key="nn_be")
                if va >= vb:
                    st.warning("⚠️ El límite inferior debe ser menor que el superior.")
                if st.button("Calcular probabilidad", type="primary", key="btn_ne"):
                    if va < vb:
                        r, ps, it, ev = calcular_normal(media_n, sigma_n, 'entre', va, vb)
                        st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=ev,
                                                     ts_n="entre", la_n=va, lb_n=vb,
                                                     ultima_dist="n"))
                        st.rerun()
            else:
                perc = st.slider("Percentil (%)", 1, 99, 95, key="nn_p")
                st.caption(f"Buscará X tal que el {perc}% de los datos está por debajo.")
                if st.button("Calcular valor X", type="primary", key="btn_np"):
                    r, ps, it, ev = calcular_normal(media_n, sigma_n, 'percentil', perc / 100)
                    st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=True,
                                                 ts_n="izquierda", la_n=r, lb_n=None,
                                                 ultima_dist="n"))
                    st.rerun()

    # -- Gráfica (columna derecha, siempre visible) ---------------
    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Datos simétricos: estatura, peso, glucosa en población sana, presión arterial. '
            '<strong>μ</strong> = centro &nbsp;·&nbsp; <strong>σ</strong> = ancho de la campana.</div>',
            unsafe_allow_html=True,
        )
        fig_n = crear_grafico("normal", {"media": media_n, "sigma": sigma_n},
                              st.session_state.get("ts_n"),
                              st.session_state.get("la_n"),
                              st.session_state.get("lb_n"))
        st.pyplot(fig_n, width='stretch')
        plt.close(fig_n)



# ── PESTAÑA: t DE STUDENT ────────────────────────────────────────
with tab_t:
    L, R = st.columns([1, 1.4], gap="large")

    with L:
        with st.container(border=True):
            paso_header(1, "Parámetros")
            gl_t = st.number_input("Grados de libertad (gl = n − 1)",
                                   value=10, min_value=1, max_value=500, step=1, key="gl_t")
            if gl_t >= 30:
                st.success(f"✅ Con {gl_t} gl ≈ Normal Estándar.")
            elif gl_t >= 10:
                st.info(f"ℹ️ Con {gl_t} gl, colas algo más anchas.")
            else:
                st.warning(f"⚠️ Con {gl_t} gl, colas bastante más anchas.")

        with st.container(border=True):
            paso_header(2, "¿Qué quieres calcular?")
            tipo_t = st.radio("", [
                "📉  P(T ≤ a)",
                "📈  P(T ≥ a)",
                "📊  P(a ≤ T ≤ b)",
                "🔑  Valor crítico t (dado α)",
            ], key="tipo_t", label_visibility="collapsed")

        with st.container(border=True):
            paso_header(3, "Valores y cálculo")
            if "≤ a)" in tipo_t:
                va = st.number_input("Valor de a", value=0.0, step=0.1, format="%.4f", key="tt_a")
                if st.button("Calcular", type="primary", key="btn_ti", width='stretch'):
                    r, ps, it, ev = calcular_t(gl_t, 'izquierda', va)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                 ts_t="izquierda", la_t=va, lb_t=None,
                                                 ultima_dist="t"))
                    st.rerun()
            elif "≥ a)" in tipo_t:
                va = st.number_input("Valor de a", value=0.0, step=0.1, format="%.4f", key="tt_ad")
                if st.button("Calcular", type="primary", key="btn_td", width='stretch'):
                    r, ps, it, ev = calcular_t(gl_t, 'derecha', va)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                 ts_t="derecha", la_t=va, lb_t=None,
                                                 ultima_dist="t"))
                    st.rerun()
            elif "≤ T ≤" in tipo_t:
                c1, c2 = st.columns(2)
                va = c1.number_input("Límite a", value=-2.0, step=0.1, format="%.4f", key="tt_ae")
                vb = c2.number_input("Límite b", value=2.0, step=0.1, format="%.4f", key="tt_be")
                if va >= vb:
                    st.warning("⚠️ a debe ser menor que b.")
                if st.button("Calcular", type="primary", key="btn_te", width='stretch'):
                    if va < vb:
                        r, ps, it, ev = calcular_t(gl_t, 'entre', va, vb)
                        st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                     ts_t="entre", la_t=va, lb_t=vb,
                                                     ultima_dist="t"))
                        st.rerun()
            else:
                alpha_t = st.select_slider("Nivel de significancia α", key="at_t",
                                           options=[0.10, 0.05, 0.01, 0.001], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico", type="primary",
                             key="btn_tvc", width='stretch'):
                    r, ps, it, ev = calcular_t(gl_t, 'valor_critico', alpha_t)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=True,
                                                 ts_t="entre", la_t=-r, lb_t=r,
                                                 ultima_dist="t"))
                    st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Muestras pequeñas (n &lt; 30) sin conocer σ poblacional. Muy usada en clínica. '
            '<strong>gl</strong> = n − 1. A mayor gl → más se parece a la Normal.</div>',
            unsafe_allow_html=True,
        )
        fig_t = crear_grafico("t", {"gl": gl_t},
                              st.session_state.get("ts_t"),
                              st.session_state.get("la_t"),
                              st.session_state.get("lb_t"))
        st.pyplot(fig_t, width='stretch')
        plt.close(fig_t)



# ── PESTAÑA: CHI-CUADRADO ────────────────────────────────────────
with tab_c:
    L, R = st.columns([1, 1.4], gap="large")

    with L:
        with st.container(border=True):
            paso_header(1, "Parámetros")
            gl_c = st.number_input("Grados de libertad (gl)", value=5,
                                   min_value=1, max_value=100, step=1, key="gl_c")
            st.caption(f"χ²({gl_c}): Media = {gl_c}  |  Varianza = {2*gl_c}")

        with st.container(border=True):
            paso_header(2, "¿Qué quieres calcular?")
            tipo_c = st.radio("", [
                "📉  P(χ² ≤ a) — probabilidad acumulada",
                "📈  P(χ² ≥ a) — p-valor de una prueba",
                "🔑  Valor crítico χ² (dado α)",
            ], key="tipo_c", label_visibility="collapsed")

        with st.container(border=True):
            paso_header(3, "Valores y cálculo")
            if "acumulada" in tipo_c:
                va = st.number_input("Valor de a", value=float(gl_c),
                                     min_value=0.001, step=0.5, format="%.4f", key="cc_a")
                if st.button("Calcular", type="primary", key="btn_ci", width='stretch'):
                    r, ps, it, ev = calcular_chi2(gl_c, 'izquierda', va)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=ev,
                                                 ts_c="izquierda", la_c=va,
                                                 ultima_dist="c"))
                    st.rerun()
            elif "p-valor" in tipo_c:
                va = st.number_input("Estadístico χ² calculado", value=float(gl_c),
                                     min_value=0.001, step=0.5, format="%.4f", key="cc_ad")
                if st.button("Calcular p-valor", type="primary",
                             key="btn_cd", width='stretch'):
                    r, ps, it, ev = calcular_chi2(gl_c, 'derecha', va)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=ev,
                                                 ts_c="derecha", la_c=va,
                                                 ultima_dist="c"))
                    st.rerun()
            else:
                alpha_c = st.select_slider("Nivel de significancia α", key="at_c",
                                           options=[0.10, 0.05, 0.01], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico", type="primary",
                             key="btn_cvc", width='stretch'):
                    r, ps, it, ev = calcular_chi2(gl_c, 'valor_critico', alpha_c)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=True,
                                                 ts_c="derecha", la_c=r,
                                                 ultima_dist="c"))
                    st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Para probar si dos variables categóricas están asociadas. '
            'Ej: ¿El sexo está asociado con tener diabetes? '
            '<strong>gl</strong> = (filas − 1) × (columnas − 1). Solo valores ≥ 0.</div>',
            unsafe_allow_html=True,
        )
        fig_c = crear_grafico("chi2", {"gl": gl_c},
                              st.session_state.get("ts_c"),
                              st.session_state.get("la_c"))
        st.pyplot(fig_c, width='stretch')
        plt.close(fig_c)



# ── PESTAÑA: F DE FISHER ─────────────────────────────────────────
with tab_f:
    L, R = st.columns([1, 1.4], gap="large")

    with L:
        with st.container(border=True):
            paso_header(1, "Parámetros")
            c1, c2 = st.columns(2)
            gl1_f = c1.number_input("gl₁  (grupos − 1)", value=3,
                                    min_value=1, max_value=100, step=1, key="gl1_f")
            gl2_f = c2.number_input("gl₂  (N total − grupos)", value=20,
                                    min_value=2, max_value=500, step=1, key="gl2_f")
            if gl2_f > 2:
                st.caption(f"F({gl1_f},{gl2_f}): Media ≈ {gl2_f/(gl2_f-2):.3f}")

        with st.container(border=True):
            paso_header(2, "¿Qué quieres calcular?")
            tipo_f = st.radio("", [
                "📈  P(F ≥ a) — p-valor del estadístico F",
                "🔑  Valor crítico F (dado α)",
            ], key="tipo_f", label_visibility="collapsed")

        with st.container(border=True):
            paso_header(3, "Valores y cálculo")
            if "p-valor" in tipo_f:
                va = st.number_input("Estadístico F calculado", value=2.0,
                                     min_value=0.001, step=0.1, format="%.4f", key="ff_a")
                if st.button("Calcular p-valor", type="primary",
                             key="btn_fd", width='stretch'):
                    r, ps, it, ev = calcular_f(gl1_f, gl2_f, 'derecha', va)
                    st.session_state.update(dict(r_f=r, ps_f=ps, it_f=it, ev_f=ev,
                                                 ts_f="derecha", la_f=va,
                                                 ultima_dist="f"))
                    st.rerun()
            else:
                alpha_f = st.select_slider("Nivel de significancia α", key="at_f",
                                           options=[0.10, 0.05, 0.01], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico F", type="primary",
                             key="btn_fvc", width='stretch'):
                    r, ps, it, ev = calcular_f(gl1_f, gl2_f, 'valor_critico', alpha_f)
                    st.session_state.update(dict(r_f=r, ps_f=ps, it_f=it, ev_f=True,
                                                 ts_f="derecha", la_f=r,
                                                 ultima_dist="f"))
                    st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Para comparar medias de 3 o más grupos (ANOVA). '
            'Ej: ¿Tres dietas producen pérdidas de peso distintas? '
            '<strong>gl₁</strong> = grupos − 1 &nbsp;·&nbsp; <strong>gl₂</strong> = N total − grupos.</div>',
            unsafe_allow_html=True,
        )
        fig_f = crear_grafico("f", {"gl1": gl1_f, "gl2": gl2_f},
                              st.session_state.get("ts_f"),
                              st.session_state.get("la_f"))
        st.pyplot(fig_f, width='stretch')
        plt.close(fig_f)



# ================================================================
# BLOQUE 7 — RESULTADO (fuera de los tabs, en su propio contenedor)
#
# Aparece únicamente después de presionar un botón de cálculo.
# ultima_dist indica qué distribución se calculó por última vez.
# ================================================================

_ud = st.session_state.get("ultima_dist")

if _ud == "n" and "r_n" in st.session_state:
    _ts = st.session_state.get("ts_n"); _la = st.session_state.get("la_n"); _lb = st.session_state.get("lb_n"); _r = st.session_state["r_n"]
    if _ts == "izquierda":
        _desc_g = (
            f"La curva en forma de campana representa la distribución Normal con "
            f"<b>μ = {media_n}</b> (centro) y <b>σ = {sigma_n}</b> (ancho). "
            f"La línea vertical en <b>a = {_la:.4f}</b> divide el área total en dos partes. "
            f"La <strong>zona azul sombreada a la izquierda</strong> acumula el <b>{_r*100:.2f}%</b> del área — "
            f"eso significa que el {_r*100:.2f}% de las observaciones son ≤ {_la:.4f}. "
            f"El área blanca restante ({(1-_r)*100:.2f}%) corresponde a P(X &gt; {_la:.4f})."
        )
    elif _ts == "derecha":
        _desc_g = (
            f"La campana está centrada en <b>μ = {media_n}</b> con dispersión <b>σ = {sigma_n}</b>. "
            f"La línea vertical en <b>a = {_la:.4f}</b> separa la cola derecha. "
            f"La <strong>zona azul sombreada a la derecha</strong> representa el <b>{_r*100:.2f}%</b> del área total — "
            f"la probabilidad de que una observación supere {_la:.4f}. "
            f"La parte izquierda sin sombrear ({(1-_r)*100:.2f}%) es P(X &lt; {_la:.4f}). "
            f"Recuerda: el área total bajo toda la curva siempre es 1 (= 100%)."
        )
    elif _ts == "entre":
        _desc_g = (
            f"La campana se centra en <b>μ = {media_n}</b>. Las dos líneas verticales marcan "
            f"<b>a = {_la:.4f}</b> y <b>b = {_lb:.4f}</b>. "
            f"La <strong>zona azul entre ambas líneas</strong> acumula el <b>{_r*100:.2f}%</b> del área — "
            f"la probabilidad de que X caiga en ese intervalo. "
            f"Las dos colas externas (sin sombra) suman el {(1-_r)*100:.2f}% restante: "
            f"{_r*50:.2f}% a cada lado aproximadamente."
        )
    else:
        _desc_g = (
            f"La línea vertical en <b>X = {_la:.4f}</b> es el percentil solicitado. "
            f"La <strong>zona azul a la izquierda</strong> representa exactamente el <b>{_r*100:.2f}%</b> del área total — "
            f"significa que el {_r*100:.2f}% de todos los valores de esta distribución "
            f"N(μ={media_n}, σ={sigma_n}) son menores que {_la:.4f}. "
            f"Solo el {(1-_r)*100:.2f}% de los valores superan ese punto."
        )
    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '📈 &nbsp;Distribución Normal</p>',
                unsafe_allow_html=True,
            )
            _fig = crear_grafico("normal", {"media": media_n, "sigma": sigma_n},
                                 _ts, _la, _lb)
            st.pyplot(_fig, width='stretch')
            plt.close(_fig)
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            mostrar_panel(_r, st.session_state["it_n"],
                          st.session_state["ps_n"], st.session_state.get("ev_n", False),
                          parte="resultado")
        with rR:
            mostrar_panel(_r, st.session_state["it_n"],
                          st.session_state["ps_n"], st.session_state.get("ev_n", False),
                          parte="pasos")

elif _ud == "t" and "r_t" in st.session_state:
    _ts = st.session_state.get("ts_t"); _la = st.session_state.get("la_t"); _lb = st.session_state.get("lb_t"); _r = st.session_state["r_t"]
    if _ts == "izquierda":
        _desc_g = (
            f"La curva t con <b>{gl_t} grados de libertad</b> es simétrica y acampanada, pero con "
            f"colas más gruesas que la Normal — esto refleja la mayor incertidumbre en muestras pequeñas. "
            f"La <strong>zona azul a la izquierda</strong> de <b>a = {_la:.4f}</b> acumula <b>P(T ≤ {_la:.4f}) = {_r:.4f}</b> ({_r*100:.2f}%). "
            f"A mayor número de gl, la curva t se acerca más a la Normal estándar."
        )
    elif _ts == "derecha":
        _desc_g = (
            f"La <strong>zona azul a la derecha</strong> de <b>a = {_la:.4f}</b> es el <b>p-valor = {_r:.4f}</b> ({_r*100:.2f}%). "
            f"El p-valor indica la probabilidad de obtener un estadístico tan extremo como el observado <em>si H₀ fuera verdadera</em>. "
            f"Con {gl_t} gl: si p-valor &lt; 0.05 → evidencia significativa para rechazar H₀; "
            f"si p-valor ≥ 0.05 → no hay suficiente evidencia para rechazarla."
        )
    elif _ts == "entre":
        _desc_g = (
            f"Las dos líneas verticales en <b>{_la:.4f}</b> y <b>{_lb:.4f}</b> son los valores críticos bilaterales. "
            f"La <strong>zona azul central</strong> ({_r*100:.2f}%) es la <em>región de no rechazo</em> de H₀. "
            f"Las <strong>dos colas externas</strong> ({(1-_r)*100:.2f}% en total, {(1-_r)*50:.2f}% cada una) "
            f"forman la región de rechazo bilateral con {gl_t} grados de libertad."
        )
    else:
        _desc_g = (
            f"Las líneas verticales marcan los <b>valores críticos ±{_lb:.4f}</b> con {gl_t} gl. "
            f"Si el estadístico t calculado en tu experimento supera este umbral en valor absoluto, "
            f"cae en la zona de rechazo (colas sombreadas). "
            f"Regla: <b>|t calculado| &gt; {_lb:.4f}</b> → se rechaza H₀ al nivel α especificado."
        )
    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '📉 &nbsp;Distribución t de Student</p>',
                unsafe_allow_html=True,
            )
            _fig = crear_grafico("t", {"gl": gl_t}, _ts, _la, _lb)
            st.pyplot(_fig, width='stretch')
            plt.close(_fig)
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            mostrar_panel(_r, st.session_state["it_t"],
                          st.session_state["ps_t"], st.session_state.get("ev_t", False),
                          parte="resultado")
        with rR:
            mostrar_panel(_r, st.session_state["it_t"],
                          st.session_state["ps_t"], st.session_state.get("ev_t", False),
                          parte="pasos")

elif _ud == "c" and "r_c" in st.session_state:
    _ts = st.session_state.get("ts_c"); _la = st.session_state.get("la_c"); _r = st.session_state["r_c"]
    if _ts == "izquierda":
        _desc_g = (
            f"La distribución χ² con <b>{gl_c} grados de libertad</b> es <em>asimétrica hacia la derecha</em> "
            f"y solo toma valores ≥ 0 — a diferencia de la Normal, no es simétrica. "
            f"La <strong>zona azul a la izquierda</strong> de <b>χ² = {_la:.4f}</b> acumula el <b>{_r*100:.2f}%</b> del área. "
            f"A más grados de libertad, la curva se aplana y se desplaza a la derecha, acercándose a una forma más simétrica."
        )
    elif _ts == "derecha":
        _desc_g = (
            f"La <strong>zona azul a la derecha</strong> de <b>χ² = {_la:.4f}</b> es el <b>p-valor = {_r:.4f}</b> ({_r*100:.2f}%). "
            f"Esta cola derecha es la región donde caen los estadísticos χ² grandes — "
            f"que ocurren cuando hay gran discrepancia entre frecuencias observadas y esperadas. "
            f"Con {gl_c} gl: si p-valor &lt; 0.05 → existe asociación estadísticamente significativa (se rechaza H₀)."
        )
    else:
        _desc_g = (
            f"La línea vertical marca el <b>valor crítico χ² = {_la:.4f}</b> con {gl_c} gl. "
            f"La <strong>zona sombreada a la derecha</strong> representa el nivel de significancia α. "
            f"Si el estadístico χ² calculado de tu tabla supera este umbral, "
            f"los datos muestran una asociación estadísticamente significativa — se rechaza H₀."
        )
    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '📊 &nbsp;Distribución Chi-cuadrado χ²</p>',
                unsafe_allow_html=True,
            )
            _fig = crear_grafico("chi2", {"gl": gl_c}, _ts, _la)
            st.pyplot(_fig, width='stretch')
            plt.close(_fig)
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            mostrar_panel(_r, st.session_state["it_c"],
                          st.session_state["ps_c"], st.session_state.get("ev_c", False),
                          parte="resultado")
        with rR:
            mostrar_panel(_r, st.session_state["it_c"],
                          st.session_state["ps_c"], st.session_state.get("ev_c", False),
                          parte="pasos")

elif _ud == "f" and "r_f" in st.session_state:
    _ts = st.session_state.get("ts_f"); _la = st.session_state.get("la_f"); _r = st.session_state["r_f"]
    if _ts == "derecha" and not st.session_state.get("ev_f", False):
        _desc_g = (
            f"La distribución F con <b>gl₁ = {gl1_f}</b> (numerador) y <b>gl₂ = {gl2_f}</b> (denominador) "
            f"es asimétrica hacia la derecha y solo toma valores positivos. "
            f"La <strong>zona azul a la derecha</strong> de <b>F = {_la:.4f}</b> es el <b>p-valor = {_r:.4f}</b> ({_r*100:.2f}%). "
            f"Un F grande indica que la varianza entre grupos supera la varianza dentro de los grupos — "
            f"si p-valor &lt; 0.05, las medias de los grupos son estadísticamente diferentes (se rechaza H₀ en ANOVA)."
        )
    else:
        _desc_g = (
            f"La línea vertical marca el <b>valor crítico F = {_la:.4f}</b> con gl₁ = {gl1_f} y gl₂ = {gl2_f}. "
            f"La curva F es asimétrica y siempre positiva; su forma depende de ambos parámetros de grados de libertad. "
            f"Estadísticos F calculados que superen este umbral caen en la <strong>región de rechazo</strong> (cola derecha), "
            f"indicando que las varianzas o medias de los grupos difieren significativamente."
        )
    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '📋 &nbsp;Distribución F de Fisher</p>',
                unsafe_allow_html=True,
            )
            _fig = crear_grafico("f", {"gl1": gl1_f, "gl2": gl2_f}, _ts, _la)
            st.pyplot(_fig, width='stretch')
            plt.close(_fig)
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            mostrar_panel(_r, st.session_state["it_f"],
                          st.session_state["ps_f"], st.session_state.get("ev_f", False),
                          parte="resultado")
        with rR:
            mostrar_panel(_r, st.session_state["it_f"],
                          st.session_state["ps_f"], st.session_state.get("ev_f", False),
                          parte="pasos")


# ================================================================
# BLOQUE 8 — PIE DE PÁGINA
# ================================================================

st.divider()
st.markdown("""
<div style="text-align:center;color:#334155;font-size:.79rem;padding:4px 0 10px;">
  Proyecto de Software Pedagógico · Bioestadística · Alejandra Acosta<br>
  <em>El área bajo la curva = probabilidad. La altura de la curva ≠ probabilidad.</em>
</div>
""", unsafe_allow_html=True)
