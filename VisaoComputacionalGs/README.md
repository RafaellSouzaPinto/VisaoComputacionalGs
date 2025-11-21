# 🧠 EqualMind - Análise Emocional Corporativa com IA

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)
![GPT](https://img.shields.io/badge/ChatGPT-4o--mini-purple.svg)
![BERT](https://img.shields.io/badge/BERT-Deep%20Learning-orange.svg)

Sistema de saúde mental corporativa com **Deep Learning (BERT)**, **IA Generativa (ChatGPT)** e **Oracle Database**.

## ⚡ Início Rápido

```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar (Windows)
run.bat

# 3. Executar (Linux/Mac)
./run.sh

# 4. Acessar
# http://localhost:5000
```

**📖 Para instruções detalhadas, veja a seção [🎯 Como Executar](#-como-executar)**

## 🚀 Funcionalidades

✅ **Registro Emocional** - Input manual (estresse, felicidade, ansiedade, motivação)  
✅ **🧠 Deep Learning (BERT)** - Análise de sentimento com modelo transformer pré-treinado  
✅ **🤖 IA Generativa (ChatGPT)** - Análise avançada, recomendações personalizadas e coach virtual  
✅ **Mapas de Calor** - Visualização por setor com matplotlib/seaborn  
✅ **Dashboard RH** - Métricas e insights estratégicos  
✅ **Oracle Database** - Criação automática de tabelas  
✅ **Análise de Sentimento Híbrida** - BERT + GPT para máxima precisão

## 📋 Pré-requisitos

- **Python 3.9+**
- **Oracle Database** (acesso configurado)
- **Oracle Instant Client** instalado (para Windows: `C:\oracle\instantclient_23_4`)
- **OpenAI API Key** (opcional, para funcionalidades de IA)

## ⚡ Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone <seu-repositorio>
cd VisaoComputacional
```

### 2. Crie um Ambiente Virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

**⏱️ Tempo estimado:** 5-10 minutos (depende da conexão)

**📦 Tamanho total:** ~2GB (incluindo modelo BERT)

**⚠️ Primeira instalação:** O modelo BERT será baixado automaticamente (~400MB) na primeira execução. Isso pode levar alguns minutos.

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (ou configure diretamente no `config.py`):

```env
# Oracle Database
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/orcl

# OpenAI (opcional - para funcionalidades de IA)
OPENAI_API_KEY=sua_chave_api

# Flask
FLASK_SECRET_KEY=chave-secreta-aleatoria
FLASK_DEBUG=True
PORT=5000
```

**Ou edite diretamente o arquivo `config.py`** com suas credenciais.

### 5. Configure o Oracle Instant Client (Windows)

Certifique-se de que o Oracle Instant Client está instalado em:

```
C:\oracle\instantclient_23_4
```

Se estiver em outro local, edite a linha 10 do arquivo `database/db_connection.py`.

### 6. Teste a Instalação

Antes de rodar a aplicação completa, teste se tudo está configurado:

```bash
# Testar modelo BERT
python test_bert.py

# Testar conexão Oracle (se configurado)
python test_oracle_connection.py
```

## 🎯 Como Executar

### 📋 Pré-requisitos Antes de Executar

1. **Python 3.9+** instalado
2. **Ambiente virtual** criado e ativado
3. **Dependências instaladas** (`pip install -r requirements.txt`)
4. **Oracle Database** configurado (opcional, mas recomendado)
5. **OpenAI API Key** (opcional, para funcionalidades de IA Generativa)

### 🚀 Passo a Passo Completo

#### **1. Criar e Ativar Ambiente Virtual**

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### **2. Instalar Dependências**

```bash
pip install -r requirements.txt
```

**⚠️ Importante:** Na primeira instalação, o modelo BERT será baixado automaticamente (~400MB). Isso pode levar alguns minutos.

#### **3. Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto (ou edite `config.py`):

```env
# Oracle Database
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/orcl

# OpenAI (opcional)
OPENAI_API_KEY=sua_chave_api

# Flask
FLASK_SECRET_KEY=chave-secreta-aleatoria
FLASK_DEBUG=True
PORT=5000
```

#### **4. Executar a Aplicação**

**Opção 1: Script Automático (Windows) - RECOMENDADO**

```bash
run.bat
```

O script automaticamente:

- ✅ Ativa o ambiente virtual
- ✅ Verifica conexão com Oracle
- ✅ Inicia o servidor Flask

**Opção 2: Script Automático (Linux/Mac)**

```bash
chmod +x run.sh
./run.sh
```

**Opção 3: Execução Manual**

```bash
python app.py
```

**Opção 4: Usando Flask CLI**

```bash
export FLASK_APP=app.py  # Linux/Mac
set FLASK_APP=app.py     # Windows
flask run
```

#### **5. Acessar a Aplicação**

Após iniciar, acesse no navegador:

```
http://localhost:5000
```

### 🧪 Testar o Modelo BERT

Para verificar se o Deep Learning está funcionando:

```bash
python test_bert.py
```

Este script completo executa:

**FASE 1: Verificação de Carregamento**

- ✅ Importação do SentimentAnalyzer
- ✅ Status do modelo BERT
- ✅ Verificação de configuração

**FASE 2: Testes de Análise de Sentimento (14 testes)**

- ✅ Textos positivos (alegria, satisfação, perfeição)
- ✅ Textos negativos (estresse, tristeza, frustração, angústia)
- ✅ Textos neutros (normal, rotina, indiferença)
- ✅ Casos especiais (misto, muito positivo/negativo)

**FASE 3: Testes de Performance**

- ✅ Texto vazio
- ✅ Texto muito curto
- ✅ Texto muito longo (>512 tokens)
- ✅ Caracteres especiais e emojis

**FASE 4: Estatísticas e Resumo**

- ✅ Taxa de acerto
- ✅ Distribuição de resultados
- ✅ Status do Deep Learning

**Resultado esperado:**

```
🎉 SUCESSO! O sistema está funcionando perfeitamente com Deep Learning!
🧠 Deep Learning: ✅ SIM em todos os testes
```

### 📊 Logs e Verificação

Ao iniciar, você verá logs como:

```
🔄 Carregando modelo de Deep Learning: neuralmind/bert-base-portuguese-cased
✅ Modelo BERT carregado com sucesso (pipeline sentiment-analysis)
🚀 EqualMind iniciado com sucesso!
```

**Verificar status da API:**

```bash
curl http://localhost:5000/api/health
```

Resposta esperada:

```json
{
  "status": "online",
  "database": "connected",
  "ai_model": "loaded",
  "gpt_service": "available"
}
```

## ✨ Funcionalidades Automáticas

### 🗄️ Criação Automática de Tabelas

**As tabelas são criadas automaticamente** quando você inicia a aplicação pela primeira vez!

O sistema verifica e cria automaticamente as seguintes tabelas no Oracle:

- `EMPRESAS_WorkWell` - Cadastro de empresas
- `SETORES_WorkWell` - Setores por empresa
- `COLABORADORES_WorkWell` - Colaboradores
- `REGISTROS_EMOCIONAIS_WorkWell` - Registros emocionais

**Não é necessário executar scripts SQL manualmente!** A aplicação faz tudo automaticamente.

### 📊 Estrutura do Banco de Dados

```
EMPRESAS_WorkWell
├── ID (PK)
├── NOME
├── CNPJ
└── DATA_CADASTRO

SETORES_WorkWell
├── ID (PK)
├── EMPRESA_ID (FK)
├── NOME
└── DESCRICAO

COLABORADORES_WorkWell
├── ID (PK)
├── EMPRESA_ID (FK)
├── SETOR_ID (FK)
└── CODIGO_ACESSO

REGISTROS_EMOCIONAIS_WorkWell
├── ID (PK)
├── COLABORADOR_ID (FK)
├── EMPRESA_ID (FK)
├── SETOR_ID (FK)
├── NIVEL_ESTRESSE (1-10)
├── NIVEL_FELICIDADE (1-10)
├── NIVEL_ANSIEDADE (1-10)
├── NIVEL_MOTIVACAO (1-10)
├── COMENTARIO
├── SENTIMENTO_TEXTO
├── SCORE_SENTIMENTO
└── DATA_REGISTRO
```

## 🌐 Acessando a Aplicação

Após iniciar, acesse no navegador:

```
http://localhost:5000
```

## 📡 API Endpoints

```http
POST /api/registro-emocional      # Criar registro emocional
GET  /api/setores/{empresa_id}    # Listar setores
GET  /api/mapa-calor/{empresa_id} # Gerar mapa de calor
GET  /api/dashboard/{empresa_id}  # Dashboard completo
POST /api/recomendacoes-ia         # 🤖 Recomendações GPT
POST /api/coach-virtual           # 🤖 Chat com coach IA
GET  /api/relatorio-ia/{id}       # 🤖 Relatório estratégico IA
GET  /api/estatisticas/{id}       # Estatísticas gerais
GET  /api/health                   # Status do sistema
```

## 🛠️ Stack Tecnológica

**Backend:**

- Python 3.9+
- Flask (API REST)
- **🧠 Deep Learning:**
  - **BERT (neuralmind/bert-base-portuguese-cased)** - Modelo transformer para análise de sentimento em português
  - PyTorch 2.1.0 + Transformers 4.36.0
  - TensorFlow 2.15.0 (suporte adicional)
- **🤖 IA Generativa:**
  - OpenAI GPT-4o-mini (Análise avançada, recomendações, coach virtual)
- **📊 Processamento:**
  - TextBlob (Análise complementar)
  - Matplotlib/Seaborn (Visualizações)
  - NLTK (Processamento de texto)

**Database:**

- Oracle Database 19c+
- cx_Oracle (Driver Python)

**Frontend:**

- HTML5, CSS3, JavaScript
- Design responsivo

## 🧠 Deep Learning - Modelo BERT (INTEGRADO AO SISTEMA)

### ⚠️ IMPORTANTE: BERT NÃO É SEPARADO!

O modelo **BERT está totalmente integrado** ao sistema EqualMind. Ele funciona **automaticamente** quando você usa a aplicação - você não precisa fazer nada especial!

### 🔄 Como o BERT Funciona no Sistema

**1. Quando você inicia a aplicação:**

```
🔄 Carregando modelo de Deep Learning: neuralmind/bert-base-portuguese-cased
✅ Modelo BERT carregado com sucesso
🚀 EqualMind iniciado com sucesso!
```

- O BERT é carregado **automaticamente** ao iniciar o servidor Flask
- Fica pronto para uso em todas as análises

**2. Quando você registra um estado emocional:**

```
Usuário preenche formulário → Envia comentário → Sistema usa BERT automaticamente
```

**Fluxo completo:**

1. Usuário preenche o formulário na interface web (`templates/index.html`)
2. JavaScript envia dados para `/api/registro-emocional` (`static/js/app.js`)
3. Backend Flask recebe o comentário (`app.py` linha 122)
4. **🧠 BERT analisa automaticamente** o comentário (`ai/sentiment_analyzer.py`)
5. Resultado é salvo no banco Oracle (`database/db_connection.py`)
6. Interface mostra a análise para o usuário

**3. Onde o BERT é usado:**

| Funcionalidade            | Endpoint                        | Quando BERT é Usado                                             |
| ------------------------- | ------------------------------- | --------------------------------------------------------------- |
| **Registro Emocional**    | `POST /api/registro-emocional`  | ✅ **Sempre** - quando há comentário                            |
| **Análise de Sentimento** | `POST /api/analisar-sentimento` | ✅ **Sempre** - análise direta                                  |
| **Recomendações IA**      | `POST /api/recomendacoes-ia`    | ✅ **Sempre** - analisa comentário antes de gerar recomendações |

### 📊 Exemplo Prático

**Cenário:** Usuário registra estado emocional com comentário

```javascript
// Frontend (JavaScript)
{
  "comentario": "Estou me sentindo muito bem hoje! O trabalho está ótimo."
}
```

```python
# Backend (Python) - app.py linha 122
resultado_sentimento = analyzer.analisar_texto(comentario)
# ↑ Aqui o BERT é chamado automaticamente!
```

```python
# ai/sentiment_analyzer.py - linha 333
# 🧠 PRIORIDADE 1: Análise com Deep Learning (BERT)
if self.modelo_carregado:
    logger.info("🧠 Usando modelo BERT (Deep Learning) para análise...")
    polaridade_bert = self._analisar_com_bert(texto)
    # ↑ BERT processa o texto aqui!
```

**Resultado retornado:**

```json
{
  "analise_sentimento": {
    "sentimento": "positivo",
    "score": 0.75,
    "metodo": "deep_learning_bert", // ← Indica que usou BERT!
    "deep_learning": true, // ← Confirma Deep Learning
    "confianca": 0.92
  }
}
```

### 🎯 Modelo Utilizado

- **Modelo:** `neuralmind/bert-base-portuguese-cased`
- **Arquitetura:** BERT base (110M parâmetros)
- **Especialização:** Português brasileiro
- **Localização no código:** `ai/sentiment_analyzer.py`

### 🔧 Pipeline de Análise Automático

Quando um texto é analisado, o sistema tenta nesta ordem:

1. **🧠 BERT (Deep Learning)** - Prioridade máxima

   - Se disponível, usa automaticamente
   - Alta precisão (confiança 0.85+)
   - Método: `deep_learning_bert`

2. **📝 Análise Básica** - Fallback

   - Se BERT não carregou, usa análise por palavras-chave
   - Método: `basico_fallback`

3. **🤖 GPT (Opcional)** - Complemento
   - Pode ser combinado com BERT para análise contextual
   - Método: `deep_learning_bert_+_gpt`

### 📈 Métricas e Performance

- **Precisão:** Alta (modelo pré-treinado em grandes volumes de texto em português)
- **Confiança:** 0.85+ quando usa BERT diretamente
- **Latência:** ~100-500ms por análise (depende do hardware)
- **Suporte GPU:** Aceleração automática se CUDA disponível
- **Uso:** Automático - sem necessidade de configuração adicional

### 💡 Resumo

✅ **BERT está INTEGRADO** - não é um sistema separado  
✅ **Funciona AUTOMATICAMENTE** - você não precisa fazer nada  
✅ **Usado em TODAS as análises** - sempre que há um comentário  
✅ **Transparente para o usuário** - funciona nos bastidores

**Nota:** Na primeira execução, o modelo será baixado do Hugging Face (~400MB). Execuções subsequentes usam o cache local.

## 🐛 Solução de Problemas

### Erro ao conectar ao Oracle

1. Verifique se o Oracle Instant Client está instalado
2. Confirme as credenciais no `config.py` ou `.env`
3. Teste a conexão: `python test_oracle_connection.py`

### Tabelas não são criadas

1. Verifique os logs no console ao iniciar a aplicação
2. Confirme que o usuário tem permissões para criar tabelas
3. As tabelas são criadas automaticamente na primeira execução

### Erro com OpenAI API

- A API Key é opcional
- Funcionalidades básicas funcionam sem ela
- Para usar IA, configure `OPENAI_API_KEY` no `.env`

### Erro ao carregar modelo BERT (Deep Learning)

1. **Primeira execução:** O modelo será baixado automaticamente (~400MB)

   - Requer conexão com internet
   - Pode levar alguns minutos na primeira vez

2. **Memória insuficiente:**

   - O modelo requer ~2GB de RAM
   - Se não houver memória, o sistema usa análise básica como fallback

3. **GPU não detectada:**

   - O sistema funciona normalmente em CPU
   - GPU acelera o processamento mas não é obrigatória

4. **Verificar logs:**
   - Procure por mensagens "✅ Modelo BERT carregado" nos logs
   - Se aparecer "⚠️ Usando análise básica", o modelo não carregou mas o sistema continua funcionando

## 📁 Estrutura do Projeto

```
VisaoComputacional/
├── app.py                          # Flask backend principal
├── config.py                       # Configurações
├── requirements.txt                 # Dependências Python
├── run.bat                         # Script de execução (Windows)
├── run.sh                          # Script de execução (Linux/Mac)
│
├── ai/
│   ├── gpt_service.py              # 🤖 Serviço OpenAI GPT
│   ├── sentiment_analyzer.py       # Análise de sentimento
│   └── heatmap_generator.py        # Geração de mapas de calor
│
├── database/
│   ├── db_connection.py            # Conexão Oracle + criação automática
│   ├── auto_create_tables.py       # Script de criação de tabelas
│   └── schema.sql                  # Schema SQL (referência)
│
├── templates/
│   └── index.html                  # Interface web
│
└── static/
    ├── css/
    │   └── style.css               # Estilos
    └── js/
        └── app.js                  # JavaScript frontend
```

## 🎯 ODS da ONU

🎯 **ODS 3** - Saúde e Bem-Estar  
💼 **ODS 8** - Trabalho Decente  
⚖️ **ODS 10** - Redução de Desigualdades  
🎓 **ODS 4** - Educação de Qualidade

## 📝 Notas Importantes

- **Criação Automática**: As tabelas são criadas automaticamente na primeira execução
- **Sem Scripts Manuais**: Não é necessário executar SQL manualmente
- **Oracle Instant Client**: Necessário para conexão (Windows: `C:\oracle\instantclient_23_4`)
- **OpenAI API**: Opcional, mas recomendado para funcionalidades completas de IA

## 📄 Licença

MIT License - FIAP 2025

---

<div align="center">

**🤖 Powered by OpenAI GPT-4o-mini**

"A tecnologia não substitui o humano, mas potencializa o cuidado."

💙 **EqualMind** | FIAP 2025

</div>


