"""
Módulo de análisis estadístico de microplásticos.

Este módulo contiene funciones para analizar estadísticamente
las propiedades morfológicas de microplásticos detectados.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from scipy import stats
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.config import MORPHOLOGY_PARAMS


class StatisticalAnalyzer:
    """Clase para análisis estadístico de partículas de microplásticos."""
    
    def __init__(self):
        """Inicializa el analizador estadístico."""
        self.size_categories = MORPHOLOGY_PARAMS['size_categories']
        self.aspect_ratio_categories = MORPHOLOGY_PARAMS['aspect_ratio_categories']
    
    def particles_to_dataframe(self, particles: List[Dict], 
                              sample_id: str = None) -> pd.DataFrame:
        """
        Convierte lista de partículas a DataFrame de pandas.
        
        Args:
            particles: Lista de diccionarios con propiedades de partículas.
            sample_id: Identificador de la muestra.
            
        Returns:
            DataFrame con información de partículas.
        """
        df = pd.DataFrame(particles)
        
        if sample_id:
            df['sample_id'] = sample_id
        
        # Clasificar por tamaño
        df['size_category'] = df['equivalent_diameter_um'].apply(
            self._classify_by_size
        )
        
        # Clasificar por forma
        df['shape_category'] = df['aspect_ratio'].apply(
            self._classify_by_aspect_ratio
        )
        
        return df
    
    def _classify_by_size(self, diameter: float) -> str:
        """Clasifica una partícula por tamaño."""
        for category, (min_val, max_val) in self.size_categories.items():
            if min_val <= diameter < max_val:
                return category
        return 'indefinido'
    
    def _classify_by_aspect_ratio(self, aspect_ratio: float) -> str:
        """Clasifica una partícula por relación de aspecto."""
        for category, (min_val, max_val) in self.aspect_ratio_categories.items():
            if min_val <= aspect_ratio < max_val:
                return category
        return 'indefinido'
    
    def calculate_descriptive_stats(self, df: pd.DataFrame,
                                   column: str = 'area_um2') -> Dict:
        """
        Calcula estadísticos descriptivos para una columna.
        
        Args:
            df: DataFrame con datos de partículas.
            column: Nombre de la columna a analizar.
            
        Returns:
            Diccionario con estadísticos descriptivos.
        """
        data = df[column].dropna()
        
        stats_dict = {
            'count': len(data),
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'q25': data.quantile(0.25),
            'q75': data.quantile(0.75),
            'iqr': data.quantile(0.75) - data.quantile(0.25),
            'cv': (data.std() / data.mean() * 100) if data.mean() != 0 else 0,
        }
        
        return stats_dict
    
    def analyze_size_distribution(self, df: pd.DataFrame) -> Dict:
        """
        Analiza la distribución de tamaños de partículas.
        
        Args:
            df: DataFrame con datos de partículas.
            
        Returns:
            Diccionario con análisis de distribución de tamaños.
        """
        size_stats = {
            'area': self.calculate_descriptive_stats(df, 'area_um2'),
            'perimeter': self.calculate_descriptive_stats(df, 'perimeter_um'),
            'diameter': self.calculate_descriptive_stats(df, 'equivalent_diameter_um'),
        }
        
        # Distribución por categorías de tamaño
        size_distribution = df['size_category'].value_counts().to_dict()
        size_stats['category_distribution'] = size_distribution
        
        # Porcentajes
        total = len(df)
        size_stats['category_percentages'] = {
            cat: (count / total * 100) for cat, count in size_distribution.items()
        }
        
        return size_stats
    
    def analyze_shape_distribution(self, df: pd.DataFrame) -> Dict:
        """
        Analiza la distribución de formas de partículas.
        
        Args:
            df: DataFrame con datos de partículas.
            
        Returns:
            Diccionario con análisis de distribución de formas.
        """
        shape_stats = {
            'aspect_ratio': self.calculate_descriptive_stats(df, 'aspect_ratio'),
            'eccentricity': self.calculate_descriptive_stats(df, 'eccentricity'),
            'solidity': self.calculate_descriptive_stats(df, 'solidity'),
        }
        
        # Distribución por categorías de forma
        shape_distribution = df['shape_category'].value_counts().to_dict()
        shape_stats['category_distribution'] = shape_distribution
        
        # Porcentajes
        total = len(df)
        shape_stats['category_percentages'] = {
            cat: (count / total * 100) for cat, count in shape_distribution.items()
        }
        
        return shape_stats
    
    def compare_samples(self, dfs: Dict[str, pd.DataFrame],
                       parameter: str = 'area_um2') -> Dict:
        """
        Compara un parámetro entre múltiples muestras.
        
        Args:
            dfs: Diccionario con {sample_id: DataFrame}.
            parameter: Parámetro a comparar.
            
        Returns:
            Diccionario con resultados de comparación.
        """
        comparison = {
            'samples': {},
            'statistical_tests': {}
        }
        
        # Estadísticos para cada muestra
        for sample_id, df in dfs.items():
            comparison['samples'][sample_id] = self.calculate_descriptive_stats(
                df, parameter
            )
        
        # Test de normalidad (Shapiro-Wilk) para cada muestra
        for sample_id, df in dfs.items():
            data = df[parameter].dropna()
            if len(data) >= 3:  # Mínimo para test de Shapiro-Wilk
                statistic, p_value = stats.shapiro(data)
                comparison['statistical_tests'][f'{sample_id}_shapiro'] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'is_normal': p_value > 0.05
                }
        
        # Si hay dos muestras, realizar test t o Mann-Whitney
        if len(dfs) == 2:
            samples = list(dfs.values())
            data1 = samples[0][parameter].dropna()
            data2 = samples[1][parameter].dropna()
            
            # Test t de Student (paramétrico)
            t_stat, t_pval = stats.ttest_ind(data1, data2)
            comparison['statistical_tests']['t_test'] = {
                'statistic': t_stat,
                'p_value': t_pval,
                'significant': t_pval < 0.05
            }
            
            # Test de Mann-Whitney U (no paramétrico)
            u_stat, u_pval = stats.mannwhitneyu(data1, data2, alternative='two-sided')
            comparison['statistical_tests']['mann_whitney'] = {
                'statistic': u_stat,
                'p_value': u_pval,
                'significant': u_pval < 0.05
            }
        
        # Si hay más de dos muestras, realizar ANOVA o Kruskal-Wallis
        elif len(dfs) > 2:
            data_groups = [df[parameter].dropna() for df in dfs.values()]
            
            # ANOVA (paramétrico)
            f_stat, f_pval = stats.f_oneway(*data_groups)
            comparison['statistical_tests']['anova'] = {
                'statistic': f_stat,
                'p_value': f_pval,
                'significant': f_pval < 0.05
            }
            
            # Kruskal-Wallis (no paramétrico)
            h_stat, h_pval = stats.kruskal(*data_groups)
            comparison['statistical_tests']['kruskal_wallis'] = {
                'statistic': h_stat,
                'p_value': h_pval,
                'significant': h_pval < 0.05
            }
        
        return comparison
    
    def calculate_concentration(self, df: pd.DataFrame,
                               sample_volume_ml: float,
                               dilution_factor: float = 1.0) -> Dict:
        """
        Calcula la concentración de microplásticos en la muestra.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_volume_ml: Volumen de la muestra en mililitros.
            dilution_factor: Factor de dilución aplicado.
            
        Returns:
            Diccionario con concentraciones calculadas.
        """
        n_particles = len(df)
        
        concentration = {
            'particles_per_ml': (n_particles * dilution_factor) / sample_volume_ml,
            'total_area_um2_per_ml': (df['area_um2'].sum() * dilution_factor) / sample_volume_ml,
            'mean_area_per_ml': (df['area_um2'].mean() * dilution_factor) / sample_volume_ml,
        }
        
        return concentration
    
    def generate_summary_report(self, df: pd.DataFrame,
                               sample_id: str = None) -> str:
        """
        Genera un reporte de resumen textual.
        
        Args:
            df: DataFrame con datos de partículas.
            sample_id: Identificador de la muestra.
            
        Returns:
            Reporte de resumen como string.
        """
        report = []
        report.append("=" * 60)
        report.append(f"REPORTE DE ANÁLISIS DE MICROPLÁSTICOS")
        if sample_id:
            report.append(f"Muestra: {sample_id}")
        report.append("=" * 60)
        report.append("")
        
        # Información general
        report.append(f"Número total de partículas detectadas: {len(df)}")
        report.append("")
        
        # Análisis de tamaño
        report.append("DISTRIBUCIÓN DE TAMAÑOS:")
        report.append("-" * 40)
        size_analysis = self.analyze_size_distribution(df)
        for category, percentage in size_analysis['category_percentages'].items():
            count = size_analysis['category_distribution'][category]
            report.append(f"  {category.capitalize()}: {count} partículas ({percentage:.1f}%)")
        report.append("")
        
        # Estadísticos de área
        area_stats = size_analysis['area']
        report.append("ESTADÍSTICOS DE ÁREA (μm²):")
        report.append("-" * 40)
        report.append(f"  Media: {area_stats['mean']:.2f}")
        report.append(f"  Mediana: {area_stats['median']:.2f}")
        report.append(f"  Desviación estándar: {area_stats['std']:.2f}")
        report.append(f"  Mínimo: {area_stats['min']:.2f}")
        report.append(f"  Máximo: {area_stats['max']:.2f}")
        report.append("")
        
        # Análisis de forma
        report.append("DISTRIBUCIÓN DE FORMAS:")
        report.append("-" * 40)
        shape_analysis = self.analyze_shape_distribution(df)
        for category, percentage in shape_analysis['category_percentages'].items():
            count = shape_analysis['category_distribution'][category]
            report.append(f"  {category.capitalize()}: {count} partículas ({percentage:.1f}%)")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
