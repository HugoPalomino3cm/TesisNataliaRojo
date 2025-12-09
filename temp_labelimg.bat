@echo off
cd /d "c:\Users\xg645\Downloads\TesisNataliaRojo"
echo Verificando instalacion de labelImg...
python -c "import labelImg" 2>nul
if errorlevel 1 (
    echo labelImg no esta instalado. Instalando...
    pip install labelImg PyQt5
    if errorlevel 1 (
        echo Error al instalar labelImg
        pause
        exit /b 1
    )
)
echo Abriendo labelImg...
labelImg "c:\Users\xg645\Downloads\TesisNataliaRojo\data\raw_images" "c:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations\predefined_classes.txt" "c:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations"
if errorlevel 1 (
    echo.
    echo Error al abrir labelImg
    echo Intenta ejecutar: pip install labelImg PyQt5
    pause
)
