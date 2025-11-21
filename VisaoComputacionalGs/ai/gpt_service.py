"""
EqualMind - Integração com OpenAI GPT (IA Generativa)
Análise avançada de sentimentos e geração de insights
"""
import openai
from openai import OpenAI
from config import Config
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPTService:
    """
    Serviço de IA Generativa usando ChatGPT
    Fornece análises avançadas e recomendações personalizadas
    """
    
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.GPT_MODEL
        self.temperature = Config.GPT_TEMPERATURE
        self.max_tokens = Config.GPT_MAX_TOKENS
        
        if not self.api_key:
            logger.warning("⚠️ OpenAI API Key não configurada!")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("✅ OpenAI GPT Service inicializado")
    
    def analisar_sentimento_avancado(self, texto):
        """
        Análise de sentimento avançada usando GPT
        Identifica emoções complexas e contexto
        
        Args:
            texto (str): Texto a ser analisado
            
        Returns:
            dict: Análise detalhada com emoções, intensidade e insights
        """
        if not self.client or not texto:
            return None
        
        try:
            prompt = f"""
Você é um psicólogo especializado em análise emocional corporativa. 
Analise o seguinte relato de um colaborador sobre como ele está se sentindo no trabalho:

"{texto}"

Retorne uma análise em formato JSON com:
1. sentimento_primario: (positivo/neutro/negativo)
2. emocoes_detectadas: lista de emoções específicas (ex: ansiedade, felicidade, frustração)
3. intensidade: (baixa/média/alta)
4. contexto_trabalho: breve interpretação do contexto profissional
5. sinais_alerta: lista de possíveis sinais de alerta (vazio se não houver)
6. recomendacao_imediata: uma frase curta de apoio/orientação

Seja empático e profissional. Responda APENAS com o JSON válido.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente de análise emocional especializado em saúde mental corporativa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            resultado_texto = response.choices[0].message.content.strip()
            
            # Extrair JSON (remover markdown se existir)
            if "```json" in resultado_texto:
                resultado_texto = resultado_texto.split("```json")[1].split("```")[0].strip()
            elif "```" in resultado_texto:
                resultado_texto = resultado_texto.split("```")[1].split("```")[0].strip()
            
            resultado = json.loads(resultado_texto)
            
            logger.info(f"✅ GPT: Análise concluída - {resultado.get('sentimento_primario')}")
            return resultado
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao parsear JSON do GPT: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro na análise GPT: {e}")
            return None
    
    def gerar_recomendacoes_personalizadas(self, nivel_estresse, nivel_felicidade, 
                                           nivel_ansiedade, nivel_motivacao, 
                                           comentario=""):
        """
        Gera recomendações personalizadas baseadas nos níveis emocionais
        
        Returns:
            dict: Recomendações práticas e personalizadas
        """
        if not self.client:
            return None
        
        try:
            # Determinar contexto geral
            contexto_geral = "positivo" if (nivel_felicidade >= 6 and nivel_estresse <= 5 and nivel_motivacao >= 6) else \
                           "negativo" if (nivel_estresse >= 7 or nivel_felicidade <= 3) else "neutro"
            
            # Se há comentário, considerar seu sentimento
            if comentario:
                comentario_lower = comentario.lower()
                if any(palavra in comentario_lower for palavra in ['bem', 'bom', 'ótimo', 'feliz', 'satisfeito', 'está bem']):
                    contexto_geral = "positivo"
                elif any(palavra in comentario_lower for palavra in ['mal', 'ruim', 'triste', 'estressado', 'cansado']):
                    contexto_geral = "negativo"
            
            prompt = f"""
Você é um coach de bem-estar corporativo. Um colaborador reportou:
- Nível de Estresse: {nivel_estresse}/10
- Nível de Felicidade: {nivel_felicidade}/10
- Nível de Ansiedade: {nivel_ansiedade}/10
- Nível de Motivação: {nivel_motivacao}/10
{f'- Comentário: "{comentario}"' if comentario else ''}

IMPORTANTE: Analise o contexto geral. Se o comentário for positivo (ex: "está bem", "tudo bem", "satisfeito"), 
mesmo que alguns valores numéricos sejam moderados, o contexto geral é POSITIVO e as recomendações devem ser 
encorajadoras e de manutenção, não alarmistas.

Gere recomendações práticas e aplicáveis em formato JSON:
{{
    "prioridade": "alta/media/baixa",
    "acoes_imediatas": ["ação 1", "ação 2", "ação 3"],
    "habitos_sugeridos": ["hábito 1", "hábito 2"],
    "recursos_disponiveis": ["recurso 1", "recurso 2"],
    "mensagem_motivacional": "mensagem curta e encorajadora"
}}

Seja prático, empático e focado em ações concretas. 
Se o contexto for positivo, priorize mensagens de manutenção e celebração.
Se o contexto for negativo, priorize ações de apoio e melhoria.
Responda APENAS com JSON válido.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um coach de bem-estar especializado em saúde mental no trabalho."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )
            
            resultado_texto = response.choices[0].message.content.strip()
            
            # Extrair JSON
            if "```json" in resultado_texto:
                resultado_texto = resultado_texto.split("```json")[1].split("```")[0].strip()
            elif "```" in resultado_texto:
                resultado_texto = resultado_texto.split("```")[1].split("```")[0].strip()
            
            resultado = json.loads(resultado_texto)
            logger.info("✅ GPT: Recomendações geradas com sucesso")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar recomendações: {e}")
            return None
    
    def gerar_relatorio_rh(self, dados_setores):
        """
        Gera relatório executivo inteligente para o RH
        
        Args:
            dados_setores (list): Lista de dados dos setores
            
        Returns:
            dict: Relatório com insights e recomendações estratégicas
        """
        if not self.client or not dados_setores:
            return None
        
        try:
            # Preparar resumo dos dados
            resumo = ""
            for setor in dados_setores:
                resumo += f"- {setor.get('NOME_SETOR', 'N/A')}: Estresse {setor.get('MEDIA_ESTRESSE', 0):.1f}/10, Felicidade {setor.get('MEDIA_FELICIDADE', 0):.1f}/10\n"
            
            prompt = f"""
Você é um consultor de RH especializado em análise de dados e gestão de pessoas.

Analise os seguintes dados de saúde emocional dos setores de uma empresa:

{resumo}

Gere um relatório executivo em formato JSON:
{{
    "resumo_geral": "visão geral da situação (2-3 frases)",
    "setores_criticos": ["setor 1", "setor 2"],
    "pontos_positivos": ["ponto 1", "ponto 2"],
    "riscos_identificados": ["risco 1", "risco 2"],
    "acoes_recomendadas": [
        {{"acao": "descrição", "prioridade": "alta/media/baixa", "setor": "nome ou 'geral'"}},
        ...
    ],
    "indicadores_chave": {{"tendencia": "positiva/negativa/estavel", "nivel_alerta": "verde/amarelo/vermelho"}}
}}

Seja estratégico e objetivo. Responda APENAS com JSON válido.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um consultor de RH especializado em People Analytics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            
            resultado_texto = response.choices[0].message.content.strip()
            
            # Extrair JSON
            if "```json" in resultado_texto:
                resultado_texto = resultado_texto.split("```json")[1].split("```")[0].strip()
            elif "```" in resultado_texto:
                resultado_texto = resultado_texto.split("```")[1].split("```")[0].strip()
            
            resultado = json.loads(resultado_texto)
            logger.info("✅ GPT: Relatório RH gerado com sucesso")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório RH: {e}")
            return None
    
    def chat_coach_virtual(self, mensagem_usuario, historico=[]):
        """
        Coach virtual interativo para apoio emocional
        
        Args:
            mensagem_usuario (str): Mensagem do usuário
            historico (list): Histórico da conversa
            
        Returns:
            str: Resposta do coach
        """
        if not self.client:
            return "Desculpe, o coach virtual não está disponível no momento."
        
        try:
            messages = [
                {"role": "system", "content": """Você é um coach de bem-estar empático e profissional.
Seu objetivo é apoiar colaboradores com questões emocionais e de carreira.
Seja breve (máximo 3 parágrafos), empático e prático.
Se identificar sinais graves de saúde mental, recomende buscar ajuda profissional."""}
            ]
            
            # Adicionar histórico
            for msg in historico[-5:]:  # Últimas 5 mensagens
                messages.append(msg)
            
            # Adicionar mensagem atual
            messages.append({"role": "user", "content": mensagem_usuario})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=300
            )
            
            resposta = response.choices[0].message.content.strip()
            logger.info("✅ GPT: Coach respondeu")
            return resposta
            
        except Exception as e:
            logger.error(f"❌ Erro no chat do coach: {e}")
            return "Desculpe, ocorreu um erro. Tente novamente."
    
    def verificar_disponibilidade(self):
        """Verifica se o serviço GPT está disponível"""
        return self.client is not None and bool(self.api_key)


# Instância global
gpt_service = GPTService()

