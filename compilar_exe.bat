@echo off
REM Script para compilar localmente el ejecutable (prueba antes de GitHub Actions)
echo ========================================
echo Compilando Analisis de Microplasticos
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist "venv_py311\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv_py311\Scripts\activate.bat
)

REM Verificar si PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller no esta instalado. Instalando...
    pip install pyinstaller
)

REM Limpiar compilaciones anteriores
if exist "build" (
    echo Limpiando archivos anteriores...
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)

REM Compilar usando el archivo .spec (más control)
echo.
echo Compilando ejecutable...
echo Esto puede tomar varios minutos...
echo.

pyinstaller build.spec

if errorlevel 1 (
    echo.
    echo ERROR: La compilacion fallo
    echo Revisa los mensajes anteriores para mas detalles
    pause
    exit /b 1
)

echo.
echo ========================================
echo COMPILACION EXITOSA!
echo ========================================
echo El ejecutable esta en: dist\AnalisisMicroplasticos.exe
echo.
echo Puedes probarlo ejecutandolo desde la carpeta dist\
echo.

REM Abrir la carpeta dist
start dist

pause
