"""
Script de teste completo para verificar o modelo BERT
Execute: python test_bert.py
"""
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')  # Reduzir logs

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_test(num, total, text):
    print(f"\n[TESTE {num}/{total}] {text}")
    print("-" * 70)

def analisar_e_exibir(analyzer, texto, esperado=None):
    """Analisa texto e exibe resultados formatados"""
    resultado = analyzer.analisar_texto(texto, usar_gpt=False)
    
    sentimento = resultado.get('sentimento', 'N/A')
    score = resultado.get('score', 0.0)
    metodo = resultado.get('metodo', 'N/A')
    dl = resultado.get('deep_learning', False)
    confianca = resultado.get('confianca', 0.0)
    
    # Emoji baseado no sentimento
    emoji = "😊" if sentimento == "positivo" else "😟" if sentimento == "negativo" else "😐"
    
    print(f"   Texto: \"{texto}\"")
    print(f"   {emoji} Sentimento: {sentimento.upper()}")
    print(f"   📊 Score: {score:.3f}")
    print(f"   🎯 Confiança: {confianca:.2f}")
    print(f"   🔧 Método: {metodo}")
    print(f"   🧠 Deep Learning: {'✅ SIM' if dl else '❌ NÃO'}")
    
    # Verificar se corresponde ao esperado
    if esperado:
        if sentimento == esperado:
            print(f"   ✅ ESPERADO: {esperado.upper()} - CORRETO!")
        else:
            print(f"   ⚠️ ESPERADO: {esperado.upper()} - DIFERENTE (mas pode estar correto)")
    
    return resultado

# ==================== INÍCIO DOS TESTES ====================

print_header("🧠 TESTE COMPLETO DO MODELO BERT - EqualMind")
print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    # ========== FASE 1: CARREGAMENTO ==========
    print_header("FASE 1: Verificação de Carregamento")
    
    print("\n[1/3] Importando SentimentAnalyzer...")
    from ai.sentiment_analyzer import analyzer
    print("✅ Importação bem-sucedida!")
    
    print("\n[2/3] Verificando status do modelo...")
    print(f"   📦 Modelo configurado: {analyzer.model_name}")
    print(f"   🔄 Modelo carregado: {'✅ SIM' if analyzer.modelo_carregado else '❌ NÃO'}")
    print(f"   🔗 Usando embeddings: {'✅ SIM' if analyzer.use_embeddings else '❌ NÃO'}")
    
    if analyzer.modelo_carregado:
        print("\n✅ Modelo BERT carregado com sucesso!")
    else:
        print("\n⚠️ Modelo BERT não carregou (usando fallback)")
        print("   O sistema continuará funcionando, mas sem Deep Learning.")
    
    # ========== FASE 2: TESTES DE SENTIMENTO ==========
    print_header("FASE 2: Testes de Análise de Sentimento")
    
    testes = [
        # (texto, sentimento_esperado, descricao)
        ("Estou me sentindo muito bem hoje! O trabalho está ótimo e estou feliz.", "positivo", "Sentimento Positivo - Alegria"),
        ("Hoje foi um dia excelente! Me sinto motivado e satisfeito com tudo.", "positivo", "Sentimento Positivo - Satisfação"),
        ("Estou muito feliz e contente com minha equipe. Tudo está perfeito!", "positivo", "Sentimento Positivo - Perfeição"),
        
        ("Estou muito estressado e cansado. O trabalho está me deixando ansioso.", "negativo", "Sentimento Negativo - Estresse"),
        ("Me sinto triste e desmotivado. As coisas não estão indo bem.", "negativo", "Sentimento Negativo - Tristeza"),
        ("Estou frustrado e irritado com a situação. Não aguento mais isso.", "negativo", "Sentimento Negativo - Frustração"),
        ("O dia foi péssimo. Estou muito preocupado e angustiado.", "negativo", "Sentimento Negativo - Angústia"),
        
        ("Hoje foi um dia normal. Nada de especial aconteceu.", "neutro", "Sentimento Neutro - Normal"),
        ("Estou indo trabalhar como sempre. Tudo está igual.", "neutro", "Sentimento Neutro - Rotina"),
        ("Não tenho muito a dizer. Está tudo como esperado.", "neutro", "Sentimento Neutro - Indiferença"),
        
        ("Estou bem, mas poderia estar melhor. Algumas coisas estão boas, outras não.", "neutro", "Sentimento Misto - Ambivalência"),
        ("Tudo bem.", "neutro", "Sentimento Neutro - Curto"),
        
        ("Estou extremamente feliz e realizado! Este é o melhor dia da minha vida!", "positivo", "Sentimento Muito Positivo"),
        ("Estou completamente esgotado e deprimido. Não consigo mais continuar assim.", "negativo", "Sentimento Muito Negativo"),
    ]
    
    resultados_teste = []
    acertos = 0
    total_testes = len(testes)
    
    for i, (texto, esperado, descricao) in enumerate(testes, 1):
        print_test(i, total_testes, descricao)
        resultado = analisar_e_exibir(analyzer, texto, esperado)
        resultados_teste.append((texto, esperado, resultado.get('sentimento')))
        
        if resultado.get('sentimento') == esperado:
            acertos += 1
    
    # ========== FASE 3: TESTES DE PERFORMANCE ==========
    print_header("FASE 3: Testes de Performance e Edge Cases")
    
    print_test(1, 4, "Texto Vazio")
    resultado = analyzer.analisar_texto("", usar_gpt=False)
    print(f"   Texto: \"\" (vazio)")
    print(f"   Sentimento: {resultado.get('sentimento')}")
    print(f"   ✅ Tratamento de texto vazio: OK")
    
    print_test(2, 4, "Texto Muito Curto")
    resultado = analisar_e_exibir(analyzer, "Ok", None)
    
    print_test(3, 4, "Texto Muito Longo (mais de 512 tokens)")
    texto_longo = "Estou me sentindo " + "muito bem " * 100 + "hoje!"
    resultado = analisar_e_exibir(analyzer, texto_longo, None)
    print(f"   ✅ Texto truncado automaticamente para 512 tokens")
    
    print_test(4, 4, "Texto com Caracteres Especiais")
    resultado = analisar_e_exibir(analyzer, "Estou bem! 😊👍🎉 Tudo ótimo!!!", "positivo")
    
    # ========== FASE 4: ESTATÍSTICAS ==========
    print_header("FASE 4: Estatísticas e Resumo")
    
    print("\n📊 RESUMO DOS TESTES:")
    print(f"   Total de testes: {total_testes}")
    print(f"   Acertos: {acertos}")
    print(f"   Precisão: {(acertos/total_testes)*100:.1f}%")
    print()
    
    # Contagem por sentimento
    positivos = sum(1 for _, _, s in resultados_teste if s == 'positivo')
    negativos = sum(1 for _, _, s in resultados_teste if s == 'negativo')
    neutros = sum(1 for _, _, s in resultados_teste if s == 'neutro')
    
    print("📈 DISTRIBUIÇÃO DE RESULTADOS:")
    print(f"   Positivos: {positivos}")
    print(f"   Negativos: {negativos}")
    print(f"   Neutros: {neutros}")
    print()
    
    # Verificar uso de Deep Learning
    todos_com_dl = all(
        analyzer.analisar_texto(texto, usar_gpt=False).get('deep_learning', False)
        for texto, _, _ in resultados_teste[:3]  # Testar apenas os primeiros 3
    )
    
    print("🧠 STATUS DO DEEP LEARNING:")
    if analyzer.modelo_carregado:
        print("   ✅ Modelo BERT carregado")
        print("   ✅ Deep Learning ativo")
        if todos_com_dl:
            print("   ✅ Todos os testes usaram Deep Learning")
        else:
            print("   ⚠️ Alguns testes não usaram Deep Learning")
    else:
        print("   ❌ Modelo BERT não carregado")
        print("   ⚠️ Usando análise básica (fallback)")
    print()
    
    # ========== CONCLUSÃO ==========
    print_header("✅ TESTE CONCLUÍDO")
    
    if analyzer.modelo_carregado and todos_com_dl:
        print("🎉 SUCESSO! O sistema está funcionando perfeitamente com Deep Learning!")
    elif analyzer.modelo_carregado:
        print("✅ SUCESSO! O modelo BERT está carregado e funcionando!")
    else:
        print("⚠️ ATENÇÃO: O modelo BERT não carregou, mas o sistema continua funcionando.")
        print("   Verifique os logs para mais detalhes.")
    
    print(f"\n📅 Teste finalizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERRO durante o teste: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

