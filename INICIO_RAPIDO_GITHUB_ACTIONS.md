# 🚀 INICIO RÁPIDO - GitHub Actions

## ✅ Lo que ya está configurado

He configurado tu proyecto con **compilación automática en la nube** usando GitHub Actions. Esto significa que GitHub compilará tu aplicación a `.exe` automáticamente.

## 📁 Archivos creados

1. **`.github/workflows/build.yml`** - Configuración principal de GitHub Actions
2. **`build.spec`** - Configuración avanzada de PyInstaller
3. **`compilar_exe.bat`** - Script para compilar localmente (opcional)
4. **`GITHUB_ACTIONS.md`** - Guía completa y detallada
5. **`.github/workflows/README.md`** - Documentación técnica

## 🎯 Próximos pasos

### Paso 1: Subir a GitHub (si aún no lo has hecho)

```bash
# Abre PowerShell en la carpeta del proyecto
git init
git add .
git commit -m "Configurar GitHub Actions para compilación automática"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TesisNataliaRojo.git
git push -u origin main
```

### Paso 2: Ver la compilación automática

1. Ve a tu repositorio en **GitHub.com**
2. Click en la pestaña **"Actions"** (arriba)
3. Verás el workflow **"Build Windows Executable"** ejecutándose
4. Tarda ~5-10 minutos la primera vez

### Paso 3: Descargar el .exe

**Opción A: Desde Actions (después de cada commit)**
1. Click en el workflow terminado (✅ verde)
2. Scroll abajo hasta **"Artifacts"**
3. Descarga **"AnalisisMicroplasticos-Windows.zip"**
4. Descomprime y ejecuta el `.exe`

**Opción B: Crear un Release (recomendado para versiones oficiales)**
1. En GitHub, click **"Releases"** → **"Create a new release"**
2. Tag: `v1.0.0`
3. Título: `Primera versión estable`
4. Click **"Publish release"**
5. El `.exe` se compila y adjunta automáticamente

### Paso 4: Compilar sin hacer commit (manual)

1. Ve a **"Actions"** en GitHub
2. Click **"Build Windows Executable"** (izquierda)
3. Click **"Run workflow"** → **"Run workflow"**
4. Descarga desde "Artifacts" cuando termine

## 🔧 Probar localmente primero (recomendado)

Antes de subir a GitHub, prueba en tu PC:

```cmd
compilar_exe.bat
```

Esto verifica que la compilación funcione antes de usar GitHub Actions.

## 📊 ¿Qué hace GitHub Actions?

Cuando subes código a GitHub:

1. ✅ Detecta los cambios automáticamente
2. ✅ Crea un servidor Windows temporal en la nube
3. ✅ Instala Python 3.11 y todas las dependencias
4. ✅ Ejecuta PyInstaller para compilar el `.exe`
5. ✅ Sube el `.exe` para que lo descargues
6. ✅ Destruye el servidor temporal

**Todo gratis, todo automático.**

## 💡 Ventajas

✅ No necesitas PyInstaller en tu PC  
✅ Compila en un ambiente limpio (sin conflictos)  
✅ Cualquiera puede descargar el `.exe` desde GitHub  
✅ Historial completo de todas las versiones  
✅ Distribución fácil sin instalar Python  

## 📖 Más información

- **Guía detallada:** [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)
- **README principal:** [README.md](README.md)
- **Documentación técnica:** [.github/workflows/README.md](.github/workflows/README.md)

## 🐛 ¿Algo no funciona?

1. Ve a "Actions" en GitHub
2. Click en el workflow fallido
3. Lee los logs (expandiendo los pasos con ❌)
4. Si el error no es claro, compila localmente con `compilar_exe.bat`

## 🎓 Recursos

- [GitHub Actions Docs](https://docs.github.com/actions)
- [PyInstaller Manual](https://pyinstaller.org/)

---

✨ **¡Todo listo!** Tu proyecto ahora se compila automáticamente en GitHub.
