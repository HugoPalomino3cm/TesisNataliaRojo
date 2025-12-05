@echo off
REM ========================================================
REM Script de Instalacion - Analisis de Microplasticos
REM Instalacion completa automatica
REM ========================================================

echo.
echo ================================================================
echo   INSTALACION COMPLETA - ANALISIS DE MICROPLASTICOS
echo ================================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor, instale Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante la instalacion, marque la opcion
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

echo ================================================================
echo   PASO 1: ACTUALIZANDO PIP
echo ================================================================
echo.
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] No se pudo actualizar pip
    pause
    exit /b 1
)
echo [OK] pip actualizado correctamente
echo.

echo ================================================================
echo   PASO 2: INSTALANDO DEPENDENCIAS PRINCIPALES
echo ================================================================
echo.
echo Instalando librerias de procesamiento de imagenes...
pip install numpy>=1.24.0 opencv-python>=4.8.0 Pillow>=10.0.0 scikit-image>=0.21.0
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de librerias de imagenes
    pause
    exit /b 1
)
echo [OK] Librerias de imagenes instaladas
echo.

echo Instalando librerias de analisis de datos...
pip install pandas>=2.0.0 scipy>=1.11.0
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de librerias de datos
    pause
    exit /b 1
)
echo [OK] Librerias de datos instaladas
echo.

echo Instalando librerias de visualizacion...
pip install matplotlib>=3.7.0 seaborn>=0.12.0
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de librerias de visualizacion
    pause
    exit /b 1
)
echo [OK] Librerias de visualizacion instaladas
echo.

echo Instalando utilidades...
pip install openpyxl>=3.1.0 python-dateutil>=2.8.2
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de utilidades
    pause
    exit /b 1
)
echo [OK] Utilidades instaladas
echo.

echo ================================================================
echo   PASO 3: INSTALANDO LABELIMG
echo ================================================================
echo.
pip install labelImg>=1.8.6 PyQt5>=5.15.0
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de LabelImg
    pause
    exit /b 1
)
echo [OK] LabelImg instalado correctamente
echo.

echo ================================================================
echo   PASO 4: INSTALANDO YOLOV8 Y PYTORCH
echo ================================================================
echo.
echo Instalando PyTorch y TorchVision...
pip install torch>=2.0.0 torchvision>=0.15.0
if errorlevel 1 (
    echo [ADVERTENCIA] Fallo la instalacion de PyTorch
    echo El sistema funcionara sin YOLOv8 (solo deteccion tradicional)
    echo Para usar YOLOv8, instale manualmente:
    echo   pip install torch torchvision ultralytics
) else (
    echo [OK] PyTorch instalado correctamente
)
echo.

echo Instalando Ultralytics YOLOv8...
pip install ultralytics>=8.0.0 pyyaml>=6.0
if errorlevel 1 (
    echo [ADVERTENCIA] Fallo la instalacion de Ultralytics
    echo El sistema funcionara sin YOLOv8 (solo deteccion tradicional)
) else (
    echo [OK] YOLOv8 instalado correctamente
)
echo.

echo ================================================================
echo   PASO 5: CREANDO ESTRUCTURA DE DIRECTORIOS
echo ================================================================
echo.
if not exist "data\raw_images" mkdir data\raw_images
if not exist "data\processed_images" mkdir data\processed_images
if not exist "data\annotations" mkdir data\annotations
if not exist "results\graphs" mkdir results\graphs
if not exist "results\reports" mkdir results\reports
if not exist "backups" mkdir backups
if not exist "yolo_training\dataset" mkdir yolo_training\dataset
if not exist "yolo_training\models" mkdir yolo_training\models
if not exist "models" mkdir models
echo [OK] Directorios creados
echo.

echo ================================================================
echo   PASO 6: CONFIGURANDO LABELIMG Y YOLO
echo ================================================================
echo.
REM Crear archivo de clases predefinidas
if not exist "data\annotations\predefined_classes.txt" (
    echo fibra> data\annotations\predefined_classes.txt
    echo fragmento>> data\annotations\predefined_classes.txt
    echo pelicula>> data\annotations\predefined_classes.txt
    echo esfera>> data\annotations\predefined_classes.txt
    echo microplastico_irregular>> data\annotations\predefined_classes.txt
    echo aglomerado>> data\annotations\predefined_classes.txt
    echo [OK] Clases predefinidas creadas
) else (
    echo [OK] Clases predefinidas ya existen
)
echo.

echo ================================================================
echo   PASO 7: VERIFICANDO INSTALACION
echo ================================================================
echo.
echo Verificando LabelImg...
pip show labelImg >nul 2>&1
if errorlevel 1 (
    echo [ERROR] LabelImg no se instalo correctamente
    pause
    exit /b 1
) else (
    echo [OK] LabelImg verificado
)

echo Verificando PyQt5...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyQt5 no se instalo correctamente
    pause
    exit /b 1
) else (
    echo [OK] PyQt5 verificado
)

echo Verificando numpy...
python -c "import numpy" 2>nul
if errorlevel 1 (
    echo [ERROR] numpy no funciona correctamente
    pause
    exit /b 1
) else (
    echo [OK] numpy verificado
)

echo Verificando opencv...
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo [ERROR] opencv no funciona correctamente
    pause
    exit /b 1
) else (
    echo [OK] opencv verificado
)

echo Verificando matplotlib...
python -c "import matplotlib" 2>nul
if errorlevel 1 (
    echo [ERROR] matplotlib no funciona correctamente
    pause
    exit /b 1
) else (
    echo [OK] matplotlib verificado
)

echo Verificando pandas...
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo [ERROR] pandas no funciona correctamente
    pause
    exit /b 1
) else (
    echo [OK] pandas verificado
)

echo Verificando ultralytics (opcional)...
python -c "import ultralytics" 2>nul
if errorlevel 1 (
    echo [ADVERTENCIA] ultralytics no disponible - YOLOv8 no funcionara
    echo              El sistema usara deteccion tradicional
) else (
    echo [OK] ultralytics verificado - YOLOv8 disponible
)
echo.

echo ================================================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ================================================================
echo.
echo Todas las dependencias estan instaladas y verificadas:
echo   [OK] Procesamiento de imagenes (numpy, opencv, pillow, scikit-image)
echo   [OK] Analisis de datos (pandas, scipy)
echo   [OK] Visualizacion (matplotlib, seaborn)
echo   [OK] Anotacion de imagenes (LabelImg, PyQt5)
echo   [OK] Deteccion con IA (YOLOv8, PyTorch) - si esta disponible
echo   [OK] Utilidades (openpyxl, python-dateutil)
echo.
echo Estructura de directorios lista:
echo   [OK] data\raw_images           (coloque aqui sus imagenes)
echo   [OK] data\processed_images     (imagenes procesadas)
echo   [OK] data\annotations          (anotaciones de LabelImg)
echo   [OK] results\graphs            (graficos generados)
echo   [OK] results\reports           (reportes y datos)
echo   [OK] backups                   (respaldos automaticos)
echo   [OK] yolo_training             (entrenamiento YOLOv8)
echo   [OK] models                    (modelos YOLO entrenados)
echo.
echo ================================================================
echo   COMO USAR EL SISTEMA
echo ================================================================
echo.
echo 1. Coloque sus imagenes microscopicas en:
echo    data\raw_images\
echo.
echo 2. Ejecute el programa:
echo    python main.py
echo.
echo 3. Siga el flujo en las pestanas:
echo    a. Configuracion: Cargar imagenes y calibrar
echo    b. Anotar Imagenes: Etiquetar con LabelImg
echo    c. Entrenar YOLOv8: Entrenar modelo de deteccion (NUEVO!)
echo    d. Analisis: Procesar imagenes (tradicional o con YOLO)
echo    e. Ver Graficos: Visualizar resultados
echo    f. Gestion: Administrar archivos
echo.
echo 4. Para usar YOLOv8:
echo    - Anote imagenes con LabelImg (pestana 2)
echo    - Entrene el modelo (pestana 3)
echo    - Active YOLOv8 en pestana 3
echo    - Analice con IA (pestana 4)
echo.
echo 5. Para abrir LabelImg directamente:
echo    - Doble clic en: abrir_labelimg.vbs
echo    - O desde la pestana "Anotar Imagenes" en el programa
echo.
echo ================================================================
echo   DOCUMENTACION
echo ================================================================
echo.
echo README.md - Documentacion completa del sistema
echo.
echo ================================================================
echo.
echo Presione cualquier tecla para ejecutar el programa...
pause >nul

echo.
echo Iniciando el programa...
python main.py
