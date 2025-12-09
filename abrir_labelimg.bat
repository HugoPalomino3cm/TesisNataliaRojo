@echo off
cd /d "%~dp0"

echo.
echo ================================================
echo       LABELIMG - ANOTADOR DE IMAGENES
echo ================================================
echo.

REM Verificar si existe el entorno virtual Python 3.11
if not exist "venv_py311\Scripts\python.exe" (
    echo [!] Creando entorno virtual con Python 3.11...
    py -3.11 -m venv venv_py311
    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudo crear el entorno virtual
        echo Asegurate de tener Python 3.11 instalado
        pause
        exit /b 1
    )
    
    echo [!] Instalando PyQt5 y lxml en el entorno virtual...
    venv_py311\Scripts\pip.exe install PyQt5 lxml
    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudo instalar las dependencias
        pause
        exit /b 1
    )
)

echo [OK] Entorno Python 3.11 listo
echo.
echo Iniciando labelImg desde repositorio clonado...
echo.

REM Ejecutar labelImg desde repositorio clonado con Python 3.11
cd labelImg_tool
..\venv_py311\Scripts\python.exe labelImg.py "%cd%\..\data\raw_images" "%cd%\..\data\annotations\predefined_classes.txt" "%cd%\..\data\annotations"

if errorlevel 1 (
    echo.
    echo [!] labelImg cerrado con errores
) else (
    echo.
    echo [OK] labelImg cerrado correctamente
)

cd ..
echo.
pause
