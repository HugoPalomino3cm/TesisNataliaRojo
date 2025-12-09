@echo off
REM Script para ejecutar labelImg desde repositorio clonado
cd /d "%~dp0"

if not exist "venv_py311\Scripts\activate" (
    echo Creando entorno virtual...
    py -3.11 -m venv venv_py311
    call venv_py311\Scripts\activate
    pip install PyQt5 lxml
) else (
    call venv_py311\Scripts\activate
)

REM Ejecutar labelImg desde el repositorio clonado
cd labelImg_tool
python labelImg.py "%cd%\..\data\raw_images" "%cd%\..\data\annotations\predefined_classes.txt" "%cd%\..\data\annotations"
