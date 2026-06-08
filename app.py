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
    calcular_prueba_t,
    calcular_prueba_chi2_ind,
    calcular_prueba_fisher,
    crear_grafico,
    crear_grafico_fisher,
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
        '<span style="color:#F87171;font-size:.84rem;font-weight:700;margin-top:6px;display:block;">'
        'P(X = a) = 0 &nbsp;para cualquier valor puntual a</span>'
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
                                                 perc_frac_n=perc/100,
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
            paso_header(1, "Datos de la muestra")
            c1, c2 = st.columns(2)
            xbar_t = c1.number_input("Media muestral (x̄)", value=19.2,
                                     step=0.1, format="%.4f", key="xbar_t")
            mu0_t  = c2.number_input("Media hipotética (μ₀)", value=20.0,
                                     step=0.1, format="%.4f", key="mu0_t")
            c3, c4 = st.columns(2)
            s_val_t = c3.number_input("Desv. estándar muestral (s)", value=1.1,
                                      min_value=0.0001, step=0.1, format="%.4f", key="s_val_t")
            n_val_t = int(c4.number_input("Tamaño de muestra (n)", value=10,
                                          min_value=2, max_value=10000, step=1, key="n_val_t"))
            st.caption(f"gl = n − 1 = {n_val_t} − 1 = **{n_val_t - 1}**")
            alpha_val_t = st.select_slider(
                "Nivel de significancia α", key="alpha_val_t",
                options=[0.10, 0.05, 0.01, 0.001], value=0.05,
                format_func=lambda x: f"α = {x}  ({x*100:.1f}%)",
            )

        with st.container(border=True):
            paso_header(2, "Tipo de hipótesis")
            hip_radio_t = st.radio("", [
                "Bilateral  (H₁: μ ≠ μ₀)",
                "Cola izquierda  (H₁: μ < μ₀)",
                "Cola derecha  (H₁: μ > μ₀)",
            ], key="hip_radio_t", label_visibility="collapsed")
            _mu0_lbl = f"{mu0_t:g}"
            if "Bilateral" in hip_radio_t:
                _h0_lbl, _h1_lbl = f"H₀: μ = {_mu0_lbl}", f"H₁: μ ≠ {_mu0_lbl}"
            elif "izquierda" in hip_radio_t:
                _h0_lbl, _h1_lbl = f"H₀: μ = {_mu0_lbl}", f"H₁: μ < {_mu0_lbl}"
            else:
                _h0_lbl, _h1_lbl = f"H₀: μ = {_mu0_lbl}", f"H₁: μ > {_mu0_lbl}"
            st.markdown(
                f'<div class="ficha" style="text-align:center;">'
                f'<b>{_h0_lbl}</b>&nbsp;&nbsp;&nbsp;&nbsp;<b>{_h1_lbl}</b></div>',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            paso_header(3, "Calcular")
            if st.button("Calcular prueba t", type="primary",
                         key="btn_prueba_t", width='stretch'):
                _tipo_map = {
                    "Bilateral  (H₁: μ ≠ μ₀)":      "bilateral",
                    "Cola izquierda  (H₁: μ < μ₀)":  "izquierda",
                    "Cola derecha  (H₁: μ > μ₀)":    "derecha",
                }
                _tipo = _tipo_map[hip_radio_t]
                _res = calcular_prueba_t(xbar_t, mu0_t, s_val_t, n_val_t, alpha_val_t, _tipo)
                st.session_state.update(dict(
                    r_t=_res['p_val'], ps_t=_res['pasos'],
                    it_t=_res['interp'], ev_t=False,
                    ts_t=_res['shade_type'], la_t=_res['la'], lb_t=_res['lb'],
                    tc_t=_res['t_calc'], tcrit_t=_res['t_crit'],
                    gl_t=_res['gl'], dec_t=_res['rechazar'],
                    hip_t=_tipo, alpha_t_res=alpha_val_t,
                    ultima_dist="t",
                ))
                st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Contrasta si la media de una muestra difiere de un valor hipotético μ₀ '
            'cuando σ poblacional es <strong>desconocida</strong>. '
            'Se aplica con cualquier n cuando no se conoce la desviación estándar poblacional.</div>',
            unsafe_allow_html=True,
        )
        _gl_prev = max(1, n_val_t - 1)
        fig_t = crear_grafico("t", {"gl": _gl_prev},
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
            paso_header(1, "Tabla de frecuencias observadas")
            cr1, cr2 = st.columns(2)
            lbl_r1_chi2 = cr1.text_input("Etiqueta fila 1",    value="Expuestos",    key="lbl_r1_chi2")
            lbl_r2_chi2 = cr2.text_input("Etiqueta fila 2",    value="No expuestos", key="lbl_r2_chi2")
            cc1, cc2 = st.columns(2)
            lbl_c1_chi2 = cc1.text_input("Etiqueta columna 1", value="Evento",       key="lbl_c1_chi2")
            lbl_c2_chi2 = cc2.text_input("Etiqueta columna 2", value="No evento",    key="lbl_c2_chi2")

            st.caption(f"**{lbl_r1_chi2}**")
            ca1, ca2 = st.columns(2)
            a_chi2 = int(ca1.number_input(
                f"a  ({lbl_c1_chi2})", value=38,  min_value=0, step=1, key="a_chi2"))
            b_chi2 = int(ca2.number_input(
                f"b  ({lbl_c2_chi2})", value=462, min_value=0, step=1, key="b_chi2"))

            st.caption(f"**{lbl_r2_chi2}**")
            ca3, ca4 = st.columns(2)
            c_chi2 = int(ca3.number_input(
                f"c  ({lbl_c1_chi2})", value=22,  min_value=0, step=1, key="c_chi2"))
            d_chi2 = int(ca4.number_input(
                f"d  ({lbl_c2_chi2})", value=478, min_value=0, step=1, key="d_chi2"))

            _N_prev = a_chi2 + b_chi2 + c_chi2 + d_chi2
            st.caption(
                f"n₁={a_chi2+b_chi2} | n₂={c_chi2+d_chi2} | "
                f"{lbl_c1_chi2}={a_chi2+c_chi2} | {lbl_c2_chi2}={b_chi2+d_chi2} | **N={_N_prev}**"
            )
            alpha_chi2 = st.select_slider(
                "Nivel de significancia α", key="alpha_chi2",
                options=[0.10, 0.05, 0.01], value=0.05,
                format_func=lambda x: f"α = {x}  ({x*100:.1f}%)",
            )

        with st.container(border=True):
            paso_header(2, "Hipótesis")
            st.markdown(
                '<div class="ficha" style="text-align:center;">'
                '<b>H₀:</b> No existe asociación entre las variables'
                '&emsp;&emsp;'
                '<b>H₁:</b> Existe asociación entre las variables'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="ficha" style="font-size:.83rem;margin-top:6px;">'
                '<span class="ficha-lbl">Tipo:</span>'
                'Prueba bilateral · cola derecha · gl = (2−1)(2−1) = 1'
                '</div>',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            paso_header(3, "Calcular")
            if st.button("Calcular prueba χ²", type="primary",
                         key="btn_chi2ind", width='stretch'):
                _res_ci = calcular_prueba_chi2_ind(
                    a_chi2, b_chi2, c_chi2, d_chi2, alpha_chi2,
                    lbl_r1_chi2, lbl_r2_chi2, lbl_c1_chi2, lbl_c2_chi2,
                )
                st.session_state.update(dict(
                    r_chi2ind    = _res_ci['chi2_stat'],
                    ps_chi2ind   = _res_ci['pasos'],
                    it_chi2ind   = _res_ci['conclusion'],
                    ts_chi2ind   = "derecha",
                    la_chi2ind   = _res_ci['chi2_stat'],
                    gl_chi2ind   = _res_ci['gl'],
                    pv_chi2ind   = _res_ci['p_val'],
                    crit_chi2ind = _res_ci['chi2_crit'],
                    dec_chi2ind  = _res_ci['rechazar'],
                    epi_chi2ind  = _res_ci['epi'],
                    ultima_dist  = "chi2ind",
                ))
                st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Evalúa si dos variables categóricas están <strong>asociadas</strong> en estudios '
            'epidemiológicos, clínicos o de salud pública (ej: exposición–enfermedad). '
            'Incluye RR, OR, DAR y NNH/NNT automáticamente.</div>',
            unsafe_allow_html=True,
        )
        _gl_ci_prev = st.session_state.get("gl_chi2ind", 1)
        _la_ci_prev = st.session_state.get("la_chi2ind")
        fig_chi2ind = crear_grafico(
            "chi2", {"gl": _gl_ci_prev},
            "derecha" if _la_ci_prev else None, _la_ci_prev,
        )
        st.pyplot(fig_chi2ind, width='stretch')
        plt.close(fig_chi2ind)



# ── PESTAÑA: F DE FISHER ─────────────────────────────────────────
with tab_f:
    L, R = st.columns([1, 1.4], gap="large")

    with L:
        with st.container(border=True):
            paso_header(1, "Datos observados")
            fr1, fr2 = st.columns(2)
            lbl_r1_fsh = fr1.text_input("Etiqueta fila 1",    value="Grupo 1",   key="lbl_r1_fsh")
            lbl_r2_fsh = fr2.text_input("Etiqueta fila 2",    value="Grupo 2",   key="lbl_r2_fsh")
            fc1, fc2 = st.columns(2)
            lbl_c1_fsh = fc1.text_input("Etiqueta columna 1", value="Evento",    key="lbl_c1_fsh")
            lbl_c2_fsh = fc2.text_input("Etiqueta columna 2", value="No evento", key="lbl_c2_fsh")

            st.caption(f"**{lbl_r1_fsh}**")
            fa1, fa2 = st.columns(2)
            a_fsh = int(fa1.number_input(
                f"a  ({lbl_c1_fsh})", value=4,  min_value=0, step=1, key="a_fsh"))
            b_fsh = int(fa2.number_input(
                f"b  ({lbl_c2_fsh})", value=11, min_value=0, step=1, key="b_fsh"))

            st.caption(f"**{lbl_r2_fsh}**")
            fa3, fa4 = st.columns(2)
            c_fsh = int(fa3.number_input(
                f"c  ({lbl_c1_fsh})", value=0,  min_value=0, step=1, key="c_fsh"))
            d_fsh = int(fa4.number_input(
                f"d  ({lbl_c2_fsh})", value=15, min_value=0, step=1, key="d_fsh"))

            _N_fsh = a_fsh + b_fsh + c_fsh + d_fsh
            st.caption(
                f"n₁={a_fsh+b_fsh} | n₂={c_fsh+d_fsh} | "
                f"{lbl_c1_fsh}={a_fsh+c_fsh} | {lbl_c2_fsh}={b_fsh+d_fsh} | **N={_N_fsh}**"
            )
            alpha_fsh = st.select_slider(
                "Nivel de significancia α", key="alpha_fsh",
                options=[0.10, 0.05, 0.01], value=0.05,
                format_func=lambda x: f"α = {x}  ({x*100:.1f}%)",
            )

        with st.container(border=True):
            paso_header(2, "Tipo de prueba e hipótesis")
            tipo_fsh = st.radio("", [
                "↔️  Bilateral (dos colas)",
                "⬅️  Unilateral izquierda",
                "➡️  Unilateral derecha",
            ], key="tipo_fsh", label_visibility="collapsed")
            st.markdown(
                '<div class="ficha" style="text-align:center;">'
                '<b>H₀:</b> No existe asociación entre las variables'
                '&emsp;&emsp;'
                '<b>H₁:</b> Existe asociación entre las variables'
                '</div>',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            paso_header(3, "Calcular")
            _val_ok = _N_fsh > 0
            if not _val_ok:
                st.warning("⚠️ El total general debe ser mayor que cero.")
            if st.button("Calcular prueba exacta de Fisher", type="primary",
                         key="btn_fisher", width='stretch',
                         disabled=not _val_ok):
                _tipo_map_fsh = {
                    "↔️  Bilateral (dos colas)": "bilateral",
                    "⬅️  Unilateral izquierda":  "izquierda",
                    "➡️  Unilateral derecha":    "derecha",
                }
                _tipo_f = _tipo_map_fsh[tipo_fsh]
                _res_fsh = calcular_prueba_fisher(
                    a_fsh, b_fsh, c_fsh, d_fsh, alpha_fsh, _tipo_f,
                    lbl_r1_fsh, lbl_r2_fsh, lbl_c1_fsh, lbl_c2_fsh,
                )
                st.session_state.update(dict(
                    r_fisher    = _res_fsh['OR'],
                    ps_fisher   = _res_fsh['pasos'],
                    it_fisher   = _res_fsh['conclusion'],
                    pv_fisher   = _res_fsh['p_val'],
                    dec_fisher  = _res_fsh['rechazar'],
                    OR_fsh      = _res_fsh['OR'],
                    OR_str_fsh  = _res_fsh['OR_str'],
                    OR_interp_fsh = _res_fsh['OR_interp'],
                    any_small_fsh = _res_fsh['any_small'],
                    epi_fisher  = _res_fsh['epi'],
                    exp_fisher  = _res_fsh['expected'],
                    obs_fisher  = {'a': a_fsh, 'b': b_fsh, 'c': c_fsh, 'd': d_fsh},
                    lbls_fisher = (lbl_r1_fsh, lbl_r2_fsh, lbl_c1_fsh, lbl_c2_fsh),
                    alpha_fisher = alpha_fsh,
                    ultima_dist = "fisher",
                ))
                st.rerun()

    with R:
        st.markdown(
            '<div class="ficha"><span class="ficha-lbl">¿Cuándo se usa?</span>'
            'Cuando las frecuencias esperadas son pequeñas (&lt;5) y χ² no es adecuada. '
            'Ideal en <strong>farmacovigilancia, estudios clínicos, epidemiología</strong> '
            'con muestras pequeñas o eventos raros. Calcula probabilidades exactas '
            'mediante la distribución hipergeométrica.</div>',
            unsafe_allow_html=True,
        )
        _obs_p = st.session_state.get("obs_fisher", {'a': 4, 'b': 11, 'c': 0, 'd': 15})
        _exp_p = st.session_state.get("exp_fisher", {'E11': 2.0, 'E12': 13.0, 'E21': 2.0, 'E22': 13.0})
        _ll_p  = st.session_state.get("lbls_fisher", ("Grupo 1", "Grupo 2", "Evento", "No evento"))
        fig_fsh = crear_grafico_fisher(
            _obs_p['a'], _obs_p['b'], _obs_p['c'], _obs_p['d'],
            _exp_p['E11'], _exp_p['E12'], _exp_p['E21'], _exp_p['E22'],
            _ll_p[0], _ll_p[1], _ll_p[2], _ll_p[3],
        )
        st.pyplot(fig_fsh, width='stretch')
        plt.close(fig_fsh)


# ================================================================
# BLOQUE 7 — RESULTADO (fuera de los tabs, en su propio contenedor)
#
# Aparece únicamente después de presionar un botón de cálculo.
# ultima_dist indica qué distribución se calculó por última vez.
# ================================================================

_ud = st.session_state.get("ultima_dist")

if _ud == "n" and "r_n" in st.session_state:
    _ts = st.session_state.get("ts_n"); _la = st.session_state.get("la_n"); _lb = st.session_state.get("lb_n"); _r = st.session_state["r_n"]
    _ev_n = st.session_state.get("ev_n", False)
    _perc_frac = st.session_state.get("perc_frac_n", 0.95)
    if _ts == "izquierda" and _ev_n:
        # Percentile case: _r is an X value, not a probability — use _perc_frac for the area
        _desc_g = (
            f"La línea vertical en <b>X = {_la:.4f}</b> es el percentil {_perc_frac*100:.0f} "
            f"de la distribución N(μ={media_n}, σ={sigma_n}). "
            f"La <strong>zona azul a la izquierda</strong> representa el "
            f"<b>{_perc_frac*100:.1f}%</b> del área total bajo la curva — "
            f"el {_perc_frac*100:.1f}% de todos los valores posibles son menores que {_la:.4f}. "
            f"Solo el {(1-_perc_frac)*100:.1f}% del área queda a la derecha. "
            f"Recuerda: esta área sombreada ES la probabilidad (P(X &lt; {_la:.4f}) = {_perc_frac:.4f}), "
            f"no la altura de la curva en ese punto."
        )
    elif _ts == "izquierda":
        _desc_g = (
            f"La curva en forma de campana representa la distribución Normal con "
            f"<b>μ = {media_n}</b> (centro) y <b>σ = {sigma_n}</b> (ancho). "
            f"La línea vertical en <b>a = {_la:.4f}</b> divide el área total en dos partes. "
            f"La <strong>zona azul sombreada a la izquierda</strong> acumula el <b>{_r*100:.2f}%</b> del área — "
            f"el área bajo la curva hasta a es P(X ≤ {_la:.4f}) = {_r:.4f}. "
            f"La zona sin sombra (área derecha = {(1-_r)*100:.2f}%) corresponde a P(X &gt; {_la:.4f})."
        )
    elif _ts == "derecha":
        _desc_g = (
            f"La campana está centrada en <b>μ = {media_n}</b> con dispersión <b>σ = {sigma_n}</b>. "
            f"La línea vertical en <b>a = {_la:.4f}</b> separa la cola derecha. "
            f"La <strong>zona azul sombreada a la derecha</strong> es el <b>{_r*100:.2f}%</b> del área total — "
            f"el área bajo la curva desde a en adelante es P(X ≥ {_la:.4f}) = {_r:.4f}. "
            f"La zona izquierda (área = {(1-_r)*100:.2f}%) es P(X &lt; {_la:.4f}). "
            f"Área total bajo toda la curva = 1 (= 100%)."
        )
    elif _ts == "entre":
        _desc_g = (
            f"La campana se centra en <b>μ = {media_n}</b>. Las dos líneas verticales marcan "
            f"<b>a = {_la:.4f}</b> y <b>b = {_lb:.4f}</b>. "
            f"La <strong>zona azul entre ambas líneas</strong> es el <b>{_r*100:.2f}%</b> del área total — "
            f"el área bajo la curva entre a y b es P({_la:.4f} ≤ X ≤ {_lb:.4f}) = {_r:.4f}. "
            f"Las dos colas externas (áreas sin sombra) acumulan el {(1-_r)*100:.2f}% restante."
        )
    else:
        _desc_g = f"Distribución Normal N(μ={media_n}, σ={sigma_n}). La zona sombreada representa el área = probabilidad."
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
            mostrar_panel(_r, st.session_state["it_n"],
                          st.session_state["ps_n"], st.session_state.get("ev_n", False),
                          parte="resultado")
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            if _ts == "izquierda" and _ev_n:
                _interp_n = (
                    f"El valor <b>{_la:.4f}</b> es el percentil {_perc_frac*100:.0f} de "
                    f"N(μ={media_n}, σ={sigma_n}). Se espera que el "
                    f"<b>{_perc_frac*100:.1f}%</b> de las observaciones sean menores que "
                    f"este punto, y el <b>{(1-_perc_frac)*100:.1f}%</b> lo supere."
                )
            elif _ts == "izquierda":
                _interp_n = (
                    f"Se espera que aproximadamente el <b>{_r*100:.1f}%</b> de las "
                    f"observaciones de N(μ={media_n}, σ={sigma_n}) sean menores o iguales "
                    f"a <b>{_la:.4f}</b>. El restante <b>{(1-_r)*100:.1f}%</b> supera ese valor."
                )
            elif _ts == "derecha":
                _interp_n = (
                    f"Se espera que aproximadamente el <b>{_r*100:.1f}%</b> de las "
                    f"observaciones superen <b>{_la:.4f}</b>. "
                    f"El <b>{(1-_r)*100:.1f}%</b> restante queda por debajo de ese punto."
                )
            elif _ts == "entre":
                _interp_n = (
                    f"Se espera que aproximadamente el <b>{_r*100:.1f}%</b> de las "
                    f"observaciones de N(μ={media_n}, σ={sigma_n}) se encuentren entre "
                    f"<b>{_la:.4f}</b> y <b>{_lb:.4f}</b>. "
                    f"Las dos colas externas acumulan el restante <b>{(1-_r)*100:.1f}%</b>."
                )
            else:
                _interp_n = f"La zona sombreada representa el <b>{_r*100:.2f}%</b> del área bajo la curva."
            st.markdown(
                f'<div style="background:#050F1E;border-left:4px solid #3B82F6;'
                f'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px;">'
                f'<p style="color:#60A5FA;font-weight:700;font-size:.75rem;letter-spacing:.6px;'
                f'text-transform:uppercase;margin:0 0 6px;">📊 Interpretación del área calculada</p>'
                f'<p style="color:#94A3B8;font-size:.83rem;line-height:1.7;margin:0;">{_interp_n}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with rR:
            mostrar_panel(_r, st.session_state["it_n"],
                          st.session_state["ps_n"], st.session_state.get("ev_n", False),
                          parte="pasos")

elif _ud == "t" and "r_t" in st.session_state:
    _ts   = st.session_state.get("ts_t")
    _la   = st.session_state.get("la_t")
    _lb   = st.session_state.get("lb_t")
    _r    = st.session_state["r_t"]
    gl_t  = st.session_state.get("gl_t", 9)
    _tc   = st.session_state.get("tc_t")
    _tcrit = st.session_state.get("tcrit_t")
    _dec  = st.session_state.get("dec_t", False)
    _hip  = st.session_state.get("hip_t", "bilateral")
    _alpha_r = st.session_state.get("alpha_t_res", 0.05)

    _tc_display    = f"{_tc:.4f}"    if _tc    is not None else "—"
    _tcrit_display = f"±{_tcrit:.4f}" if (_tcrit is not None and _hip == "bilateral") \
                     else (f"{_tcrit:.4f}" if _tcrit is not None else "—")

    if _ts == "colas" and _tc is not None:
        _desc_g = (
            f"La curva t({gl_t}) muestra las dos <strong>regiones de rechazo sombreadas</strong> "
            f"más allá de ±|t| = ±<b>{abs(_tc):.4f}</b>. "
            f"El área total sombreada es el p-valor = <b>{_r:.4f}</b> ({_r*100:.2f}%). "
            f"{'Como p &lt; α → se rechaza H₀.' if _dec else 'Como p ≥ α → no se rechaza H₀.'}"
        )
    elif _ts == "izquierda" and _tc is not None:
        _desc_g = (
            f"La <strong>zona azul a la izquierda</strong> de t = <b>{_tc:.4f}</b> "
            f"es el p-valor = <b>{_r:.4f}</b> ({_r*100:.2f}%). "
            f"Con {gl_t} gl: "
            f"{'p &lt; α → se rechaza H₀.' if _dec else 'p ≥ α → no se rechaza H₀.'}"
        )
    elif _ts == "derecha" and _tc is not None:
        _desc_g = (
            f"La <strong>zona azul a la derecha</strong> de t = <b>{_tc:.4f}</b> "
            f"es el p-valor = <b>{_r:.4f}</b> ({_r*100:.2f}%). "
            f"Con {gl_t} gl: "
            f"{'p &lt; α → se rechaza H₀.' if _dec else 'p ≥ α → no se rechaza H₀.'}"
        )
    else:
        _desc_g = f"Distribución t({gl_t}). La zona sombreada es el p-valor = <b>{_r:.4f}</b>."

    _dec_color = "#10B981" if _dec else "#F59E0B"
    _dec_text  = "✗  Rechazar H₀" if _dec else "✓  No rechazar H₀"

    _cards_html = f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;
                    text-transform:uppercase;">Estadístico t</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;
                    margin-top:4px;">{_tc_display}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;
                    text-transform:uppercase;">Grados de libertad</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;
                    margin-top:4px;">{gl_t}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;
                    text-transform:uppercase;">Valor crítico t</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;
                    margin-top:4px;">{_tcrit_display}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;
                    text-transform:uppercase;">Valor p</div>
        <div style="font-size:1.3rem;font-weight:700;color:#6EE7B7;
                    margin-top:4px;">{_r:.4f}</div>
      </div>
    </div>
    <div style="background:#0D1628;border:2px solid {_dec_color}55;border-radius:10px;
                padding:12px 14px;text-align:center;margin-bottom:10px;">
      <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;
                  text-transform:uppercase;">Decisión</div>
      <div style="font-size:1.15rem;font-weight:700;color:{_dec_color};
                  margin-top:4px;">{_dec_text}</div>
    </div>
    """

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
            if _ts == "colas" and _tc is not None:
                _interp_t = (
                    f"Si H₀ fuera cierta, existiría un <b>{_r*100:.2f}%</b> de probabilidad "
                    f"de obtener |t| ≥ <b>{abs(_tc):.4f}</b> solo por azar con {gl_t} gl "
                    f"(prueba bilateral). "
                    f"{'Como p &lt; α, esta evidencia es suficiente para <b>rechazar H₀</b>.' if _dec else 'Como p ≥ α, no hay evidencia suficiente para rechazar H₀.'}"
                )
            elif _ts == "izquierda" and _tc is not None:
                _interp_t = (
                    f"Si H₀ fuera cierta, existiría un <b>{_r*100:.2f}%</b> de probabilidad "
                    f"de obtener t ≤ <b>{_tc:.4f}</b> solo por azar con {gl_t} gl. "
                    f"{'Como p &lt; α, esta evidencia es suficiente para <b>rechazar H₀</b>.' if _dec else 'Como p ≥ α, no hay evidencia suficiente para rechazar H₀.'}"
                )
            elif _ts == "derecha" and _tc is not None:
                _interp_t = (
                    f"Si H₀ fuera cierta, existiría un <b>{_r*100:.2f}%</b> de probabilidad "
                    f"de obtener t ≥ <b>{_tc:.4f}</b> solo por azar con {gl_t} gl. "
                    f"{'Como p &lt; α, esta evidencia es suficiente para <b>rechazar H₀</b>.' if _dec else 'Como p ≥ α, no hay evidencia suficiente para rechazar H₀.'}"
                )
            else:
                _interp_t = f"La zona sombreada es el p-valor = <b>{_r:.4f}</b> con {gl_t} gl."
            st.markdown(
                f'<div style="background:#050F1E;border-left:4px solid #F97316;'
                f'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px;">'
                f'<p style="color:#FB923C;font-weight:700;font-size:.75rem;letter-spacing:.6px;'
                f'text-transform:uppercase;margin:0 0 6px;">📊 Interpretación del p-valor</p>'
                f'<p style="color:#94A3B8;font-size:.83rem;line-height:1.7;margin:0;">{_interp_t}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with rR:
            st.markdown(_cards_html, unsafe_allow_html=True)
            mostrar_panel(_r, st.session_state["it_t"],
                          st.session_state["ps_t"], False,
                          parte="pasos")

elif _ud == "chi2ind" and "r_chi2ind" in st.session_state:
    _chi2_s  = st.session_state["r_chi2ind"]
    _pv_ci   = st.session_state.get("pv_chi2ind", 0.0)
    _gl_ci   = st.session_state.get("gl_chi2ind", 1)
    _crit_ci = st.session_state.get("crit_chi2ind", 0.0)
    _dec_ci  = st.session_state.get("dec_chi2ind", False)
    _epi     = st.session_state.get("epi_chi2ind", {})
    _ps_ci   = st.session_state.get("ps_chi2ind", [])
    _it_ci   = st.session_state.get("it_chi2ind", "")

    _dec_color = "#10B981" if _dec_ci else "#F59E0B"
    _dec_text  = "✗  Rechazar H₀" if _dec_ci else "✓  No rechazar H₀"

    _RR       = _epi.get('RR');        _OR       = _epi.get('OR')
    _DAR      = _epi.get('DAR');       _NNX      = _epi.get('NNX')
    _NNX_type = _epi.get('NNX_type', '—')
    _RR_i  = _epi.get('RR_interp',  ''); _OR_i  = _epi.get('OR_interp',  '')
    _DAR_i = _epi.get('DAR_interp', ''); _NNX_i = _epi.get('NNX_interp', '')

    _RR_d  = f"{_RR:.3f}"  if _RR  is not None else "—"
    _OR_d  = f"{_OR:.3f}"  if _OR  is not None else "—"
    _DAR_d = f"{_DAR*100:.2f}%" if _DAR is not None else "—"
    _NNX_d = f"{int(round(_NNX))}" if _NNX is not None else "—"

    _desc_g = (
        f"La distribución χ²({_gl_ci}) es asimétrica hacia la derecha. "
        f"La <strong>zona azul a la derecha</strong> de χ² = <b>{_chi2_s:.4f}</b> "
        f"es el p-valor = <b>{_pv_ci:.4f}</b>. "
        f"{'Como p &lt; α → se rechaza H₀: existe asociación.' if _dec_ci else 'Como p ≥ α → no se rechaza H₀.'}"
    )

    _cards_ci = f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">χ² calculado</div>
        <div style="font-size:1.3rem;font-weight:700;color:#A855F7;margin-top:4px;">{_chi2_s:.4f}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Valor p</div>
        <div style="font-size:1.3rem;font-weight:700;color:#6EE7B7;margin-top:4px;">{_pv_ci:.4f}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Grados de libertad</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;margin-top:4px;">{_gl_ci}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">χ² crítico</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;margin-top:4px;">{_crit_ci:.4f}</div>
      </div>
    </div>
    <div style="background:#0D1628;border:2px solid {_dec_color}55;border-radius:10px;
                padding:12px 14px;text-align:center;margin-bottom:12px;">
      <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Decisión</div>
      <div style="font-size:1.15rem;font-weight:700;color:{_dec_color};margin-top:4px;">{_dec_text}</div>
    </div>
    <p style="color:#CBD5E1;margin:6px 0 8px;font-weight:600;font-size:.85rem;
              letter-spacing:.4px;text-transform:uppercase;">Medidas Epidemiológicas</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">Riesgo Relativo (RR)</div>
        <div style="font-size:1.15rem;font-weight:700;color:#60A5FA;margin:3px 0;">{_RR_d}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_RR_i}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">Odds Ratio (OR)</div>
        <div style="font-size:1.15rem;font-weight:700;color:#60A5FA;margin:3px 0;">{_OR_d}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_OR_i}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">DAR</div>
        <div style="font-size:1.15rem;font-weight:700;color:#60A5FA;margin:3px 0;">{_DAR_d}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_DAR_i}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">{_NNX_type}</div>
        <div style="font-size:1.15rem;font-weight:700;color:#60A5FA;margin:3px 0;">{_NNX_d}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_NNX_i}</div>
      </div>
    </div>
    """

    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#A855F7;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '🧪 &nbsp;Prueba χ² de Independencia</p>',
                unsafe_allow_html=True,
            )
            _fig_ci = crear_grafico("chi2", {"gl": _gl_ci}, "derecha", _chi2_s)
            st.pyplot(_fig_ci, width='stretch')
            plt.close(_fig_ci)
            st.markdown(f'<div class="ficha">{_desc_g}</div>', unsafe_allow_html=True)
            _interp_ci = (
                f"El área sombreada (p = <b>{_pv_ci:.4f}</b>) es la probabilidad de "
                f"observar discrepancias iguales o mayores que χ² = <b>{_chi2_s:.4f}</b> "
                f"si las variables fueran independientes ({_gl_ci} gl). "
                + (
                    "Como p &lt; α, esta evidencia es suficiente para "
                    "<b>rechazar H₀</b>: existe asociación estadística entre las variables."
                    if _dec_ci else
                    "Como p ≥ α, no hay evidencia suficiente para rechazar la "
                    "hipótesis de independencia entre las variables."
                )
            )
            st.markdown(
                f'<div style="background:#050F1E;border-left:4px solid #A855F7;'
                f'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px;">'
                f'<p style="color:#C084FC;font-weight:700;font-size:.75rem;letter-spacing:.6px;'
                f'text-transform:uppercase;margin:0 0 6px;">📊 Interpretación del p-valor</p>'
                f'<p style="color:#94A3B8;font-size:.83rem;line-height:1.7;margin:0;">{_interp_ci}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with rR:
            st.markdown(_cards_ci, unsafe_allow_html=True)
            mostrar_panel(_chi2_s, _it_ci, _ps_ci, False, parte="pasos")

elif _ud == "fisher" and "r_fisher" in st.session_state:
    _pv_fsh   = st.session_state.get("pv_fisher", 1.0)
    _dec_fsh  = st.session_state.get("dec_fisher", False)
    _OR_v     = st.session_state.get("OR_fsh")
    _OR_s     = st.session_state.get("OR_str_fsh", "—")
    _OR_i     = st.session_state.get("OR_interp_fsh", "")
    _any_sm   = st.session_state.get("any_small_fsh", False)
    _epi_fsh  = st.session_state.get("epi_fisher", {})
    _ps_fsh   = st.session_state.get("ps_fisher", [])
    _it_fsh   = st.session_state.get("it_fisher", "")
    _obs_fsh  = st.session_state.get("obs_fisher", {'a': 4, 'b': 11, 'c': 0, 'd': 15})
    _exp_fsh  = st.session_state.get("exp_fisher", {'E11': 2.0, 'E12': 13.0, 'E21': 2.0, 'E22': 13.0})
    _ll_fsh   = st.session_state.get("lbls_fisher", ("Grupo 1", "Grupo 2", "Evento", "No evento"))
    _a_fsh    = st.session_state.get("alpha_fisher", 0.05)

    _dec_color = "#10B981" if _dec_fsh else "#F59E0B"
    _dec_text  = "✗  Rechazar H₀" if _dec_fsh else "✓  No rechazar H₀"

    _RR_fsh   = _epi_fsh.get('RR_str', '—')
    _DAR_fsh  = _epi_fsh.get('DAR')
    _NNX_fsh  = _epi_fsh.get('NNX')
    _NNX_type_fsh = _epi_fsh.get('NNX_type', '—')
    _RR_i_fsh  = _epi_fsh.get('RR_interp',  '')
    _DAR_i_fsh = _epi_fsh.get('DAR_interp', '')
    _NNX_i_fsh = _epi_fsh.get('NNX_interp', '')
    _DAR_d_fsh = f"{_DAR_fsh*100:.2f}%" if _DAR_fsh is not None else "—"
    _NNX_d_fsh = f"{int(round(_NNX_fsh))}" if _NNX_fsh is not None else "—"

    _desc_g_fsh = (
        "Barras <strong style='color:#EF4444;'>rojas</strong> = frecuencias observadas · "
        "Barras grises = frecuencias esperadas bajo H₀. "
        + ("Las celdas marcadas ⚠ tienen frecuencia esperada &lt; 5 → <b>Fisher es apropiado</b>. "
           if _any_sm else "Todas las frecuencias esperadas ≥ 5. ") +
        f"p-valor = <b>{_pv_fsh:.4f}</b> {'→ se rechaza H₀.' if _dec_fsh else '→ no se rechaza H₀.'}"
    )

    _sm_badge = ('<span style="color:#6EE7B7;font-size:.75rem;">'
                 '✓ Fisher recomendado (E &lt; 5)</span>'
                 if _any_sm else
                 '<span style="color:#94A3B8;font-size:.75rem;">'
                 'También válida: χ²</span>')

    _cards_fsh = f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Odds Ratio</div>
        <div style="font-size:1.3rem;font-weight:700;color:#EF4444;margin-top:4px;">{_OR_s}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Valor p</div>
        <div style="font-size:1.3rem;font-weight:700;color:#6EE7B7;margin-top:4px;">{_pv_fsh:.4f}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">α</div>
        <div style="font-size:1.3rem;font-weight:700;color:#60A5FA;margin-top:4px;">{_a_fsh}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;
                  padding:12px 14px;text-align:center;">
        <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Frec. esperadas</div>
        <div style="font-size:.85rem;font-weight:600;margin-top:4px;">{_sm_badge}</div>
      </div>
    </div>
    <div style="background:#0D1628;border:1px solid #EF444440;border-radius:10px;
                padding:10px 14px;margin-bottom:10px;">
      <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">OR: interpretación</div>
      <div style="font-size:.88rem;color:#CBD5E1;margin-top:4px;line-height:1.5;">{_OR_i}</div>
    </div>
    <div style="background:#0D1628;border:2px solid {_dec_color}55;border-radius:10px;
                padding:12px 14px;text-align:center;margin-bottom:12px;">
      <div style="font-size:.7rem;color:#64748B;letter-spacing:.5px;text-transform:uppercase;">Decisión</div>
      <div style="font-size:1.15rem;font-weight:700;color:{_dec_color};margin-top:4px;">{_dec_text}</div>
    </div>
    <p style="color:#CBD5E1;margin:6px 0 8px;font-weight:600;font-size:.85rem;
              letter-spacing:.4px;text-transform:uppercase;">Medidas Epidemiológicas</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">Riesgo Relativo (RR)</div>
        <div style="font-size:1.15rem;font-weight:700;color:#EF4444;margin:3px 0;">{_RR_fsh}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_RR_i_fsh}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">DAR</div>
        <div style="font-size:1.15rem;font-weight:700;color:#EF4444;margin:3px 0;">{_DAR_d_fsh}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_DAR_i_fsh}</div>
      </div>
      <div style="background:#0D1628;border:1px solid #1E3055;border-radius:10px;padding:10px 12px;grid-column:span 2;">
        <div style="font-size:.68rem;color:#64748B;letter-spacing:.4px;text-transform:uppercase;">{_NNX_type_fsh}</div>
        <div style="font-size:1.15rem;font-weight:700;color:#EF4444;margin:3px 0;">{_NNX_d_fsh}</div>
        <div style="font-size:.75rem;color:#94A3B8;line-height:1.4;">{_NNX_i_fsh}</div>
      </div>
    </div>
    """

    with st.container(border=True):
        rL, rR = st.columns([1, 1.4], gap="large")
        with rL:
            st.markdown(
                '<p style="color:#EF4444;font-weight:700;font-size:.9rem;'
                'letter-spacing:.6px;text-transform:uppercase;margin:0 0 8px;">'
                '🔬 &nbsp;Prueba Exacta de Fisher</p>',
                unsafe_allow_html=True,
            )
            _fig_fsh = crear_grafico_fisher(
                _obs_fsh['a'], _obs_fsh['b'], _obs_fsh['c'], _obs_fsh['d'],
                _exp_fsh['E11'], _exp_fsh['E12'], _exp_fsh['E21'], _exp_fsh['E22'],
                _ll_fsh[0], _ll_fsh[1], _ll_fsh[2], _ll_fsh[3],
            )
            st.pyplot(_fig_fsh, width='stretch')
            plt.close(_fig_fsh)
            st.markdown(f'<div class="ficha">{_desc_g_fsh}</div>', unsafe_allow_html=True)
            _N_fsh_r = (_obs_fsh.get('a', 0) + _obs_fsh.get('b', 0)
                        + _obs_fsh.get('c', 0) + _obs_fsh.get('d', 0))
            _interp_fsh_r = (
                f"El p-valor exacto <b>{_pv_fsh:.4f}</b> es la probabilidad de obtener "
                f"esta tabla 2×2 (u otra más extrema en la misma dirección) con los "
                f"mismos totales marginales, asumiendo que H₀ es cierta (N = {_N_fsh_r}). "
                + (
                    "Como p &lt; α, existe evidencia estadística para "
                    "<b>rechazar H₀</b>: hay asociación significativa entre las variables."
                    if _dec_fsh else
                    "Como p ≥ α, no hay evidencia estadística suficiente para afirmar "
                    "que existe asociación entre las variables."
                )
            )
            st.markdown(
                f'<div style="background:#050F1E;border-left:4px solid #EF4444;'
                f'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px;">'
                f'<p style="color:#F87171;font-weight:700;font-size:.75rem;letter-spacing:.6px;'
                f'text-transform:uppercase;margin:0 0 6px;">📊 Interpretación del p-valor exacto</p>'
                f'<p style="color:#94A3B8;font-size:.83rem;line-height:1.7;margin:0;">{_interp_fsh_r}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with rR:
            st.markdown(_cards_fsh, unsafe_allow_html=True)
            mostrar_panel(_pv_fsh, _it_fsh, _ps_fsh, False, parte="pasos")


# ================================================================
# BLOQUE 8 — PIE DE PÁGINA
# ================================================================

st.divider()
st.markdown("""
<div style="text-align:center;color:#64748B;font-size:.79rem;padding:4px 0 10px;">
  Proyecto de Software Pedagógico · Bioestadística · Alejandra Acosta<br>
  <em style="color:#94A3B8;">El área bajo la curva = probabilidad &nbsp;·&nbsp; La altura de la curva = densidad f(x) ≠ probabilidad &nbsp;·&nbsp; P(X = a) = 0</em>
</div>
""", unsafe_allow_html=True)
