# Actualización: Gráficos de Distribución por Tipo de Microplástico

## 📊 Resumen de Cambios

Se ha actualizado el sistema de análisis para incluir **gráficos que muestran la distribución por tipo de microplástico detectado**. Ahora los gráficos reflejan correctamente las **6 clases de etiquetas** que estás usando:

### 🏷️ Tipos de Microplásticos Detectados:
1. **fibra** - Color azul (#2563eb)
2. **fragmento** - Color verde (#16a34a)
3. **película** - Color amarillo (#eab308)
4. **esfera** - Color rojo (#dc2626)
5. **microplástico_irregular** - Color púrpura (#9333ea)
6. **aglomerado** - Color naranja (#ea580c)

---

## ✨ Nuevas Funcionalidades

### 🎨 **Generación Automática de Colores**

El sistema ahora **genera colores automáticamente** para cualquier tipo de microplástico que agregues:

- ✅ Los 6 tipos predefinidos tienen colores específicos
- ✅ **Cualquier tipo nuevo recibe un color único automáticamente**
- ✅ Los colores se asignan de forma consistente (mismo nombre = mismo color)
- ✅ Paleta de 15+ colores adicionales disponibles
- ✅ Si agregas más de 15 tipos nuevos, los colores se reciclan automáticamente

#### Ejemplo:
Si agregas nuevos tipos como `espuma`, `film`, `pellet`, etc., cada uno recibirá automáticamente un color distintivo de la paleta extendida (cyan, violeta, rosa, teal, etc.).

### 1. **Nuevo Gráfico: Distribución por Tipo de Microplástico**

Se creó la función `plot_class_distribution()` que genera un gráfico completo con 4 paneles:

#### Panel 1: Gráfico de Barras
- Muestra la **cantidad** de cada tipo de microplástico
- Cada barra tiene su color distintivo
- Incluye valores numéricos sobre las barras

#### Panel 2: Gráfico de Pastel
- Muestra el **porcentaje** de cada tipo
- Con colores distintivos para cada categoría
- Porcentajes claramente visibles

#### Panel 3: Tabla de Estadísticas
- **Cantidad** y **porcentaje** de cada tipo
- **Área promedio** en μm²
- **Diámetro promedio** en μm
- Formato claro y profesional

#### Panel 4: Boxplot Comparativo
- Compara la **distribución de tamaños** entre tipos
- Permite ver diferencias morfológicas entre categorías
- Identifica valores atípicos por tipo

### 2. **Dashboard Actualizado**

El dashboard principal (`create_summary_dashboard()`) ahora muestra:
- **Tipos de microplástico** en lugar de solo categorías de tamaño
- Si no hay datos de YOLO, muestra categorías de tamaño como respaldo
- Mantiene compatibilidad con análisis sin clasificación

### 3. **Análisis Estadístico por Tipo**

Nueva función `analyze_class_distribution()` que calcula:
- Conteo y porcentaje de cada tipo
- Estadísticas descriptivas (área, diámetro, aspect ratio) por tipo
- Comparaciones entre tipos

### 4. **Reportes Mejorados**

Los reportes de texto ahora incluyen:
- Sección dedicada a "DISTRIBUCIÓN POR TIPO DE MICROPLÁSTICO"
- Estadísticas detalladas para cada tipo detectado
- Área y diámetro promedio con desviación estándar

---

## 🎯 Cómo Usar

### Al ejecutar el análisis:

1. **Carga tus imágenes** en la interfaz gráfica
2. **Anota las imágenes** con LabelImg usando las 6 clases
3. **Entrena el modelo YOLOv8** con tus anotaciones
4. **Ejecuta el análisis** con el modelo entrenado

### Gráficos generados automáticamente:

Para cada muestra analizada, se crearán:
- `[muestra]_class_distribution.png` - **NUEVO: Distribución por tipo**
- `[muestra]_size_distribution.png` - Distribución de tamaños
- `[muestra]_shape_distribution.png` - Distribución de formas
- `[muestra]_dashboard.png` - Dashboard completo (con tipos)
- `[muestra]_frequency_curve.png` - Curva de frecuencia
- `[muestra]_correlation_matrix.png` - Matriz de correlación

---

## 📁 Archivos Modificados

### 1. `src/visualization.py`
- ✅ Nueva función `plot_class_distribution()`
- ✅ Actualizado `create_summary_dashboard()` para mostrar tipos

### 2. `src/statistical_analysis.py`
- ✅ Nueva función `analyze_class_distribution()`
- ✅ Actualizado `generate_summary_report()` para incluir tipos

### 3. `main.py`
- ✅ Integrado gráfico de tipos en el flujo de análisis
- ✅ Se genera automáticamente si hay datos de clasificación

---

## 🔍 Verificación de Etiquetas

### Tus clases están definidas en:
- `data/annotations/predefined_classes.txt`
- `src/yolo_detector.py` (CLASS_NAMES)
- `src/train_yolo.py`
- `src/image_annotation.py`

### Para verificar que todo funciona:

1. **Revisa tus anotaciones**: Las etiquetas XML deben tener nombres exactos
2. **Entrena YOLO**: El modelo aprenderá las 6 clases
3. **Analiza una muestra**: Verás el nuevo gráfico de tipos
4. **Revisa el reporte**: Contendrá estadísticas por tipo

---

## 💡 Beneficios

✅ **Concordancia visual**: Los gráficos ahora muestran exactamente lo que etiquetaste
✅ **Análisis detallado**: Puedes ver qué tipos de microplástico predominan
✅ **Comparación por tipo**: Identifica diferencias morfológicas entre categorías
✅ **Reportes completos**: Toda la información en texto y gráficos
✅ **Colores distintivos**: Cada tipo tiene su propio color para fácil identificación
✅ **🆕 Escalabilidad**: Puedes agregar **infinitos tipos nuevos** sin modificar código
✅ **🆕 Colores automáticos**: Cualquier tipo nuevo recibe un color único automáticamente
✅ **🆕 Consistencia**: El mismo tipo siempre tiene el mismo color

---

## 🎨 Paleta de Colores

### Colores Predefinidos (6 tipos base):

| Tipo | Color | Código Hex | Uso |
|------|-------|------------|-----|
| Fibra | Azul | #2563eb | Estructuras alargadas |
| Fragmento | Verde | #16a34a | Piezas irregulares |
| Película | Amarillo | #eab308 | Láminas finas |
| Esfera | Rojo | #dc2626 | Partículas redondas |
| Microplástico irregular | Púrpura | #9333ea | Formas atípicas |
| Aglomerado | Naranja | #ea580c | Agrupaciones |

### 🆕 Paleta Extendida para Tipos Adicionales:

Si agregas nuevos tipos de microplásticos (por ejemplo: `espuma`, `film`, `pellet`, `granulo`, etc.), se asignarán automáticamente colores de esta paleta:

| Color | Código Hex | Nombre |
|-------|------------|--------|
| Cyan | #06b6d4 | Color 1 |
| Naranja oscuro | #f97316 | Color 2 |
| Violeta | #8b5cf6 | Color 3 |
| Rosa | #ec4899 | Color 4 |
| Teal | #14b8a6 | Color 5 |
| Ámbar | #f59e0b | Color 6 |
| Lima | #84cc16 | Color 7 |
| Índigo | #6366f1 | Color 8 |
| Púrpura claro | #a855f7 | Color 9 |
| Rojo claro | #ef4444 | Color 10 |
| Esmeralda | #10b981 | Color 11 |
| Azul claro | #3b82f6 | Color 12 |
| Fucsia | #d946ef | Color 13 |
| Cyan claro | #22d3ee | Color 14 |
| Amarillo oro | #facc15 | Color 15 |

**💡 Nota:** El sistema asigna colores de forma consistente usando el nombre del tipo. El mismo nombre siempre tendrá el mismo color, incluso entre diferentes análisis.

---

## 📊 Ejemplo de Salida

Cuando analices una muestra, verás en la consola:

```
3. Generando visualizaciones...
   ✓ Guardado: muestra_class_distribution.png    ← NUEVO
   ✓ Guardado: muestra_size_distribution.png
   ✓ Guardado: muestra_shape_distribution.png
   ✓ Guardado: muestra_dashboard.png
   ...
```

Y en el reporte de texto:

```
DISTRIBUCIÓN POR TIPO DE MICROPLÁSTICO
------------------------------------------------------------
fibra:
  Cantidad: 45 (30.0%)
  Área promedio: 125.50 ± 35.20 μm²
  Diámetro promedio: 12.65 ± 3.10 μm

fragmento:
  Cantidad: 38 (25.3%)
  Área promedio: 98.30 ± 28.50 μm²
  Diámetro promedio: 11.20 ± 2.80 μm

...
```

---

## ⚙️ Requisitos

- ✅ Python 3.11+
- ✅ YOLOv8 (ultralytics)
- ✅ Modelo entrenado con tus 6 clases
- ✅ Imágenes anotadas con LabelImg

---

## 🚀 Próximos Pasos

1. **Anota más imágenes** con las 6 clases definidas (o las que decidas usar)
2. **¿Necesitas más tipos?** Simplemente agrégalos a `predefined_classes.txt` y obtendrán colores automáticamente
3. **Entrena tu modelo YOLOv8** con suficientes ejemplos de cada clase
4. **Ejecuta el análisis** y verifica los nuevos gráficos con colores automáticos
5. **Utiliza los gráficos** en tu tesis para mostrar la distribución de tipos

### 📝 Cómo agregar nuevos tipos:

1. Edita `data/annotations/predefined_classes.txt`
2. Agrega tus nuevos tipos (uno por línea):
   ```
   fibra
   fragmento
   pelicula
   esfera
   microplastico_irregular
   aglomerado
   espuma          ← NUEVO
   film            ← NUEVO
   pellet          ← NUEVO
   ```
3. Anota tus imágenes con LabelImg usando los nuevos tipos
4. Entrena el modelo YOLO
5. ¡Los gráficos mostrarán los nuevos tipos con colores automáticos!

---

**Fecha de actualización:** Diciembre 9, 2025
**Desarrollado por:** Natalia Rojo (con asistencia de GitHub Copilot)
