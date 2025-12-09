"""
Script para parchear labelImg y hacerlo compatible con PyQt5 5.15.11+
"""
import sys
from pathlib import Path

# Encontrar la ubicación de labelImg
try:
    import labelImg
    labelimg_dir = Path(labelImg.__file__).parent
    canvas_file = labelimg_dir / "canvas.py"
    
    print(f"📁 labelImg encontrado en: {labelimg_dir}")
    print(f"📄 Parcheando: {canvas_file}")
    
    if not canvas_file.exists():
        print("❌ No se encontró canvas.py")
        sys.exit(1)
    
    # Leer el archivo
    with open(canvas_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Aplicar parche: convertir floats a ints en drawLine
    original = "p.drawLine(self.prev_point.x(), self.prev_point.y(), point.x(), point.y())"
    patched = "p.drawLine(int(self.prev_point.x()), int(self.prev_point.y()), int(point.x()), int(point.y()))"
    
    if original in content:
        content = content.replace(original, patched)
        print("✅ Parche aplicado: convertir floats a ints en drawLine")
        
        # Guardar
        with open(canvas_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo parcheado correctamente")
        print("\n🎉 labelImg ahora debería funcionar correctamente")
    else:
        print("⚠️  El código ya está parcheado o tiene una versión diferente")
    
except ImportError:
    print("❌ labelImg no está instalado")
    print("Ejecuta: pip install labelImg PyQt5")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
