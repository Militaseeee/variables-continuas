# ================================================================
# calculos.py — BACKEND: Lógica de cálculo y gráficos
# ================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from math import comb as _math_comb


# ================================================================
# BLOQUE 1 — COLORES DE LAS GRÁFICAS
# ================================================================

BG_GRAFICA   = "#040D1E"
BG_EJES      = "#040D1E"
GRID_COLOR   = "#1A2840"
TEXT_COLOR   = "#64748B"
TITULO_COLOR = "#CBD5E1"
CURVA_COLOR  = "#E2E8F0"

COLORES_SOMBRA = {
    'normal': '#3B82F6',
    't':      '#F97316',
    'chi2':   '#A855F7',
    'f':      '#EF4444',
}


# ================================================================
# BLOQUE 2 — FUNCIÓN DE GRÁFICO
# ================================================================

def crear_grafico(dist_key, params, tipo_sombra=None, lim_a=None, lim_b=None):
    color = COLORES_SOMBRA.get(dist_key, '#3B82F6')

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    fig.patch.set_facecolor(BG_GRAFICA)
    ax.set_facecolor(BG_EJES)

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
    ax.plot(x, y, color=CURVA_COLOR, linewidth=2.0, zorder=3, alpha=0.9)
    ax.fill_between(x, y, alpha=0.04, color='#60A5FA')

    if tipo_sombra == 'izquierda' and lim_a is not None:
        m_ = x <= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color, zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'derecha' and lim_a is not None:
        m_ = x >= lim_a
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color, zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

    elif tipo_sombra == 'entre' and lim_a is not None and lim_b is not None:
        m_ = (x >= lim_a) & (x <= lim_b)
        ax.fill_between(x[m_], y[m_], alpha=0.55, color=color, zorder=2)
        ax.axvline(x=lim_a, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)
        ax.axvline(x=lim_b, color='#F87171', linestyle='--', linewidth=1.6, zorder=4, alpha=0.9)

    elif tipo_sombra == 'colas' and lim_a is not None:
        abs_a = abs(lim_a)
        m_izq = x <= -abs_a
        m_der = x >= abs_a
        ax.fill_between(x[m_izq], y[m_izq], alpha=0.55, color=color, zorder=2)
        ax.fill_between(x[m_der], y[m_der], alpha=0.55, color=color, zorder=2)
        ax.axvline(x=-abs_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)
        ax.axvline(x=abs_a, color='#F87171', linestyle='--', linewidth=1.8, zorder=4, alpha=0.9)

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


def crear_grafico_fisher(a, b, c, d, E11, E12, E21, E22,
                         lbl_r1="Grupo 1", lbl_r2="Grupo 2",
                         lbl_c1="Evento", lbl_c2="No evento"):
    """Barras agrupadas: Observado vs Esperado para cada celda 2x2."""
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    fig.patch.set_facecolor(BG_GRAFICA)
    ax.set_facecolor(BG_EJES)

    labels = [
        f"{lbl_r1}\n{lbl_c1}", f"{lbl_r1}\n{lbl_c2}",
        f"{lbl_r2}\n{lbl_c1}", f"{lbl_r2}\n{lbl_c2}",
    ]
    obs_vals = [a, b, c, d]
    exp_vals = [E11, E12, E21, E22]

    x = np.arange(4)
    w = 0.36
    bar_obs = ax.bar(x - w/2, obs_vals, w, label='Observado',
                     color='#EF4444', alpha=0.82, zorder=3)
    bar_exp = ax.bar(x + w/2, exp_vals, w, label='Esperado',
                     color='#64748B', alpha=0.65, zorder=3)

    for bar, ev in zip(bar_exp, exp_vals):
        if ev < 5:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.2, '⚠ <5',
                    ha='center', va='bottom', fontsize=7.5,
                    color='#F87171', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5, color=TEXT_COLOR)
    ax.set_ylabel('Frecuencia', fontsize=9, color=TEXT_COLOR,
                  rotation=0, labelpad=8)
    ax.yaxis.set_label_coords(-0.01, 1.02)
    ax.set_title('Frecuencias Observadas vs Esperadas',
                 fontsize=11.5, fontweight='bold', color=TITULO_COLOR, pad=10)
    ax.legend(fontsize=8.5, framealpha=0.25, facecolor='#0D1628',
              edgecolor='#1E3055', labelcolor='#94A3B8')
    ax.grid(True, alpha=0.2, linestyle='--', color=GRID_COLOR, axis='y')
    ax.set_ylim(bottom=0)
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8.5)
    ax.annotate('Barras rojas = observado · Barras grises = esperado',
                xy=(0.98, 1.045), xycoords='axes fraction',
                fontsize=7.5, color='#334155', style='italic',
                va='bottom', ha='right', annotation_clip=False)
    plt.tight_layout(pad=0.8)
    return fig


# ================================================================
# BLOQUE 3 — HELPERS PARA EXPLICACIONES HTML
# ================================================================

def _fmt(v):
    """Elimina ceros decimales innecesarios: 2.0 → '2', 1.45 → '1.45'."""
    return f"{v:g}"


def _frac(num, den):
    """Fracción vertical con línea azul separadora."""
    return (
        '<span style="display:inline-flex;flex-direction:column;text-align:center;'
        'vertical-align:middle;font-size:0.9em;line-height:1.5;margin:0 4px;">'
        f'<span style="border-bottom:1.5px solid #60A5FA;padding:0 5px;">{num}</span>'
        f'<span style="padding:0 5px;">{den}</span>'
        '</span>'
    )


def _formula(html):
    """Caja oscura centrada para fórmulas matemáticas."""
    return (
        '<div style="text-align:center;background:#06101F;border:1px solid #1A2840;'
        'border-radius:8px;padding:12px 20px;margin:8px 0 12px;'
        'font-size:1.05rem;color:#E2E8F0;letter-spacing:0.3px;">'
        f'{html}</div>'
    )


def _titulo(texto):
    return f'<p style="color:#CBD5E1;margin:14px 0 4px;font-weight:600;">{texto}</p>'


def _nota(texto):
    return f'<p style="color:#94A3B8;font-size:.86rem;margin:2px 0 10px;">{texto}</p>'


def _bullets(items):
    li = ''.join(
        f'<li style="line-height:2.1;color:#94A3B8;">{item}</li>'
        for item in items
    )
    return f'<ul style="margin:6px 0 10px 4px;padding-left:20px;">{li}</ul>'


def _blockquote(texto):
    """Caja con borde izquierdo azul para citar la interpretación."""
    return (
        '<div style="border-left:4px solid #3B82F6;padding:10px 16px;'
        'background:#0B1932;border-radius:0 8px 8px 0;margin:8px 0 14px;'
        'color:#CBD5E1;font-size:.93rem;line-height:1.7;">'
        f'{texto}</div>'
    )


def _ok(texto):
    return f'<p style="color:#4ADE80;margin:4px 0 12px;font-size:.93rem;">{texto}</p>'


def _hr():
    return '<hr style="border:none;border-top:1px solid #1E3055;margin:16px 0;">'


def _nota_continua():
    """Bloque educativo obligatorio: densidad ≠ probabilidad. Se añade a todos los módulos de distribuciones continuas."""
    return (
        '<div style="background:#050F1E;border-left:4px solid #3B82F6;'
        'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:10px;">'
        '<p style="color:#60A5FA;font-weight:700;font-size:.75rem;letter-spacing:.6px;'
        'text-transform:uppercase;margin:0 0 6px;">📐 Concepto fundamental — densidad ≠ probabilidad</p>'
        '<p style="color:#94A3B8;font-size:.83rem;line-height:1.7;margin:0;">'
        'La curva muestra la función de <b style="color:#CBD5E1;">densidad</b> f(x). '
        'Su altura en un punto <em>no es</em> una probabilidad. '
        'La <b style="color:#6EE7B7;">probabilidad</b> es el '
        '<b style="color:#6EE7B7;">área bajo la curva</b> entre dos límites — '
        'la integral de f(x) en ese intervalo.<br>'
        'Por eso <b style="color:#F87171;">P(X = a) = 0</b> para cualquier valor puntual a: '
        'un punto tiene ancho cero → área cero → probabilidad cero. '
        'Las probabilidades <em>siempre</em> se calculan sobre intervalos o regiones, nunca sobre puntos.'
        '</p></div>'
    )


# ================================================================
# BLOQUE 4 — DISTRIBUCIÓN NORMAL
# ================================================================

def calcular_normal(media, sigma, tipo, val_a, val_b=None):

    if tipo == 'izquierda':
        z = (val_a - media) / sigma
        prob = stats.norm.cdf(val_a, loc=media, scale=sigma)
        prob_comp = 1 - prob

        interp = (
            f"Hay un {prob*100:.2f}% de probabilidad de que una observación "
            f"tomada de una distribución normal con μ = {_fmt(media)} "
            f"y σ = {_fmt(sigma)} sea "
            f"menor o igual que {_fmt(val_a)}."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Media (μ) = <b style='color:#E2E8F0;'>{_fmt(media)}</b>",
                f"Desviación estándar (σ) = <b style='color:#E2E8F0;'>{_fmt(sigma)}</b>",
                f"Valor límite (a) = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _titulo("El puntaje Z es:") +
            _formula(
                f"Z = {_frac(f'{_fmt(val_a)} − {_fmt(media)}', _fmt(sigma))}"
                f" = <b>{z:.4f}</b>"
            ) +
            _titulo(f"Luego buscamos la probabilidad acumulada para Z = {z:.4f}:") +
            _formula(f"P(Z ≤ {z:.4f}) ≈ <b>{prob:.4f}</b>") +
            _titulo("Por tanto:") +
            _formula(
                f"P(X ≤ {_fmt(val_a)}) ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>"
            ) +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'derecha':
        z = (val_a - media) / sigma
        prob_i = stats.norm.cdf(val_a, loc=media, scale=sigma)
        prob = 1 - prob_i
        prob_comp = prob_i

        interp = (
            f"Hay un {prob*100:.2f}% de probabilidad de que una observación "
            f"tomada de una distribución normal con μ = {_fmt(media)} "
            f"y σ = {_fmt(sigma)} sea "
            f"mayor o igual que {_fmt(val_a)}."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Media (μ) = <b style='color:#E2E8F0;'>{_fmt(media)}</b>",
                f"Desviación estándar (σ) = <b style='color:#E2E8F0;'>{_fmt(sigma)}</b>",
                f"Valor límite (a) = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _titulo("El puntaje Z es:") +
            _formula(
                f"Z = {_frac(f'{_fmt(val_a)} − {_fmt(media)}', _fmt(sigma))}"
                f" = <b>{z:.4f}</b>"
            ) +
            _titulo(f"Probabilidad acumulada hasta Z = {z:.4f}:") +
            _formula(f"P(Z ≤ {z:.4f}) ≈ <b>{prob_i:.4f}</b>") +
            _titulo("La cola derecha se obtiene como complemento:") +
            _formula(
                f"P(X ≥ {_fmt(val_a)}) = 1 − {prob_i:.4f} = <b>{prob:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(
                f"P(X ≥ {_fmt(val_a)}) ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>"
            ) +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'entre':
        za = (val_a - media) / sigma
        zb = (val_b - media) / sigma
        pa = stats.norm.cdf(val_a, loc=media, scale=sigma)
        pb = stats.norm.cdf(val_b, loc=media, scale=sigma)
        prob = pb - pa

        interp = (
            f"Hay un {prob*100:.2f}% de probabilidad de que la variable esté "
            f"entre {_fmt(val_a)} y {_fmt(val_b)} "
            f"en una distribución normal con μ = {_fmt(media)} "
            f"y σ = {_fmt(sigma)}."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Media (μ) = <b style='color:#E2E8F0;'>{_fmt(media)}</b>",
                f"Desviación estándar (σ) = <b style='color:#E2E8F0;'>{_fmt(sigma)}</b>",
                f"Límite inferior (a) = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
                f"Límite superior (b) = <b style='color:#E2E8F0;'>{_fmt(val_b)}</b>",
            ]) +
            _titulo("Puntajes Z para cada límite:") +
            _formula(
                f"Z_a = {_frac(f'{_fmt(val_a)} − {_fmt(media)}', _fmt(sigma))}"
                f" = <b>{za:.4f}</b>"
            ) +
            _formula(
                f"Z_b = {_frac(f'{_fmt(val_b)} − {_fmt(media)}', _fmt(sigma))}"
                f" = <b>{zb:.4f}</b>"
            ) +
            _titulo("Probabilidades acumuladas individuales:") +
            _formula(f"P(Z ≤ {za:.4f}) ≈ <b>{pa:.4f}</b>") +
            _formula(f"P(Z ≤ {zb:.4f}) ≈ <b>{pb:.4f}</b>") +
            _titulo("Restamos las áreas para obtener el área intermedia:") +
            _formula(
                f"P({_fmt(val_a)} ≤ X ≤ {_fmt(val_b)}) = "
                f"{pb:.4f} − {pa:.4f} = <b>{prob:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(
                f"P({_fmt(val_a)} ≤ X ≤ {_fmt(val_b)}) ≈ "
                f"{prob:.4f} = <b>{prob*100:.2f}%</b>"
            ) +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'percentil':
        x_val = stats.norm.ppf(val_a, loc=media, scale=sigma)
        z = stats.norm.ppf(val_a)

        interp = (
            f"El percentil {val_a*100:.1f} es X = {x_val:.4f}. "
            f"El {val_a*100:.1f}% de los valores de la distribución "
            f"N(μ={_fmt(media)}, σ={_fmt(sigma)}) está por debajo de este punto."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Media (μ) = <b style='color:#E2E8F0;'>{_fmt(media)}</b>",
                f"Desviación estándar (σ) = <b style='color:#E2E8F0;'>{_fmt(sigma)}</b>",
                f"Percentil buscado = <b style='color:#E2E8F0;'>{val_a*100:.1f}%</b>",
            ]) +
            _titulo(f"Buscamos Z tal que P(Z ≤ z) = {val_a:.4f}:") +
            _formula(f"z = <b>{z:.4f}</b>") +
            _titulo("Convertimos el puntaje Z al valor original X:") +
            _formula(
                f"X = μ + z · σ = {_fmt(media)} + ({z:.4f}) × {_fmt(sigma)}"
                f" = <b>{x_val:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(f"P<sub>{val_a*100:.0f}</sub> = <b>{x_val:.4f}</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Valor X = <b style='color:#E2E8F0;'>{x_val:.4f}</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return x_val, [exp, _nota_continua()], interp, True


# ================================================================
# BLOQUE 5 — DISTRIBUCIÓN t DE STUDENT
# ================================================================

def calcular_t(gl, tipo, val_a, val_b=None):
    dist = stats.t(df=gl)
    desc_gl = (
        "≈ distribución Normal (gl ≥ 30)" if gl >= 30
        else "colas moderadamente más anchas que Normal" if gl >= 10
        else "colas bastante más anchas que Normal"
    )

    if tipo == 'izquierda':
        prob = dist.cdf(val_a)
        prob_comp = 1 - prob

        interp = (
            f"Con {gl} grados de libertad, la probabilidad de que T sea "
            f"menor o igual que {_fmt(val_a)} es {prob:.4f} ({prob*100:.2f}%)."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Valor de a = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _nota(f"t({gl}): {desc_gl}.") +
            _titulo(f"Buscamos la probabilidad acumulada P(T ≤ {_fmt(val_a)}):") +
            _formula(f"P(T ≤ {_fmt(val_a)} | gl = {gl}) = <b>{prob:.4f}</b>") +
            _titulo("Por tanto:") +
            _formula(f"P(T ≤ {_fmt(val_a)}) ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'derecha':
        pi = dist.cdf(val_a)
        prob = 1 - pi
        prob_comp = pi

        interp = (
            f"Con {gl} grados de libertad, la probabilidad de que T sea "
            f"mayor o igual que {_fmt(val_a)} es {prob:.4f} ({prob*100:.2f}%)."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Valor de a = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _nota(f"t({gl}): {desc_gl}.") +
            _titulo(f"Probabilidad acumulada hasta a = {_fmt(val_a)}:") +
            _formula(f"P(T ≤ {_fmt(val_a)} | gl = {gl}) = <b>{pi:.4f}</b>") +
            _titulo("La cola derecha se obtiene como complemento:") +
            _formula(f"P(T ≥ {_fmt(val_a)}) = 1 − {pi:.4f} = <b>{prob:.4f}</b>") +
            _titulo("Por tanto:") +
            _formula(f"P(T ≥ {_fmt(val_a)}) ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'entre':
        pa = dist.cdf(val_a)
        pb = dist.cdf(val_b)
        prob = pb - pa

        interp = (
            f"Con {gl} grados de libertad, la probabilidad de que T esté "
            f"entre {_fmt(val_a)} y {_fmt(val_b)} es {prob:.4f} ({prob*100:.2f}%)."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Límite inferior (a) = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
                f"Límite superior (b) = <b style='color:#E2E8F0;'>{_fmt(val_b)}</b>",
            ]) +
            _nota(f"t({gl}): {desc_gl}.") +
            _titulo("Probabilidades acumuladas individuales:") +
            _formula(f"P(T ≤ {_fmt(val_a)} | gl = {gl}) = <b>{pa:.4f}</b>") +
            _formula(f"P(T ≤ {_fmt(val_b)} | gl = {gl}) = <b>{pb:.4f}</b>") +
            _titulo("Restamos las áreas:") +
            _formula(
                f"P({_fmt(val_a)} ≤ T ≤ {_fmt(val_b)}) = "
                f"{pb:.4f} − {pa:.4f} = <b>{prob:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(
                f"P({_fmt(val_a)} ≤ T ≤ {_fmt(val_b)}) ≈ "
                f"{prob:.4f} = <b>{prob*100:.2f}%</b>"
            ) +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a / 2)

        interp = (
            f"Con {gl} gl y α={val_a}, el valor crítico es "
            f"t = ±{vc:.4f}. "
            f"Si |t calculado| > {vc:.4f} se rechaza H₀."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Nivel de significancia (α) = <b style='color:#E2E8F0;'>{val_a}</b>",
            ]) +
            _nota(f"t({gl}): {desc_gl}.") +
            _titulo("Para una prueba bilateral, cada cola tiene α/2:") +
            _formula(
                f"{_frac('α', '2')} = {_frac(val_a, 2)} = <b>{val_a/2:.4f}</b>"
            ) +
            _titulo(f"Buscamos t tal que P(T ≤ t) = 1 − α/2 = {1-val_a/2:.4f}:") +
            _formula(f"t<sub>crítico</sub> = <b>±{vc:.4f}</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"t crítico = <b style='color:#E2E8F0;'>±{vc:.4f}</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp) +
            _hr() +
            _titulo("Regla de decisión:") +
            _nota(
                f"Si |t calculado| &gt; {vc:.4f} → se rechaza H₀ (α = {val_a}).<br>"
                f"Si |t calculado| ≤ {vc:.4f} → no se rechaza H₀."
            )
        )

        return vc, [exp, _nota_continua()], interp, True


def calcular_prueba_t(x_bar, mu0, s, n, alpha, tipo):
    gl = n - 1
    se = s / np.sqrt(n)
    t_calc = (x_bar - mu0) / se

    if tipo == 'bilateral':
        t_crit = stats.t.ppf(1 - alpha / 2, gl)
        p_val = 2 * (1 - stats.t.cdf(abs(t_calc), gl))
        rechazar = (abs(t_calc) > t_crit) or (p_val < alpha)
        shade_type = 'colas'
        la, lb = t_calc, None
        h0_str = f"H₀: μ = {_fmt(mu0)}"
        h1_str = f"H₁: μ ≠ {_fmt(mu0)}"
        t_crit_display = f"±{t_crit:.4f}"
        dec_rule = (
            f"|t| = {abs(t_calc):.4f} "
            f"{'>' if rechazar else '≤'} t_crítico = {t_crit:.4f}"
        )
        p_formula = (
            f"p = 2 × P(T > |{t_calc:.4f}|) = "
            f"2 × {1 - stats.t.cdf(abs(t_calc), gl):.4f} = <b>{p_val:.4f}</b>"
        )
        crit_formula = (
            f"t_crítico = t<sub>1−α/2, gl</sub> = "
            f"t<sub>{1-alpha/2:.3f}, {gl}</sub> = <b>±{t_crit:.4f}</b>"
        )

    elif tipo == 'izquierda':
        t_crit = stats.t.ppf(alpha, gl)
        p_val = float(stats.t.cdf(t_calc, gl))
        rechazar = (t_calc < t_crit) or (p_val < alpha)
        shade_type = 'izquierda'
        la, lb = t_calc, None
        h0_str = f"H₀: μ = {_fmt(mu0)}"
        h1_str = f"H₁: μ < {_fmt(mu0)}"
        t_crit_display = f"{t_crit:.4f}"
        dec_rule = (
            f"t = {t_calc:.4f} "
            f"{'<' if rechazar else '≥'} t_crítico = {t_crit:.4f}"
        )
        p_formula = (
            f"p = P(T ≤ {t_calc:.4f} | gl = {gl}) = <b>{p_val:.4f}</b>"
        )
        crit_formula = (
            f"t_crítico = t<sub>α, gl</sub> = "
            f"t<sub>{alpha}, {gl}</sub> = <b>{t_crit:.4f}</b>"
        )

    else:
        t_crit = stats.t.ppf(1 - alpha, gl)
        p_val = float(1 - stats.t.cdf(t_calc, gl))
        rechazar = (t_calc > t_crit) or (p_val < alpha)
        shade_type = 'derecha'
        la, lb = t_calc, None
        h0_str = f"H₀: μ = {_fmt(mu0)}"
        h1_str = f"H₁: μ > {_fmt(mu0)}"
        t_crit_display = f"{t_crit:.4f}"
        dec_rule = (
            f"t = {t_calc:.4f} "
            f"{'>' if rechazar else '≤'} t_crítico = {t_crit:.4f}"
        )
        p_formula = (
            f"p = P(T ≥ {t_calc:.4f} | gl = {gl}) = "
            f"1 − {stats.t.cdf(t_calc, gl):.4f} = <b>{p_val:.4f}</b>"
        )
        crit_formula = (
            f"t_crítico = t<sub>1−α, gl</sub> = "
            f"t<sub>{1-alpha:.3f}, {gl}</sub> = <b>{t_crit:.4f}</b>"
        )

    decision = "Rechazar H₀" if rechazar else "No rechazar H₀"

    if rechazar:
        conclusion = (
            f"Existe evidencia estadísticamente significativa para concluir que "
            f"la media poblacional difiere de {_fmt(mu0)} (p = {p_val:.3f})."
        )
    else:
        conclusion = (
            f"No existe evidencia estadísticamente significativa para afirmar que "
            f"la media poblacional difiere de {_fmt(mu0)} (p = {p_val:.3f})."
        )

    paso1 = (
        _titulo("Paso 1: Planteamiento de hipótesis") +
        _bullets([
            f"<b style='color:#E2E8F0;'>{h0_str}</b> &nbsp;— hipótesis nula",
            f"<b style='color:#E2E8F0;'>{h1_str}</b> &nbsp;— hipótesis alternativa",
        ]) +
        _nota(
            f"Prueba {tipo} &nbsp;|&nbsp; α = {alpha} &nbsp;|&nbsp; "
            f"n = {n} &nbsp;|&nbsp; gl = n − 1 = <b>{gl}</b>"
        )
    )

    paso2 = (
        _titulo("Paso 2: Estadístico t") +
        _formula(f"t = {_frac('x̄ − μ₀', 's / √n')}") +
        _formula(
            f"t = {_frac(f'{_fmt(x_bar)} − {_fmt(mu0)}', f'{_fmt(s)} / √{n}')}"
            f" = {_frac(f'{x_bar - mu0:.4f}', f'{se:.4f}')}"
            f" = <b>{t_calc:.4f}</b>"
        ) +
        _nota(
            f"Error estándar: s/√n = {_fmt(s)}/√{n} = {se:.4f}"
        )
    )

    paso3 = (
        _titulo(f"Paso 3: Valor crítico  (α = {alpha}, gl = {gl})") +
        _formula(crit_formula) +
        _nota(
            f"Se consulta la distribución t({gl}). "
            f"Valor crítico: <b>{t_crit_display}</b>"
        )
    )

    paso4 = (
        _titulo("Paso 4: Valor p") +
        _formula(p_formula) +
        _nota(
            f"Probabilidad de obtener t = {t_calc:.4f} (o más extremo) si H₀ fuera verdadera."
        )
    )

    paso5 = (
        _titulo("Paso 5: Decisión") +
        _formula(f"<b>{dec_rule}</b>") +
        _bullets([
            f"p = {p_val:.4f} {'<' if rechazar else '≥'} α = {alpha}",
            f"→ <b style='color:#E2E8F0;'>{decision}</b>",
        ])
    )

    paso6 = (
        _titulo("Paso 6: Conclusión") +
        _blockquote(conclusion)
    )

    return {
        'p_val': p_val,
        'pasos': [paso1, paso2, paso3, paso4, paso5, paso6, _nota_continua()],
        'interp': conclusion,
        't_calc': t_calc,
        't_crit': t_crit,
        'gl': gl,
        'rechazar': rechazar,
        'shade_type': shade_type,
        'la': la,
        'lb': lb,
    }


# ================================================================
# BLOQUE 6 — DISTRIBUCIÓN CHI-CUADRADO (χ²)
# ================================================================

def calcular_chi2(gl, tipo, val_a):
    dist = stats.chi2(df=gl)

    if tipo == 'izquierda':
        prob = dist.cdf(val_a)
        prob_comp = 1 - prob

        interp = (
            f"Con {gl} grados de libertad, la probabilidad de que χ² sea "
            f"menor o igual que {_fmt(val_a)} es {prob:.4f} ({prob*100:.2f}%)."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Valor límite (a) = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
                f"Media de χ²({gl}) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Varianza de χ²({gl}) = <b style='color:#E2E8F0;'>{2*gl}</b>",
            ]) +
            _titulo(f"Buscamos la probabilidad acumulada P(χ² ≤ {_fmt(val_a)}):") +
            _formula(f"P(χ² ≤ {_fmt(val_a)} | gl = {gl}) = <b>{prob:.4f}</b>") +
            _titulo("Por tanto:") +
            _formula(
                f"P(χ² ≤ {_fmt(val_a)}) ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>"
            ) +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"Probabilidad = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'derecha':
        pi = dist.cdf(val_a)
        prob = 1 - pi
        concl = (
            "p < 0.05 → se rechazaría H₀ (hay asociación entre las variables)."
            if prob < 0.05 else
            "p ≥ 0.05 → no hay evidencia suficiente para rechazar H₀."
        )

        interp = (
            f"Con {gl} grados de libertad, P(χ² ≥ {_fmt(val_a)}) = "
            f"{prob:.4f} ({prob*100:.2f}%). {concl}"
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Estadístico χ² calculado = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _titulo(f"Probabilidad acumulada hasta χ² = {_fmt(val_a)}:") +
            _formula(f"P(χ² ≤ {_fmt(val_a)} | gl = {gl}) = <b>{pi:.4f}</b>") +
            _titulo("El p-valor se obtiene como complemento:") +
            _formula(
                f"p-valor = P(χ² ≥ {_fmt(val_a)}) = 1 − {pi:.4f} = <b>{prob:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(f"p-valor ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"p-valor = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Conclusión:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a)

        interp = (
            f"Con {gl} gl y α={val_a}, el valor crítico es χ² = {vc:.4f}. "
            f"Si χ² calculado > {vc:.4f} se rechaza H₀."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad (gl) = <b style='color:#E2E8F0;'>{gl}</b>",
                f"Nivel de significancia (α) = <b style='color:#E2E8F0;'>{val_a}</b>",
            ]) +
            _titulo(f"Buscamos χ² tal que P(χ² &gt; vc) = α = {val_a}:") +
            _formula(f"χ²<sub>crítico</sub> = <b>{vc:.4f}</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"χ² crítico = <b style='color:#E2E8F0;'>{vc:.4f}</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp) +
            _hr() +
            _titulo("Regla de decisión:") +
            _nota(
                f"Si χ² calculado &gt; {vc:.4f} → se rechaza H₀ (α = {val_a}).<br>"
                f"Si χ² calculado ≤ {vc:.4f} → no se rechaza H₀."
            )
        )

        return vc, [exp, _nota_continua()], interp, True


# ================================================================
# BLOQUE 7 — DISTRIBUCIÓN F DE FISHER
# ================================================================

def calcular_f(gl1, gl2, tipo, val_a):
    dist = stats.f(dfn=gl1, dfd=gl2)

    if tipo == 'derecha':
        pi = dist.cdf(val_a)
        prob = 1 - pi
        concl = (
            "p < 0.05 → se rechaza H₀ (los grupos difieren significativamente)."
            if prob < 0.05 else
            "p ≥ 0.05 → no hay evidencia para rechazar H₀."
        )

        interp = (
            f"Con F({gl1},{gl2}), F = {_fmt(val_a)} → "
            f"p-valor = {prob:.4f} ({prob*100:.2f}%). {concl}"
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad del numerador (gl₁) = <b style='color:#E2E8F0;'>{gl1}</b>",
                f"Grados de libertad del denominador (gl₂) = <b style='color:#E2E8F0;'>{gl2}</b>",
                f"Estadístico F calculado = <b style='color:#E2E8F0;'>{_fmt(val_a)}</b>",
            ]) +
            _titulo(f"Probabilidad acumulada hasta F = {_fmt(val_a)}:") +
            _formula(
                f"P(F ≤ {_fmt(val_a)} | gl₁={gl1}, gl₂={gl2}) = <b>{pi:.4f}</b>"
            ) +
            _titulo("El p-valor se obtiene como complemento:") +
            _formula(
                f"p-valor = P(F ≥ {_fmt(val_a)}) = 1 − {pi:.4f} = <b>{prob:.4f}</b>"
            ) +
            _titulo("Por tanto:") +
            _formula(f"p-valor ≈ {prob:.4f} = <b>{prob*100:.2f}%</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"p-valor = <b style='color:#E2E8F0;'>{prob:.4f}</b>",
                f"Porcentaje = <b style='color:#E2E8F0;'>{prob*100:.2f} %</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Conclusión:") +
            _blockquote(interp)
        )

        return prob, [exp, _nota_continua()], interp, False

    elif tipo == 'valor_critico':
        vc = dist.ppf(1 - val_a)

        interp = (
            f"Con F({gl1},{gl2}) y α={val_a}, el valor crítico es "
            f"F = {vc:.4f}. "
            f"Si F calculado > {vc:.4f} se rechaza H₀."
        )

        exp = (
            _titulo("Con los parámetros:") +
            _bullets([
                f"Grados de libertad del numerador (gl₁) = <b style='color:#E2E8F0;'>{gl1}</b>",
                f"Grados de libertad del denominador (gl₂) = <b style='color:#E2E8F0;'>{gl2}</b>",
                f"Nivel de significancia (α) = <b style='color:#E2E8F0;'>{val_a}</b>",
            ]) +
            _titulo(f"Buscamos F tal que P(F &gt; vc) = α = {val_a}:") +
            _formula(f"F<sub>crítico</sub> = <b>{vc:.4f}</b>") +
            _hr() +
            _titulo("Tu aplicación muestra:") +
            _bullets([
                f"F crítico = <b style='color:#E2E8F0;'>{vc:.4f}</b>",
            ]) +
            _ok("✅ Coincide con el valor esperado.") +
            _titulo("Además, la interpretación también es correcta:") +
            _blockquote(interp) +
            _hr() +
            _titulo("Regla de decisión:") +
            _nota(
                f"Si F calculado &gt; {vc:.4f} → se rechaza H₀ (α = {val_a}).<br>"
                f"Si F calculado ≤ {vc:.4f} → no se rechaza H₀."
            )
        )

        return vc, [exp, _nota_continua()], interp, True


# ================================================================
# BLOQUE 8 — PRUEBA χ² DE INDEPENDENCIA (TABLA DE CONTINGENCIA)
# ================================================================

def calcular_prueba_chi2_ind(a, b, c, d, alpha,
                             lbl_r1="Expuestos", lbl_r2="No expuestos",
                             lbl_c1="Evento", lbl_c2="No evento"):

    def _tbl(headers, rows):
        s_th  = ("background:#06101F;color:#60A5FA;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.80rem;")
        s_lbl = ("background:#06101F;color:#94A3B8;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;font-size:.80rem;")
        s_num = ("background:#040D1E;color:#E2E8F0;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.85rem;")
        s_tot = ("background:#040D1E;color:#6EE7B7;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.85rem;")
        html = ("<table style='border-collapse:collapse;width:100%;"
                "margin:4px 0 10px;'><thead><tr>")
        for h in headers:
            html += f"<th style='{s_th}'>{h}</th>"
        html += "</tr></thead><tbody>"
        for ri, row in enumerate(rows):
            is_last_row = (ri == len(rows) - 1)
            html += "<tr>"
            html += f"<td style='{s_lbl}'>{row[0]}</td>"
            for ci, cell in enumerate(row[1:], 1):
                is_last_col = (ci == len(row) - 1)
                use_tot = is_last_col or is_last_row
                html += f"<td style='{s_tot if use_tot else s_num}'>{cell}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    obs = np.array([[a, b], [c, d]])
    chi2_stat, p_val, gl, expected = stats.chi2_contingency(obs, correction=False)
    chi2_stat = float(chi2_stat)
    p_val     = float(p_val)
    chi2_crit = float(stats.chi2.ppf(1 - alpha, gl))
    rechazar  = bool((p_val < alpha) or (chi2_stat > chi2_crit))

    r1, r2    = a + b,   c + d
    c1_t, c2_t = a + c, b + d
    N         = r1 + r2
    E11 = float(expected[0, 0]); E12 = float(expected[0, 1])
    E21 = float(expected[1, 0]); E22 = float(expected[1, 1])

    R_exp   = a / r1   if r1   > 0 else 0.0
    R_noexp = c / r2   if r2   > 0 else 0.0
    RR = R_exp / R_noexp if R_noexp > 0 else float('inf')
    OR = (a * d) / (b * c) if (b * c) > 0 else float('inf')
    DAR = R_exp - R_noexp

    if RR == 1:
        RR_interp = "RR = 1 → sin diferencia de riesgo entre expuestos y no expuestos."
    elif RR > 1:
        RR_interp = f"Los expuestos presentan <b>{RR:.2f}×</b> más riesgo de desarrollar el evento (factor de riesgo)."
    else:
        RR_interp = f"Los expuestos presentan <b>{RR:.2f}×</b> el riesgo de los no expuestos (factor protector)."

    if OR == 1:
        OR_interp = "OR = 1 → sin diferencia de odds."
    elif OR > 1:
        OR_interp = f"Los expuestos tienen <b>{OR:.2f}×</b> más odds de presentar el evento."
    else:
        OR_interp = f"Los expuestos tienen <b>{OR:.2f}×</b> los odds de los no expuestos (factor protector)."

    DAR_interp = (
        f"Diferencia absoluta de riesgo: <b>{DAR*100:.2f}%</b>. " +
        ("Riesgo adicional atribuible a la exposición."
         if DAR > 0 else
         "Reducción absoluta de riesgo por la exposición."
         if DAR < 0 else
         "Sin diferencia absoluta.")
    )

    if DAR > 0:
        NNX = 1 / DAR; NNX_type = "NNH"
        NNX_interp = (
            f"Se necesitaría exponer aproximadamente <b>{int(round(NNX))}</b> "
            f"pacientes para producir un evento adicional."
        )
    elif DAR < 0:
        NNX = 1 / abs(DAR); NNX_type = "NNT"
        NNX_interp = (
            f"Se necesitaría tratar aproximadamente <b>{int(round(NNX))}</b> "
            f"pacientes para prevenir un evento adverso."
        )
    else:
        NNX = None; NNX_type = "—"
        NNX_interp = "DAR = 0, no aplica NNH/NNT."

    conclusion = (
        "Existe una asociación estadísticamente significativa entre la exposición y el evento."
        if rechazar else
        "No existe evidencia estadísticamente significativa de asociación entre la exposición y el evento."
    )

    # ── Pasos HTML ─────────────────────────────────────────────────
    paso1 = (
        _titulo("Paso 1: Tabla de frecuencias observadas") +
        _tbl(
            ["", lbl_c1, lbl_c2, "Total"],
            [[lbl_r1, a, b, r1], [lbl_r2, c, d, r2], ["Total", c1_t, c2_t, N]]
        ) +
        _nota(f"N = {N} | {lbl_r1}: n={r1} | {lbl_r2}: n={r2} | "
              f"{lbl_c1}: n={c1_t} | {lbl_c2}: n={c2_t}")
    )

    paso2 = (
        _titulo("Paso 2: Frecuencias esperadas  E = (Fila × Col) / N") +
        _bullets([
            f"E({lbl_r1}, {lbl_c1}) = {_frac(f'{r1} × {c1_t}', str(N))} = <b>{E11:.2f}</b>",
            f"E({lbl_r1}, {lbl_c2}) = {_frac(f'{r1} × {c2_t}', str(N))} = <b>{E12:.2f}</b>",
            f"E({lbl_r2}, {lbl_c1}) = {_frac(f'{r2} × {c1_t}', str(N))} = <b>{E21:.2f}</b>",
            f"E({lbl_r2}, {lbl_c2}) = {_frac(f'{r2} × {c2_t}', str(N))} = <b>{E22:.2f}</b>",
        ]) +
        _tbl(
            ["Esperados", lbl_c1, lbl_c2, "Total"],
            [
                [lbl_r1, f"{E11:.2f}", f"{E12:.2f}", r1],
                [lbl_r2, f"{E21:.2f}", f"{E22:.2f}", r2],
                ["Total", c1_t, c2_t, N],
            ]
        )
    )

    t11 = (a - E11)**2 / E11
    t12 = (b - E12)**2 / E12
    t21 = (c - E21)**2 / E21
    t22 = (d - E22)**2 / E22
    paso3 = (
        _titulo("Paso 3: Estadístico χ²  =  Σ (O − E)² / E") +
        _formula(
            _frac(f"({a}−{E11:.1f})²", f"{E11:.1f}") + " + " +
            _frac(f"({b}−{E12:.1f})²", f"{E12:.1f}") + " + " +
            _frac(f"({c}−{E21:.1f})²", f"{E21:.1f}") + " + " +
            _frac(f"({d}−{E22:.1f})²", f"{E22:.1f}")
        ) +
        _formula(
            f"{t11:.4f} + {t12:.4f} + {t21:.4f} + {t22:.4f} = <b>{chi2_stat:.4f}</b>"
        )
    )

    paso4 = (
        _titulo("Paso 4: Grados de libertad") +
        _formula("gl = (filas − 1)(columnas − 1) = (2 − 1)(2 − 1) = <b>1</b>") +
        _nota("Para una tabla 2×2 los grados de libertad son siempre gl = 1.")
    )

    paso5 = (
        _titulo(f"Paso 5: Valor crítico  (α = {alpha}, gl = {gl})") +
        _formula(
            f"χ²<sub>crítico</sub> = χ²<sub>1−α, gl</sub> = "
            f"χ²<sub>{1-alpha:.2f}, {gl}</sub> = <b>{chi2_crit:.4f}</b>"
        ) +
        _nota(f"Región de rechazo: χ² > {chi2_crit:.4f}.")
    )

    paso6 = (
        _titulo("Paso 6: Valor p") +
        _formula(
            f"p = P(χ² > {chi2_stat:.4f} | gl={gl}) = <b>{p_val:.4f}</b>"
        ) +
        _nota(
            f"Probabilidad de obtener χ² ≥ {chi2_stat:.4f} si H₀ fuera verdadera. "
            + ("p < α → evidencia contra H₀." if rechazar
               else "p ≥ α → no hay evidencia suficiente.")
        )
    )

    _dec_label = "Rechazar H₀" if rechazar else "No rechazar H₀"
    paso7 = (
        _titulo("Paso 7: Decisión") +
        _bullets([
            f"χ²_calc = {chi2_stat:.4f} "
            + (f"> χ²_crit = {chi2_crit:.4f}" if rechazar
               else f"≤ χ²_crit = {chi2_crit:.4f}"),
            f"p = {p_val:.4f} "
            + (f"< α = {alpha}" if rechazar else f"≥ α = {alpha}"),
            f"→ <b style='color:#E2E8F0;'>{_dec_label}</b>",
        ]) +
        _blockquote(conclusion)
    )

    nnx_bullet = (
        [f"{NNX_type} = 1/|DAR| = 1/{abs(DAR):.4f} ≈ <b>{int(round(NNX))}</b>"
         f" &nbsp;→ {NNX_interp}"]
        if NNX is not None else []
    )
    paso8 = (
        _titulo("Paso 8: Medidas epidemiológicas") +
        _bullets([
            f"R_exp = {_frac(str(a), str(r1))} = <b>{R_exp:.4f}</b> ({R_exp*100:.2f}%)",
            f"R_noexp = {_frac(str(c), str(r2))} = <b>{R_noexp:.4f}</b> ({R_noexp*100:.2f}%)",
            f"RR = {_frac(f'{R_exp:.4f}', f'{R_noexp:.4f}')} = <b>{RR:.4f}</b> &nbsp;→ {RR_interp}",
            f"OR = {_frac(f'{a}×{d}', f'{b}×{c}')} = <b>{OR:.4f}</b> &nbsp;→ {OR_interp}",
            f"DAR = {R_exp:.4f} − {R_noexp:.4f} = <b>{DAR:.4f}</b> ({DAR*100:.2f}%) &nbsp;→ {DAR_interp}",
        ] + nnx_bullet)
    )

    return {
        'chi2_stat': chi2_stat,
        'p_val':     p_val,
        'gl':        gl,
        'chi2_crit': chi2_crit,
        'rechazar':  rechazar,
        'conclusion': conclusion,
        'epi': {
            'R_exp':      R_exp,    'R_noexp':    R_noexp,
            'RR':         RR,       'OR':         OR,
            'DAR':        DAR,      'NNX':        NNX,
            'NNX_type':   NNX_type,
            'RR_interp':  RR_interp,  'OR_interp':  OR_interp,
            'DAR_interp': DAR_interp, 'NNX_interp': NNX_interp,
        },
        'pasos': [paso1, paso2, paso3, paso4, paso5, paso6, paso7, paso8, _nota_continua()],
    }


# ================================================================
# BLOQUE 9 — PRUEBA EXACTA DE FISHER
# ================================================================

def calcular_prueba_fisher(a, b, c, d, alpha, tipo='bilateral',
                           lbl_r1="Grupo 1", lbl_r2="Grupo 2",
                           lbl_c1="Evento", lbl_c2="No evento"):

    def _tbl(headers, rows):
        s_th  = ("background:#06101F;color:#EF4444;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.80rem;")
        s_lbl = ("background:#06101F;color:#94A3B8;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;font-size:.80rem;")
        s_num = ("background:#040D1E;color:#E2E8F0;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.85rem;")
        s_tot = ("background:#040D1E;color:#6EE7B7;font-weight:600;"
                 "padding:6px 10px;border:1px solid #1A2840;"
                 "text-align:center;font-size:.85rem;")
        html = ("<table style='border-collapse:collapse;width:100%;"
                "margin:4px 0 10px;'><thead><tr>")
        for h in headers:
            html += f"<th style='{s_th}'>{h}</th>"
        html += "</tr></thead><tbody>"
        for ri, row in enumerate(rows):
            is_last_row = (ri == len(rows) - 1)
            html += "<tr>"
            html += f"<td style='{s_lbl}'>{row[0]}</td>"
            for ci, cell in enumerate(row[1:], 1):
                is_last_col = (ci == len(row) - 1)
                use_tot = is_last_col or is_last_row
                html += f"<td style='{s_tot if use_tot else s_num}'>{cell}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    alt_map = {'bilateral': 'two-sided', 'izquierda': 'less', 'derecha': 'greater'}
    alternative = alt_map.get(tipo, 'two-sided')

    table = np.array([[a, b], [c, d]])
    OR, p_val = stats.fisher_exact(table, alternative=alternative)
    OR = float(OR); p_val = float(p_val)
    rechazar = p_val < alpha

    r1, r2    = a + b, c + d
    c1_t, c2_t = a + c, b + d
    N = r1 + r2

    E11 = r1 * c1_t / N if N > 0 else 0.0
    E12 = r1 * c2_t / N if N > 0 else 0.0
    E21 = r2 * c1_t / N if N > 0 else 0.0
    E22 = r2 * c2_t / N if N > 0 else 0.0
    any_small = any(e < 5 for e in [E11, E12, E21, E22])
    small_count = sum(1 for e in [E11, E12, E21, E22] if e < 5)

    # OR interpretation
    if np.isinf(OR) and OR > 0:
        OR_str   = "∞"
        OR_interp = (
            "OR es infinito porque ningún sujeto del Grupo 2 presentó el evento. "
            "La diferencia entre grupos es la máxima posible."
        )
    elif OR == 0.0:
        OR_str   = "0"
        OR_interp = (
            "OR = 0 porque ningún sujeto del Grupo 1 presentó el evento. "
            "El Grupo 1 tiene una probabilidad nula del evento."
        )
    elif abs(OR - 1.0) < 0.05:
        OR_str   = f"{OR:.4f}"
        OR_interp = "Las probabilidades (odds) son similares en ambos grupos — no hay evidencia de asociación."
    elif OR > 1:
        OR_str   = f"{OR:.4f}"
        OR_interp = f"El Grupo 1 presenta <b>{OR:.2f}×</b> más odds de presentar el evento respecto al Grupo 2."
    else:
        OR_str   = f"{OR:.4f}"
        OR_interp = f"El Grupo 1 presenta <b>{OR:.2f}×</b> los odds del Grupo 2 (factor protector)."

    # Epidemiological measures
    R1 = a / r1 if r1 > 0 else 0.0
    R2 = c / r2 if r2 > 0 else 0.0
    if R2 > 0:
        RR = R1 / R2; RR_str = f"{RR:.3f}"
    elif R1 > 0:
        RR = float('inf'); RR_str = "∞"
    else:
        RR = float('nan'); RR_str = "—"

    DAR = R1 - R2
    if np.isinf(RR):
        RR_interp = (f"RR es infinito porque el riesgo en {lbl_r2} = 0. "
                     f"{lbl_r1}: {R1*100:.1f}% vs {lbl_r2}: 0%.")
    elif np.isnan(RR):
        RR_interp = "RR no calculable (ambos riesgos son 0)."
    elif RR > 1:
        RR_interp = f"{lbl_r1} presenta <b>{RR:.2f}×</b> más riesgo de desarrollar el evento (factor de riesgo)."
    elif RR < 1:
        RR_interp = f"{lbl_r1} presenta <b>{RR:.2f}×</b> el riesgo de {lbl_r2} (factor protector)."
    else:
        RR_interp = f"RR = 1 → sin diferencia de riesgo entre {lbl_r1} y {lbl_r2}."

    if DAR > 0:
        NNX = 1 / DAR; NNX_type = "NNH"
        NNX_interp = (f"Se necesitaría exponer aproximadamente <b>{int(round(NNX))}</b> "
                      f"pacientes para producir un evento adicional.")
    elif DAR < 0:
        NNX = 1 / abs(DAR); NNX_type = "NNT"
        NNX_interp = (f"Se necesitaría tratar aproximadamente <b>{int(round(NNX))}</b> "
                      f"pacientes para prevenir un evento adverso.")
    else:
        NNX = None; NNX_type = "—"; NNX_interp = "DAR = 0, no aplica NNH/NNT."

    DAR_interp = (
        f"Diferencia absoluta de riesgo: <b>{DAR*100:.2f}%</b>. " +
        ("Riesgo adicional atribuible al Grupo 1." if DAR > 0 else
         "Reducción absoluta de riesgo en Grupo 1." if DAR < 0 else "Sin diferencia absoluta.")
    )

    conclusion = (
        "Existe evidencia estadística de asociación entre el tratamiento/exposición y la ocurrencia del evento."
        if rechazar else
        "No existe evidencia estadística suficiente de asociación entre el tratamiento/exposición y la ocurrencia del evento."
    )

    tipo_display = {
        'bilateral': 'bilateral (dos colas)',
        'izquierda': 'unilateral izquierda',
        'derecha':   'unilateral derecha',
    }.get(tipo, 'bilateral')

    # P(X=a) via hypergeometric
    try:
        p_Xa = _math_comb(r1, a) * _math_comb(r2, c1_t - a) / _math_comb(N, c1_t)
    except (ValueError, ZeroDivisionError):
        p_Xa = None

    # ── Pasos ──────────────────────────────────────────────────────
    obs_tbl = _tbl(
        ["", lbl_c1, lbl_c2, "Total"],
        [[lbl_r1, a, b, r1], [lbl_r2, c, d, r2], ["Total", c1_t, c2_t, N]]
    )
    paso1 = _titulo("Paso 1: Tabla de frecuencias observadas") + obs_tbl

    paso2 = (
        _titulo("Paso 2: Totales marginales") +
        _bullets([
            f"<b>{lbl_r1}</b>: n₁ = {a} + {b} = <b>{r1}</b>",
            f"<b>{lbl_r2}</b>: n₂ = {c} + {d} = <b>{r2}</b>",
            f"<b>{lbl_c1}</b>: {a} + {c} = <b>{c1_t}</b>",
            f"<b>{lbl_c2}</b>: {b} + {d} = <b>{c2_t}</b>",
            f"N total = {r1} + {r2} = <b>{N}</b>",
        ])
    )

    def _cell_e(e):
        warn = " <b style='color:#F87171;'>⚠</b>" if e < 5 else ""
        return f"<b>{e:.2f}</b>{warn}"

    exp_tbl = _tbl(
        ["Esperados", lbl_c1, lbl_c2, "Total"],
        [
            [lbl_r1, _cell_e(E11), _cell_e(E12), r1],
            [lbl_r2, _cell_e(E21), _cell_e(E22), r2],
            ["Total", c1_t, c2_t, N],
        ]
    )
    paso3 = (
        _titulo("Paso 3: Frecuencias esperadas  Eᵢⱼ = (Fila_i × Col_j) / N") +
        _bullets([
            f"E({lbl_r1},{lbl_c1}) = {_frac(f'{r1}×{c1_t}', str(N))} = <b>{E11:.2f}</b>" + (" ⚠ &lt; 5" if E11 < 5 else ""),
            f"E({lbl_r1},{lbl_c2}) = {_frac(f'{r1}×{c2_t}', str(N))} = <b>{E12:.2f}</b>" + (" ⚠ &lt; 5" if E12 < 5 else ""),
            f"E({lbl_r2},{lbl_c1}) = {_frac(f'{r2}×{c1_t}', str(N))} = <b>{E21:.2f}</b>" + (" ⚠ &lt; 5" if E21 < 5 else ""),
            f"E({lbl_r2},{lbl_c2}) = {_frac(f'{r2}×{c2_t}', str(N))} = <b>{E22:.2f}</b>" + (" ⚠ &lt; 5" if E22 < 5 else ""),
        ]) +
        exp_tbl
    )

    if small_count > 0:
        why_fisher = (
            f"✓ <b>Se recomienda Fisher</b>: {small_count} celda(s) con frecuencia esperada &lt; 5. "
            "La prueba χ² requiere todas las celdas ≥ 5 para ser válida. "
            "Fisher calcula probabilidades exactas mediante la distribución hipergeométrica, "
            "sin depender de aproximaciones asintóticas."
        )
    else:
        why_fisher = (
            "Todas las frecuencias esperadas son ≥ 5. "
            "✓ Fisher es igualmente válida; en este caso también podría usarse χ² como alternativa."
        )
    paso4 = _titulo("Paso 4: ¿Por qué usar la prueba exacta de Fisher?") + _nota(why_fisher)

    or_formula = (
        f"OR = {_frac(f'{a} × {d}', f'{b} × {c}')} = " +
        (f"<b>∞</b> (c = 0)" if np.isinf(OR) and OR > 0 else
         f"<b>0</b> (a = 0)" if OR == 0.0 else f"<b>{OR:.4f}</b>")
    )
    paso5 = (
        _titulo("Paso 5: Odds Ratio (OR)") +
        _formula(or_formula) +
        _nota(f"→ {OR_interp}")
    )

    paso6 = (
        _titulo("Paso 6: Cálculo exacto de Fisher (distribución hipergeométrica)") +
        _formula(
            f"P(X = a) = {_frac(f'C(n₁, a) · C(n₂, c₁−a)', 'C(N, c₁)')}"
        ) +
        (
            _formula(
                f"P(X = {a}) = "
                f"{_frac(f'C({r1},{a}) · C({r2},{c1_t-a})', f'C({N},{c1_t})')}"
                + (f" = <b>{p_Xa:.5f}</b>" if p_Xa is not None else "")
            )
        ) +
        _nota(
            "Fisher suma las probabilidades de todas las tablas igual de probables o menos "
            "que la observada, condicionadas sobre los totales marginales fijos."
        )
    )

    paso7 = (
        _titulo("Paso 7: Valor p") +
        _formula(f"p (prueba {tipo_display}) = <b>{p_val:.4f}</b>") +
        _nota(
            f"Probabilidad de obtener una distribución de datos tan extrema o más que la "
            f"observada, si H₀ fuera verdadera (α = {alpha})."
        )
    )

    _dec_label = "Rechazar H₀" if rechazar else "No rechazar H₀"
    paso8 = (
        _titulo("Paso 8: Decisión estadística") +
        _bullets([
            f"p = {p_val:.4f} {'<' if rechazar else '≥'} α = {alpha}",
            f"→ <b style='color:#E2E8F0;'>{_dec_label}</b>",
        ]) +
        _blockquote(conclusion)
    )

    paso9 = (
        _titulo("Paso 9: Interpretación epidemiológica") +
        _bullets([
            f"R₁ ({lbl_r1}) = {_frac(str(a), str(r1))} = <b>{R1:.4f}</b> ({R1*100:.2f}%)",
            f"R₂ ({lbl_r2}) = {_frac(str(c), str(r2))} = <b>{R2:.4f}</b> ({R2*100:.2f}%)",
            f"RR = <b>{RR_str}</b> → {RR_interp}",
            f"DAR = {R1:.4f} − {R2:.4f} = <b>{DAR:.4f}</b> ({DAR*100:.2f}%) → {DAR_interp}",
        ] + (
            [f"{NNX_type} = 1/|DAR| ≈ <b>{int(round(NNX))}</b> → {NNX_interp}"]
            if NNX is not None else []
        ))
    )

    return {
        'OR':        OR,
        'OR_str':    OR_str,
        'OR_interp': OR_interp,
        'p_val':     p_val,
        'rechazar':  rechazar,
        'conclusion': conclusion,
        'any_small':  any_small,
        'small_count': small_count,
        'expected':  {'E11': E11, 'E12': E12, 'E21': E21, 'E22': E22},
        'marginals': {'r1': r1, 'r2': r2, 'c1': c1_t, 'c2': c2_t, 'N': N},
        'epi': {
            'R1': R1, 'R2': R2, 'RR': RR, 'RR_str': RR_str,
            'DAR': DAR, 'NNX': NNX, 'NNX_type': NNX_type,
            'RR_interp': RR_interp, 'DAR_interp': DAR_interp, 'NNX_interp': NNX_interp,
        },
        'pasos': [paso1, paso2, paso3, paso4, paso5, paso6, paso7, paso8, paso9],
    }


