"""
Módulo de visualización de datos para análisis de microplásticos.

Este módulo contiene funciones para generar gráficos y visualizaciones
de los resultados del análisis de microplásticos.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.config import PLOT_PARAMS, SAMPLES_INFO


class DataVisualizer:
    """Clase para visualización de datos de microplásticos."""
    
    def __init__(self):
        """Inicializa el visualizador con estilos predeterminados."""
        # Configurar estilo de matplotlib
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette(PLOT_PARAMS['color_palette'])
        plt.rcParams['figure.figsize'] = PLOT_PARAMS['figure_size']
        plt.rcParams['figure.dpi'] = PLOT_PARAMS['dpi']
        plt.rcParams['font.size'] = PLOT_PARAMS['font_size']
    
    def plot_size_distribution(self, df: pd.DataFrame,
                              sample_id: str = None,
                              save_path: str = None) -> plt.Figure:
        """
        Genera histograma de distribución de tamaños.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_id: Identificador de la muestra.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Histograma de área
        axes[0, 0].hist(df['area_um2'], bins=30, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Área (μm²)')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].set_title('Distribución de Áreas')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Histograma de diámetro equivalente
        axes[0, 1].hist(df['equivalent_diameter_um'], bins=30, 
                       edgecolor='black', alpha=0.7, color='orange')
        axes[0, 1].set_xlabel('Diámetro Equivalente (μm)')
        axes[0, 1].set_ylabel('Frecuencia')
        axes[0, 1].set_title('Distribución de Diámetros')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico de caja de áreas
        axes[1, 0].boxplot(df['area_um2'], vert=True)
        axes[1, 0].set_ylabel('Área (μm²)')
        axes[1, 0].set_title('Box Plot de Áreas')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Distribución por categorías de tamaño
        size_counts = df['size_category'].value_counts()
        axes[1, 1].bar(size_counts.index, size_counts.values, 
                      edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('Categoría de Tamaño')
        axes[1, 1].set_ylabel('Número de Partículas')
        axes[1, 1].set_title('Distribución por Categorías de Tamaño')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # Título general
        if sample_id:
            fig.suptitle(f'Análisis de Distribución de Tamaños - {sample_id}',
                        fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
    
    def plot_shape_distribution(self, df: pd.DataFrame,
                               sample_id: str = None,
                               save_path: str = None) -> plt.Figure:
        """
        Genera gráficos de distribución de formas.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_id: Identificador de la muestra.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Histograma de relación de aspecto
        axes[0, 0].hist(df['aspect_ratio'], bins=30, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Relación de Aspecto')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].set_title('Distribución de Relación de Aspecto')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Histograma de excentricidad
        axes[0, 1].hist(df['eccentricity'], bins=30, 
                       edgecolor='black', alpha=0.7, color='green')
        axes[0, 1].set_xlabel('Excentricidad')
        axes[0, 1].set_ylabel('Frecuencia')
        axes[0, 1].set_title('Distribución de Excentricidad')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Distribución por categorías de forma
        shape_counts = df['shape_category'].value_counts()
        axes[1, 0].bar(shape_counts.index, shape_counts.values,
                      edgecolor='black', alpha=0.7, color='coral')
        axes[1, 0].set_xlabel('Categoría de Forma')
        axes[1, 0].set_ylabel('Número de Partículas')
        axes[1, 0].set_title('Distribución por Categorías de Forma')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico de dispersión: área vs relación de aspecto
        scatter = axes[1, 1].scatter(df['area_um2'], df['aspect_ratio'],
                                     alpha=0.6, edgecolors='black', linewidth=0.5)
        axes[1, 1].set_xlabel('Área (μm²)')
        axes[1, 1].set_ylabel('Relación de Aspecto')
        axes[1, 1].set_title('Área vs Relación de Aspecto')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Título general
        if sample_id:
            fig.suptitle(f'Análisis de Distribución de Formas - {sample_id}',
                        fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
    
    def plot_comparative_analysis(self, dfs: Dict[str, pd.DataFrame],
                                 parameter: str = 'area_um2',
                                 save_path: str = None) -> plt.Figure:
        """
        Genera gráficos comparativos entre muestras.
        
        Args:
            dfs: Diccionario con {sample_id: DataFrame}.
            parameter: Parámetro a comparar.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Preparar datos para visualización
        sample_ids = list(dfs.keys())
        colors = [SAMPLES_INFO.get(sid, {}).get('color', f'C{i}') 
                 for i, sid in enumerate(sample_ids)]
        
        # Box plot comparativo
        data_for_boxplot = [dfs[sid][parameter].dropna() for sid in sample_ids]
        bp = axes[0, 0].boxplot(data_for_boxplot, labels=sample_ids,
                               patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        axes[0, 0].set_ylabel(self._get_parameter_label(parameter))
        axes[0, 0].set_title(f'Comparación de {self._get_parameter_label(parameter)}')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Histogramas superpuestos
        for sid, color in zip(sample_ids, colors):
            axes[0, 1].hist(dfs[sid][parameter], bins=20, alpha=0.5,
                          label=sid, color=color, edgecolor='black')
        axes[0, 1].set_xlabel(self._get_parameter_label(parameter))
        axes[0, 1].set_ylabel('Frecuencia')
        axes[0, 1].set_title('Distribuciones Superpuestas')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico de violín
        data_for_violin = pd.concat([
            pd.DataFrame({parameter: dfs[sid][parameter], 'sample': sid})
            for sid in sample_ids
        ])
        sns.violinplot(data=data_for_violin, x='sample', y=parameter,
                      ax=axes[1, 0], palette=colors)
        axes[1, 0].set_xlabel('Muestra')
        axes[1, 0].set_ylabel(self._get_parameter_label(parameter))
        axes[1, 0].set_title('Gráfico de Violín')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico de barras con estadísticos
        means = [dfs[sid][parameter].mean() for sid in sample_ids]
        stds = [dfs[sid][parameter].std() for sid in sample_ids]
        x_pos = np.arange(len(sample_ids))
        axes[1, 1].bar(x_pos, means, yerr=stds, capsize=5,
                      color=colors, edgecolor='black', alpha=0.7)
        axes[1, 1].set_xticks(x_pos)
        axes[1, 1].set_xticklabels(sample_ids, rotation=45)
        axes[1, 1].set_ylabel(self._get_parameter_label(parameter))
        axes[1, 1].set_title('Media ± Desviación Estándar')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        # Título general
        fig.suptitle(f'Análisis Comparativo entre Muestras',
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
    
    def plot_correlation_matrix(self, df: pd.DataFrame,
                               save_path: str = None) -> plt.Figure:
        """
        Genera matriz de correlación de parámetros morfológicos.
        
        Args:
            df: DataFrame con datos de partículas.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        # Seleccionar columnas numéricas relevantes
        numeric_cols = ['area_um2', 'perimeter_um', 'equivalent_diameter_um',
                       'aspect_ratio', 'eccentricity', 'solidity',
                       'major_axis', 'minor_axis']
        
        # Filtrar columnas que existan en el DataFrame
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        # Calcular matriz de correlación
        corr_matrix = df[available_cols].corr()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax)
        
        ax.set_title('Matriz de Correlación de Parámetros Morfológicos',
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
    
    def plot_size_frequency_curve(self, df: pd.DataFrame,
                                 sample_id: str = None,
                                 save_path: str = None) -> plt.Figure:
        """
        Genera curva de frecuencia acumulada de tamaños.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_id: Identificador de la muestra.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Ordenar datos
        sorted_diameters = np.sort(df['equivalent_diameter_um'])
        cumulative_freq = np.arange(1, len(sorted_diameters) + 1) / len(sorted_diameters) * 100
        
        # Frecuencia acumulada
        axes[0].plot(sorted_diameters, cumulative_freq, linewidth=2)
        axes[0].set_xlabel('Diámetro Equivalente (μm)')
        axes[0].set_ylabel('Frecuencia Acumulada (%)')
        axes[0].set_title('Curva de Frecuencia Acumulada')
        axes[0].grid(True, alpha=0.3)
        
        # Percentiles
        percentiles = [10, 25, 50, 75, 90]
        percentile_values = np.percentile(sorted_diameters, percentiles)
        
        axes[1].bar(range(len(percentiles)), percentile_values,
                   tick_label=[f'P{p}' for p in percentiles],
                   edgecolor='black', alpha=0.7)
        axes[1].set_ylabel('Diámetro Equivalente (μm)')
        axes[1].set_title('Percentiles de Distribución de Tamaños')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # Agregar valores en las barras
        for i, v in enumerate(percentile_values):
            axes[1].text(i, v, f'{v:.1f}', ha='center', va='bottom')
        
        # Título general
        if sample_id:
            fig.suptitle(f'Análisis de Frecuencia de Tamaños - {sample_id}',
                        fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
    
    def _get_parameter_label(self, parameter: str) -> str:
        """Convierte nombre de parámetro a etiqueta legible."""
        labels = {
            'area_um2': 'Área (μm²)',
            'perimeter_um': 'Perímetro (μm)',
            'equivalent_diameter_um': 'Diámetro Equivalente (μm)',
            'aspect_ratio': 'Relación de Aspecto',
            'eccentricity': 'Excentricidad',
            'solidity': 'Solidez',
            'major_axis': 'Eje Mayor (μm)',
            'minor_axis': 'Eje Menor (μm)',
        }
        return labels.get(parameter, parameter)
    
    def create_summary_dashboard(self, df: pd.DataFrame,
                                sample_id: str = None,
                                save_path: str = None) -> plt.Figure:
        """
        Crea un dashboard resumen con múltiples gráficos.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_id: Identificador de la muestra.
            save_path: Ruta para guardar la figura.
            
        Returns:
            Figura de matplotlib.
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Histograma de áreas
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(df['area_um2'], bins=30, edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Área (μm²)')
        ax1.set_ylabel('Frecuencia')
        ax1.set_title('Distribución de Áreas')
        ax1.grid(True, alpha=0.3)
        
        # 2. Distribución por categorías de tamaño
        ax2 = fig.add_subplot(gs[0, 1])
        size_counts = df['size_category'].value_counts()
        ax2.pie(size_counts.values, labels=size_counts.index, autopct='%1.1f%%',
               startangle=90)
        ax2.set_title('Categorías de Tamaño')
        
        # 3. Distribución por categorías de forma
        ax3 = fig.add_subplot(gs[0, 2])
        shape_counts = df['shape_category'].value_counts()
        ax3.pie(shape_counts.values, labels=shape_counts.index, autopct='%1.1f%%',
               startangle=90)
        ax3.set_title('Categorías de Forma')
        
        # 4. Box plot de áreas
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.boxplot(df['area_um2'], vert=True)
        ax4.set_ylabel('Área (μm²)')
        ax4.set_title('Box Plot de Áreas')
        ax4.grid(True, alpha=0.3)
        
        # 5. Relación de aspecto
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.hist(df['aspect_ratio'], bins=30, edgecolor='black', alpha=0.7, color='orange')
        ax5.set_xlabel('Relación de Aspecto')
        ax5.set_ylabel('Frecuencia')
        ax5.set_title('Distribución de Relación de Aspecto')
        ax5.grid(True, alpha=0.3)
        
        # 6. Área vs Relación de Aspecto
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.scatter(df['area_um2'], df['aspect_ratio'], alpha=0.6,
                   edgecolors='black', linewidth=0.5)
        ax6.set_xlabel('Área (μm²)')
        ax6.set_ylabel('Relación de Aspecto')
        ax6.set_title('Área vs Relación de Aspecto')
        ax6.grid(True, alpha=0.3)
        
        # 7. Estadísticos textuales
        ax7 = fig.add_subplot(gs[2, :])
        ax7.axis('off')
        
        stats_text = f"""
        ESTADÍSTICOS PRINCIPALES
        ─────────────────────────────────────────────────────────────
        Número total de partículas: {len(df)}
        
        Área (μm²):
            Media: {df['area_um2'].mean():.2f} ± {df['area_um2'].std():.2f}
            Mediana: {df['area_um2'].median():.2f}
            Rango: [{df['area_um2'].min():.2f}, {df['area_um2'].max():.2f}]
        
        Diámetro Equivalente (μm):
            Media: {df['equivalent_diameter_um'].mean():.2f} ± {df['equivalent_diameter_um'].std():.2f}
            Mediana: {df['equivalent_diameter_um'].median():.2f}
        
        Relación de Aspecto:
            Media: {df['aspect_ratio'].mean():.2f} ± {df['aspect_ratio'].std():.2f}
            Mediana: {df['aspect_ratio'].median():.2f}
        """
        
        ax7.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        # Título general
        if sample_id:
            fig.suptitle(f'Dashboard de Análisis de Microplásticos - {sample_id}',
                        fontsize=18, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=PLOT_PARAMS['dpi'])
        
        return fig
