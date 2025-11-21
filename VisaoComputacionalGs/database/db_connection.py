"""
EqualMind - Conexão com Oracle Database
"""
import cx_Oracle
from config import Config
import logging

# Inicializar Oracle Instant Client
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_4")
    print("[OK] Oracle Client inicializado")
except Exception as e:
    print(f"[INFO] Oracle Client ja inicializado ou erro: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar auto create após logging estar configurado
from database.auto_create_tables import create_tables_if_not_exist


class OracleDB:
    """Gerenciador de conexão Oracle"""
    
    def __init__(self):
        self.user = Config.ORACLE_USER
        self.password = Config.ORACLE_PASSWORD
        self.dsn = Config.ORACLE_DSN
        self.connection = None
    
    def connect(self):
        """Estabelece conexão com o banco"""
        try:
            self.connection = cx_Oracle.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn,
                encoding="UTF-8"
            )
            logger.info("Conexao com Oracle estabelecida com sucesso!")
            
            # Criação automática de tabelas
            try:
                create_tables_if_not_exist(self.connection)
                logger.info("✅ Tabelas verificadas/criadas automaticamente")
            except Exception as e:
                logger.warning(f"⚠️ Aviso ao criar tabelas (continuando): {e}")
            
            return self.connection
        except cx_Oracle.Error as error:
            logger.error(f"Erro ao conectar ao Oracle: {error}")
            raise
    
    def disconnect(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            logger.info("Conexao com Oracle encerrada")
    
    def execute_query(self, query, params=None):
        """Executa uma query SELECT e retorna resultados"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor:
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            return results
        except cx_Oracle.Error as error:
            logger.error(f"Erro ao executar query: {error}")
            raise
    
    def execute_insert(self, query, params):
        """Executa INSERT/UPDATE/DELETE"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except cx_Oracle.Error as error:
            logger.error(f"Erro ao executar INSERT: {error}")
            self.connection.rollback()
            raise
    
    def inserir_registro_emocional(self, colaborador_id, empresa_id, setor_id, nivel_estresse, nivel_felicidade, nivel_ansiedade, nivel_motivacao, comentario, sentimento_texto, score_sentimento):
        """Insere um novo registro emocional"""
        query = """
        INSERT INTO REGISTROS_EMOCIONAIS_WorkWell 
        (COLABORADOR_ID, EMPRESA_ID, SETOR_ID, NIVEL_ESTRESSE, NIVEL_FELICIDADE, NIVEL_ANSIEDADE, NIVEL_MOTIVACAO, COMENTARIO, SENTIMENTO_TEXTO, SCORE_SENTIMENTO)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
        """
        params = (colaborador_id, empresa_id, setor_id, nivel_estresse, nivel_felicidade, nivel_ansiedade, nivel_motivacao, comentario, sentimento_texto, score_sentimento)
        return self.execute_insert(query, params)
    
    def obter_setores(self, empresa_id):
        """Retorna lista de setores da empresa"""
        query = """
            SELECT ID, NOME, DESCRICAO 
            FROM SETORES_WorkWell 
            WHERE EMPRESA_ID = :1
            ORDER BY NOME
        """
        return self.execute_query(query, (empresa_id,))
    
    def obter_dados_mapa_calor(self, empresa_id, dias=30):
        """Obtém dados para gerar mapa de calor"""
        query = f"""
        SELECT
            S.NOME AS SETOR_NOME,
            ROUND(AVG(R.NIVEL_ESTRESSE), 1) AS MEDIA_ESTRESSE,
            ROUND(AVG(R.NIVEL_FELICIDADE), 1) AS MEDIA_FELICIDADE,
            ROUND(AVG(R.NIVEL_ANSIEDADE), 1) AS MEDIA_ANSIEDADE,
            ROUND(AVG(R.NIVEL_MOTIVACAO), 1) AS MEDIA_MOTIVACAO,
            COUNT(R.ID) AS TOTAL_REGISTROS
        FROM
            REGISTROS_EMOCIONAIS_WorkWell R
        JOIN
            SETORES_WorkWell S ON R.SETOR_ID = S.ID
        WHERE
            R.EMPRESA_ID = :1
            AND R.DATA_REGISTRO >= SYSTIMESTAMP - INTERVAL '{dias}' DAY
        GROUP BY
            S.NOME
        ORDER BY
            S.NOME
        """
        return self.execute_query(query, (empresa_id,))
    
    def obter_estatisticas(self, empresa_id, dias=30):
        """Obtém estatísticas gerais da empresa"""
        query = f"""
        SELECT
            ROUND(AVG(NIVEL_ESTRESSE), 1) AS MEDIA_ESTRESSE,
            ROUND(AVG(NIVEL_FELICIDADE), 1) AS MEDIA_FELICIDADE,
            ROUND(AVG(NIVEL_ANSIEDADE), 1) AS MEDIA_ANSIEDADE,
            ROUND(AVG(NIVEL_MOTIVACAO), 1) AS MEDIA_MOTIVACAO,
            COUNT(ID) AS TOTAL_REGISTROS,
            COUNT(DISTINCT COLABORADOR_ID) AS TOTAL_COLABORADORES
        FROM
            REGISTROS_EMOCIONAIS_WorkWell
        WHERE
            EMPRESA_ID = :1
            AND DATA_REGISTRO >= SYSTIMESTAMP - INTERVAL '{dias}' DAY
        """
        results = self.execute_query(query, (empresa_id,))
        return results[0] if results else None
    
    def obter_dashboard_rh(self, empresa_id):
        """Retorna dados do dashboard RH"""
        return self.obter_dados_mapa_calor(empresa_id, 30)
    
    def insert_registro_emocional(self, colaborador_id, setor_id, estresse, felicidade, ansiedade=5, motivacao=5, comentario='', anonimo='N'):
        """Insere um novo registro emocional no banco."""
        try:
            cursor = self.connection.cursor()
            
            # Variável de saída para capturar o ID gerado
            registro_id_var = cursor.var(cx_Oracle.NUMBER)
            
            # SQL de inserção com RETURNING para obter o ID gerado
            sql = """
                INSERT INTO REGISTROS_EMOCIONAIS_WorkWell 
                (COLABORADOR_ID, EMPRESA_ID, SETOR_ID, NIVEL_ESTRESSE, NIVEL_FELICIDADE, 
                 NIVEL_ANSIEDADE, NIVEL_MOTIVACAO, COMENTARIO, DATA_REGISTRO)
                VALUES 
                (:colaborador_id, 1, :setor_id, :estresse, :felicidade, 
                 :ansiedade, :motivacao, :comentario, SYSTIMESTAMP)
                RETURNING ID INTO :registro_id
            """
            
            cursor.execute(sql, {
                'colaborador_id': colaborador_id,
                'setor_id': setor_id,
                'estresse': estresse,
                'felicidade': felicidade,
                'ansiedade': ansiedade,
                'motivacao': motivacao,
                'comentario': comentario,
                'registro_id': registro_id_var
            })
            
            self.connection.commit()
            
            # Obter o ID gerado
            registro_id = registro_id_var.getvalue()[0]
            
            logger.info(f"[OK] Registro emocional inserido com sucesso (ID: {registro_id})")
            return registro_id
            
        except cx_Oracle.Error as e:
            logger.error(f"[ERRO] Ao inserir registro emocional: {e}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def atualizar_sentimento(self, registro_id, sentimento, score):
        """Atualiza o sentimento e score de um registro emocional"""
        try:
            cursor = self.connection.cursor()
            
            sql = """
                UPDATE REGISTROS_EMOCIONAIS_WorkWell
                SET SENTIMENTO_TEXTO = :sentimento,
                    SCORE_SENTIMENTO = :score
                WHERE ID = :registro_id
            """
            
            cursor.execute(sql, {
                'sentimento': sentimento,
                'score': score,
                'registro_id': registro_id
            })
            
            self.connection.commit()
            logger.info(f"[OK] Sentimento atualizado para registro {registro_id}")
            
        except cx_Oracle.Error as e:
            logger.error(f"[ERRO] Ao atualizar sentimento: {e}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()


# Instância global
db = OracleDB()
try:
    db.connect()
except Exception as e:
    logger.error(f"Erro ao conectar ao banco na inicializacao: {e}")
    db.connection = None
