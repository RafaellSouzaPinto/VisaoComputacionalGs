"""
EqualMind - Configurações da Aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações gerais da aplicação"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # Oracle Database FIAP
    ORACLE_USER = os.getenv('ORACLE_USER', '')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', '')
    ORACLE_DSN = os.getenv('ORACLE_DSN', 'oracle.fiap.com.br:1521/orcl')
    
    # Configurações de Análise
    DIAS_ANALISE_PADRAO = 30
    LIMITE_ESTRESSE_ALTO = 7
    LIMITE_FELICIDADE_BAIXA = 3
    
    # Deep Learning
    MODELO_SENTIMENTO = 'neuralmind/bert-base-portuguese-cased'
    CONFIANCA_MINIMA = 0.6
    
    # OpenAI / ChatGPT
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GPT_MODEL = 'gpt-4o-mini'  # Modelo mais econômico e rápido
    GPT_TEMPERATURE = 0.7
    GPT_MAX_TOKENS = 500

