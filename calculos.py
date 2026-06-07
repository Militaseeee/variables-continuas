# ================================================================
# calculos.py — BACKEND: Lógica de cálculo y gráficos
#
# Este archivo contiene TODO lo que no se ve en pantalla:
#   · Las funciones matemáticas que calculan probabilidades
#   · La función que dibuja las gráficas
#
# No toques este archivo si solo quieres cambiar colores o textos.
# Para eso ve a app.py.
# ================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ================================================================
# BLOQUE 1 — COLORES DE LAS GRÁFICAS
#
# Aquí se definen los colores que usa la gráfica (fondo, curva,
# grilla, títulos). Si quieres cambiar el color de la curva o
# el fondo del gráfico, modifica estas variables.
# ================================================================

BG_GRAFICA   = "#040D1E"   # color de fondo del área de la gráfica
BG_EJES      = "#040D1E"   # color de fondo de los ejes
GRID_COLOR   = "#1A2840"   # color de las líneas de la cuadrícula
TEXT_COLOR   = "#64748B"   # color del texto de los ejes
TITULO_COLOR = "#CBD5E1"   # color del título de la gráfica
CURVA_COLOR  = "#E2E8F0"   # color de la línea principal de la curva

# Cada distribución tiene un color de sombra distinto
COLORES_SOMBRA = {
    'normal': '#3B82F6',   # azul    → Normal
    't':      '#F97316',   # naranja → t de Student
    'chi2':   '#A855F7',   # púrpura → Chi-cuadrado
    'f':      '#EF4444',   # rojo    → F de Fisher
}


# ================================================================
# BLOQUE 2 — FUNCIÓN DE GRÁFICO
#
# crear_grafico() dibuja la curva de la distribución seleccionada.
#
# Parámetros que recibe:
#   dist_key   → qué distribución: 'normal', 't', 'chi2' o 'f'
#   params     → diccionario con los parámetros (media, sigma, gl…)
#   tipo_sombra→ qué área colorear: 'izquierda', 'derecha', 'entre'
#   lim_a      → límite izquierdo del área sombreada
#   lim_b      → límite derecho (solo si tipo_sombra='entre')
#
# Devuelve: un objeto Figure de matplotlib listo para mostrar.
# ================================================================

def crear_grafico(dist_key, params, tipo_sombra=None, lim_a=None, lim_b=None):
    color = COLORES_SOMBRA.get(dist_key, '#3B82F6')

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    fig.patch.set_facecolor(BG_GRAFICA)
    ax.set_facecolor(BG_EJES)

    # -- Configura la distribución y el rango del eje X ----------
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

    # -- Dibuja la curva principal --------------------------------
    x = np.linspace(xmin, xmax, 700)
    y = d.pdf(x)
    ax.plot(x, y, color=CURVA_COLOR, linewidth=2.0, zorder=3, alpha=0.9)
    ax.fill_between(x, y, alpha=0.04, color='#60A5FA')

    # -- Colorea el área de probabilidad según el tipo -----------
    if tipo_sombra == 'izquierda' and lim_a is not None:
        m_ = x <= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label='Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'derecha' and lim_a is not None:
        m_ = x >= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label='Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'entre' and lim_a is not None and lim_b is not None:
        m_ = (x >= lim_a) & (x <= lim_b)
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color,
                        label='Área sombreada', zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)
        ax.axvline(x=lim_b, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)

    # -- Estilo visual de los ejes y grilla ----------------------
    ax.set_xlabel('Valor', fontsize=9.5, color=TEXT_COLOR)
    ax.set_ylabel('Densidad  f(x)', fontsize=9.5, color=TEXT_COLOR, rotation=0, labelpad=8)
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
                xy=(0.98, 1.045), xycoords='axes fraction',
                fontsize=7.5, color='#334155', style='italic',
                va='bottom', ha='right', annotation_clip=False)

    plt.tight_layout(pad=0.8)
    return fig


# ================================================================
# BLOQUE 3 — DISTRIBUCIÓN NORMAL
#
# calcular_normal() calcula probabilidades para X ~ N(μ, σ).
#
# Tipos disponibles:
#   'izquierda' → P(X ≤ a)          usa la CDF directamente
#   'derecha'   → P(X ≥ a)          = 1 − CDF(a)
#   'entre'     → P(a ≤ X ≤ b)      = CDF(b) − CDF(a)
#   'percentil' → ¿qué X tiene p%?  usa la función inversa PPF
#
# Devuelve: (resultado, lista_de_pasos, interpretación, es_valor)
#   es_valor=True significa que el resultado es un valor X, no prob.
# ================================================================

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


# ================================================================
# BLOQUE 4 — DISTRIBUCIÓN t DE STUDENT
#
# calcular_t() calcula probabilidades para T ~ t(gl).
# Se usa cuando la muestra es pequeña (n < 30) y no se conoce σ.
#
# Tipos disponibles:
#   'izquierda'      → P(T ≤ a)
#   'derecha'        → P(T ≥ a)
#   'entre'          → P(a ≤ T ≤ b)
#   'valor_critico'  → t tal que P(|T| > t) = α  (prueba bilateral)
# ================================================================

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
        pi = dist.cdf(val_a)
        prob = 1 - pi
        pasos.append(f"**2 — Cola derecha**\n\nP(T ≥ {val_a}) = 1 − {pi:.4f} = **{prob:.4f}**")
        interp = f"Con {gl} gl, P(T ≥ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%)."
        return prob, pasos, interp, False

    elif tipo == 'entre':
        pa = dist.cdf(val_a)
        pb = dist.cdf(val_b)
        prob = pb - pa
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


# ================================================================
# BLOQUE 5 — DISTRIBUCIÓN CHI-CUADRADO (χ²)
#
# calcular_chi2() calcula probabilidades para χ²(gl).
# Se usa para tablas de contingencia (¿dos variables están
# relacionadas?) y bondad de ajuste. Solo toma valores ≥ 0.
#
# Tipos disponibles:
#   'izquierda'     → P(χ² ≤ a)
#   'derecha'       → P(χ² ≥ a)  ← p-valor de una prueba
#   'valor_critico' → χ² tal que P(χ² > vc) = α
# ================================================================

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
        pi = dist.cdf(val_a)
        prob = 1 - pi
        concl = ("p < 0.05 → se rechazaría H₀ (hay asociación)." if prob < 0.05
                 else "p ≥ 0.05 → no se rechazaría H₀.")
        pasos.append(f"**2 — p-valor**\n\nP(χ² ≥ {val_a}) = 1 − {pi:.4f} = **{prob:.4f}**\n\n{concl}")
        interp = f"Con {gl} gl, P(χ² ≥ {val_a}) = **{prob:.4f}** ({prob*100:.2f}%). {concl}"
        return prob, pasos, interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a)
        pasos.append(f"**2 — Valor crítico (α = {val_a})**\n\nχ²_crítico = **{vc:.4f}**")
        interp = (f"Con {gl} gl y α={val_a}, **χ²_crítico = {vc:.4f}**. "
                  f"Si χ² calculado > {vc:.4f} → se rechaza H₀.")
        return vc, pasos, interp, True


# ================================================================
# BLOQUE 6 — DISTRIBUCIÓN F DE FISHER
#
# calcular_f() calcula probabilidades para F(gl1, gl2).
# Se usa en ANOVA para comparar varianzas/medias de 3+ grupos.
#   gl1 = grupos − 1  (grados de libertad del numerador)
#   gl2 = N total − grupos  (grados de libertad del denominador)
#
# Tipos disponibles:
#   'derecha'        → P(F ≥ a)  ← p-valor de ANOVA
#   'valor_critico'  → F tal que P(F > vc) = α
# ================================================================

def calcular_f(gl1, gl2, tipo, val_a):
    pasos = []
    dist = stats.f(dfn=gl1, dfd=gl2)
    pasos.append(f"**1 — Distribución**\n\nF({gl1},{gl2})  —  Cociente de dos χ². Solo valores positivos.")

    if tipo == 'derecha':
        pi = dist.cdf(val_a)
        prob = 1 - pi
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
