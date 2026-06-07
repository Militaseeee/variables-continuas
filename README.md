# Distribuciones Continuas en Bioestadística

**Autora:** Alejandra Acosta  
**Materia:** Bioestadística  
**Tema:** 4 — Distribuciones continuas (Normal, t de Student, Chi-cuadrado, F de Fisher)

---

## Objetivo pedagógico

Visualizar e interpretar distribuciones de probabilidad continuas. El software
permite entender que en variables continuas la probabilidad es el **área bajo la
curva**, no la altura; calcular probabilidades y percentiles; y obtener una
interpretación en lenguaje bioestadístico paso a paso.

---

## Librerías utilizadas

| Librería       | Para qué se usa                                      |
|----------------|------------------------------------------------------|
| `streamlit`    | Crear la interfaz web interactiva                    |
| `scipy.stats`  | Calcular probabilidades y percentiles de distribuciones |
| `numpy`        | Generar los puntos de las curvas                     |
| `matplotlib`   | Dibujar las gráficas con áreas sombreadas            |

---

## Instalación y ejecución

### Paso 1 — Instalar Python
Descargar Python desde https://www.python.org (versión 3.10 o superior).

### Paso 2 — Instalar las dependencias
Abrir la terminal (cmd o PowerShell) en la carpeta del proyecto y ejecutar:

```
pip install -r requirements.txt
```

### Paso 3 — Ejecutar la aplicación

```
streamlit run app.py
```

El navegador se abre automáticamente en `http://localhost:8501`.

---

## Estructura del proyecto

```
variables-continuas/
├── app.py              ← Aplicación principal (interfaz + cálculos + gráficos)
├── requirements.txt    ← Lista de librerías necesarias
├── README.md           ← Este archivo: instrucciones y descripción
├── ejemplos/
│   └── ejercicios_ejemplo.txt  ← Ejercicios resueltos para verificar
└── pruebas/
    └── verificar_calculos.py   ← Script que comprueba que los cálculos son correctos
```

---

## Ejemplo de uso

1. Abrir la pestaña **Normal**.
2. Ingresar media μ = 161 y desviación estándar σ = 7.5 (estatura de mujeres adultas).
3. Seleccionar **P(a ≤ X ≤ b)** e ingresar a = 155, b = 170.
4. Hacer clic en **Calcular probabilidad**.
5. Observar el área sombreada y leer la interpretación.

---

## Interpretación de resultados

- **Probabilidad calculada:** Número entre 0 y 1 que representa el área sombreada.
- **Paso a paso:** Explica cada operación realizada (estandarización, consulta de tabla, etc.).
- **Interpretación:** Traduce el resultado a lenguaje de Bioestadística.

---

## Limitaciones del programa

- Solo trabaja con las distribuciones incluidas (Normal, t, χ², F).
- Para la distribución F solo se calcula la cola derecha (uso más común en ANOVA).
- No verifica si los supuestos de cada distribución se cumplen para los datos del usuario.
- Los cálculos usan precisión de punto flotante estándar de Python/scipy.

---

## Fuentes

- Triola, M. F. (2018). *Estadística*. Pearson.
- Documentación de `scipy.stats`: https://docs.scipy.org/doc/scipy/reference/stats.html
- Documentación de Streamlit: https://docs.streamlit.io
