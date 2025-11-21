"""
EqualMind - Análise de Sentimento com Deep Learning
Utiliza modelos transformer para português (BERT) + OpenAI GPT
"""
import logging
from textblob import TextBlob
import nltk
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification, pipeline
from config import Config
from ai.gpt_service import gpt_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download de recursos necessários
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass


class SentimentAnalyzer:
    """
    Analisador de Sentimento usando Deep Learning
    Utiliza modelo BERT pré-treinado para português (neuralmind/bert-base-portuguese-cased)
    Processa texto em português e retorna sentimento + score
    """
    
    def __init__(self):
        self.modelo_carregado = False
        self.modelo_bert = None
        self.tokenizer = None
        self.sentiment_pipeline = None
        self.use_embeddings = False  # Flag para usar embeddings se modelo não for fine-tuned
        self.model_name = Config.MODELO_SENTIMENTO
        self._carregar_modelo()
    
    def _carregar_modelo(self):
        """
        Carrega o modelo de Deep Learning (BERT) para análise de sentimento
        Usa modelo pré-treinado neuralmind/bert-base-portuguese-cased
        """
        try:
            logger.info(f"🔄 Carregando modelo de Deep Learning: {self.model_name}")
            
            # Tentar carregar modelo fine-tuned para sentimento primeiro
            # Se não encontrar, usar modelo base com embeddings
            try:
                # Tentar pipeline de sentiment-analysis (requer modelo fine-tuned)
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=self.model_name,
                    tokenizer=self.model_name,
                    device=0 if torch.cuda.is_available() else -1,
                    return_all_scores=True
                )
                self.modelo_carregado = True
                logger.info("✅ Modelo BERT carregado com sucesso (pipeline sentiment-analysis)")
                
            except Exception as e:
                logger.info(f"ℹ️ Pipeline de sentiment não disponível, tentando modelo base: {e}")
                
                # Tentar carregar modelo fine-tuned para classificação
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                    self.model_bert = AutoModelForSequenceClassification.from_pretrained(
                        self.model_name,
                        device_map="auto" if torch.cuda.is_available() else None
                    )
                    self.model_bert.eval()
                    self.modelo_carregado = True
                    logger.info("✅ Modelo BERT carregado (SequenceClassification)")
                    
                except Exception as e2:
                    logger.info(f"ℹ️ Modelo de classificação não disponível, usando embeddings: {e2}")
                    
                    # Fallback: usar modelo base BERT com embeddings
                    try:
                        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                        self.model_bert = AutoModel.from_pretrained(
                            self.model_name,
                            device_map="auto" if torch.cuda.is_available() else None
                        )
                        self.model_bert.eval()
                        self.use_embeddings = True
                        self.modelo_carregado = True
                        logger.info("✅ Modelo BERT base carregado (usando embeddings para análise)")
                        
                    except Exception as e3:
                        logger.error(f"❌ Erro ao carregar modelo BERT: {e3}")
                        logger.warning("⚠️ Usando análise básica como fallback")
                        self.modelo_carregado = False
                    
        except Exception as e:
            logger.error(f"❌ Erro geral ao carregar modelo: {e}")
            logger.warning("⚠️ Usando análise básica como fallback")
            self.modelo_carregado = False
    
    def _analisar_com_bert(self, texto):
        """
        Análise de sentimento usando modelo BERT de Deep Learning
        Retorna score de sentimento baseado no modelo pré-treinado
        """
        if not self.modelo_carregado or not texto:
            return None
        
        try:
            # Limitar tamanho do texto (BERT tem limite de tokens)
            max_length = 512
            if len(texto) > max_length:
                texto = texto[:max_length]
            
            # Usar pipeline se disponível (mais simples)
            if self.sentiment_pipeline:
                try:
                    resultados = self.sentiment_pipeline(texto)
                    
                    # Processar resultados do pipeline
                    # O pipeline retorna lista de scores para cada label
                    if resultados and len(resultados) > 0:
                        # Normalmente retorna [{'label': 'POSITIVE', 'score': 0.9}, {'label': 'NEGATIVE', 'score': 0.1}]
                        # ou [{'label': 'LABEL_0', 'score': 0.1}, {'label': 'LABEL_1', 'score': 0.9}]
                        scores = resultados[0] if isinstance(resultados[0], list) else resultados
                        
                        # Encontrar scores positivo e negativo
                        score_positivo = 0.0
                        score_negativo = 0.0
                        
                        for item in scores:
                            label = str(item.get('label', '')).upper()
                            score = item.get('score', 0.0)
                            
                            # Verificar diferentes formatos de labels
                            if 'POS' in label or 'POSITIVE' in label or 'LABEL_1' in label or label == '1':
                                score_positivo = score
                            elif 'NEG' in label or 'NEGATIVE' in label or 'LABEL_0' in label or label == '0':
                                score_negativo = score
                        
                        # Se não encontrou labels específicos, usar o score mais alto como positivo
                        if score_positivo == 0.0 and score_negativo == 0.0 and len(scores) >= 2:
                            # Assumir que o maior score é positivo
                            scores_sorted = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)
                            score_positivo = scores_sorted[0].get('score', 0.5)
                            score_negativo = scores_sorted[1].get('score', 0.5) if len(scores_sorted) > 1 else 1.0 - score_positivo
                        
                        # Calcular polaridade (-1 a 1)
                        if score_positivo > 0 or score_negativo > 0:
                            polaridade = score_positivo - score_negativo
                            logger.info(f"✅ Pipeline BERT: positivo={score_positivo:.3f}, negativo={score_negativo:.3f}, polaridade={polaridade:.3f}")
                            return polaridade
                except Exception as e:
                    logger.warning(f"⚠️ Erro no pipeline BERT: {e}, tentando método direto...")
                    # Continuar para método direto
                    
            # Fallback: usar modelo e tokenizer diretamente
            elif self.tokenizer and self.model_bert:
                # Tokenizar texto
                inputs = self.tokenizer(
                    texto,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                )
                
                # Mover para GPU se disponível
                device = "cuda" if torch.cuda.is_available() else "cpu"
                if torch.cuda.is_available():
                    inputs = {k: v.to(device) for k, v in inputs.items()}
                    if hasattr(self.model_bert, 'to'):
                        self.model_bert = self.model_bert.to(device)
                
                # Fazer inferência
                with torch.no_grad():
                    outputs = self.model_bert(**inputs)
                    
                    # Se usar embeddings (modelo base), fazer análise baseada em embeddings
                    if self.use_embeddings:
                        # Obter embeddings do [CLS] token
                        if hasattr(outputs, 'last_hidden_state'):
                            embeddings = outputs.last_hidden_state
                        elif hasattr(outputs, 'pooler_output'):
                            embeddings = outputs.pooler_output
                        else:
                            # Tentar obter do primeiro token
                            embeddings = outputs[0][:, 0, :]  # [CLS] token
                        
                        # Análise de sentimento baseada em embeddings
                        # Usar palavras-chave positivas/negativas como referência
                        palavras_pos_ref = ['bom', 'ótimo', 'feliz', 'satisfeito', 'alegre']
                        palavras_neg_ref = ['ruim', 'triste', 'estressado', 'cansado', 'ansioso']
                        
                        # Tokenizar palavras de referência e obter seus embeddings
                        pos_embeddings = []
                        neg_embeddings = []
                        
                        for palavra in palavras_pos_ref:
                            try:
                                tokens = self.tokenizer(palavra, return_tensors="pt", padding=True, truncation=True)
                                if torch.cuda.is_available():
                                    tokens = {k: v.to(device) for k, v in tokens.items()}
                                with torch.no_grad():
                                    out = self.model_bert(**tokens)
                                    if hasattr(out, 'last_hidden_state'):
                                        pos_embeddings.append(out.last_hidden_state[:, 0, :].mean(dim=0))
                            except:
                                pass
                        
                        for palavra in palavras_neg_ref:
                            try:
                                tokens = self.tokenizer(palavra, return_tensors="pt", padding=True, truncation=True)
                                if torch.cuda.is_available():
                                    tokens = {k: v.to(device) for k, v in tokens.items()}
                                with torch.no_grad():
                                    out = self.model_bert(**tokens)
                                    if hasattr(out, 'last_hidden_state'):
                                        neg_embeddings.append(out.last_hidden_state[:, 0, :].mean(dim=0))
                            except:
                                pass
                        
                        # Calcular similaridade com embeddings de referência
                        if pos_embeddings and neg_embeddings:
                            # Média dos embeddings de referência
                            pos_ref = torch.stack(pos_embeddings).mean(dim=0)
                            neg_ref = torch.stack(neg_embeddings).mean(dim=0)
                            
                            # Embedding do texto (usar [CLS] token)
                            text_embedding = embeddings[:, 0, :].squeeze() if len(embeddings.shape) > 2 else embeddings.squeeze()
                            
                            # Calcular similaridade cosseno
                            cos_sim_pos = F.cosine_similarity(text_embedding.unsqueeze(0), pos_ref.unsqueeze(0))
                            cos_sim_neg = F.cosine_similarity(text_embedding.unsqueeze(0), neg_ref.unsqueeze(0))
                            
                            # Normalizar para -1 a 1
                            polaridade = (cos_sim_pos.item() - cos_sim_neg.item()) / 2.0
                            return max(-1.0, min(1.0, polaridade))
                        else:
                            # Se não conseguiu embeddings de referência, usar análise básica
                            return None
                    
                    # Se é modelo de classificação (SequenceClassification)
                    elif hasattr(outputs, 'logits'):
                        logits = outputs.logits
                        probs = F.softmax(logits, dim=-1)
                        
                        if probs.shape[1] >= 2:
                            score_negativo = probs[0][0].item()
                            score_positivo = probs[0][1].item()
                            polaridade = score_positivo - score_negativo
                            return polaridade
                        else:
                            return (probs[0][0].item() - 0.5) * 2
                    else:
                        return None
                        
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise BERT: {e}")
            return None
        
        return None
    
    def _analisar_portugues_basico(self, texto):
        """Análise básica de sentimento em português usando palavras-chave (fallback)"""
        texto_lower = texto.lower()
        
        # Palavras positivas
        palavras_positivas = [
            'bem', 'bom', 'ótimo', 'excelente', 'feliz', 'satisfeito', 'satisfeita',
            'alegre', 'contente', 'animado', 'animada', 'motivado', 'motivada',
            'ótima', 'bom dia', 'tudo bem', 'está bem', 'estou bem', 'estamos bem',
            'perfeito', 'maravilhoso', 'gratidão', 'grato', 'grata', 'satisfação',
            'prazer', 'entusiasmado', 'entusiasmada', 'confiante', 'tranquilo', 'tranquila'
        ]
        
        # Palavras negativas
        palavras_negativas = [
            'mal', 'ruim', 'péssimo', 'terrível', 'triste', 'infeliz', 'insatisfeito',
            'insatisfeita', 'deprimido', 'deprimida', 'ansioso', 'ansiosa', 'estressado',
            'estressada', 'cansado', 'cansada', 'desmotivado', 'desmotivada', 'preocupado',
            'preocupada', 'angustiado', 'angustiada', 'frustrado', 'frustrada', 'irritado',
            'irritada', 'nervoso', 'nervosa', 'medo', 'medo', 'pânico', 'desesperado'
        ]
        
        # Contar ocorrências
        count_positivo = sum(1 for palavra in palavras_positivas if palavra in texto_lower)
        count_negativo = sum(1 for palavra in palavras_negativas if palavra in texto_lower)
        
        # Calcular score
        total_palavras = len(texto.split())
        if total_palavras == 0:
            return 0.0
        
        # Score baseado na diferença entre positivo e negativo
        score = (count_positivo - count_negativo) / max(total_palavras, 1) * 2
        score = max(-1.0, min(1.0, score))  # Limitar entre -1 e 1
        
        return score
    
    def analisar_texto(self, texto, usar_gpt=True):
        """
        Análise de sentimento híbrida usando Deep Learning (BERT) + GPT (se disponível)
        
        Pipeline de análise:
        1. Tenta usar modelo BERT (Deep Learning) - PRIORIDADE
        2. Se BERT falhar, usa análise básica por palavras-chave
        3. Opcionalmente combina com GPT para análise avançada
        
        Args:
            texto (str): Texto a ser analisado
            usar_gpt (bool): Se deve usar GPT para análise avançada
            
        Returns:
            dict: Análise completa com sentimento, score e insights
        """
        if not texto or len(texto.strip()) < 3:
            return {
                'sentimento': 'neutro',
                'score': 0.0,
                'confianca': 0.0,
                'metodo': 'vazio'
            }
        
        try:
            polaridade = None
            metodo_usado = 'basico'
            confianca_base = 0.5
            
            # 🧠 PRIORIDADE 1: Análise com Deep Learning (BERT)
            if self.modelo_carregado:
                logger.info("🧠 Usando modelo BERT (Deep Learning) para análise...")
                polaridade_bert = self._analisar_com_bert(texto)
                
                if polaridade_bert is not None:
                    polaridade = polaridade_bert
                    metodo_usado = 'deep_learning_bert'
                    confianca_base = 0.85  # Alta confiança no modelo BERT
                    logger.info(f"✅ Análise BERT concluída: polaridade={polaridade:.3f}")
            
            # 🔄 FALLBACK: Se BERT não funcionou, usar análise básica
            if polaridade is None:
                logger.info("⚠️ BERT não disponível, usando análise básica...")
                score_portugues = self._analisar_portugues_basico(texto)
                
                # Tentar TextBlob como complemento
                try:
                    analise = TextBlob(texto)
                    polaridade_textblob = analise.sentiment.polarity
                    # Combinar análises (dar mais peso à análise em português)
                    polaridade = (score_portugues * 0.7) + (polaridade_textblob * 0.3)
                except:
                    polaridade = score_portugues
                
                metodo_usado = 'basico_fallback'
                confianca_base = 0.6
            
            # Classificar sentimento baseado na polaridade
            if polaridade > 0.15:
                sentimento = 'positivo'
            elif polaridade < -0.15:
                sentimento = 'negativo'
            else:
                sentimento = 'neutro'
            
            # Calcular confiança final
            confianca = min(abs(polaridade) * 1.2 + confianca_base * 0.3, 1.0)
            
            resultado = {
                'sentimento': sentimento,
                'score': round(polaridade, 3),
                'confianca': round(confianca, 2),
                'metodo': metodo_usado,
                'deep_learning': self.modelo_carregado,  # Indica se usou DL
                'detalhes': {
                    'polaridade': polaridade,
                    'palavras': len(texto.split()),
                    'modelo': self.model_name if self.modelo_carregado else None
                }
            }
            
            # 🚀 PRIORIDADE 2: Análise avançada com GPT (se disponível e solicitado)
            if usar_gpt and gpt_service.verificar_disponibilidade():
                logger.info("🤖 Combinando com GPT para análise avançada...")
                analise_gpt = gpt_service.analisar_sentimento_avancado(texto)
                
                if analise_gpt:
                    resultado['gpt_analise'] = analise_gpt
                    resultado['metodo'] = f'{metodo_usado}_+_gpt'
                    
                    # Usar sentimento do GPT se disponível (mais confiável para contexto)
                    sentimento_gpt = analise_gpt.get('sentimento_primario', '').lower()
                    if sentimento_gpt in ['positivo', 'negativo', 'neutro']:
                        # Combinar sentimento BERT com GPT (peso maior para GPT em contexto)
                        if metodo_usado == 'deep_learning_bert':
                            # Se ambos concordam, aumentar confiança
                            if sentimento_gpt == sentimento:
                                resultado['confianca'] = min(resultado['confianca'] + 0.1, 1.0)
                            else:
                                # Se discordam, dar mais peso ao GPT (contexto)
                                resultado['sentimento'] = sentimento_gpt
                        else:
                            # Se não usou BERT, confiar mais no GPT
                            resultado['sentimento'] = sentimento_gpt
                            if sentimento_gpt == 'positivo':
                                resultado['score'] = max(resultado['score'], 0.3)
                            elif sentimento_gpt == 'negativo':
                                resultado['score'] = min(resultado['score'], -0.3)
                            resultado['confianca'] = min(resultado['confianca'] + 0.2, 1.0)
            
            logger.info(f"📊 Sentimento analisado: {sentimento} (score: {resultado['score']}, método: {resultado['metodo']}, DL: {self.modelo_carregado})")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de sentimento: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                'sentimento': 'erro',
                'score': 0.0,
                'confianca': 0.0,
                'metodo': 'erro'
            }
    
    def analisar_emocoes_numerico(self, estresse, felicidade, ansiedade, motivacao, comentario_sentimento=None):
        """
        Analisa os valores numéricos e gera insights
        Considera também o sentimento do comentário se disponível
        
        Args:
            estresse (int): 1-10
            felicidade (int): 1-10
            ansiedade (int): 1-10
            motivacao (int): 1-10
            comentario_sentimento (dict): Resultado da análise de sentimento do comentário (opcional)
            
        Returns:
            dict: Análise e classificação do estado emocional
        """
        # Cálculo do índice de bem-estar (0-100)
        # Cada métrica contribui com até 25 pontos (10 * 2.5)
        # Estresse e ansiedade: quanto menor, melhor (10 - valor)
        # Felicidade e motivação: quanto maior, melhor (valor direto)
        indice_bem_estar = (
            (10 - estresse) * 2.5 +
            felicidade * 2.5 +
            (10 - ansiedade) * 2.5 +
            motivacao * 2.5
        )
        # Não dividir por 4! Cada componente já está na escala correta (0-25)
        
        # Ajustar índice baseado no sentimento do comentário
        if comentario_sentimento:
            sentimento = comentario_sentimento.get('sentimento', 'neutro')
            score_sentimento = comentario_sentimento.get('score', 0.0)
            
            # Se o comentário for positivo, aumentar o índice
            if sentimento == 'positivo' and score_sentimento > 0.2:
                # Aumentar índice em até 15 pontos se comentário muito positivo
                bonus = min(score_sentimento * 20, 15)
                indice_bem_estar = min(indice_bem_estar + bonus, 100)
                logger.info(f"📈 Ajuste positivo baseado no comentário: +{bonus:.1f} pontos")
            # Se o comentário for negativo, diminuir o índice
            elif sentimento == 'negativo' and score_sentimento < -0.2:
                # Diminuir índice em até 15 pontos se comentário muito negativo
                penalidade = min(abs(score_sentimento) * 20, 15)
                indice_bem_estar = max(indice_bem_estar - penalidade, 0)
                logger.info(f"📉 Ajuste negativo baseado no comentário: -{penalidade:.1f} pontos")
        
        # Classificação ajustada para escala 0-100
        if indice_bem_estar >= 80:
            classificacao = 'excelente'
            cor = 'green'
        elif indice_bem_estar >= 65:
            classificacao = 'bom'
            cor = 'lightgreen'
        elif indice_bem_estar >= 50:
            classificacao = 'moderado'
            cor = 'yellow'
        elif indice_bem_estar >= 35:
            classificacao = 'preocupante'
            cor = 'orange'
        else:
            classificacao = 'crítico'
            cor = 'red'
        
        # Identificar principais problemas (thresholds mais realistas)
        problemas = []
        if estresse >= 8:
            problemas.append('Estresse muito elevado')
        elif estresse >= 6:
            problemas.append('Estresse moderado')
            
        if felicidade <= 2:
            problemas.append('Felicidade muito baixa')
        elif felicidade <= 4:
            problemas.append('Felicidade baixa')
            
        if ansiedade >= 8:
            problemas.append('Ansiedade muito alta')
        elif ansiedade >= 6:
            problemas.append('Ansiedade moderada')
            
        if motivacao <= 2:
            problemas.append('Motivação muito baixa')
        elif motivacao <= 4:
            problemas.append('Motivação baixa')
        
        # Se o índice é alto (bom estado), não mostrar problemas menores
        if indice_bem_estar >= 70:
            problemas = []  # Não mostrar problemas se o estado é excelente
        elif indice_bem_estar >= 55:
            # Se está bom, só mostrar problemas graves
            problemas = [p for p in problemas if 'muito' in p.lower()]
        # Se não há problemas significativos e o comentário é positivo, não mostrar problemas
        elif comentario_sentimento and comentario_sentimento.get('sentimento') == 'positivo':
            if len(problemas) <= 1 and indice_bem_estar >= 40:
                problemas = []  # Limpar problemas menores se o comentário é positivo
        
        return {
            'indice_bem_estar': round(indice_bem_estar, 1),
            'classificacao': classificacao,
            'cor': cor,
            'problemas': problemas,
            'recomendacao': self._gerar_recomendacao(classificacao, problemas)
        }
    
    def _gerar_recomendacao(self, classificacao, problemas):
        """Gera recomendações baseadas na análise"""
        recomendacoes = {
            'crítico': 'Atenção imediata necessária! Considere conversar com RH ou psicólogo.',
            'preocupante': 'Situação merece atenção. Busque apoio e considere pausas regulares.',
            'moderado': 'Estado emocional equilibrado, mas pode melhorar. Pratique autocuidado.',
            'bom': 'Você está indo bem! Continue cuidando da sua saúde mental.',
            'excelente': 'Excelente! Você está em ótimo estado emocional.'
        }
        
        recomendacao = recomendacoes.get(classificacao, '')
        
        if problemas:
            recomendacao += f" Pontos de atenção: {', '.join(problemas)}."
        
        return recomendacao


# Instância global
analyzer = SentimentAnalyzer()

