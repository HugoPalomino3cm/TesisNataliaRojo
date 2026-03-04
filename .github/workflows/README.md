# 🚀 Compilación Automática con GitHub Actions

Este proyecto usa **GitHub Actions** para compilar automáticamente el archivo `.exe` en la nube, sin necesidad de hacerlo en tu computadora.

## 📋 ¿Cómo funciona?

Cuando subes cambios a GitHub, los servidores de GitHub:
1. ✅ Descargan tu código
2. ✅ Instalan Python y todas las dependencias
3. ✅ Compilan el `.exe` con PyInstaller
4. ✅ Te lo entregan listo para descargar

## 🎯 Descargar el .exe compilado

### Opción 1: Desde Actions (Después de cada commit)
1. Ve a tu repositorio en GitHub
2. Click en la pestaña **"Actions"**
3. Click en el workflow más reciente (debe tener ✅ check verde)
4. Baja hasta **"Artifacts"**
5. Descarga **"AnalisisMicroplasticos-Windows.zip"**
6. Descomprime y ejecuta el `.exe`

### Opción 2: Desde Releases (Versiones oficiales)
1. Ve a tu repositorio en GitHub
2. Click en **"Releases"** (lado derecho)
3. Click en **"Create a new release"**
4. Pon un tag (ej: `v1.0.0`) y título
5. Click en **"Publish release"**
6. GitHub compilará automáticamente y adjuntará el `.exe`

### Opción 3: Manual (Cuando quieras)
1. Ve a **"Actions"** en tu repositorio
2. Click en **"Build Windows Executable"**
3. Click en **"Run workflow"** → **"Run workflow"**
4. Espera a que termine (5-10 minutos)
5. Descarga desde "Artifacts"

## ⚙️ Configuración Inicial

### 1. Subir el proyecto a GitHub
```bash
# Si aún no tienes el repositorio en GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 2. Verificar que funciona
- GitHub ejecutará automáticamente el workflow
- Ve a la pestaña "Actions" para ver el progreso
- El primer build toma ~10 minutos

## 🔧 Personalizar la compilación

Edita el archivo `.github/workflows/build.yml` para:
- Cambiar el nombre del `.exe`
- Agregar más archivos de datos
- Modificar opciones de PyInstaller
- Cambiar cuándo se ejecuta el workflow

## 📊 Estado del Build

El badge muestra si la última compilación fue exitosa:

```markdown
![Build Status](https://github.com/TU_USUARIO/TU_REPO/workflows/Build%20Windows%20Executable/badge.svg)
```

## ❓ Problemas Comunes

### El workflow falla
- Revisa los logs en la pestaña "Actions"
- Verifica que `requirements.txt` tenga todas las dependencias
- Asegúrate de que el código funcione localmente primero

### El .exe no inicia
- Puede faltar algún archivo de datos (agrégalo con `--add-data`)
- Revisa los imports ocultos en el workflow

### Tarda mucho en compilar
- Es normal: primera vez ~10 min, después ~5 min
- GitHub cachea las dependencias para acelerar

## 💡 Ventajas

✅ No necesitas PyInstaller instalado localmente  
✅ Compila en un ambiente limpio (sin conflictos)  
✅ Puedes compilar desde cualquier computadora  
✅ Historial de todas las versiones compiladas  
✅ Automatización completa  

## 🎓 Recursos

- [Documentación GitHub Actions](https://docs.github.com/actions)
- [PyInstaller Docs](https://pyinstaller.org/)
