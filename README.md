# 🔬 Sistema de Análisis de Microplásticos en Máscaras de Pestañas

Sistema automatizado con interfaz gráfica para el análisis morfológico de microplásticos detectados en imágenes microscópicas de máscaras de pestañas.

## 📋 Descripción

Este proyecto implementa un sistema completo de análisis de imágenes con interfaz gráfica que permite:
- ✅ Detectar y segmentar partículas de microplásticos en imágenes microscópicas
- ✅ Calcular parámetros morfológicos (área, perímetro, relación de aspecto, etc.)
- ✅ Clasificar partículas por tamaño y forma
- ✅ Generar análisis estadísticos descriptivos e inferenciales
- ✅ Crear visualizaciones y gráficos de alta calidad
- ✅ Comparar múltiples muestras
- ✅ Exportar resultados en múltiples formatos (Excel, PNG, TXT)
- ✅ Visualizar gráficos con zoom y filtros
- ✅ Gestionar resultados con respaldos automáticos

## 🗂️ Estructura del Proyecto

```
mascaraPesta-a/
├── main_gui.py                      # ⭐ Interfaz gráfica principal
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
│
├── config/
│   └── config.py                    # Configuración del proyecto
│
├── src/
│   ├── image_processing.py          # Procesamiento de imágenes
│   ├── statistical_analysis.py      # Análisis estadístico
│   └── visualization.py             # Generación de gráficos
│
├── data/
│   ├── raw_images/                  # ⚠️ COLOCAR IMÁGENES AQUÍ
│   └── processed_images/            # Imágenes procesadas (auto-generado)
│
├── results/
│   ├── graphs/                      # Gráficos generados (auto-generado)
│   └── reports/                     # Reportes y datos (auto-generado)
│
└── backups/                         # Respaldos de resultados (auto-generado)
```

## 🚀 Instalación

### Prerequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto** (si aún no lo has hecho)

2. **Crear un entorno virtual** (recomendado):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar las dependencias**:
   ```cmd
   pip install -r requirements.txt
   ```

## 📸 Preparar Imágenes

### ⚠️ IMPORTANTE: Archivos de Imagen Requeridos

**Antes de ejecutar el programa**, necesitas preparar tus imágenes:

#### Ubicación
Coloca todas tus imágenes microscópicas en:
```
data/raw_images/
```

#### Formatos Soportados
- `.jpg` / `.jpeg`
- `.png`
- `.tif` / `.tiff`
- `.bmp`

#### Requisitos de las Imágenes

Las imágenes deben ser:

1. **Imágenes microscópicas** de microplásticos extraídos de máscaras de pestañas
2. **Buena calidad**:
   - Buena iluminación y contraste
   - Fondo uniforme (preferiblemente claro o oscuro uniforme)
   - Enfoque nítido
   - Resolución suficiente para distinguir partículas individuales

3. **Convenciones de nombres** (recomendado):
   ```
   M1_muestra1.jpg
   M2_muestra1.jpg
   M3_muestra1.jpg
   ```
   O cualquier nombre descriptivo. El programa usará el nombre del archivo como identificador de muestra.

#### Ejemplo de Estructura
```
data/raw_images/
├── M1_20x_campo1.jpg
├── M1_20x_campo2.jpg
├── M2_20x_campo1.jpg
└── M3_20x_campo1.jpg
```

### 📏 Calibración del Microscopio

**MUY IMPORTANTE**: Para obtener mediciones precisas en micrómetros (μm), necesitas conocer el factor de conversión de tu microscopio.

#### ¿Cómo obtener el factor de calibración?

1. **Con una regla micrométrica**:
   - Toma una foto de una regla micrométrica calibrada con tu microscopio
   - Mide cuántos píxeles corresponden a una distancia conocida (ej. 100 μm)
   - Calcula: `factor = distancia_real_μm / distancia_píxeles`

2. **Ejemplo**:
   - Si 100 μm en la regla = 500 píxeles en la imagen
   - Factor de conversión = 100 / 500 = 0.2 μm/píxel

3. **Configurar el factor**:
   - Opción A: Edita `config/config.py` y modifica `'pixels_to_um'`
   - Opción B: El programa te lo preguntará al ejecutarse

#### Valores Típicos por Magnificación

| Magnificación | Factor aproximado (μm/píxel) |
|--------------|------------------------------|
| 4x           | 2.5 - 5.0                   |
| 10x          | 1.0 - 2.0                   |
| 20x          | 0.3 - 0.8                   |
| 40x          | 0.15 - 0.4                  |
| 100x         | 0.06 - 0.15                 |

⚠️ **Nota**: Estos son valores aproximados. Siempre calibra con tu propio equipo.

## ▶️ Uso

### Ejecución

Una vez que hayas colocado tus imágenes en `data/raw_images/`:

```cmd
python main_gui.py
```

### Interfaz Gráfica

El programa abrirá una ventana con 4 pestañas:

#### 1️⃣ **Configuración**
- Establece el factor de conversión píxeles → micrómetros
- Ajusta parámetros de umbral y tamaño de partículas

#### 2️⃣ **Análisis**
- Ejecuta el análisis completo de todas las imágenes
- Monitorea el progreso en tiempo real
- Genera reportes, gráficos y archivos Excel

#### 3️⃣ **Ver Gráficos**
- Visualiza los gráficos generados
- Control de zoom (30%-500%)
- Filtros por tipo de gráfico
- Navegación con mouse wheel

#### 4️⃣ **Gestión de Resultados**
- Crea respaldos con fecha/hora
- Limpia resultados antiguos
- Abre carpetas de resultados y respaldos
- Monitorea espacio usado

### Flujo del Programa

1. **Verificación de imágenes**: El programa busca imágenes en `data/raw_images/`
2. **Confirmación**: Te pregunta si deseas continuar
3. **Calibración**: Opcionalmente, puedes ingresar el factor de calibración
4. **Procesamiento**: Analiza cada imagen automáticamente
5. **Resultados**: Genera gráficos, reportes y datos exportados

### Salida del Programa

El programa genera automáticamente:

#### 📊 Gráficos (`results/graphs/`)
Para cada muestra:
- `[muestra]_size_distribution.png` - Distribución de tamaños
- `[muestra]_shape_distribution.png` - Distribución de formas
- `[muestra]_dashboard.png` - Dashboard resumen completo
- `[muestra]_frequency_curve.png` - Curvas de frecuencia acumulada
- `[muestra]_correlation_matrix.png` - Matriz de correlación

Para comparaciones (si hay múltiples muestras):
- `comparative_area.png` - Comparación de áreas
- `comparative_diameter.png` - Comparación de diámetros
- `comparative_aspect_ratio.png` - Comparación de formas

#### 📄 Reportes (`results/reports/`)
Para cada muestra:
- `[muestra]_report.txt` - Reporte textual con estadísticos
- `[muestra]_data.xlsx` - Datos completos de cada partícula

Consolidados:
- `consolidated_data.xlsx` - Todos los datos juntos
- `summary_statistics.xlsx` - Resumen estadístico por muestra
- `consolidated_report.txt` - Reporte general

#### 🖼️ Imágenes Procesadas (`data/processed_images/`)
- Imágenes binarizadas mostrando partículas detectadas

## ⚙️ Configuración Avanzada

### Archivo `config/config.py`

Puedes ajustar varios parámetros:

#### Parámetros de Procesamiento de Imágenes
```python
IMAGE_PARAMS = {
    'pixels_to_um': 1.0,           # Factor de conversión
    'threshold': 127,              # Umbral de segmentación (0-255)
    'min_particle_area': 10,       # Área mínima en píxeles
    'max_particle_area': 50000,    # Área máxima en píxeles
}
```

#### Categorías de Clasificación
```python
MORPHOLOGY_PARAMS = {
    'size_categories': {
        'pequeño': (0, 50),        # Diámetro en μm
        'mediano': (50, 200),
        'grande': (200, float('inf'))
    },
    'aspect_ratio_categories': {
        'esférico': (0.8, 1.2),
        'alargado': (1.2, 3.0),
        'fibra': (3.0, float('inf'))
    }
}
```

## 📊 Parámetros Calculados

Para cada partícula detectada, el sistema calcula:

### Parámetros Geométricos
- **Área (μm²)**: Área total de la partícula
- **Perímetro (μm)**: Longitud del contorno
- **Diámetro equivalente (μm)**: Diámetro de un círculo con la misma área
- **Eje mayor (μm)**: Longitud del eje más largo
- **Eje menor (μm)**: Longitud del eje más corto

### Parámetros de Forma
- **Relación de aspecto**: Eje mayor / Eje menor
- **Excentricidad**: Medida de cuán elíptica es la forma (0=círculo, 1=línea)
- **Solidez**: Proporción del área respecto a su envolvente convexa
- **Orientación**: Ángulo del eje mayor

### Clasificaciones
- **Categoría de tamaño**: Pequeño, mediano, grande
- **Categoría de forma**: Esférico, alargado, fibra

## 🔬 Análisis Estadísticos

El sistema realiza:

### Estadística Descriptiva
- Media, mediana, desviación estándar
- Mínimo, máximo, cuartiles
- Coeficiente de variación

### Análisis Comparativo (múltiples muestras)
- Test t de Student (paramétrico)
- Test de Mann-Whitney U (no paramétrico)
- ANOVA / Kruskal-Wallis (más de 2 muestras)
- Test de normalidad (Shapiro-Wilk)

## 🛠️ Solución de Problemas

### Error: "No se encontraron imágenes"
✅ Verifica que las imágenes estén en `data/raw_images/`
✅ Asegúrate de usar formatos soportados (.jpg, .png, etc.)

### Error: "No se pudo cargar la imagen"
✅ Verifica que la imagen no esté corrupta
✅ Intenta abrir la imagen con otro programa

### Pocas partículas detectadas
✅ Ajusta el parámetro `threshold` en `config/config.py`
✅ Verifica que las imágenes tengan buen contraste
✅ Considera ajustar `min_particle_area` y `max_particle_area`

### Mediciones incorrectas
✅ Verifica que el factor de calibración (`pixels_to_um`) sea correcto
✅ Calibra tu microscopio con una regla micrométrica

## 📚 Dependencias Principales

- **numpy**: Cálculos numéricos
- **opencv-python**: Procesamiento de imágenes
- **pandas**: Manejo de datos
- **matplotlib**: Visualización
- **seaborn**: Visualización estadística
- **scipy**: Análisis estadístico
- **scikit-image**: Procesamiento de imágenes avanzado

## 📖 Referencias

Este sistema está basado en metodologías estándar de análisis de imágenes microscópicas y análisis morfológico de partículas.

## 📝 Notas Importantes

1. **Calibración**: La precisión de las mediciones depende completamente de la calibración correcta del microscopio.

2. **Calidad de imágenes**: Imágenes de mejor calidad = mejores resultados. Asegúrate de que:
   - Haya buen contraste entre partículas y fondo
   - El fondo sea lo más uniforme posible
   - Las partículas estén bien enfocadas

3. **Parámetros de umbralización**: El parámetro `threshold` puede necesitar ajuste dependiendo de tus imágenes específicas.

4. **Clasificación automática**: Las categorías de tamaño y forma son configurables según tus necesidades específicas.

## 🆘 Soporte

Si encuentras problemas:
1. Verifica que todas las dependencias estén instaladas correctamente
2. Revisa la configuración en `config/config.py`
3. Asegúrate de que las imágenes cumplan los requisitos de calidad
4. Consulta los mensajes de error para diagnóstico

---

**Versión**: 1.0  
**Fecha**: Diciembre 2025  
**Licencia**: Uso académico/investigación
