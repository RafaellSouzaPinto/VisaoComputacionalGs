"""
Work Well - Backend Flask
Sistema de Análise Emocional Corporativa com Deep Learning
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from config import Config
from database.db_connection import db
from ai.sentiment_analyzer import analyzer
from ai.heatmap_generator import heatmap_gen
from ai.gpt_service import gpt_service
import logging
import traceback

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Conectar ao banco de dados ao iniciar
try:
    db.connect()
    logger.info("🚀 Work Well iniciado com sucesso!")
except Exception as e:
    logger.error(f"❌ Erro ao conectar ao banco: {e}")


# ==================== ROTAS DA API ====================

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica saúde da aplicação"""
    return jsonify({
        'status': 'online',
        'database': 'connected' if db.connection else 'disconnected',
        'ai_model': 'loaded' if analyzer.modelo_carregado else 'error',
        'gpt_service': 'available' if gpt_service.verificar_disponibilidade() else 'unavailable'
    })


@app.route('/api/setores/<int:empresa_id>', methods=['GET'])
def listar_setores(empresa_id):
    """Lista todos os setores de uma empresa"""
    try:
        setores = db.obter_setores(empresa_id)
        return jsonify({
            'success': True,
            'setores': setores
        })
    except Exception as e:
        logger.error(f"Erro ao listar setores: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/registro-emocional', methods=['POST'])
def criar_registro_emocional():
    """
    Cria um novo registro emocional
    
    Body JSON:
    {
        "colaborador_id": 1,
        "setor_id": 1,
        "nivel_estresse": 5,
        "nivel_felicidade": 7,
        "nivel_ansiedade": 4,
        "nivel_motivacao": 8,
        "comentario": "Me sinto bem hoje",
        "anonimo": "N"
    }
    """
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['colaborador_id', 'setor_id', 'nivel_estresse', 'nivel_felicidade']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }), 400
        
        # Limpar e validar comentário
        comentario = data.get('comentario', '').strip() if data.get('comentario') else ''
        # Limitar tamanho do comentário (VARCHAR2(1000) no banco)
        if len(comentario) > 1000:
            comentario = comentario[:1000]
        
        # Inserir no banco
        registro_id = db.insert_registro_emocional(
            colaborador_id=data['colaborador_id'],
            setor_id=data['setor_id'],
            estresse=data['nivel_estresse'],
            felicidade=data['nivel_felicidade'],
            ansiedade=data.get('nivel_ansiedade', 5),
            motivacao=data.get('nivel_motivacao', 5),
            comentario=comentario,
            anonimo=data.get('anonimo', 'N')
        )
        
        # Análise de sentimento (se houver comentário)
        analise_sentimento = None
        if comentario:
            try:
                resultado_sentimento = analyzer.analisar_texto(comentario)
                if resultado_sentimento and resultado_sentimento.get('sentimento') != 'erro':
                    try:
                        db.atualizar_sentimento(
                            registro_id,
                            resultado_sentimento['sentimento'],
                            resultado_sentimento['score']
                        )
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao atualizar sentimento no banco (continuando): {e}")
                analise_sentimento = resultado_sentimento
            except Exception as e:
                logger.warning(f"⚠️ Erro na análise de sentimento (continuando): {e}")
                # Continua mesmo se a análise falhar
        
        # Análise numérica (considerando o sentimento do comentário se disponível)
        analise_numerica = analyzer.analisar_emocoes_numerico(
            data['nivel_estresse'],
            data['nivel_felicidade'],
            data.get('nivel_ansiedade', 5),
            data.get('nivel_motivacao', 5),
            comentario_sentimento=analise_sentimento  # Passar análise de sentimento para ajustar índice
        )
        
        logger.info(f"✅ Registro {registro_id} criado com sucesso")
        
        return jsonify({
            'success': True,
            'registro_id': registro_id,
            'analise_sentimento': analise_sentimento,
            'analise_numerica': analise_numerica,
            'mensagem': 'Registro criado com sucesso!'
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar registro: {e}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/mapa-calor/<int:empresa_id>', methods=['GET'])
def gerar_mapa_calor(empresa_id):
    """
    Gera mapa de calor dos setores
    
    Query params:
    - dias: número de dias para análise (default: 30)
    - metrica: estresse|felicidade|ansiedade|motivacao (default: estresse)
    """
    try:
        dias = request.args.get('dias', 30, type=int)
        metrica = request.args.get('metrica', 'estresse')
        
        # Obter dados do banco
        dados = db.obter_dados_mapa_calor(empresa_id, dias)
        
        if not dados:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado encontrado para gerar mapa de calor'
            }), 404
        
        # Gerar mapa de calor
        imagem_base64 = heatmap_gen.gerar_mapa_calor_setores(dados, metrica)
        
        if not imagem_base64:
            return jsonify({
                'success': False,
                'error': 'Erro ao gerar imagem do mapa de calor'
            }), 500
        
        return jsonify({
            'success': True,
            'mapa_base64': imagem_base64,
            'total_setores': len(dados),
            'periodo_dias': dias
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar mapa de calor: {e}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/dashboard/<int:empresa_id>', methods=['GET'])
def obter_dashboard(empresa_id):
    """Retorna dados completos do dashboard"""
    try:
        dias = request.args.get('dias', 30, type=int)
        
        # Obter dados
        dados_setores = db.obter_dados_mapa_calor(empresa_id, dias)
        dashboard_rh = db.obter_dashboard_rh(empresa_id)
        
        # Gerar visualizações
        visualizacoes = heatmap_gen.gerar_dashboard_completo(dados_setores)
        
        return jsonify({
            'success': True,
            'dados_setores': dados_setores,
            'dashboard_rh': dashboard_rh,
            'visualizacoes': visualizacoes,
            'periodo_dias': dias
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter dashboard: {e}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analisar-sentimento', methods=['POST'])
def analisar_sentimento():
    """Analisa sentimento de um texto (com GPT se disponível)"""
    try:
        data = request.get_json()
        texto = data.get('texto', '')
        usar_gpt = data.get('usar_gpt', True)
        
        if not texto:
            return jsonify({
                'success': False,
                'error': 'Texto não fornecido'
            }), 400
        
        resultado = analyzer.analisar_texto(texto, usar_gpt=usar_gpt)
        
        return jsonify({
            'success': True,
            'resultado': resultado
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao analisar sentimento: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recomendacoes-ia', methods=['POST'])
def gerar_recomendacoes_ia():
    """
    Gera recomendações personalizadas com IA Generativa (GPT)
    
    Body JSON:
    {
        "nivel_estresse": 7,
        "nivel_felicidade": 5,
        "nivel_ansiedade": 6,
        "nivel_motivacao": 4,
        "comentario": "opcional"
    }
    """
    try:
        if not gpt_service.verificar_disponibilidade():
            return jsonify({
                'success': False,
                'error': 'Serviço de IA Generativa não está disponível'
            }), 503
        
        data = request.get_json()
        
        recomendacoes = gpt_service.gerar_recomendacoes_personalizadas(
            nivel_estresse=data.get('nivel_estresse', 5),
            nivel_felicidade=data.get('nivel_felicidade', 5),
            nivel_ansiedade=data.get('nivel_ansiedade', 5),
            nivel_motivacao=data.get('nivel_motivacao', 5),
            comentario=data.get('comentario', '')
        )
        
        if not recomendacoes:
            return jsonify({
                'success': False,
                'error': 'Erro ao gerar recomendações'
            }), 500
        
        return jsonify({
            'success': True,
            'recomendacoes': recomendacoes
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar recomendações IA: {e}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/relatorio-ia/<int:empresa_id>', methods=['GET'])
def gerar_relatorio_ia(empresa_id):
    """Gera relatório executivo inteligente com IA para o RH"""
    try:
        if not gpt_service.verificar_disponibilidade():
            return jsonify({
                'success': False,
                'error': 'Serviço de IA Generativa não está disponível'
            }), 503
        
        dias = request.args.get('dias', 30, type=int)
        
        # Obter dados dos setores
        dados_setores = db.obter_dados_mapa_calor(empresa_id, dias)
        
        if not dados_setores:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado disponível para análise'
            }), 404
        
        # Gerar relatório com IA
        relatorio = gpt_service.gerar_relatorio_rh(dados_setores)
        
        if not relatorio:
            return jsonify({
                'success': False,
                'error': 'Erro ao gerar relatório'
            }), 500
        
        return jsonify({
            'success': True,
            'relatorio': relatorio,
            'dados_base': dados_setores,
            'periodo_dias': dias
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar relatório IA: {e}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/coach-virtual', methods=['POST'])
def chat_coach_virtual():
    """
    Coach virtual interativo com GPT
    
    Body JSON:
    {
        "mensagem": "Como lidar com estresse?",
        "historico": [...]  # opcional
    }
    """
    try:
        if not gpt_service.verificar_disponibilidade():
            return jsonify({
                'success': False,
                'error': 'Coach virtual não está disponível no momento'
            }), 503
        
        data = request.get_json()
        mensagem = data.get('mensagem', '')
        historico = data.get('historico', [])
        
        if not mensagem:
            return jsonify({
                'success': False,
                'error': 'Mensagem não fornecida'
            }), 400
        
        resposta = gpt_service.chat_coach_virtual(mensagem, historico)
        
        return jsonify({
            'success': True,
            'resposta': resposta
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no coach virtual: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/estatisticas/<int:empresa_id>', methods=['GET'])
def obter_estatisticas(empresa_id):
    """Retorna estatísticas gerais da empresa"""
    try:
        # Usar método do db_connection.py
        resultado = db.obter_estatisticas(empresa_id, 30)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'estatisticas': {
                'total_colaboradores': resultado.get('TOTAL_COLABORADORES', 0),
                'total_registros': resultado.get('TOTAL_REGISTROS', 0),
                'media_estresse': float(resultado.get('MEDIA_ESTRESSE', 0) or 0),
                'media_felicidade': float(resultado.get('MEDIA_FELICIDADE', 0) or 0),
                'media_ansiedade': float(resultado.get('MEDIA_ANSIEDADE', 0) or 0),
                'media_motivacao': float(resultado.get('MEDIA_MOTIVACAO', 0) or 0)
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500


# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    try:
        logger.info("🚀 Iniciando servidor Flask...")
        app.run(
            host='0.0.0.0',
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except KeyboardInterrupt:
        logger.info("⏹️ Servidor interrompido pelo usuário")
    finally:
        db.disconnect()
        logger.info("👋 Work Well encerrado")

