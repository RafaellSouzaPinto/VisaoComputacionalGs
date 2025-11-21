-- =====================================================
-- Work Well - Schema Oracle Database (REFERÊNCIA)
-- Sistema de Análise Emocional Corporativa
-- =====================================================
-- 
-- ATENÇÃO: Este arquivo é APENAS para referência/documentação.
-- O código Python usa automaticamente o schema com sufixo _WorkWell
-- definido em: database/auto_create_tables.py
-- 
-- As tabelas são criadas automaticamente ao iniciar a aplicação.
-- NÃO é necessário executar este SQL manualmente.
-- =====================================================

-- Tabela de Empresas
CREATE TABLE empresas (
    id_empresa NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_empresa VARCHAR2(200) NOT NULL,
    cnpj VARCHAR2(18) UNIQUE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo CHAR(1) DEFAULT 'S' CHECK (ativo IN ('S', 'N'))
);

-- Tabela de Setores
CREATE TABLE setores (
    id_setor NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_empresa NUMBER NOT NULL,
    nome_setor VARCHAR2(100) NOT NULL,
    descricao VARCHAR2(500),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_setor_empresa FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    CONSTRAINT uk_setor_empresa UNIQUE (id_empresa, nome_setor)
);

-- Tabela de Colaboradores
CREATE TABLE colaboradores (
    id_colaborador NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_empresa NUMBER NOT NULL,
    id_setor NUMBER NOT NULL,
    nome_colaborador VARCHAR2(200) NOT NULL,
    email VARCHAR2(200) UNIQUE NOT NULL,
    codigo_acesso VARCHAR2(50) UNIQUE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo CHAR(1) DEFAULT 'S' CHECK (ativo IN ('S', 'N')),
    CONSTRAINT fk_colab_empresa FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    CONSTRAINT fk_colab_setor FOREIGN KEY (id_setor) REFERENCES setores(id_setor) ON DELETE CASCADE
);

-- Tabela de Registros Emocionais (CORE DA APLICAÇÃO)
CREATE TABLE registros_emocionais (
    id_registro NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_colaborador NUMBER NOT NULL,
    id_setor NUMBER NOT NULL,
    nivel_estresse NUMBER(2) NOT NULL CHECK (nivel_estresse BETWEEN 1 AND 10),
    nivel_felicidade NUMBER(2) NOT NULL CHECK (nivel_felicidade BETWEEN 1 AND 10),
    nivel_ansiedade NUMBER(2) CHECK (nivel_ansiedade BETWEEN 1 AND 10),
    nivel_motivacao NUMBER(2) CHECK (nivel_motivacao BETWEEN 1 AND 10),
    comentario CLOB,
    sentimento_detectado VARCHAR2(50), -- resultado da análise de sentimento
    score_sentimento NUMBER(3,2), -- confiança da análise (-1 a 1)
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    anonimo CHAR(1) DEFAULT 'N' CHECK (anonimo IN ('S', 'N')),
    CONSTRAINT fk_reg_colaborador FOREIGN KEY (id_colaborador) REFERENCES colaboradores(id_colaborador) ON DELETE CASCADE,
    CONSTRAINT fk_reg_setor FOREIGN KEY (id_setor) REFERENCES setores(id_setor) ON DELETE CASCADE
);

-- Tabela de Alertas Automáticos
CREATE TABLE alertas (
    id_alerta NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_setor NUMBER NOT NULL,
    tipo_alerta VARCHAR2(50) NOT NULL, -- 'ESTRESSE_ALTO', 'FELICIDADE_BAIXA', 'ENGAJAMENTO_BAIXO'
    descricao VARCHAR2(500),
    nivel_severidade VARCHAR2(20) CHECK (nivel_severidade IN ('BAIXO', 'MEDIO', 'ALTO', 'CRITICO')),
    data_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolvido CHAR(1) DEFAULT 'N' CHECK (resolvido IN ('S', 'N')),
    CONSTRAINT fk_alerta_setor FOREIGN KEY (id_setor) REFERENCES setores(id_setor) ON DELETE CASCADE
);

-- Índices para Performance
CREATE INDEX idx_reg_setor_data ON registros_emocionais(id_setor, data_registro);
CREATE INDEX idx_reg_colaborador ON registros_emocionais(id_colaborador);
CREATE INDEX idx_reg_data ON registros_emocionais(data_registro);
CREATE INDEX idx_alertas_setor ON alertas(id_setor, resolvido);

-- =====================================================
-- VIEWS para Análises
-- =====================================================

-- View: Média Emocional por Setor (últimos 30 dias)
CREATE OR REPLACE VIEW vw_media_emocional_setor AS
SELECT 
    s.id_setor,
    s.nome_setor,
    e.nome_empresa,
    ROUND(AVG(r.nivel_estresse), 2) as media_estresse,
    ROUND(AVG(r.nivel_felicidade), 2) as media_felicidade,
    ROUND(AVG(NVL(r.nivel_ansiedade, 5)), 2) as media_ansiedade,
    ROUND(AVG(NVL(r.nivel_motivacao, 5)), 2) as media_motivacao,
    COUNT(r.id_registro) as total_registros,
    MAX(r.data_registro) as ultima_atualizacao
FROM setores s
JOIN empresas e ON s.id_empresa = e.id_empresa
LEFT JOIN registros_emocionais r ON s.id_setor = r.id_setor
    AND r.data_registro >= CURRENT_TIMESTAMP - INTERVAL '30' DAY
GROUP BY s.id_setor, s.nome_setor, e.nome_empresa;

-- View: Dashboard RH - Indicadores Críticos
CREATE OR REPLACE VIEW vw_dashboard_rh AS
SELECT 
    s.id_setor,
    s.nome_setor,
    COUNT(DISTINCT r.id_colaborador) as colaboradores_ativos,
    COUNT(r.id_registro) as registros_mes,
    ROUND(AVG(r.nivel_estresse), 2) as estresse_medio,
    ROUND(AVG(r.nivel_felicidade), 2) as felicidade_media,
    COUNT(CASE WHEN r.nivel_estresse >= 8 THEN 1 END) as casos_estresse_alto,
    COUNT(CASE WHEN r.nivel_felicidade <= 3 THEN 1 END) as casos_felicidade_baixa,
    CASE 
        WHEN AVG(r.nivel_estresse) >= 7 THEN 'CRITICO'
        WHEN AVG(r.nivel_estresse) >= 6 THEN 'ALTO'
        WHEN AVG(r.nivel_estresse) >= 4 THEN 'MEDIO'
        ELSE 'BAIXO'
    END as status_setor
FROM setores s
LEFT JOIN registros_emocionais r ON s.id_setor = r.id_setor
    AND r.data_registro >= CURRENT_TIMESTAMP - INTERVAL '30' DAY
GROUP BY s.id_setor, s.nome_setor;

-- =====================================================
-- PROCEDURES
-- =====================================================

-- Procedure: Inserir Registro Emocional com Análise
CREATE OR REPLACE PROCEDURE sp_inserir_registro_emocional (
    p_id_colaborador IN NUMBER,
    p_id_setor IN NUMBER,
    p_nivel_estresse IN NUMBER,
    p_nivel_felicidade IN NUMBER,
    p_nivel_ansiedade IN NUMBER,
    p_nivel_motivacao IN NUMBER,
    p_comentario IN CLOB,
    p_anonimo IN CHAR,
    p_id_registro OUT NUMBER
)
AS
BEGIN
    INSERT INTO registros_emocionais (
        id_colaborador, id_setor, nivel_estresse, nivel_felicidade,
        nivel_ansiedade, nivel_motivacao, comentario, anonimo
    ) VALUES (
        p_id_colaborador, p_id_setor, p_nivel_estresse, p_nivel_felicidade,
        p_nivel_ansiedade, p_nivel_motivacao, p_comentario, p_anonimo
    ) RETURNING id_registro INTO p_id_registro;
    
    -- Gerar alerta se necessário
    IF p_nivel_estresse >= 8 OR p_nivel_felicidade <= 2 THEN
        INSERT INTO alertas (id_setor, tipo_alerta, descricao, nivel_severidade)
        VALUES (
            p_id_setor,
            CASE WHEN p_nivel_estresse >= 8 THEN 'ESTRESSE_ALTO' ELSE 'FELICIDADE_BAIXA' END,
            'Colaborador reportou ' || CASE WHEN p_nivel_estresse >= 8 THEN 'estresse muito alto' ELSE 'felicidade muito baixa' END,
            'ALTO'
        );
    END IF;
    
    COMMIT;
END;
/

-- Procedure: Atualizar Sentimento (chamada pelo backend após análise de IA)
CREATE OR REPLACE PROCEDURE sp_atualizar_sentimento (
    p_id_registro IN NUMBER,
    p_sentimento IN VARCHAR2,
    p_score IN NUMBER
)
AS
BEGIN
    UPDATE registros_emocionais
    SET sentimento_detectado = p_sentimento,
        score_sentimento = p_score
    WHERE id_registro = p_id_registro;
    
    COMMIT;
END;
/

-- Procedure: Obter Dados para Mapa de Calor
CREATE OR REPLACE PROCEDURE sp_dados_mapa_calor (
    p_id_empresa IN NUMBER,
    p_dias IN NUMBER DEFAULT 30,
    p_cursor OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_cursor FOR
    SELECT 
        s.id_setor,
        s.nome_setor,
        ROUND(AVG(r.nivel_estresse), 2) as media_estresse,
        ROUND(AVG(r.nivel_felicidade), 2) as media_felicidade,
        ROUND(AVG(NVL(r.nivel_ansiedade, 5)), 2) as media_ansiedade,
        ROUND(AVG(NVL(r.nivel_motivacao, 5)), 2) as media_motivacao,
        COUNT(r.id_registro) as total_registros
    FROM setores s
    LEFT JOIN registros_emocionais r ON s.id_setor = r.id_setor
        AND r.data_registro >= CURRENT_TIMESTAMP - INTERVAL p_dias DAY
    WHERE s.id_empresa = p_id_empresa
    GROUP BY s.id_setor, s.nome_setor
    ORDER BY media_estresse DESC;
END;
/

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger: Detectar Padrões Críticos Automaticamente
CREATE OR REPLACE TRIGGER trg_analise_automatica
AFTER INSERT ON registros_emocionais
FOR EACH ROW
DECLARE
    v_media_estresse NUMBER;
    v_count_alto NUMBER;
BEGIN
    -- Verificar média de estresse do setor nos últimos 7 dias
    SELECT AVG(nivel_estresse), COUNT(*)
    INTO v_media_estresse, v_count_alto
    FROM registros_emocionais
    WHERE id_setor = :NEW.id_setor
      AND data_registro >= CURRENT_TIMESTAMP - INTERVAL '7' DAY
      AND nivel_estresse >= 7;
    
    -- Se mais de 5 registros com estresse alto, gerar alerta crítico
    IF v_count_alto >= 5 AND v_media_estresse >= 7 THEN
        INSERT INTO alertas (id_setor, tipo_alerta, descricao, nivel_severidade)
        VALUES (
            :NEW.id_setor,
            'ESTRESSE_ALTO',
            'Padrão crítico detectado: ' || v_count_alto || ' colaboradores com estresse alto nos últimos 7 dias',
            'CRITICO'
        );
    END IF;
END;
/

-- =====================================================
-- DADOS DE EXEMPLO (para testes)
-- =====================================================

-- Inserir empresa exemplo
INSERT INTO empresas (nome_empresa, cnpj) VALUES ('FIAP Tecnologia S.A.', '12.345.678/0001-99');

-- Inserir setores exemplo
INSERT INTO setores (id_empresa, nome_setor, descricao) VALUES (1, 'Tecnologia', 'Desenvolvimento e Infraestrutura');
INSERT INTO setores (id_empresa, nome_setor, descricao) VALUES (1, 'Recursos Humanos', 'Gestão de Pessoas');
INSERT INTO setores (id_empresa, nome_setor, descricao) VALUES (1, 'Comercial', 'Vendas e Marketing');
INSERT INTO setores (id_empresa, nome_setor, descricao) VALUES (1, 'Financeiro', 'Contabilidade e Finanças');
INSERT INTO setores (id_empresa, nome_setor, descricao) VALUES (1, 'Operações', 'Logística e Produção');

-- Inserir colaboradores exemplo
INSERT INTO colaboradores (id_empresa, id_setor, nome_colaborador, email, codigo_acesso) 
VALUES (1, 1, 'João Silva', 'joao.silva@fiap.com.br', 'FIAP-TEC-001');

INSERT INTO colaboradores (id_empresa, id_setor, nome_colaborador, email, codigo_acesso) 
VALUES (1, 2, 'Maria Santos', 'maria.santos@fiap.com.br', 'FIAP-RH-001');

INSERT INTO colaboradores (id_empresa, id_setor, nome_colaborador, email, codigo_acesso) 
VALUES (1, 3, 'Pedro Oliveira', 'pedro.oliveira@fiap.com.br', 'FIAP-COM-001');

COMMIT;

