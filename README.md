# 🔬 Sistema de Análisis de Microplásticos con YOLOv8

Sistema automatizado con interfaz gráfica para la detección y análisis morfológico de microplásticos en imágenes microscópicas usando **inteligencia artificial (YOLOv8)**.

## 📋 Características

- 🤖 **Detección con IA:** YOLOv8 (deep learning) para detección automática
- 🏷️ **Anotación intuitiva:** Integración con LabelImg para etiquetar imágenes
- 🎓 **Entrenamiento personalizado:** Entrena modelos YOLOv8 con tus propios datos
- 📊 **Clasificación automática:** 6 tipos de microplásticos (fibra, fragmento, película, esfera, irregular, aglomerado)
- 📐 **Análisis morfológico:** Área, perímetro, circularidad, elongación, etc.
- 📈 **Estadísticas avanzadas:** Distribuciones, correlaciones, pruebas estadísticas
- 🎨 **Visualización profesional:** Gráficos, dashboards y reportes automáticos
- 💾 **Exportación completa:** Excel, PNG, TXT
- 🖥️ **Interfaz moderna:** 6 pestañas para flujo de trabajo completo
- 🔄 **Respaldos automáticos:** Sistema de gestión de resultados

## 🗂️ Estructura del Proyecto

```
TesisNataliaRojo/
├── instalar.bat                     # ⭐ EJECUTAR PRIMERO
├── main.py                          # Programa principal con GUI
├── entrenar_yolo.py                 # Script de entrenamiento YOLO
├── abrir_labelimg.vbs               # Abrir LabelImg directamente
├── README.md                        # Esta guía
├── GUIA_YOLO.md                     # 📖 Guía completa de YOLOv8
├── requirements.txt                 # Dependencias
│
├── config/
│   └── config.py                    # Configuración
│
├── src/
│   ├── image_processing.py          # Procesamiento (tradicional + YOLO)
│   ├── yolo_detector.py             # 🤖 Detector YOLOv8
│   ├── train_yolo.py                # 🎓 Entrenador YOLOv8
│   ├── image_annotation.py          # Anotación con LabelImg
│   ├── statistical_analysis.py      # Análisis estadístico
│   └── visualization.py             # Generación de gráficos
│
├── data/
│   ├── raw_images/                  # ⚠️ COLOCAR IMÁGENES AQUÍ
│   ├── processed_images/            # Imágenes procesadas (auto)
│   └── annotations/                 # Anotaciones de LabelImg (auto)
│
├── yolo_training/                   # 🤖 Entrenamiento YOLOv8 (auto)
│   ├── dataset/                     # Dataset convertido
│   └── models/                      # Modelos entrenados
│
├── models/                          # 📦 Modelos YOLO guardados
│
└── results/
    ├── graphs/                      # Gráficos generados (auto)
    └── reports/                     # Reportes y datos (auto)
```

## 🚀 Instalación Rápida

### Paso 1: Requisitos Previos
- **Python 3.8 o superior** ([Descargar](https://www.python.org/downloads/))
- Durante la instalación, marcar **"Add Python to PATH"**

### Paso 2: Instalar Todo Automáticamente

```cmd
instalar.bat
```

Este script:
- ✅ Verifica Python
- ✅ Actualiza pip
- ✅ Instala todas las dependencias
- ✅ Instala LabelImg para anotación
- ✅ Crea estructura de directorios
- ✅ Verifica que todo funcione
- ✅ Ejecuta el programa automáticamente

**¡Listo! El instalador hace todo por ti.**

## 📦 Compilar a Ejecutable (.exe)

### 🤖 Compilación Automática con GitHub Actions

Este proyecto incluye **compilación automática en la nube** usando GitHub Actions:

- ✅ **Sin PyInstaller local**: GitHub compila por ti en sus servidores
- ✅ **Gratis**: 2000 minutos/mes de compilación gratuita
- ✅ **Automático**: Cada vez que subes cambios, se genera un nuevo `.exe`
- ✅ **Distribución fácil**: Cualquiera puede descargar el `.exe` sin instalar Python

#### 📥 Descargar el .exe compilado

1. Ve a tu repositorio en GitHub
2. Click en **"Actions"** → Workflow más reciente
3. Descarga desde **"Artifacts"** → **"AnalisisMicroplasticos-Windows.zip"**
4. También puedes crear un **Release** y el `.exe` se adjunta automáticamente

#### 🔧 Compilar localmente (opcional)

Si prefieres compilar en tu PC:

```cmd
compilar_exe.bat
```

El `.exe` estará en `dist/AnalisisMicroplasticos.exe`

**📖 Guía completa:** Ver [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)

## ▶️ Uso del Sistema

### 1️⃣ Preparar Imágenes

Coloca tus imágenes microscópicas en:
```
data/raw_images/
```

Formatos soportados: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.bmp`

### 2️⃣ Ejecutar el Programa

```cmd
python main.py
```

### 3️⃣ Flujo de Trabajo

La interfaz tiene **6 pestañas** en orden de uso:

#### **⚙️ Configuración**
- Cargar imágenes desde tu computadora
- Establecer factor de calibración (μm/píxel)
- Cargar imágenes por defecto automáticamente

#### **🏷️ Anotar Imágenes**
- Abrir LabelImg para etiquetar microplásticos
- Clasificar por tipo: fibra, fragmento, película, esfera, etc.
- Ver estadísticas de anotación en tiempo real

#### **🤖 Entrenar YOLOv8**
- Entrenar tu modelo personalizado de detección con IA
- Configurar épocas, batch size y tamaño de modelo
- **Seleccionar modelo entrenado** (REQUERIDO para análisis)
- Ver log de entrenamiento en tiempo real

#### **🔬 Análisis**
- **Requiere modelo YOLOv8 seleccionado**
- Detecta y clasifica microplásticos automáticamente
- Genera reportes y datos morfológicos completos
- Exporta resultados a Excel

#### **📊 Ver Gráficos**
- Visualizar distribuciones de tamaño y forma
- Comparar muestras
- Zoom y filtros interactivos

#### **📁 Gestión de Resultados**
- Crear respaldos
- Limpiar resultados antiguos
- Abrir carpetas de resultados

## 🤖 Sistema de Detección con YOLOv8

### ¿Por qué YOLOv8?

- ✅ **Alta precisión** en detección de objetos pequeños
- ✅ **Clasificación automática** de 6 tipos de microplásticos
- ✅ **Aprendizaje personalizado** - se adapta a tus datos
- ✅ **Robusto** ante cambios de iluminación y fondo
- ✅ **Rápido** con GPU (también funciona en CPU)

### Flujo de Trabajo

```
1. 📸 Cargar imágenes microscópicas
   ↓
2. 🏷️ Anotar 50-100 imágenes con LabelImg
   ↓  
3. 🎓 Entrenar modelo YOLOv8 (30 min - 3 horas)
   ↓
4. ✅ Seleccionar modelo entrenado (.pt)
   ↓
5. 🔬 Analizar imágenes con IA
   ↓
6. 📊 Visualizar resultados y estadísticas
```

### Entrenamiento Rápido

**Desde la GUI:**
1. Pestaña **"🤖 Entrenar YOLOv8"**
2. Configurar:
   - Modelo: **n** (rápido) → **m** (recomendado) → **x** (preciso)
   - Épocas: **100-300**
   - Batch: **8-32**
3. Clic **"🚀 Entrenar Modelo YOLO"**
4. Esperar entrenamiento
5. Clic **"📁 Buscar Modelo"** → Seleccionar `.pt`

**Desde terminal:**
```bash
python entrenar_yolo.py
```

### ⚠️ Requisito Importante

El sistema **requiere un modelo YOLOv8 entrenado** para funcionar. Opciones:

1. **Entrenar tu propio modelo** (recomendado)
   - Anota tus imágenes específicas
   - Modelo adaptado a tus condiciones

2. **Usar modelo pre-entrenado** (si tienes uno)
   - Debe estar entrenado para microplásticos
   - Formato `.pt` de YOLOv8

### 📖 Guía Completa

Ver **`GUIA_YOLO.md`** para:
- Configuración avanzada
- Ajuste de umbrales
- Solución de problemas
- Mejores prácticas
- Ejemplos de código

## 🏷️ Anotación con LabelImg

### Abrir LabelImg

**Opción 1:** Desde el programa
- Pestaña "🏷️ Anotar Imágenes"
- Clic en botón verde

**Opción 2:** Directamente
- Doble clic en `abrir_labelimg.vbs`

### Usar LabelImg

1. Presiona `W` → Crear caja alrededor del microplástico
2. Selecciona la clase:
   - **fibra**: Alargado, filamento
   - **fragmento**: Pedazo irregular
   - **pelicula**: Lámina delgada
   - **esfera**: Redondo
   - **microplastico_irregular**: Forma extraña
   - **aglomerado**: Grupo de partículas
3. Presiona `Ctrl+S` → Guardar
4. Presiona `D` → Siguiente imagen

### Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `W` | Crear caja |
| `Ctrl+S` | Guardar |
| `D` | Siguiente |
| `A` | Anterior |
| `Del` | Borrar caja |

## 📏 Calibración del Microscopio

Para mediciones precisas, necesitas el factor de conversión píxeles → micrómetros.

### Valores Típicos

| Magnificación | Factor (μm/píxel) |
|--------------|-------------------|
| 4x  | 2.5 - 5.0 |
| 10x | 1.0 - 2.0 |
| 20x | 0.3 - 0.8 |
| 40x | 0.15 - 0.4 |
| 100x | 0.06 - 0.15 |

⚠️ Estos son aproximados. Calibra con tu equipo usando una regla micrométrica.

## 📊 Resultados Generados

### Gráficos (`results/graphs/`)
- Distribución de tamaños
- Distribución de formas
- Dashboard resumen
- Curvas de frecuencia
- Comparaciones entre muestras

### Reportes (`results/reports/`)
- Reporte textual por muestra
- Datos Excel por muestra
- Consolidado de todas las muestras
- Resumen estadístico

### Anotaciones (`data/annotations/`)
- Archivos XML (formato PASCAL VOC)
- Compatible con TensorFlow, PyTorch, YOLO

## ⚙️ Configuración Avanzada

Edita `config/config.py` para ajustar:

```python
IMAGE_PARAMS = {
    'pixels_to_um': 1.0,           # Factor de conversión
    'threshold': 127,              # Umbral de segmentación
    'min_particle_area': 10,       # Área mínima (píxeles)
    'max_particle_area': 50000,    # Área máxima (píxeles)
}
```

## 🔧 Solución de Problemas

### LabelImg no se abre desde el botón
- Usa el botón alternativo en la pestaña
- O ejecuta: `abrir_labelimg.vbs`

### Error de dependencias
- Ejecuta nuevamente: `instalar.bat`
- O manual: `pip install -r requirements.txt`

### Sin imágenes en raw_images
- Coloca al menos una imagen en `data/raw_images/`
- Formatos válidos: jpg, png, tif, bmp

## 📚 Dependencias

### Requeridas
- **Procesamiento:** numpy, opencv-python, Pillow, scikit-image
- **Análisis:** pandas, scipy
- **Visualización:** matplotlib, seaborn
- **Anotación:** labelImg, PyQt5
- **🤖 YOLOv8 (REQUERIDO):** ultralytics, torch, torchvision, pyyaml
- **Utilidades:** openpyxl, python-dateutil

**Nota:** El instalador (`instalar.bat`) instala automáticamente todas las dependencias, incluyendo YOLOv8.

## 👥 Autor

**Desarrollado por:** Natalia Rojo  
**Institución:** Pontificia Universidad Católica de Valparaíso

## 📄 Licencia

Este proyecto es de uso académico.

---

**¿Problemas?** Revisa que:
1. ✅ Python 3.8+ instalado con PATH configurado
2. ✅ Ejecutaste `instalar.bat`
3. ✅ Tienes imágenes en `data/raw_images/`
4. ✅ Todas las dependencias se instalaron correctamente

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
- ✅ **🏷️ Anotar y etiquetar imágenes con LabelImg** (NUEVO)

## 🗂️ Estructura del Proyecto

```
mascaraPesta-a/
├── main.py                          # ⭐ Interfaz gráfica principal
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── GUIA_LABELIMG.md                 # 🏷️ Guía de anotación con LabelImg
├── instalar.bat                     # Script de instalación automática
│
├── config/
│   └── config.py                    # Configuración del proyecto
│
├── src/
│   ├── image_processing.py          # Procesamiento de imágenes
│   ├── statistical_analysis.py      # Análisis estadístico
│   ├── visualization.py             # Generación de gráficos
│   └── image_annotation.py          # 🏷️ Anotación con LabelImg (NUEVO)
│
├── ejemplos/
│   ├── ejemplo_basico.py            # Ejemplo básico de uso
│   ├── generar_muestras.py          # Generar imágenes de prueba
│   ├── ajustar_parametros.py        # Ajustar parámetros
│   ├── ejemplo_anotacion.py         # 🏷️ Ejemplo de anotación (NUEVO)
│   └── analizar_anotaciones.py      # 🏷️ Análisis de anotaciones (NUEVO)
│
├── data/
│   ├── raw_images/                  # ⚠️ COLOCAR IMÁGENES AQUÍ
│   ├── processed_images/            # Imágenes procesadas (auto-generado)
│   └── annotations/                 # 🏷️ Anotaciones de LabelImg (NUEVO)
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

**Método 1: Instalación Automática (Recomendado)**

1. **Ejecutar el script de instalación**:
   ```cmd
   instalar.bat
   ```
   Este script instalará todas las dependencias automáticamente, incluyendo LabelImg.

**Método 2: Instalación Manual**

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

El programa abrirá una ventana con 5 pestañas:

#### 1️⃣ **Configuración**
- Selecciona las imágenes a analizar
- Establece el factor de conversión píxeles → micrómetros
- Ajusta parámetros de umbral y tamaño de partículas

#### 2️⃣ **Análisis**
- Ejecuta el análisis completo de todas las imágenes
- Monitorea el progreso en tiempo real
- Genera reportes, gráficos y archivos Excel

#### 3️⃣ **🏷️ Anotar Imágenes** (NUEVO)
- **Anotación manual con LabelImg**: Herramienta gráfica para etiquetar microplásticos
- **Clases predefinidas**: fibra, fragmento, película, esfera, aglomerado
- **Exportación XML**: Formato PASCAL VOC para machine learning
- **Estadísticas de anotación**: Visualiza cuántos objetos has etiquetado

#### 4️⃣ **Ver Gráficos**
- Visualiza los gráficos generados
- Control de zoom (30%-500%)
- Filtros por tipo de gráfico
- Navegación con mouse wheel

#### 5️⃣ **Gestión de Resultados**
- Crea respaldos con fecha/hora
- Limpia resultados antiguos
- Abre carpetas de resultados y respaldos
- Monitorea espacio usado

## 🏷️ Anotación de Imágenes con LabelImg

### ¿Qué es LabelImg?

LabelImg es una herramienta gráfica que permite dibujar cajas delimitadoras (bounding boxes) alrededor de objetos en imágenes y asignarles etiquetas. Es especialmente útil para:

- **Validación manual**: Verificar qué partículas están presentes en las imágenes
- **Entrenamiento de IA**: Crear datasets para modelos de detección automática (YOLO, Faster R-CNN, etc.)
- **Clasificación de microplásticos**: Diferenciar tipos de partículas (fibras, fragmentos, películas, esferas)

### Cómo Usar LabelImg

1. **Abrir la pestaña "🏷️ Anotar Imágenes"** en la interfaz principal
2. **Hacer clic en "🏷️ Abrir LabelImg"**
3. **En LabelImg**:
   - Haz clic en **"Create RectBox"** (o presiona `w`) para dibujar una caja
   - Dibuja alrededor de cada microplástico
   - Selecciona la clase apropiada:
     - `fibra`: Microplásticos alargados en forma de filamento
     - `fragmento`: Pedazos irregulares de plástico
     - `pelicula`: Láminas delgadas de plástico
     - `esfera`: Partículas esféricas o microesferas
     - `microplastico_irregular`: Formas no clasificables
     - `aglomerado`: Conjunto de partículas unidas
   - Guarda la anotación (Ctrl+S)
   - Pasa a la siguiente imagen (teclas `d` o `a`)

4. **Ver estadísticas**: Regresa a la interfaz y haz clic en "🔄 Actualizar Estadísticas"

### Ubicación de las Anotaciones

Las anotaciones se guardan automáticamente en:
```
data/annotations/
├── predefined_classes.txt    # Clases predefinidas
├── imagen1.xml                # Anotación de imagen1.jpg
├── imagen2.xml                # Anotación de imagen2.jpg
└── ...
```

Cada archivo XML contiene las coordenadas de las cajas y las clases asignadas, compatible con frameworks de machine learning.

### Atajos de Teclado en LabelImg

| Tecla | Acción |
|-------|--------|
| `w` | Crear caja delimitadora |
| `d` | Siguiente imagen |
| `a` | Imagen anterior |
| `del` | Eliminar caja seleccionada |
| `Ctrl+S` | Guardar anotaciones |
| `Ctrl+D` | Duplicar caja |
| `Space` | Marcar imagen como verificada |



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
