@echo off
echo ==========================================
echo    EqualMind - Iniciando Aplicacao
echo ==========================================
echo.

REM Ativar ambiente virtual
echo [1/3] Ativando ambiente virtual...
call venv\Scripts\activate

REM Verificar conexao com banco
echo.
echo [2/3] Verificando conexao com Oracle...
python -c "from database.db_connection import db; db.connect(); print('   Conexao OK!')" 2>nul
if errorlevel 1 (
    echo    ERRO: Nao foi possivel conectar ao Oracle!
    echo    Verifique se o banco esta rodando e as credenciais no .env
    pause
    exit /b 1
)

REM Iniciar servidor Flask
echo.
echo [3/3] Iniciando servidor Flask...
echo.
echo ==========================================
echo    Acesse: http://localhost:5000
echo ==========================================
echo.
python app.py

pause

