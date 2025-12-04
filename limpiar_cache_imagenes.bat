@echo off
echo Limpiando cache de imagenes...

REM Eliminar archivos de cache de thumbnails de Windows
del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db 2>nul
del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\iconcache_*.db 2>nul

REM Eliminar imagenes actuales
echo Eliminando imagenes antiguas...
cd /d "%~dp0"
del /f /q data\raw_images\*.jpg 2>nul
del /f /q data\raw_images\*.png 2>nul

REM Esperar un momento
timeout /t 2 /nobreak >nul

REM Limpiar atributos de la carpeta
attrib -h -s data\raw_images /s /d

REM Regenerar imagenes
echo Generando imagenes nuevas...
python ejemplos\generar_imagenes_prueba.py

REM Limpiar cache de Explorer nuevamente
ie4uinit.exe -show

echo.
echo Listo! Las imagenes han sido regeneradas sin cache.
echo Presiona cualquier tecla para cerrar...
pause >nul
