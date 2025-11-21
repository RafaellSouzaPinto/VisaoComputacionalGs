#!/bin/bash

echo "=========================================="
echo "   Work Well - Iniciando Aplicação"
echo "=========================================="
echo ""

# Ativar ambiente virtual
echo "[1/3] Ativando ambiente virtual..."
source venv/bin/activate

# Verificar conexão com banco
echo ""
echo "[2/3] Verificando conexão com Oracle..."
python3 -c "from database.db_connection import db; db.connect(); print('✅ Conexão OK!')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERRO: Não foi possível conectar ao Oracle!"
    echo "Verifique se o banco está rodando e as credenciais no .env"
    exit 1
fi

# Iniciar servidor Flask
echo ""
echo "[3/3] Iniciando servidor Flask..."
echo ""
echo "=========================================="
echo "   Acesse: http://localhost:5000"
echo "=========================================="
echo ""
python3 app.py

