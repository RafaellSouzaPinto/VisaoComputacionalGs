"""
EqualMind - Gerador de Mapas de Calor
Cria visualizações avançadas usando Deep Learning patterns
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do matplotlib para não usar interface gráfica
plt.switch_backend('Agg')


class HeatmapGenerator:
    """Gerador de mapas de calor e visualizações"""
    
    def __init__(self):
        # Paletas de cores personalizadas
        self.paleta_estresse = sns.color_palette("YlOrRd", as_cmap=True)
        self.paleta_felicidade = sns.color_palette("RdYlGn", as_cmap=True)
        self.paleta_geral = sns.color_palette("coolwarm", as_cmap=True)
        
        # Configurar estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def gerar_mapa_calor_setores(self, dados, metrica='estresse'):
        """
        Gera mapa de calor por setor
        
        Args:
            dados (list): Lista de dicionários com dados dos setores
            metrica (str): 'estresse', 'felicidade', 'ansiedade', 'motivacao'
            
        Returns:
            str: Imagem em base64
        """
        if not dados:
            logger.warning("⚠️ Sem dados para gerar mapa de calor")
            return None
        
        try:
            # Preparar dados
            df = pd.DataFrame(dados)
            setores = df['SETOR_NOME'].tolist()  # Corrigido: SETOR_NOME ao invés de NOME_SETOR
            
            # Mapear métricas
            metricas_map = {
                'estresse': 'MEDIA_ESTRESSE',
                'felicidade': 'MEDIA_FELICIDADE',
                'ansiedade': 'MEDIA_ANSIEDADE',
                'motivacao': 'MEDIA_MOTIVACAO'
            }
            
            col_metrica = metricas_map.get(metrica, 'MEDIA_ESTRESSE')
            valores = df[col_metrica].tolist()
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(14, max(len(setores) * 0.5, 6)))
            
            # Criar matriz para heatmap
            matriz = np.array(valores).reshape(-1, 1)
            
            # Escolher paleta
            if metrica == 'estresse' or metrica == 'ansiedade':
                cmap = self.paleta_estresse
                vmin, vmax = 1, 10
            elif metrica == 'felicidade' or metrica == 'motivacao':
                cmap = self.paleta_felicidade.reversed()
                vmin, vmax = 1, 10
            else:
                cmap = self.paleta_geral
                vmin, vmax = 1, 10
            
            # Criar heatmap
            sns.heatmap(
                matriz,
                annot=True,
                fmt='.1f',
                cmap=cmap,
                cbar_kws={'label': f'Nível de {metrica.capitalize()} (1-10)'},
                yticklabels=setores,
                xticklabels=[metrica.capitalize()],
                vmin=vmin,
                vmax=vmax,
                linewidths=2,
                linecolor='white',
                ax=ax
            )
            
            # Adicionar título
            ax.set_title(
                f'Mapa de Calor - {metrica.capitalize()} por Setor',
                fontsize=16,
                fontweight='bold',
                pad=20
            )
            
            # Adicionar informações extras
            total_registros = df['TOTAL_REGISTROS'].sum()
            ax.text(
                1.15, 0.5,
                f'Total de registros: {int(total_registros)}\n'
                f'Setores analisados: {len(setores)}',
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
            
            plt.tight_layout()
            
            # Converter para base64
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar mapa de calor: {e}")
            return None
    
    def gerar_comparativo_metricas(self, dados):
        """
        Gera visualização comparativa de todas as métricas
        
        Args:
            dados (list): Lista de dicionários com dados dos setores
            
        Returns:
            str: Imagem em base64
        """
        if not dados:
            return None
        
        try:
            df = pd.DataFrame(dados)
            setores = df['SETOR_NOME'].tolist()  # Corrigido: SETOR_NOME ao invés de NOME_SETOR
            
            # Preparar matriz com todas as métricas
            metricas = ['MEDIA_ESTRESSE', 'MEDIA_FELICIDADE', 'MEDIA_ANSIEDADE', 'MEDIA_MOTIVACAO']
            labels_metricas = ['Estresse', 'Felicidade', 'Ansiedade', 'Motivação']
            
            matriz = df[metricas].values
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(14, max(len(setores) * 0.6, 8)))
            
            # Criar heatmap
            sns.heatmap(
                matriz,
                annot=True,
                fmt='.1f',
                cmap=self.paleta_geral,
                cbar_kws={'label': 'Intensidade (1-10)'},
                yticklabels=setores,
                xticklabels=labels_metricas,
                vmin=1,
                vmax=10,
                linewidths=1.5,
                linecolor='gray',
                ax=ax
            )
            
            ax.set_title(
                'Comparativo de Métricas Emocionais por Setor',
                fontsize=16,
                fontweight='bold',
                pad=20
            )
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar comparativo: {e}")
            return None
    
    def gerar_grafico_barras_comparativo(self, dados):
        """
        Gera gráfico de barras comparativo
        
        Args:
            dados (list): Lista de dicionários com dados dos setores
            
        Returns:
            str: Imagem em base64
        """
        if not dados:
            return None
        
        try:
            df = pd.DataFrame(dados)
            
            # Preparar dados
            setores = df['SETOR_NOME'].tolist()  # Corrigido: SETOR_NOME ao invés de NOME_SETOR
            estresse = df['MEDIA_ESTRESSE'].tolist()
            felicidade = df['MEDIA_FELICIDADE'].tolist()
            
            # Criar figura
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Gráfico de Estresse
            cores_estresse = ['#d62728' if x >= 7 else '#ff7f0e' if x >= 5 else '#2ca02c' 
                             for x in estresse]
            ax1.barh(setores, estresse, color=cores_estresse, edgecolor='black', linewidth=1.5)
            ax1.set_xlabel('Nível Médio de Estresse', fontsize=12, fontweight='bold')
            ax1.set_title('Estresse por Setor', fontsize=14, fontweight='bold')
            ax1.set_xlim(0, 10)
            ax1.axvline(x=7, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Nível Crítico')
            ax1.legend()
            ax1.grid(axis='x', alpha=0.3)
            
            # Adicionar valores nas barras
            for i, v in enumerate(estresse):
                ax1.text(v + 0.2, i, f'{v:.1f}', va='center', fontweight='bold')
            
            # Gráfico de Felicidade
            cores_felicidade = ['#2ca02c' if x >= 7 else '#ff7f0e' if x >= 5 else '#d62728' 
                               for x in felicidade]
            ax2.barh(setores, felicidade, color=cores_felicidade, edgecolor='black', linewidth=1.5)
            ax2.set_xlabel('Nível Médio de Felicidade', fontsize=12, fontweight='bold')
            ax2.set_title('Felicidade por Setor', fontsize=14, fontweight='bold')
            ax2.set_xlim(0, 10)
            ax2.axvline(x=3, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Nível Crítico')
            ax2.legend()
            ax2.grid(axis='x', alpha=0.3)
            
            # Adicionar valores nas barras
            for i, v in enumerate(felicidade):
                ax2.text(v + 0.2, i, f'{v:.1f}', va='center', fontweight='bold')
            
            plt.suptitle('Análise Emocional Corporativa - EqualMind', 
                        fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar gráfico de barras: {e}")
            return None
    
    def gerar_dashboard_completo(self, dados):
        """
        Gera dashboard completo com múltiplas visualizações
        
        Args:
            dados (list): Lista de dicionários com dados dos setores
            
        Returns:
            dict: Múltiplas imagens em base64
        """
        return {
            'mapa_estresse': self.gerar_mapa_calor_setores(dados, 'estresse'),
            'mapa_felicidade': self.gerar_mapa_calor_setores(dados, 'felicidade'),
            'comparativo': self.gerar_comparativo_metricas(dados),
            'barras': self.gerar_grafico_barras_comparativo(dados)
        }
    
    def _fig_to_base64(self, fig):
        """Converte figura matplotlib para base64"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"


# Instância global
heatmap_gen = HeatmapGenerator()

