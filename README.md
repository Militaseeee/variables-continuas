# Visualizador Pedagógico de Distribuciones Continuas y Pruebas de Hipótesis

**Autora:** Alejandra Acosta  
**Materia:** Bioestadística  
**Temas:** 4 — Distribuciones continuas · 5 — Pruebas de hipótesis  
**Herramienta:** Streamlit (aplicación web interactiva)

---

## Objetivo pedagógico

Este software busca que el estudiante comprenda **cómo** y **por qué** se obtienen los resultados estadísticos, no solo cuál es el número final. Cubre dos áreas:

1. **Distribuciones continuas** — Normal y t de Student como curvas de densidad. El estudiante visualiza que la probabilidad es el **área bajo la curva** y no la altura, calcula probabilidades en cualquier región y obtiene percentiles con interpretación en lenguaje de Bioestadística.

2. **Pruebas de hipótesis** — χ² de independencia y Prueba Exacta de Fisher para tablas 2×2. El estudiante ve el procedimiento paso a paso: planteamiento de hipótesis, estadístico calculado, valor crítico, p-valor, decisión e interpretación contextual.

---

## Módulos del software

| Pestaña | Tipo | Qué calcula |
|---------|------|-------------|
| Normal | Distribución continua | P(X ≤ a), P(X ≥ a), P(a ≤ X ≤ b), percentiles de N(μ, σ) |
| t de Student | Prueba de hipótesis | Prueba t bilateral o unilateral; p-valor, valor crítico, decisión con gl definidos por el usuario |
| χ² de Independencia | Prueba de hipótesis | χ² de Pearson para tablas 2×2; frecuencias esperadas, RR, OR, decisión e interpretación |
| Prueba Exacta de Fisher | Prueba de hipótesis | p-valor exacto hipergeométrico para tablas 2×2 con frecuencias esperadas < 5; OR con IC 95% |

---

## Librerías utilizadas

| Librería | Para qué se usa |
|----------|-----------------|
| `streamlit` | Interfaz web interactiva: pestañas, botones, entradas numéricas, tarjetas |
| `scipy.stats` | Probabilidades y percentiles de distribuciones (normal, t, chi2, hypergeom, fisher_exact) |
| `numpy` | Generar los puntos de las curvas para los gráficos |
| `matplotlib` | Dibujar curvas de densidad con áreas sombreadas y gráficos de barras agrupadas |

---

## Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior ([descargar en python.org](https://www.python.org))
- Una terminal (cmd, PowerShell o Terminal de VS Code)

### Paso 1 — Clonar o descargar el proyecto
Colocar la carpeta `variables-continuas/` en cualquier directorio local.

### Paso 2 — Instalar dependencias
Abrir la terminal en la carpeta del proyecto y ejecutar:

```bash
pip install -r requirements.txt
```

### Paso 3 — Ejecutar la aplicación

```bash
streamlit run app.py
```

El navegador se abre automáticamente en `http://localhost:8501`.  
Si no abre solo, copiar esa dirección en el navegador.

### Verificar que los cálculos son correctos (opcional)

```bash
python pruebas/verificar_calculos.py
```

Debe mostrar `Todos los cálculos son correctos.` si el entorno está bien instalado.

---

## Estructura del proyecto

```
variables-continuas/
├── app.py                          ← Interfaz principal: pestañas, entradas, gráficos, resultados
├── calculos.py                     ← Toda la lógica estadística: fórmulas, pasos explicativos, interpretaciones
├── requirements.txt                ← Librerías necesarias con versiones mínimas
├── README.md                       ← Este archivo
├── .streamlit/
│   └── config.toml                 ← Tema visual oscuro de la app
├── ejemplos/
│   └── ejercicios_ejemplo.txt      ← Ejercicios resueltos manualmente para verificar el programa
└── pruebas/
    └── verificar_calculos.py       ← Script automatizado que comprueba los resultados numéricos
```

### Separación de responsabilidades

- **`calculos.py`** contiene todas las funciones estadísticas puras (sin código de interfaz). Recibe parámetros numéricos y devuelve el resultado, los pasos explicativos en HTML y la interpretación. Esto permite probar la lógica estadística de forma independiente a la interfaz.
- **`app.py`** solo maneja la interfaz: lee los valores que el usuario ingresa, llama a las funciones de `calculos.py`, y muestra los resultados y gráficos usando Streamlit.

---

## Ejemplo de uso — Distribución Normal

1. Abrir la pestaña **Normal**.
2. Ingresar **μ = 161** y **σ = 7.5** (estatura de mujeres adultas colombianas).
3. Seleccionar la opción **P(a ≤ X ≤ b)** e ingresar **a = 155**, **b = 170**.
4. Hacer clic en **Calcular probabilidad**.
5. El gráfico muestra la curva N(161, 7.5) con el área sombreada entre 155 y 170.
6. El resultado es **≈ 0.6731** → aproximadamente el 67% de las mujeres mide entre 155 y 170 cm.

**Resultado esperado:** `0.6731` (verificable con la tabla Z o `scipy.stats.norm`).

---

## Ejemplo de uso — Prueba χ² de Independencia

Estudio: Se quiere saber si fumar está asociado con enfermedad pulmonar (n = 800).

| | Enfermedad | Sin enfermedad | Total |
|---|---|---|---|
| Fumador | 120 | 280 | 400 |
| No fumador | 80 | 320 | 400 |
| **Total** | **200** | **600** | **800** |

1. Abrir la pestaña **χ² de Independencia**.
2. Ingresar los 4 valores de la tabla y definir α = 0.05.
3. El programa calcula χ² = 10.6667, gl = 1, p = 0.0011.
4. Como p < 0.05, se rechaza H₀: **hay asociación estadística** entre fumar y la enfermedad.

---

## Ejemplo de uso — Prueba Exacta de Fisher

Indicada cuando alguna frecuencia esperada es < 5 (muestras pequeñas).

| | Evento | No evento | Total |
|---|---|---|---|
| Grupo 1 | 4 | 0 | 4 |
| Grupo 2 | 11 | 15 | 26 |
| **Total** | **15** | **15** | **30** |

1. Abrir la pestaña **Fisher Exacta**.
2. Ingresar los 4 conteos y α = 0.05.
3. El programa calcula el p-valor exacto y muestra frecuencias esperadas vs. observadas.

---

## Interpretación de resultados

| Elemento | Qué significa |
|----------|---------------|
| **Probabilidad calculada** | Número entre 0 y 1; representa el área sombreada bajo la curva de densidad |
| **Valor crítico** | Límite de la región de rechazo; si el estadístico calculado lo supera, se rechaza H₀ |
| **p-valor** | Probabilidad de obtener un resultado tan extremo o más si H₀ fuera cierta; **no es** P(H₀ sea verdadera) |
| **Paso a paso** | Cada cálculo intermedio con la fórmula aplicada y su resultado numérico |
| **Interpretación** | Traducción del resultado al contexto del ejercicio en lenguaje bioestadístico |
| **RR / OR** | Razón de riesgo y de momios para tablas 2×2; solo se calculan en χ² y Fisher |

> **Concepto clave:** En distribuciones continuas, la altura de la curva es la **densidad** f(x), no una probabilidad. La probabilidad siempre es un **área** (integral de f(x) entre dos límites). Por eso P(X = a) = 0 para cualquier valor puntual a.

---

## Limitaciones del programa

- El módulo Normal calcula probabilidades solo para distribuciones N(μ, σ); no ajusta normalidad a datos reales.
- La prueba t implementada es de una muestra (contrasta μ contra un valor de referencia); no incluye prueba de dos muestras independientes.
- Las pruebas χ² y Fisher trabajan únicamente con tablas 2×2; no con tablas k×m de mayor dimensión.
- No verifica automáticamente si los supuestos de cada prueba se cumplen (normalidad, tamaño de muestra, independencia de observaciones).
- Los cálculos usan precisión de punto flotante estándar de Python/scipy (≈ 15 dígitos significativos).
- La app no guarda historial de cálculos entre sesiones; al refrescar la página los valores se reinician.

---

## Fuentes y referencias

- Triola, M. F. (2018). *Estadística* (12.ª ed.). Pearson.
- Pagano, M., & Gauvreau, K. (2001). *Principles of Biostatistics* (2.ª ed.). Duxbury.
- Fisher, R. A. (1922). On the interpretation of χ² from contingency tables, and the calculation of P. *Journal of the Royal Statistical Society*, 85(1), 87–94.
- Documentación de `scipy.stats`: https://docs.scipy.org/doc/scipy/reference/stats.html
- Documentación de Streamlit: https://docs.streamlit.io
- Documentación de Matplotlib: https://matplotlib.org/stable/index.html
