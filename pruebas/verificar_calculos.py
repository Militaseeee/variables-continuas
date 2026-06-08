# ============================================================
# verificar_calculos.py
# Comprueba que los cálculos del programa son correctos.
# Ejecutar con: python pruebas/verificar_calculos.py
# ============================================================
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scipy import stats

pasadas = 0
fallidas = 0


def verificar(nombre, obtenido, esperado, tol=0.0001):
    global pasadas, fallidas
    if abs(obtenido - esperado) <= tol:
        print(f"  OK   {nombre}: {obtenido:.6f} ≈ {esperado:.6f}")
        pasadas += 1
    else:
        print(f"  FALLO {nombre}: obtenido={obtenido:.6f}, esperado={esperado:.6f}")
        fallidas += 1


print("=" * 60)
print("VERIFICACIÓN DE CÁLCULOS")
print("Distribuciones Continuas + Pruebas de Hipótesis")
print("=" * 60)

# ---- DISTRIBUCIÓN NORMAL ----------------------------------------
print("\n[ Normal ]")

# Ejercicio 1: P(155 ≤ X ≤ 170) con N(161, 7.5)
prob_entre = (stats.norm.cdf(170, loc=161, scale=7.5)
              - stats.norm.cdf(155, loc=161, scale=7.5))
verificar("P(155 ≤ X ≤ 170) ~ N(161, 7.5)", prob_entre, 0.67307)

# Ejercicio 2: P(X ≥ 110) con N(90, 12)
prob_der = 1 - stats.norm.cdf(110, loc=90, scale=12)
verificar("P(X ≥ 110) ~ N(90, 12)", prob_der, 0.04779)

# Ejercicio 3: Percentil 90 de N(161, 7.5)
perc_90 = stats.norm.ppf(0.90, loc=161, scale=7.5)
verificar("Percentil 90 de N(161, 7.5)", perc_90, 170.6116, tol=0.001)

# Percentil 95 de N(0, 1) — valor z estándar
perc_95 = stats.norm.ppf(0.95)
verificar("Percentil 95 de N(0, 1)", perc_95, 1.64485)

# ---- t de STUDENT -----------------------------------------------
print("\n[ t de Student ]")

# Ejercicio 4: valor crítico bilateral gl=19, α=0.05
vc_t19 = stats.t.ppf(0.975, df=19)
verificar("Valor crítico t(gl=19, α=0.05) bilateral", vc_t19, 2.09302, tol=0.0001)

# p-valor de t=2.45 con gl=19 (bilateral)
pval_t = 2 * (1 - stats.t.cdf(2.45, df=19))
verificar("p-valor t=2.45, gl=19, bilateral", pval_t, 0.02431, tol=0.001)

# Valor crítico clásico gl=15, α=0.05 (bilateral)
vc_t15 = stats.t.ppf(0.975, df=15)
verificar("Valor crítico t(gl=15, α=0.05) bilateral", vc_t15, 2.13145)

# ---- χ² DE INDEPENDENCIA ----------------------------------------
print("\n[ χ² de Independencia ]")

# Ejercicio 5: tabla 2×2 (120,280,80,320), α=0.05
a, b, c, d = 120, 280, 80, 320
n = a + b + c + d
chi2_calculado = n * (a*d - b*c)**2 / ((a+b)*(c+d)*(a+c)*(b+d))
verificar("χ² tabla fumador/enfermedad (n=800)", chi2_calculado, 10.6667, tol=0.001)

pval_chi2 = 1 - stats.chi2.cdf(chi2_calculado, df=1)
verificar("p-valor χ² (gl=1)", pval_chi2, 0.0011, tol=0.0001)

vc_chi2_1gl = stats.chi2.ppf(0.95, df=1)
verificar("Valor crítico χ²(gl=1, α=0.05)", vc_chi2_1gl, 3.8415, tol=0.001)

# RR = (a/(a+b)) / (c/(c+d))
RR = (a / (a + b)) / (c / (c + d))
verificar("RR tabla fumador/enfermedad", RR, 1.5000, tol=0.001)

# OR = (a*d) / (b*c)
OR = (a * d) / (b * c)
verificar("OR tabla fumador/enfermedad", OR, 1.7143, tol=0.001)

# Verificación con tabla neutral: valor crítico gl=2
vc_chi2_2gl = stats.chi2.ppf(0.95, df=2)
verificar("Valor crítico χ²(gl=2, α=0.05)", vc_chi2_2gl, 5.99147)

# ---- PRUEBA EXACTA DE FISHER ------------------------------------
print("\n[ Prueba Exacta de Fisher ]")

# Ejercicio 6: tabla (8,2,1,9) — tratamiento vs. control
# Tratamiento: 8 eventos, 2 sin evento; Control: 1 evento, 9 sin evento
_, pval_fisher = stats.fisher_exact([[8, 2], [1, 9]])
verificar("p-valor Fisher tabla (8,2,1,9)", pval_fisher, 0.0055, tol=0.001)

# OR = (8*9)/(2*1) = 36.0
OR_fisher = (8 * 9) / (2 * 1)
verificar("OR Fisher tabla (8,2,1,9)", OR_fisher, 36.0, tol=0.001)

# Tabla simétrica de comprobación: OR = 1 → p debe ser 1.0
_, pval_sym = stats.fisher_exact([[5, 5], [5, 5]])
verificar("p-valor Fisher tabla simétrica (OR=1)", pval_sym, 1.0, tol=0.001)

# ---- RESUMEN ----------------------------------------------------
print("\n" + "=" * 60)
print(f"RESULTADO: {pasadas} pruebas pasaron, {fallidas} fallaron.")
if fallidas == 0:
    print("Todos los cálculos son correctos.")
else:
    print("Revisar las pruebas que fallaron.")
print("=" * 60)
