# 🧠 EqualMind - Análise Emocional Corporativa com IA

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)
![GPT](https://img.shields.io/badge/ChatGPT-4o--mini-purple.svg)

Sistema de saúde mental corporativa com **IA Generativa (ChatGPT)**, **Deep Learning** e **Oracle Database**.

## 🚀 Funcionalidades

✅ **Registro Emocional** - Input manual (estresse, felicidade, ansiedade, motivação)  
✅ **🤖 IA Generativa (ChatGPT)** - Análise avançada, recomendações personalizadas e coach virtual  
✅ **Mapas de Calor** - Visualização por setor com matplotlib/seaborn  
✅ **Dashboard RH** - Métricas e insights estratégicos  
✅ **Oracle Database** - Criação automática de tabelas  
✅ **Análise de Sentimento** - Detecção inteligente em português

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

## 🎯 Como Executar

### Opção 1: Usando o Script de Execução (Windows)

```bash
run.bat
```

### Opção 2: Executar Manualmente

```bash
python app.py
```

### Opção 3: Usando Flask (Linux/Mac)

```bash
export FLASK_APP=app.py
flask run
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
- OpenAI GPT-4o-mini (IA Generativa)
- TextBlob (Análise de Sentimento)
- Matplotlib/Seaborn (Visualizações)

**Database:**

- Oracle Database 19c+
- cx_Oracle (Driver Python)

**Frontend:**

- HTML5, CSS3, JavaScript
- Design responsivo

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
# Vis-oComputacional-GS
