# ============================================================
# verificar_calculos.py
# Script para comprobar que los calculos del programa son correctos.
# Ejecutar con: python pruebas/verificar_calculos.py
# ============================================================
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scipy import stats

# Lista para registrar cuántas pruebas pasan y cuántas fallan
pruebas_pasadas = 0
pruebas_fallidas = 0


def verificar(nombre, valor_obtenido, valor_esperado, tolerancia=0.0001):
    """
    Compara el valor obtenido con el esperado.
    Imprime PASÓ o FALLÓ según la diferencia.
    """
    global pruebas_pasadas, pruebas_fallidas
    diferencia = abs(valor_obtenido - valor_esperado)
    if diferencia <= tolerancia:
        print(f"  PASÓ  {nombre}: {valor_obtenido:.6f} ≈ {valor_esperado:.6f}")
        pruebas_pasadas += 1
    else:
        print(f"  FALLÓ {nombre}: obtenido={valor_obtenido:.6f}, esperado={valor_esperado:.6f}")
        pruebas_fallidas += 1


print("=" * 55)
print("VERIFICACIÓN DE CÁLCULOS — Distribuciones Continuas")
print("=" * 55)

# ---- DISTRIBUCIÓN NORMAL ----
print("\n[ Normal N(161, 7.5) ]")

# P(155 ≤ X ≤ 170) — ejercicio 1
prob_entre = (stats.norm.cdf(170, loc=161, scale=7.5)
              - stats.norm.cdf(155, loc=161, scale=7.5))
verificar("P(155 <= X <= 170)", prob_entre, 0.67307)

# P(X ≥ 110) con N(90, 12) — ejercicio 2
prob_der = 1 - stats.norm.cdf(110, loc=90, scale=12)
verificar("P(X ≥ 110) con N(90,12)", prob_der, 0.04779)

# Percentil 95 de N(0, 1) — debe dar ≈ 1.6449
perc_95 = stats.norm.ppf(0.95)
verificar("Percentil 95 de N(0,1)", perc_95, 1.64485)

# ---- DISTRIBUCIÓN t de Student ----
print("\n[ t de Student ]")

# Valor crítico t(15, α=0.05 bilateral)
vc_t = stats.t.ppf(0.975, df=15)
verificar("Valor crítico t(15, α=0.05)", vc_t, 2.13145)

# P(T ≤ 2.0) con gl=10
prob_t = stats.t.cdf(2.0, df=10)
verificar("P(T ≤ 2.0) con gl=10", prob_t, 0.96327)

# ---- DISTRIBUCIÓN CHI-CUADRADO ----
print("\n[ Chi-cuadrado ]")

# Valor crítico χ²(2, α=0.05)
vc_chi2 = stats.chi2.ppf(0.95, df=2)
verificar("Valor crítico χ²(2, α=0.05)", vc_chi2, 5.99147)

# P(χ² ≥ 7.815) con gl=3 — debe ser ≈ 0.05
pval_chi2 = 1 - stats.chi2.cdf(7.815, df=3)
verificar("P(χ² ≥ 7.815) con gl=3", pval_chi2, 0.05001)

# ---- DISTRIBUCIÓN F ----
print("\n[ F de Fisher ]")

# P(F ≥ 4.80) con F(2, 27) — ejercicio 5
pval_f = 1 - stats.f.cdf(4.80, dfn=2, dfd=27)
verificar("P(F ≥ 4.80) con F(2,27)", pval_f, 0.01641)

# Valor crítico F(3, 20, α=0.05)
vc_f = stats.f.ppf(0.95, dfn=3, dfd=20)
verificar("Valor crítico F(3,20, α=0.05)", vc_f, 3.09839)

# ---- RESUMEN ----
print("\n" + "=" * 55)
print(f"RESULTADO: {pruebas_pasadas} pruebas pasaron, {pruebas_fallidas} fallaron.")
if pruebas_fallidas == 0:
    print("Todos los cálculos son correctos.")
else:
    print("Revisar las pruebas fallidas.")
print("=" * 55)
