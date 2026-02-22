# Estructura de Carpetas de Datos

## 📂 Organización

Este proyecto tiene **3 carpetas separadas** para diferentes propósitos:

### 1. `raw_images/` - **SOLO PARA ENTRENAMIENTO** 🏋️
**Propósito:** Imágenes para entrenar el modelo YOLOv8

**Contenido:**
- Imágenes de microplásticos (.jpg, .png, etc.)
- Archivos de anotación XML (generados por LabelImg)

**Cómo usar:**
1. Copia aquí las imágenes que quieres anotar
2. Ve a la pestaña "Anotar Imágenes" y usa LabelImg para marcar partículas
3. Los archivos XML se guardan automáticamente junto a las imágenes
4. Ve a "Entrenar YOLOv8" para entrenar un modelo con estas imágenes

**⚠️ IMPORTANTE:** NO pongas aquí imágenes que quieras analizar, solo las de entrenamiento.

---

### 2. `analysis_images/` - **SOLO PARA ANÁLISIS** 🔍
**Propósito:** Imágenes que quieres analizar con el modelo entrenado

**Contenido:**
- Imágenes de microplásticos sin anotar
- NO necesitan archivos XML
- Pueden ser imágenes nuevas o de prueba

**Cómo usar:**
1. Copia aquí las imágenes que quieres analizar
2. Ve a la pestaña "Configuración" → Click "Cargar Imágenes para Analizar"
3. Ve a la pestaña "Análisis" → Click "Analizar"
4. El modelo detectará automáticamente las partículas

---

### 3. `processed_images/` - **RESULTADOS** 📊
**Propósito:** Imágenes procesadas con detecciones marcadas

**Contenido:**
- Se genera automáticamente durante el análisis
- Contiene las imágenes con las partículas detectadas marcadas

---

## 🔄 Flujo de Trabajo Completo

```
1. ENTRENAR
   ├─ Pon imágenes en raw_images/
   ├─ Anota con LabelImg (genera XML)
   └─ Entrena modelo YOLOv8
   
2. ANALIZAR
   ├─ Pon imágenes NUEVAS en analysis_images/
   ├─ Carga el modelo entrenado
   └─ Ejecuta análisis
```

---

## 📝 Ejemplo Práctico

### Escenario: Tienes 20 imágenes de microplásticos

**Paso 1: Entrenar (10 imágenes)**
```
data/raw_images/
├── muestra_01.jpg  ← Anotar
├── muestra_01.xml  ← Generado por LabelImg
├── muestra_02.jpg  ← Anotar
├── muestra_02.xml
├── ...
└── muestra_10.xml
```

**Paso 2: Analizar (10 imágenes restantes)**
```
data/analysis_images/
├── muestra_11.jpg  ← Sin anotar, solo analizar
├── muestra_12.jpg
├── ...
└── muestra_20.jpg
```

---

## ⚡ Comandos Rápidos

### Windows PowerShell:
```powershell
# Ver imágenes de entrenamiento
Get-ChildItem data\raw_images\*.jpg

# Ver imágenes para análisis
Get-ChildItem data\analysis_images\*.jpg

# Copiar imagen a análisis
Copy-Item "imagen.jpg" "data\analysis_images\"
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo analizar las mismas imágenes que entrené?**
R: Técnicamente sí, pero no es recomendable. Siempre prueba con imágenes nuevas.

**P: ¿Qué pasa si pongo imágenes sin XML en raw_images?**
R: YOLO las ignorará durante el entrenamiento (solo usa imágenes con XML).

**P: ¿Puedo tener la misma imagen en ambas carpetas?**
R: Sí, pero no tiene sentido. El objetivo es entrenar con unas y probar con otras.

**P: ¿Dónde están los modelos entrenados?**
R: En `yolo_training/models/microplasticos/yolov8_N/weights/best.pt`

---

## 📌 Resumen Rápido

| Carpeta | Propósito | Necesita XML | Uso |
|---------|-----------|--------------|-----|
| `raw_images/` | Entrenamiento | ✅ Sí | LabelImg + Entrenar |
| `analysis_images/` | Análisis | ❌ No | Solo Analizar |
| `processed_images/` | Resultados | ❌ No | Auto-generado |
