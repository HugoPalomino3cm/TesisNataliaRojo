# 🤖 GitHub Actions - Compilación Automática

## 📖 ¿Qué es GitHub Actions?

**GitHub Actions** es un servicio de automatización que GitHub ofrece **GRATIS** donde:
- Los servidores de GitHub compilan tu código por ti
- Se ejecuta en la nube (no usa tu computadora)
- Genera el `.exe` automáticamente cada vez que subes cambios
- No necesitas tener PyInstaller ni dependencias instaladas localmente

## 🎯 ¿Para qué sirve?

### Escenarios de uso:

1. **Compilar sin PyInstaller local**
   - No necesitas instalar PyInstaller en tu PC
   - GitHub lo hace todo en su servidor Windows

2. **Distribución fácil**
   - Cualquiera puede descargar el `.exe` desde GitHub
   - No necesitan Python instalado

3. **Versiones automáticas**
   - Cada commit genera un nuevo `.exe`
   - Historial completo de todas las versiones

4. **Trabajo en equipo**
   - Todos los miembros pueden descargar el `.exe`
   - No hay "en mi máquina funciona"

## 🚀 Cómo funciona

```
┌─────────────────┐
│  Haces commit   │
│   y push a      │ 
│    GitHub       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │
│   se activa     │
│  automático     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Servidor de    │
│  GitHub clona   │
│   tu código     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Instala Python  │
│    y todas las  │
│  dependencias   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ejecuta        │
│  PyInstaller    │
│  compila .exe   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Sube el .exe  │
│   para que lo   │
│   descargues    │
└─────────────────┘
```

## 📦 Lo que he creado

### 1. `.github/workflows/build.yml` 
Archivo principal que dice a GitHub qué hacer:
- Cuándo compilar (cada push, pull request, release)
- Qué instalar (Python 3.11, dependencias)
- Cómo compilar (PyInstaller con configuración específica)
- Dónde guardar el resultado (artifacts)

### 2. `build.spec`
Configuración avanzada de PyInstaller:
- Qué archivos incluir (`config/`, `src/`, `yolov8n.pt`)
- Imports ocultos necesarios
- Sin ventana de consola
- Compresión UPX

### 3. `compilar_exe.bat`
Script para compilar localmente (opcional):
- Úsalo para probar ANTES de subir a GitHub
- Verifica que funcione en tu PC primero

### 4. `.github/workflows/README.md`
Guía de uso completa

## 🎬 Guía paso a paso

### Paso 1: Subir a GitHub (si no lo has hecho)

```bash
# En PowerShell, desde la carpeta del proyecto:
git init
git add .
git commit -m "Configurar GitHub Actions para compilar .exe"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TesisNataliaRojo.git
git push -u origin main
```

### Paso 2: Ver el progreso en GitHub

1. Abre tu repositorio en GitHub.com
2. Click en la pestaña **"Actions"** (arriba)
3. Verás el workflow "Build Windows Executable" ejecutándose
4. Tarda ~5-10 minutos la primera vez

### Paso 3: Descargar el .exe

**Opción A: Desde la página de Actions**
1. Click en el workflow que terminó (✅ verde)
2. Scroll abajo hasta "Artifacts"
3. Click en **"AnalisisMicroplasticos-Windows"**
4. Se descarga un ZIP con el `.exe` dentro

**Opción B: Crear un Release (recomendado)**
1. En GitHub, click "Releases" → "Create a new release"
2. Tag: `v1.0.0` (o la versión que quieras)
3. Título: "Primera versión estable"
4. Click "Publish release"
5. GitHub compilará automáticamente y adjuntará el `.exe`

### Paso 4: Ejecutar manual (opcional)

Si quieres compilar sin hacer commit:
1. Ve a "Actions"
2. Click "Build Windows Executable" (izquierda)
3. Click "Run workflow" (derecha) → "Run workflow"
4. Espera y descarga desde Artifacts

## ⚙️ Personalización

### Cambiar cuándo se compila

Edita [.github/workflows/build.yml](.github/workflows/build.yml):

```yaml
on:
  push:
    branches: [ main ]        # Solo en la rama main
  release:
    types: [ created ]        # Cuando creas un release
  workflow_dispatch:          # Manualmente desde GitHub
```

### Agregar más archivos de datos

```yaml
--add-data "carpeta;carpeta" `
--add-data "archivo.txt;." `
```

### Cambiar el nombre del .exe

```yaml
--name="MiAplicacion" `
```

## 🔒 Límites y cuotas

GitHub Actions es **GRATIS** para repositorios públicos con:
- ✅ 2000 minutos/mes de compilación
- ✅ Cada compilación toma ~5-10 minutos
- ✅ = ~200-400 compilaciones por mes
- ✅ Más que suficiente para desarrollo normal

Para repositorios privados: 2000 minutos gratis también.

## 💡 Consejos

### ✅ DO (Hacer)
- Prueba localmente con `compilar_exe.bat` primero
- Usa releases para versiones importantes
- Revisa los logs si algo falla
- Mantén `requirements.txt` actualizado

### ❌ DON'T (No hacer)
- No subas el `.exe` al repositorio (se genera automático)
- No subas `venv/`, `build/`, `dist/` (usa .gitignore)
- No hagas commits solo para compilar (usa workflow_dispatch)

## 🐛 Solución de problemas

### El workflow falla

1. Click en el workflow fallido
2. Click en "build" (job)
3. Expande el paso que falló (❌ rojo)
4. Lee el error

**Errores comunes:**
- `ModuleNotFoundError`: Falta una dependencia en `requirements.txt`
- `File not found`: Verifica rutas en `--add-data`
- `Import Error`: Agrega a `hiddenimports` en `build.spec`

### El .exe no funciona

1. Descarga el artifact
2. Ejecuta el `.exe`
3. Si falla, compila localmente con `compilar_exe.bat`
4. Verás el error en tu PC

### Tarda mucho

- Primera vez: ~10 min (instala todo)
- Siguientes: ~5 min (usa caché)
- Es normal, GitHub compila desde cero

## 📚 Recursos adicionales

- [Documentación oficial GitHub Actions](https://docs.github.com/actions)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Ejemplo de .spec file](build.spec)

## ❓ Preguntas frecuentes

**P: ¿Es gratis?**  
R: Sí, completamente gratis para repositorios públicos.

**P: ¿Necesito instalar algo?**  
R: No, solo necesitas tener el código en GitHub.

**P: ¿Puedo compilar para Linux/Mac?**  
R: Sí, cambia `runs-on: windows-latest` a `ubuntu-latest` o `macos-latest`.

**P: ¿Se puede acelerar?**  
R: Usa caché (ya configurado) y compila solo en releases.

**P: ¿El .exe es seguro?**  
R: Sí, lo compila GitHub desde tu código fuente visible.

---

✨ **¡Listo!** Ahora tienes compilación automática configurada.
