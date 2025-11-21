"""
Teste de conexão com Oracle Database da FIAP
"""
import oracledb
from config import Config
import os

# Inicializar Oracle Client de forma flexível
caminhos_possiveis = [
    r"C:\oracle\instantclient_23_4",
    r"C:\oracle\instantclient_21_3",
    r"C:\oracle\instantclient_19_3",
    os.getenv("ORACLE_HOME", ""),
    os.getenv("TNS_ADMIN", ""),
]

inicializado = False
for caminho in caminhos_possiveis:
    if caminho and os.path.exists(caminho):
        try:
            oracledb.init_oracle_client(lib_dir=caminho)
            print(f"Oracle Client inicializado (modo thick): {caminho}")
            inicializado = True
            break
        except Exception:
            continue

if not inicializado:
    print("Oracle Instant Client não encontrado. Usando modo thin (sem Instant Client necessário)")

print("Testando conexao com Oracle Database da FIAP...")
print(f"User: {Config.ORACLE_USER}")
print(f"DSN: {Config.ORACLE_DSN}")

try:
    connection = oracledb.connect(
        user=Config.ORACLE_USER,
        password=Config.ORACLE_PASSWORD,
        dsn=Config.ORACLE_DSN
    )
    print("==> CONEXAO ESTABELECIDA COM SUCESSO!")
    
    cursor = connection.cursor()
    
    # Testar query simples
    cursor.execute("SELECT 'Hello from Oracle!' FROM DUAL")
    result = cursor.fetchone()
    print(f"==> Query teste: {result[0]}")
    
    # Listar tabelas do usuário
    cursor.execute("""
        SELECT table_name FROM user_tables ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"\n==> Tabelas encontradas ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("\n==> Nenhuma tabela encontrada. Voce precisa executar o script schema.sql")
    
    cursor.close()
    connection.close()
    print("\n==> Teste concluido com sucesso!")
    
except oracledb.Error as error:
    error_obj, = error.args
    print(f"\n==> ERRO AO CONECTAR:")
    print(f"   Codigo: {error_obj.code}")
    print(f"   Mensagem: {error_obj.message}")
    print("\n==> Verifique:")
    print("   1. Credenciais (user/password)")
    print("   2. DSN (oracle.fiap.com.br:1521/orcl)")
    print("   3. Conexao com a internet/VPN da FIAP")
except Exception as e:
    print(f"\n==> Erro inesperado: {e}")

