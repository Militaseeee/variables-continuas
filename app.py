# ============================================================
# app.py — Visualizador de Distribuciones Continuas
# Autora: Alejandra Acosta | Bioestadística | Tema 4
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(
    page_title="Distribuciones Continuas | Bioestadística",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PALETA DARK
#   fondo página    : #020817  (midnight navy)
#   fondo tarjeta   : #0D1628  (dark navy)
#   tarjeta elevada : #111E35  (navy medio)
#   borde           : #1E3055  (azul oscuro)
#   azul brillante  : #60A5FA  (accent primario)
#   azul glow       : #3B82F6
#   verde éxito     : #34D399
#   ámbar           : #FBBF24
#   texto claro     : #E2E8F0
#   texto suave     : #94A3B8
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ══ FONDO GLOBAL + FUENTE ══════════════════════════════ */
*, *::before, *::after,
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMarkdownContainer"],
button, input, label, p, span, div {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif !important;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background-color: #020817 !important; }

[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu, footer         { visibility: hidden !important; }
.block-container          { padding: 0.5rem 2.4rem 2rem !important; }

/* ══ INPUTS ═════════════════════════════════════════════ */
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

/* ══ LABELS / CAPTIONS ══════════════════════════════════ */
label, [data-testid="stWidgetLabel"] p,
[data-testid="stCaptionContainer"] p {
    color: #94A3B8 !important;
}

/* ══ RADIO BUTTONS ══════════════════════════════════════ */
[data-testid="stRadio"] label { color: #CBD5E1 !important; font-size: 0.93rem; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: #CBD5E1 !important; }

/* ══ SELECT SLIDER ══════════════════════════════════════ */
[data-testid="stSlider"] > div > div { background: #1E3055 !important; }
[data-testid="stSlider"] [role="slider"] { background: #60A5FA !important; }

/* ══ TABS ════════════════════════════════════════════════ */
[data-testid="stTabs"] > div:first-child {
    background: #0D1628;
    border-radius: 12px 12px 0 0;
    padding: 16px;
    border-bottom: 1px solid #1E3055;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
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
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 24px 28px !important;
}

/* ══ CONTAINERS CON BORDE ═══════════════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0D1628 !important;
    border: 1px solid #1E3055 !important;
    border-radius: 12px !important;
}

/* ══ EXPANDERS ══════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: #0D1628 !important;
    border: 1px solid #1E3055 !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary p { color: #94A3B8 !important; }
[data-testid="stExpander"] summary svg { fill: #64748B !important; }

/* ══ ALERTS ════════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    background: #0D1628 !important;
}

/* ══ DIVIDER ═══════════════════════════════════════════ */
hr { border-color: #1E3055 !important; }

/* ══════════════════════════════════════════════════════
   COMPONENTES PERSONALIZADOS HTML
══════════════════════════════════════════════════════ */

/* ─ Header ─ */
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
.hdr .sub  { color: #94A3B8; font-size: .97rem; margin: 0; }
.hdr .aut  { color: #475569; font-size: .83rem; margin: 5px 0 0;
             border-top: 1px solid #1E3055; padding-top: 6px; }

/* ─ Ficha de distribución ─ */
.ficha, .ficha-purple, .ficha-green {
    background: #0D1628;
    border: 1px solid #1E3055;
    border-radius: 10px;
    padding: 16px;
    font-size: .89rem;
    color: #94A3B8;
    line-height: 1.6;
    margin-bottom: 14px;
}
.ficha        { border-left: 4px solid #3B82F6; }
.ficha-purple { border-left: 4px solid #A78BFA; }
.ficha-green  { border-left: 4px solid #34D399; }
.ficha strong, .ficha-purple strong, .ficha-green strong { color: #CBD5E1; }
.ficha-lbl {
    display: block;
    color: #60A5FA;
    font-weight: 700;
    font-size: .8rem;
    text-transform: uppercase;
    letter-spacing: .6px;
    margin-bottom: 6px;
}

/* ─ Concepto cards (stMarkdownContainer dentro de columnas de concepto) ─ */
.concepto-col [data-testid="stMarkdownContainer"] > div {
    background: #0D1628;
    border: 1px solid #1E3055;
    border-radius: 12px;
    padding: 18px;
}

/* ─ Burbuja de paso ─ */
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

/* ─ Tarjeta resultado ─ */
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

/* ─ Interpretación ─ */
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

/* ─ Paso explicado ─ */
.paso-exp {
    background: #0D1628;
    border: 1px solid #1E3055;
    border-radius: 10px;
    padding: 13px 17px;
    margin-bottom: 9px;
    font-size: .88rem;
    color: #94A3B8;
    line-height: 1.65;
}
.paso-exp strong, .paso-exp b { color: #CBD5E1; }

/* ─ Botón primario ─ */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 11px 0 !important;
    font-size: 1rem !important; font-weight: 700 !important; width: 100%;
    box-shadow: 0 4px 18px rgba(37,99,235,0.45) !important;
    transition: all .2s !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(37,99,235,0.6) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES DE CÁLCULO
# ============================================================

def calcular_normal(media, sigma, tipo, val_a, val_b=None):
    pasos = []
    pasos.append(
        f"**1 — Distribución**\n\n"
        f"X ~ N(μ={media}, σ={sigma})  —  campana simétrica centrada en {media}."
    )
    if tipo == 'izquierda':
        z = (val_a - media) / sigma
        prob = stats.norm.cdf(val_a, loc=media, scale=sigma)
        pasos.append(f"**2 — Puntaje Z**\n\nZ = ({val_a} − {media}) / {sigma} = **{z:.4f}**\n\n"
                     f"Indica cuántas σ está el valor de la media.")
        pasos.append(f"**3 — Probabilidad acumulada**\n\n"
                     f"P(X ≤ {val_a}) = P(Z ≤ {z:.4f}) = **{prob:.4f}**")
        interp = (f"Hay un **{prob*100:.2f}%** de probabilidad de que la variable sea "
                  f"**menor o igual a {val_a}**.")
        return prob, pasos, interp, False

    elif tipo == 'derecha':
        z = (val_a - media) / sigma
        prob_i = stats.norm.cdf(val_a, loc=media, scale=sigma)
        prob = 1 - prob_i
        pasos.append(f"**2 — Puntaje Z**\n\nZ = ({val_a} − {media}) / {sigma} = **{z:.4f}**")
        pasos.append(f"**3 — Cola derecha**\n\nP(X ≥ {val_a}) = 1 − {prob_i:.4f} = **{prob:.4f}**")
        interp = (f"Hay un **{prob*100:.2f}%** de probabilidad de que la variable sea "
                  f"**mayor o igual a {val_a}**.")
        return prob, pasos, interp, False

    elif tipo == 'entre':
        za = (val_a - media) / sigma
        zb = (val_b - media) / sigma
        pa = stats.norm.cdf(val_a, loc=media, scale=sigma)
        pb = stats.norm.cdf(val_b, loc=media, scale=sigma)
        prob = pb - pa
        pasos.append(f"**2 — Z de ambos límites**\n\n"
                     f"Z_a = ({val_a} − {media}) / {sigma} = **{za:.4f}**\n\n"
                     f"Z_b = ({val_b} − {media}) / {sigma} = **{zb:.4f}**")
        pasos.append(f"**3 — Restar áreas**\n\n"
                     f"P({val_a} ≤ X ≤ {val_b}) = {pb:.4f} − {pa:.4f} = **{prob:.4f}**")
        interp = (f"Hay un **{prob*100:.2f}%** de probabilidad de que la variable esté "
                  f"**entre {val_a} y {val_b}**.")
        return prob, pasos, interp, False

    elif tipo == 'percentil':
        x_val = stats.norm.ppf(val_a, loc=media, scale=sigma)
        z = stats.norm.ppf(val_a)
        pasos.append(f"**2 — Z del percentil {val_a*100:.1f}**\n\n"
                     f"z tal que P(Z ≤ z) = {val_a}  →  z = **{z:.4f}**")
        pasos.append(f"**3 — Convertir Z → X**\n\n"
                     f"X = {media} + ({z:.4f}) × {sigma} = **{x_val:.4f}**")
        interp = (f"El percentil {val_a*100:.1f} es **X = {x_val:.4f}**. "
                  f"El {val_a*100:.1f}% de los valores está por debajo de este punto.")
        return x_val, pasos, interp, True


def calcular_t(gl, tipo, val_a, val_b=None):
    pasos = []
    dist = stats.t(df=gl)
    nota = ("≈ Normal" if gl >= 30 else "colas más anchas que Normal" if gl >= 10
            else "colas bastante más anchas")
    pasos.append(f"**1 — Distribución**\n\nT ~ t({gl})  —  {nota}.")

    if tipo == 'izquierda':
        prob = dist.cdf(val_a)
        pasos.append(f"**2 — Probabilidad acumulada**\n\nP(T ≤ {val_a}) = **{prob:.4f}**")
        interp = f"Con {gl} gl, P(T ≤ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%)."
        return prob, pasos, interp, False

    elif tipo == 'derecha':
        pi = dist.cdf(val_a); prob = 1 - pi
        pasos.append(f"**2 — Cola derecha**\n\nP(T ≥ {val_a}) = 1 − {pi:.4f} = **{prob:.4f}**")
        interp = f"Con {gl} gl, P(T ≥ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%)."
        return prob, pasos, interp, False

    elif tipo == 'entre':
        pa = dist.cdf(val_a); pb = dist.cdf(val_b); prob = pb - pa
        pasos.append(f"**2 — Área entre límites**\n\n"
                     f"P(T ≤ {val_a}) = {pa:.4f}  |  P(T ≤ {val_b}) = {pb:.4f}\n\n"
                     f"P({val_a} ≤ T ≤ {val_b}) = {pb:.4f} − {pa:.4f} = **{prob:.4f}**")
        interp = f"Con {gl} gl, P({val_a} ≤ T ≤ {val_b}) = **{prob:.4f}** ({prob*100:.2f}%)."
        return prob, pasos, interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a / 2)
        pasos.append(f"**2 — Valor crítico (α = {val_a})**\n\n"
                     f"Cada cola = α/2 = {val_a/2}  →  t_crítico = **±{vc:.4f}**")
        interp = (f"Con {gl} gl y α={val_a}, **t_crítico = ±{vc:.4f}**. "
                  f"Si |t calculado| > {vc:.4f} → se rechaza H₀.")
        return vc, pasos, interp, True


def calcular_chi2(gl, tipo, val_a):
    pasos = []
    dist = stats.chi2(df=gl)
    pasos.append(f"**1 — Distribución**\n\nχ²({gl})  —  Media = {gl}, Varianza = {2*gl}. Solo valores ≥ 0.")

    if tipo == 'izquierda':
        prob = dist.cdf(val_a)
        pasos.append(f"**2 — Probabilidad acumulada**\n\nP(χ² ≤ {val_a}) = **{prob:.4f}**")
        interp = f"Con {gl} gl, P(χ² ≤ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%)."
        return prob, pasos, interp, False

    elif tipo == 'derecha':
        pi = dist.cdf(val_a); prob = 1 - pi
        concl = ("p < 0.05 → se rechazaría H₀ (hay asociación)." if prob < 0.05
                 else "p ≥ 0.05 → no se rechazaría H₀.")
        pasos.append(f"**2 — p-valor**\n\nP(χ² ≥ {val_a}) = 1 − {pi:.4f} = **{prob:.4f}**\n\n{concl}")
        interp = f"Con {gl} gl, P(χ² ≥ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%). {concl}"
        return prob, pasos, interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a)
        pasos.append(f"**2 — Valor crítico (α = {val_a})**\n\n"
                     f"χ²_crítico = **{vc:.4f}**")
        interp = (f"Con {gl} gl y α={val_a}, **χ²_crítico = {vc:.4f}**. "
                  f"Si χ² calculado > {vc:.4f} → se rechaza H₀.")
        return vc, pasos, interp, True


def calcular_f(gl1, gl2, tipo, val_a):
    pasos = []
    dist = stats.f(dfn=gl1, dfd=gl2)
    pasos.append(f"**1 — Distribución**\n\nF({gl1},{gl2})  —  Cociente de dos χ². Solo valores positivos.")

    if tipo == 'derecha':
        pi = dist.cdf(val_a); prob = 1 - pi
        concl = ("p < 0.05 → se rechaza H₀ (grupos difieren)." if prob < 0.05
                 else "p ≥ 0.05 → no hay evidencia para rechazar H₀.")
        pasos.append(f"**2 — p-valor**\n\nP(F ≥ {val_a}) = 1 − {pi:.4f} = **{prob:.4f}**\n\n{concl}")
        interp = f"Con F({gl1},{gl2}), F={val_a} → **p-valor = {prob:.4f}**. {concl}"
        return prob, pasos, interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a)
        pasos.append(f"**2 — Valor crítico (α = {val_a})**\n\nF_crítico = **{vc:.4f}**")
        interp = (f"Con F({gl1},{gl2}) y α={val_a}, **F_crítico = {vc:.4f}**. "
                  f"Si F calculado > {vc:.4f} → se rechaza H₀.")
        return vc, pasos, interp, True


# ============================================================
# FUNCIÓN DE GRÁFICO — TEMA DARK
# ============================================================
BG_GRAFICA  = "#040D1E"   # fondo del gráfico
BG_EJES     = "#040D1E"
GRID_COLOR  = "#1A2840"
TEXT_COLOR  = "#64748B"
TITULO_COLOR= "#CBD5E1"
CURVA_COLOR = "#E2E8F0"

COLORES_SOMBRA = {
    'normal': '#3B82F6',   # azul
    't':      '#F97316',   # naranja
    'chi2':   '#A855F7',   # púrpura
    'f':      '#EF4444',   # rojo
}

def crear_grafico(dist_key, params, tipo_sombra=None, lim_a=None, lim_b=None):
    color = COLORES_SOMBRA.get(dist_key, '#3B82F6')

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    fig.patch.set_facecolor(BG_GRAFICA)
    ax.set_facecolor(BG_EJES)

    # Configurar distribución y rango X
    if dist_key == 'normal':
        m, s = params['media'], params['sigma']
        d = stats.norm(loc=m, scale=s)
        xmin, xmax = m - 4.5*s, m + 4.5*s
        titulo = f'Normal   N(μ={m},  σ={s})'

    elif dist_key == 't':
        gl = params['gl']
        d = stats.t(df=gl)
        xmin, xmax = -5.0, 5.0
        titulo = f't de Student   t(gl={gl})'

    elif dist_key == 'chi2':
        gl = params['gl']
        d = stats.chi2(df=gl)
        xmin, xmax = 0.0, d.ppf(0.999)
        titulo = f'Chi-cuadrado   χ²(gl={gl})'

    elif dist_key == 'f':
        g1, g2 = params['gl1'], params['gl2']
        d = stats.f(dfn=g1, dfd=g2)
        xmin, xmax = 0.0, d.ppf(0.999)
        titulo = f'F de Fisher   F({g1}, {g2})'

    x = np.linspace(xmin, xmax, 700)
    y = d.pdf(x)

    # Curva base con ligero glow
    ax.plot(x, y, color=CURVA_COLOR, linewidth=2.0, zorder=3, alpha=0.9)
    ax.fill_between(x, y, alpha=0.04, color='#60A5FA')

    # Área sombreada
    if tipo_sombra == 'izquierda' and lim_a is not None:
        m_ = x <= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label=f'Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'derecha' and lim_a is not None:
        m_ = x >= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label=f'Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'entre' and lim_a is not None and lim_b is not None:
        m_ = (x >= lim_a) & (x <= lim_b)
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label=f'Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)
        ax.axvline(x=lim_b, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)

    # Estilo
    ax.set_xlabel('Valor', fontsize=9.5, color=TEXT_COLOR)
    ax.set_ylabel('Densidad  f(x)', fontsize=9.5, color=TEXT_COLOR, rotation=0,
                  labelpad=8)
    ax.yaxis.set_label_coords(-0.01, 1.02)
    ax.set_title(titulo, fontsize=11.5, fontweight='bold', color=TITULO_COLOR, pad=10)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.25, linestyle='--', color=GRID_COLOR)
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8.5)

    if tipo_sombra:
        ax.legend(['Área = Probabilidad'], fontsize=8.5, loc='upper right',
                  framealpha=0.25, facecolor='#0D1628', edgecolor='#1E3055',
                  labelcolor='#94A3B8')

    ax.annotate('El área bajo la curva = probabilidad',
                xy=(0.02, 0.96), xycoords='axes fraction',
                fontsize=8, color='#334155', style='italic', va='top')

    plt.tight_layout(pad=0.8)
    return fig


# ============================================================
# MOSTRAR RESULTADO + PASOS (visibles directamente)
# ============================================================

def mostrar_panel(res, interp, pasos, es_valor=False):
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

    st.markdown(f'<div class="interp">💬 &nbsp;{interp}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span style="color:#60A5FA;font-weight:700;font-size:.9rem;">📐 Explicación paso a paso</span>',
                unsafe_allow_html=True)
    for paso in pasos:
        st.markdown(f'<div class="paso-exp">{paso}</div>', unsafe_allow_html=True)


def paso_header(n, texto):
    st.markdown(
        f'<div class="paso-wrap">'
        f'<div class="burbuja">{n}</div>'
        f'<div class="paso-lbl">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ============================================================
#                   INTERFAZ PRINCIPAL
# ============================================================

# ── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <h1>📊 Distribuciones Continuas en Bioestadística</h1>
  <p class="sub">Visualiza, calcula e interpreta distribuciones de probabilidad continuas paso a paso.</p>
  <p class="aut">Autora: Alejandra Acosta &nbsp;·&nbsp; Bioestadística &nbsp;·&nbsp; Tema 4 — Distribuciones continuas</p>
</div>
""", unsafe_allow_html=True)

# ── CONCEPTO CLAVE — siempre visible ────────────────────────
st.markdown(
    '<p style="color:#60A5FA;font-weight:700;font-size:.9rem;'
    'letter-spacing:.6px;text-transform:uppercase;margin:0 0 12px;">'
    '📌 &nbsp;¿Qué es una distribución continua?</p>',
    unsafe_allow_html=True,
)
ck1, ck2, ck3 = st.columns(3, gap="small")

with ck1:
    st.markdown(
        '<div class="ficha">'
        '<strong>🌊 ¿Qué es?</strong><br><br>'
        'Describe cómo se distribuye la probabilidad en una variable que puede tomar '
        '<strong>cualquier valor en un rango</strong>: '
        'estatura, peso, glucosa, presión arterial.'
        '</div>',
        unsafe_allow_html=True,
    )

with ck2:
    st.markdown(
        '<div class="ficha-purple">'
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
        '<div class="ficha-green">'
        '<strong>🗂️ ¿Cuándo usar cada una?</strong><br><br>'
        '<span style="color:#60A5FA;font-weight:700;">📈 Normal</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>datos simétricos, n grande</span><br>'
        '<span style="color:#F97316;font-weight:700;">📉 t Student</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>muestra pequeña (n &lt; 30)</span><br>'
        '<span style="color:#A855F7;font-weight:700;">📊 χ²</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>tablas de independencia</span><br>'
        '<span style="color:#EF4444;font-weight:700;">📋 F Fisher</span>'
        '<span style="color:#64748B;"> — </span>'
        '<span>comparar 3+ grupos (ANOVA)</span>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)

# ============================================================
# PESTAÑAS
# ============================================================
tab_n, tab_t, tab_c, tab_f = st.tabs([
    "📈  Normal",
    "📉  t de Student",
    "📊  Chi-cuadrado  χ²",
    "📋  F de Fisher",
])


# ── NORMAL ──────────────────────────────────────────────────
with tab_n:
    L, R = st.columns([1, 1.4], gap="large")

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
                                                 ts_n="izquierda", la_n=va, lb_n=None))
                    st.rerun()
            elif "ENCIMA" in tipo_n:
                va = st.number_input("Valor límite (a)", value=float(media_n),
                                     step=0.1, format="%.4f", key="nn_ad")
                if st.button("Calcular probabilidad", type="primary", key="btn_nd"):
                    r, ps, it, ev = calcular_normal(media_n, sigma_n, 'derecha', va)
                    st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=ev,
                                                 ts_n="derecha", la_n=va, lb_n=None))
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
                                                     ts_n="entre", la_n=va, lb_n=vb))
                        st.rerun()
            else:
                perc = st.slider("Percentil (%)", 1, 99, 95, key="nn_p")
                st.caption(f"Buscará X tal que el {perc}% de los datos está por debajo.")
                if st.button("Calcular valor X", type="primary", key="btn_np"):
                    r, ps, it, ev = calcular_normal(media_n, sigma_n, 'percentil', perc / 100)
                    st.session_state.update(dict(r_n=r, ps_n=ps, it_n=it, ev_n=True,
                                                 ts_n="izquierda", la_n=r, lb_n=None))
                    st.rerun()

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
        st.pyplot(fig_n, use_container_width=True)
        plt.close(fig_n)
        if "r_n" in st.session_state:
            mostrar_panel(st.session_state["r_n"], st.session_state["it_n"],
                          st.session_state["ps_n"], st.session_state.get("ev_n", False))


# ── t DE STUDENT ─────────────────────────────────────────────
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
                if st.button("Calcular", type="primary", key="btn_ti", use_container_width=True):
                    r, ps, it, ev = calcular_t(gl_t, 'izquierda', va)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                 ts_t="izquierda", la_t=va, lb_t=None))
                    st.rerun()
            elif "≥ a)" in tipo_t:
                va = st.number_input("Valor de a", value=0.0, step=0.1, format="%.4f", key="tt_ad")
                if st.button("Calcular", type="primary", key="btn_td", use_container_width=True):
                    r, ps, it, ev = calcular_t(gl_t, 'derecha', va)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                 ts_t="derecha", la_t=va, lb_t=None))
                    st.rerun()
            elif "≤ T ≤" in tipo_t:
                c1, c2 = st.columns(2)
                va = c1.number_input("Límite a", value=-2.0, step=0.1, format="%.4f", key="tt_ae")
                vb = c2.number_input("Límite b", value=2.0, step=0.1, format="%.4f", key="tt_be")
                if va >= vb:
                    st.warning("⚠️ a debe ser menor que b.")
                if st.button("Calcular", type="primary", key="btn_te", use_container_width=True):
                    if va < vb:
                        r, ps, it, ev = calcular_t(gl_t, 'entre', va, vb)
                        st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=ev,
                                                     ts_t="entre", la_t=va, lb_t=vb))
                        st.rerun()
            else:
                alpha_t = st.select_slider("Nivel de significancia α", key="at_t",
                                           options=[0.10, 0.05, 0.01, 0.001], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico", type="primary",
                             key="btn_tvc", use_container_width=True):
                    r, ps, it, ev = calcular_t(gl_t, 'valor_critico', alpha_t)
                    st.session_state.update(dict(r_t=r, ps_t=ps, it_t=it, ev_t=True,
                                                 ts_t="entre", la_t=-r, lb_t=r))
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
        st.pyplot(fig_t, use_container_width=True)
        plt.close(fig_t)
        if "r_t" in st.session_state:
            mostrar_panel(st.session_state["r_t"], st.session_state["it_t"],
                          st.session_state["ps_t"], st.session_state.get("ev_t", False))


# ── CHI-CUADRADO ─────────────────────────────────────────────
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
                if st.button("Calcular", type="primary", key="btn_ci", use_container_width=True):
                    r, ps, it, ev = calcular_chi2(gl_c, 'izquierda', va)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=ev,
                                                 ts_c="izquierda", la_c=va))
                    st.rerun()
            elif "p-valor" in tipo_c:
                va = st.number_input("Estadístico χ² calculado", value=float(gl_c),
                                     min_value=0.001, step=0.5, format="%.4f", key="cc_ad")
                if st.button("Calcular p-valor", type="primary",
                             key="btn_cd", use_container_width=True):
                    r, ps, it, ev = calcular_chi2(gl_c, 'derecha', va)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=ev,
                                                 ts_c="derecha", la_c=va))
                    st.rerun()
            else:
                alpha_c = st.select_slider("Nivel de significancia α", key="at_c",
                                           options=[0.10, 0.05, 0.01], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico", type="primary",
                             key="btn_cvc", use_container_width=True):
                    r, ps, it, ev = calcular_chi2(gl_c, 'valor_critico', alpha_c)
                    st.session_state.update(dict(r_c=r, ps_c=ps, it_c=it, ev_c=True,
                                                 ts_c="derecha", la_c=r))
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
        st.pyplot(fig_c, use_container_width=True)
        plt.close(fig_c)
        if "r_c" in st.session_state:
            mostrar_panel(st.session_state["r_c"], st.session_state["it_c"],
                          st.session_state["ps_c"], st.session_state.get("ev_c", False))


# ── F DE FISHER ──────────────────────────────────────────────
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
                             key="btn_fd", use_container_width=True):
                    r, ps, it, ev = calcular_f(gl1_f, gl2_f, 'derecha', va)
                    st.session_state.update(dict(r_f=r, ps_f=ps, it_f=it, ev_f=ev,
                                                 ts_f="derecha", la_f=va))
                    st.rerun()
            else:
                alpha_f = st.select_slider("Nivel de significancia α", key="at_f",
                                           options=[0.10, 0.05, 0.01], value=0.05,
                                           format_func=lambda x: f"α = {x}  ({x*100:.1f}%)")
                if st.button("Calcular valor crítico F", type="primary",
                             key="btn_fvc", use_container_width=True):
                    r, ps, it, ev = calcular_f(gl1_f, gl2_f, 'valor_critico', alpha_f)
                    st.session_state.update(dict(r_f=r, ps_f=ps, it_f=it, ev_f=True,
                                                 ts_f="derecha", la_f=r))
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
        st.pyplot(fig_f, use_container_width=True)
        plt.close(fig_f)
        if "r_f" in st.session_state:
            mostrar_panel(st.session_state["r_f"], st.session_state["it_f"],
                          st.session_state["ps_f"], st.session_state.get("ev_f", False))


# ── PIE ──────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#334155;font-size:.79rem;padding:4px 0 10px;">
  Proyecto de Software Pedagógico · Bioestadística · Alejandra Acosta<br>
  <em>El área bajo la curva = probabilidad. La altura de la curva ≠ probabilidad.</em>
</div>
""", unsafe_allow_html=True)
