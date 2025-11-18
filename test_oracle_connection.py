"""
Teste de conexão com Oracle Database da FIAP
"""
import cx_Oracle
from config import Config

# Inicializar Oracle Client explicitamente
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_4")
    print("Oracle Client inicializado: C:\\oracle\\instantclient_23_4")
except Exception as e:
    print(f"Aviso ao inicializar Oracle Client: {e}")

print("Testando conexao com Oracle Database da FIAP...")
print(f"User: {Config.ORACLE_USER}")
print(f"DSN: {Config.ORACLE_DSN}")

try:
    connection = cx_Oracle.connect(
        user=Config.ORACLE_USER,
        password=Config.ORACLE_PASSWORD,
        dsn=Config.ORACLE_DSN,
        encoding="UTF-8"
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
    
except cx_Oracle.Error as error:
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

