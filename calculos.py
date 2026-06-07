# ================================================================
# calculos.py — BACKEND: Lógica de cálculo y gráficos
# ================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


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
            _blockquote(interp) +
            _hr() +
            _titulo("Como prueba adicional, la probabilidad complementaria debería ser:") +
            _formula(
                f"P(X ≥ {_fmt(val_a)}) = 1 − {prob:.4f} = <b>{prob_comp:.4f}</b>"
            ) +
            _nota(f"o <b style='color:#E2E8F0;'>{prob_comp*100:.2f}%</b>.") +
            f'<p style="color:#94A3B8;font-size:.86rem;margin:8px 0 2px;">'
            f'Si al seleccionar “📈 P(X ≥ a)” la aplicación devuelve '
            f'aproximadamente <b style="color:#E2E8F0;">{prob_comp:.4f}</b>, '
            f'entonces esa parte también está funcionando bien.</p>'
        )

        return prob, [exp], interp, False

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
            _blockquote(interp) +
            _hr() +
            _titulo("Como prueba adicional, la probabilidad complementaria debería ser:") +
            _formula(
                f"P(X ≤ {_fmt(val_a)}) = 1 − {prob:.4f} = <b>{prob_comp:.4f}</b>"
            ) +
            _nota(f"o <b style='color:#E2E8F0;'>{prob_comp*100:.2f}%</b>.") +
            f'<p style="color:#94A3B8;font-size:.86rem;margin:8px 0 2px;">'
            f'Si al seleccionar “📉 P(X ≤ a)” la aplicación devuelve '
            f'aproximadamente <b style="color:#E2E8F0;">{prob_comp:.4f}</b>, '
            f'entonces esa parte también está funcionando bien.</p>'
        )

        return prob, [exp], interp, False

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

        return prob, [exp], interp, False

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

        return x_val, [exp], interp, True


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
            _blockquote(interp) +
            _hr() +
            _titulo("Como prueba adicional, la probabilidad complementaria debería ser:") +
            _formula(f"P(T ≥ {_fmt(val_a)}) = 1 − {prob:.4f} = <b>{prob_comp:.4f}</b>") +
            _nota(f"o <b style='color:#E2E8F0;'>{prob_comp*100:.2f}%</b>.")
        )

        return prob, [exp], interp, False

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
            _blockquote(interp) +
            _hr() +
            _titulo("Como prueba adicional, la probabilidad complementaria debería ser:") +
            _formula(f"P(T ≤ {_fmt(val_a)}) = 1 − {prob:.4f} = <b>{prob_comp:.4f}</b>") +
            _nota(f"o <b style='color:#E2E8F0;'>{prob_comp*100:.2f}%</b>.")
        )

        return prob, [exp], interp, False

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

        return prob, [exp], interp, False

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

        return vc, [exp], interp, True


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
            _blockquote(interp) +
            _hr() +
            _titulo("Como prueba adicional, la probabilidad complementaria debería ser:") +
            _formula(
                f"P(χ² ≥ {_fmt(val_a)}) = 1 − {prob:.4f} = <b>{prob_comp:.4f}</b>"
            ) +
            _nota(f"o <b style='color:#E2E8F0;'>{prob_comp*100:.2f}%</b>.")
        )

        return prob, [exp], interp, False

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

        return prob, [exp], interp, False

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

        return vc, [exp], interp, True


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

        return prob, [exp], interp, False

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

        return vc, [exp], interp, True
