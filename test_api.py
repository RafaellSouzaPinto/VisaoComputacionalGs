"""
Script de teste da API EqualMind
Execute: python test_api.py
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_health():
    """Testa health check"""
    print("\n🔍 Testando Health Check...")
    response = requests.get(f"{API_BASE}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_setores():
    """Testa listagem de setores"""
    print("\n🏢 Testando Listagem de Setores...")
    response = requests.get(f"{API_BASE}/setores/1")
    print(f"   Status: {response.status_code}")
    data = response.json()
    if data.get('success'):
        print(f"   ✅ {len(data['setores'])} setores encontrados")
        for setor in data['setores']:
            print(f"      - {setor['NOME_SETOR']}")
    return response.status_code == 200

def test_registro():
    """Testa criação de registro emocional"""
    print("\n📝 Testando Criação de Registro...")
    
    payload = {
        "colaborador_id": 1,
        "setor_id": 1,
        "nivel_estresse": 6,
        "nivel_felicidade": 7,
        "nivel_ansiedade": 5,
        "nivel_motivacao": 8,
        "comentario": "Teste automático - Me sinto muito bem hoje!",
        "anonimo": "N"
    }
    
    response = requests.post(
        f"{API_BASE}/registro-emocional",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print(f"   ✅ Registro criado: ID {data['registro_id']}")
        
        if data.get('analise_numerica'):
            an = data['analise_numerica']
            print(f"   📊 Índice Bem-Estar: {an['indice_bem_estar']}/100")
            print(f"   📊 Classificação: {an['classificacao']}")
        
        if data.get('analise_sentimento'):
            sent = data['analise_sentimento']
            print(f"   🧠 Sentimento: {sent['sentimento']} (score: {sent['score']})")
    else:
        print(f"   ❌ Erro: {data.get('error')}")
    
    return response.status_code == 200

def test_mapa_calor():
    """Testa geração de mapa de calor"""
    print("\n🔥 Testando Geração de Mapa de Calor...")
    response = requests.get(f"{API_BASE}/mapa-calor/1?metrica=estresse&dias=30")
    print(f"   Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print(f"   ✅ Mapa gerado para {data['total_setores']} setores")
        print(f"   📅 Período: {data['periodo_dias']} dias")
    else:
        print(f"   ⚠️ Aviso: {data.get('error')}")
    
    return response.status_code in [200, 404]

def test_estatisticas():
    """Testa estatísticas gerais"""
    print("\n📈 Testando Estatísticas...")
    response = requests.get(f"{API_BASE}/estatisticas/1")
    print(f"   Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        stats = data['estatisticas']
        print(f"   ✅ Colaboradores: {stats.get('TOTAL_COLABORADORES', 0)}")
        print(f"   ✅ Registros: {stats.get('TOTAL_REGISTROS', 0)}")
        print(f"   ✅ Estresse Médio: {stats.get('MEDIA_ESTRESSE_GERAL', 0)}")
        print(f"   ✅ Felicidade Média: {stats.get('MEDIA_FELICIDADE_GERAL', 0)}")
    
    return response.status_code == 200

def test_coach_virtual():
    """Testa coach virtual com IA"""
    print("\n🤖 Testando Coach Virtual IA...")
    
    payload = {
        "mensagem": "Como lidar com estresse no trabalho?"
    }
    
    response = requests.post(
        f"{API_BASE}/coach-virtual",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print(f"   ✅ Coach respondeu:")
        print(f"      {data['resposta'][:100]}...")
        return True
    elif response.status_code == 503:
        print(f"   ⚠️ Serviço GPT não disponível (configure API key)")
        return True  # Não falha o teste
    else:
        print(f"   ❌ Erro: {data.get('error')}")
        return False

def test_recomendacoes_ia():
    """Testa recomendações com IA"""
    print("\n🎯 Testando Recomendações IA...")
    
    payload = {
        "nivel_estresse": 8,
        "nivel_felicidade": 4,
        "nivel_ansiedade": 7,
        "nivel_motivacao": 3,
        "comentario": "Me sinto muito sobrecarregado"
    }
    
    response = requests.post(
        f"{API_BASE}/recomendacoes-ia",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        rec = data['recomendacoes']
        print(f"   ✅ Prioridade: {rec['prioridade']}")
        print(f"   ✅ {len(rec['acoes_imediatas'])} ações recomendadas")
        return True
    elif response.status_code == 503:
        print(f"   ⚠️ Serviço GPT não disponível")
        return True
    else:
        print(f"   ❌ Erro: {data.get('error')}")
        return False

def main():
    print("=" * 60)
    print("  🧠 EqualMind - Teste da API")
    print("=" * 60)
    print("\n⚠️  Certifique-se de que o servidor está rodando!")
    print("   Execute: python app.py")
    
    input("\nPressione ENTER para iniciar os testes...")
    
    results = []
    
    try:
        results.append(("Health Check", test_health()))
        results.append(("Listagem Setores", test_setores()))
        results.append(("Criar Registro", test_registro()))
        results.append(("Mapa de Calor", test_mapa_calor()))
        results.append(("Estatísticas", test_estatisticas()))
        results.append(("🤖 Coach Virtual IA", test_coach_virtual()))
        results.append(("🎯 Recomendações IA", test_recomendacoes_ia()))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor!")
        print("   Verifique se o servidor Flask está rodando (python app.py)")
        return
    
    # Resumo
    print("\n" + "=" * 60)
    print("  📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for nome, sucesso in results:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"   {status}: {nome}")
    
    total = len(results)
    passou = sum(1 for _, s in results if s)
    
    print(f"\n   Total: {passou}/{total} testes passaram")
    
    if passou == total:
        print("\n   🎉 Todos os testes passaram com sucesso!")
    else:
        print("\n   ⚠️ Alguns testes falharam. Verifique os logs acima.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

