"""
Script para generar imágenes adicionales de microplásticos para pruebas.

Este script crea 3 imágenes sintéticas adicionales con diferentes
características morfológicas.
"""

import numpy as np
import cv2
from pathlib import Path
import sys

# Agregar path del proyecto
sys.path.append(str(Path(__file__).parent.parent))
from config.config import DATA_DIR


def generate_synthetic_microplastics(output_path: str, 
                                    num_particles: int = 50,
                                    image_size: tuple = (1024, 1024),
                                    particle_types: dict = None):
    """
    Genera una imagen sintética con microplásticos simulados.
    
    Args:
        output_path: Ruta donde guardar la imagen
        num_particles: Número de partículas a generar
        image_size: Tamaño de la imagen (alto, ancho)
        particle_types: Diccionario con tipos de partículas y sus proporciones
    """
    if particle_types is None:
        particle_types = {
            'small_round': 0.3,
            'medium_round': 0.3,
            'large_round': 0.2,
            'fiber': 0.2
        }
    
    # Crear imagen de fondo (gris claro)
    image = np.ones((*image_size, 3), dtype=np.uint8) * 220
    
    particles_created = 0
    max_attempts = num_particles * 3
    attempts = 0
    
    while particles_created < num_particles and attempts < max_attempts:
        attempts += 1
        
        # Seleccionar tipo de partícula según probabilidades
        particle_type = np.random.choice(
            list(particle_types.keys()),
            p=list(particle_types.values())
        )
        
        # Generar posición aleatoria
        center_x = np.random.randint(50, image_size[1] - 50)
        center_y = np.random.randint(50, image_size[0] - 50)
        
        # Generar partícula según tipo
        if particle_type == 'small_round':
            radius = np.random.randint(5, 15)
            color = np.random.randint(40, 100)
            cv2.circle(image, (center_x, center_y), radius, 
                      (color, color, color), -1)
            particles_created += 1
            
        elif particle_type == 'medium_round':
            radius = np.random.randint(15, 30)
            color = np.random.randint(40, 100)
            cv2.circle(image, (center_x, center_y), radius,
                      (color, color, color), -1)
            particles_created += 1
            
        elif particle_type == 'large_round':
            radius = np.random.randint(30, 50)
            color = np.random.randint(40, 100)
            cv2.circle(image, (center_x, center_y), radius,
                      (color, color, color), -1)
            particles_created += 1
            
        elif particle_type == 'fiber':
            length = np.random.randint(40, 120)
            width = np.random.randint(3, 8)
            angle = np.random.uniform(0, 180)
            
            angle_rad = np.radians(angle)
            end_x = int(center_x + length * np.cos(angle_rad))
            end_y = int(center_y + length * np.sin(angle_rad))
            
            color = np.random.randint(40, 100)
            cv2.line(image, (center_x, center_y), (end_x, end_y),
                    (color, color, color), width)
            particles_created += 1
    
    # Agregar ruido realista
    noise = np.random.normal(0, 10, image.shape).astype(np.int16)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Aplicar desenfoque leve para simular microscopía
    image = cv2.GaussianBlur(image, (3, 3), 0.5)
    
    # Guardar imagen
    cv2.imwrite(str(output_path), image)
    print(f"[OK] Generada: {output_path} ({particles_created} particulas)")


def main():
    """Función principal para generar conjunto de imágenes de prueba."""
    
    print("\n" + "="*60)
    print("GENERADOR DE MUESTRAS ADICIONALES DE MICROPLASTICOS")
    print("="*60)
    
    # Crear directorio si no existe
    raw_images_dir = DATA_DIR / "raw_images"
    raw_images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerando imagenes en: {raw_images_dir}")
    print("-" * 60)
    
    # Generar 3 imágenes adicionales con características diferentes
    
    # Muestra 1: Solo fibras largas (simulación de contaminación textil)
    generate_synthetic_microplastics(
        output_path=raw_images_dir / "Textil_A_fibras_largas.jpg",
        num_particles=50,
        particle_types={
            'small_round': 0.05,
            'medium_round': 0.05,
            'large_round': 0.05,
            'fiber': 0.85
        }
    )
    
    # Muestra 2: Partículas medianas uniformes
    generate_synthetic_microplastics(
        output_path=raw_images_dir / "Cosmetico_B_particulas_uniformes.jpg",
        num_particles=65,
        particle_types={
            'small_round': 0.1,
            'medium_round': 0.7,
            'large_round': 0.15,
            'fiber': 0.05
        }
    )
    
    # Muestra 3: Mezcla equilibrada (simulación de muestra real)
    generate_synthetic_microplastics(
        output_path=raw_images_dir / "Ambiental_C_muestra_real.jpg",
        num_particles=48,
        particle_types={
            'small_round': 0.35,
            'medium_round': 0.25,
            'large_round': 0.25,
            'fiber': 0.15
        }
    )
    
    print("-" * 60)
    print("[OK] Generacion completada exitosamente")
    print(f"\nLas imagenes adicionales estan listas en: {raw_images_dir}")
    print("\nAhora tienes 8 imagenes diferentes para analizar.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
