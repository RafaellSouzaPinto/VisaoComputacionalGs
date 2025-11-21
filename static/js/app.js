/**
 * Work Well - Frontend JavaScript
 * Sistema de Análise Emocional Corporativa
 */

// =====================================================
// Configurações e Variáveis Globais
// =====================================================

const API_BASE_URL = "http://localhost:5000/api";
const EMPRESA_ID = 1; // ID da empresa padrão (FIAP)

// =====================================================
// Inicialização
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Work Well iniciado!");

  // Inicializar componentes
  inicializarNavegacao();
  inicializarSliders();
  inicializarFormulario();
  carregarSetores();
  carregarColaboradores();

  // Event listeners
  document
    .getElementById("btnGerarMapa")
    .addEventListener("click", gerarMapaCalor);
  document
    .getElementById("btnDashboardCompleto")
    .addEventListener("click", gerarDashboardCompleto);
  document
    .getElementById("btnEnviarChat")
    .addEventListener("click", enviarMensagemCoach);
  document
    .getElementById("btnRelatorioIA")
    .addEventListener("click", gerarRelatorioIA);

  // Enter no chat
  document.getElementById("chatInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      enviarMensagemCoach();
    }
  });

  // Sugestões de chat
  document.querySelectorAll(".btn-sugestao").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mensagem = btn.getAttribute("data-mensagem");
      document.getElementById("chatInput").value = mensagem;
      enviarMensagemCoach();
    });
  });
});

// =====================================================
// Navegação entre Seções
// =====================================================

function inicializarNavegacao() {
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();

      // Remover active de todos
      navLinks.forEach((l) => l.classList.remove("active"));
      document
        .querySelectorAll(".section")
        .forEach((s) => s.classList.remove("active"));

      // Ativar clicado
      link.classList.add("active");
      const targetId = link.getAttribute("href").substring(1);
      document.getElementById(targetId).classList.add("active");

      // Carregar dados se necessário
      if (targetId === "dashboard") {
        carregarDashboard();
      } else if (targetId === "mapas") {
        // Scroll suave para mapas
        document
          .getElementById(targetId)
          .scrollIntoView({ behavior: "smooth" });
      }
    });
  });
}

// =====================================================
// Sliders (Range Inputs)
// =====================================================

function inicializarSliders() {
  const sliders = [
    { id: "estresse", valorId: "valorEstresse" },
    { id: "felicidade", valorId: "valorFelicidade" },
    { id: "ansiedade", valorId: "valorAnsiedade" },
    { id: "motivacao", valorId: "valorMotivacao" },
  ];

  sliders.forEach((slider) => {
    const input = document.getElementById(slider.id);
    const valorDisplay = document.getElementById(slider.valorId);

    input.addEventListener("input", (e) => {
      valorDisplay.textContent = e.target.value;
      atualizarCorValor(valorDisplay, slider.id, parseInt(e.target.value));
    });
  });
}

function atualizarCorValor(elemento, tipo, valor) {
  // Atualizar cor do badge baseado no valor
  let cor;
  if (tipo === "estresse" || tipo === "ansiedade") {
    if (valor >= 8) cor = "#e74c3c";
    else if (valor >= 6) cor = "#f39c12";
    else cor = "#2ecc71";
  } else {
    if (valor >= 8) cor = "#2ecc71";
    else if (valor >= 5) cor = "#f39c12";
    else cor = "#e74c3c";
  }
  elemento.style.background = cor;
}

// =====================================================
// Carregar Dados
// =====================================================

async function carregarSetores() {
  try {
    const response = await fetch(`${API_BASE_URL}/setores/${EMPRESA_ID}`);
    const data = await response.json();

    if (data.success && data.setores && data.setores.length > 0) {
      const select = document.getElementById("setor");
      select.innerHTML = '<option value="">Selecione seu setor</option>';

      data.setores.forEach((setor) => {
        const option = document.createElement("option");
        option.value = setor.ID; // Corrigido: ID ao invés de ID_SETOR
        option.textContent = setor.NOME; // Corrigido: NOME ao invés de NOME_SETOR
        select.appendChild(option);
      });

      console.log(`✅ ${data.setores.length} setores carregados`);
    } else {
      console.warn("Nenhum setor encontrado");
    }
  } catch (error) {
    console.error("Erro ao carregar setores:", error);
    mostrarNotificacao("Erro ao carregar setores", "error");
  }
}

async function carregarColaboradores() {
  // Simulação - Em produção, buscar da API
  const select = document.getElementById("colaborador");
  const colaboradores = [
    { id: 1, nome: "João Silva" },
    { id: 2, nome: "Maria Santos" },
    { id: 3, nome: "Pedro Oliveira" },
  ];

  select.innerHTML = '<option value="">Selecione seu nome</option>';
  colaboradores.forEach((colab) => {
    const option = document.createElement("option");
    option.value = colab.id;
    option.textContent = colab.nome;
    select.appendChild(option);
  });
}

// =====================================================
// Formulário de Registro
// =====================================================

function inicializarFormulario() {
  const form = document.getElementById("formRegistro");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await enviarRegistro();
  });
}

async function enviarRegistro() {
  // Coletar dados
  const dados = {
    colaborador_id: parseInt(document.getElementById("colaborador").value),
    setor_id: parseInt(document.getElementById("setor").value),
    nivel_estresse: parseInt(document.getElementById("estresse").value),
    nivel_felicidade: parseInt(document.getElementById("felicidade").value),
    nivel_ansiedade: parseInt(document.getElementById("ansiedade").value),
    nivel_motivacao: parseInt(document.getElementById("motivacao").value),
    comentario: document.getElementById("comentario").value,
    anonimo: document.getElementById("anonimo").checked ? "S" : "N",
  };

  // Validar
  if (!dados.colaborador_id || !dados.setor_id) {
    mostrarNotificacao(
      "Por favor, preencha todos os campos obrigatórios",
      "error"
    );
    return;
  }

  try {
    mostrarLoading(true);

    const response = await fetch(`${API_BASE_URL}/registro-emocional`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });

    const result = await response.json();

    if (result.success) {
      mostrarNotificacao("✅ Registro enviado com sucesso!", "success");
      mostrarAnalise(result);

      // 🚀 Buscar recomendações IA
      buscarRecomendacoesIA(dados);

      document.getElementById("formRegistro").reset();
      // Resetar sliders
      ["estresse", "felicidade", "ansiedade", "motivacao"].forEach((id) => {
        document.getElementById(id).value = 5;
        document.getElementById(
          "valor" + id.charAt(0).toUpperCase() + id.slice(1)
        ).textContent = "5";
      });
    } else {
      mostrarNotificacao(
        "❌ Erro ao enviar registro: " + result.error,
        "error"
      );
    }
  } catch (error) {
    console.error("Erro ao enviar registro:", error);
    mostrarNotificacao("❌ Erro ao conectar com o servidor", "error");
  } finally {
    mostrarLoading(false);
  }
}

function mostrarAnalise(result) {
  const container = document.getElementById("resultadoAnalise");
  const conteudo = document.getElementById("conteudoAnalise");

  let html = "";

  // Análise Numérica
  if (result.analise_numerica) {
    const analise = result.analise_numerica;
    html += `
            <div class="analise-box">
                <h4>📊 Índice de Bem-Estar: ${analise.indice_bem_estar}/100</h4>
                <p><strong>Classificação:</strong> ${analise.classificacao.toUpperCase()}</p>
                <p><strong>Recomendação:</strong> ${analise.recomendacao}</p>
                ${
                  analise.problemas.length > 0
                    ? `
                    <p><strong>⚠️ Pontos de Atenção:</strong></p>
                    <ul>
                        ${analise.problemas
                          .map((p) => `<li>${p}</li>`)
                          .join("")}
                    </ul>
                `
                    : ""
                }
            </div>
        `;
  }

  // Análise de Sentimento
  if (result.analise_sentimento) {
    const sentimento = result.analise_sentimento;
    const emoji =
      sentimento.sentimento === "positivo"
        ? "😊"
        : sentimento.sentimento === "negativo"
        ? "😢"
        : "😐";

    html += `
            <div class="analise-box">
                <h4>${emoji} Análise de Sentimento (IA)</h4>
                <p><strong>Sentimento Detectado:</strong> ${sentimento.sentimento.toUpperCase()}</p>
                <p><strong>Score:</strong> ${sentimento.score} (Confiança: ${
      sentimento.confianca
    })</p>
                ${
                  sentimento.metodo === "hibrido"
                    ? "<p>✨ <strong>Análise híbrida com GPT</strong></p>"
                    : ""
                }
            </div>
        `;

    // Mostrar análise avançada do GPT se disponível
    if (sentimento.gpt_analise) {
      const gpt = sentimento.gpt_analise;
      html += `
                <div class="analise-box">
                    <h4>🤖 Análise Avançada com GPT</h4>
                    <p><strong>Emoções:</strong> ${
                      gpt.emocoes_detectadas
                        ? gpt.emocoes_detectadas.join(", ")
                        : "N/A"
                    }</p>
                    <p><strong>Intensidade:</strong> ${
                      gpt.intensidade || "N/A"
                    }</p>
                    ${
                      gpt.recomendacao_imediata
                        ? `<p><strong>💡 Recomendação:</strong> ${gpt.recomendacao_imediata}</p>`
                        : ""
                    }
                </div>
            `;
    }
  }

  conteudo.innerHTML = html;
  container.classList.remove("hidden");

  // Scroll suave
  container.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// =====================================================
// Recomendações IA
// =====================================================

async function buscarRecomendacoesIA(dados) {
  try {
    const response = await fetch(`${API_BASE_URL}/recomendacoes-ia`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });

    const result = await response.json();

    if (result.success) {
      mostrarRecomendacoesIA(result.recomendacoes);
    }
  } catch (error) {
    console.log("Recomendações IA não disponíveis:", error);
  }
}

function mostrarRecomendacoesIA(recomendacoes) {
  const container = document.getElementById("resultadoAnalise");
  const conteudoAtual = document.getElementById("conteudoAnalise").innerHTML;

  let html = `
        <div class="analise-box">
            <h4>🎯 Recomendações Personalizadas (IA Generativa)</h4>
            <p><strong>Prioridade:</strong> ${recomendacoes.prioridade.toUpperCase()}</p>
            
            <p><strong>✅ Ações Imediatas:</strong></p>
            <ul>
                ${recomendacoes.acoes_imediatas
                  .map((acao) => `<li>${acao}</li>`)
                  .join("")}
            </ul>
            
            ${
              recomendacoes.habitos_sugeridos
                ? `
                <p><strong>🌱 Hábitos Sugeridos:</strong></p>
                <ul>
                    ${recomendacoes.habitos_sugeridos
                      .map((habito) => `<li>${habito}</li>`)
                      .join("")}
                </ul>
            `
                : ""
            }
            
            <p style="margin-top: 1rem; font-style: italic;">💬 ${
              recomendacoes.mensagem_motivacional
            }</p>
        </div>
    `;

  document.getElementById("conteudoAnalise").innerHTML = conteudoAtual + html;
}

// =====================================================
// Dashboard
// =====================================================

async function carregarDashboard() {
  try {
    mostrarLoading(true);

    // Carregar estatísticas
    const statsResponse = await fetch(
      `${API_BASE_URL}/estatisticas/${EMPRESA_ID}`
    );
    const statsData = await statsResponse.json();

    if (statsData.success) {
      const stats = statsData.estatisticas;
      document.getElementById("statColaboradores").textContent =
        stats.total_colaboradores || 0;
      document.getElementById("statRegistros").textContent =
        stats.total_registros || 0;
      document.getElementById("statEstresse").textContent = (
        stats.media_estresse || 0
      ).toFixed(1);
      document.getElementById("statFelicidade").textContent = (
        stats.media_felicidade || 0
      ).toFixed(1);
    }

    // Carregar dashboard completo
    const dashResponse = await fetch(`${API_BASE_URL}/dashboard/${EMPRESA_ID}`);
    const dashData = await dashResponse.json();

    if (dashData.success) {
      renderizarTabelaDashboard(dashData.dashboard_rh);
    }
  } catch (error) {
    console.error("Erro ao carregar dashboard:", error);
    mostrarNotificacao("Erro ao carregar dashboard", "error");
  } finally {
    mostrarLoading(false);
  }
}

function renderizarTabelaDashboard(dados) {
  const container = document.getElementById("tabelaDashboard");

  if (!dados || dados.length === 0) {
    container.innerHTML = '<p class="info-text">Nenhum dado disponível</p>';
    return;
  }

  let html = `
        <table>
            <thead>
                <tr>
                    <th>Setor</th>
                    <th>Registros</th>
                    <th>Estresse Médio</th>
                    <th>Felicidade Média</th>
                    <th>Ansiedade Média</th>
                    <th>Motivação Média</th>
                </tr>
            </thead>
            <tbody>
    `;

  dados.forEach((setor) => {
    // Calcular status baseado no estresse
    const estresse = parseFloat(setor.MEDIA_ESTRESSE || 0);
    let status = "bom";
    if (estresse >= 7) status = "critico";
    else if (estresse >= 5) status = "atencao";

    const badgeClass = `badge-${status}`;
    html += `
            <tr>
                <td><strong>${setor.SETOR_NOME}</strong></td>
                <td>${setor.TOTAL_REGISTROS || 0}</td>
                <td>${(setor.MEDIA_ESTRESSE || 0).toFixed(1)}</td>
                <td>${(setor.MEDIA_FELICIDADE || 0).toFixed(1)}</td>
                <td>${(setor.MEDIA_ANSIEDADE || 0).toFixed(1)}</td>
                <td>${(setor.MEDIA_MOTIVACAO || 0).toFixed(1)}</td>
            </tr>
        `;
  });

  html += `
            </tbody>
        </table>
    `;

  container.innerHTML = html;
}

// =====================================================
// Mapas de Calor
// =====================================================

async function gerarMapaCalor() {
  const metrica = document.getElementById("metricaMapa").value;
  const dias = document.getElementById("diasAnalise").value;

  if (!metrica) {
    mostrarNotificacao("Selecione uma métrica", "error");
    return;
  }

  try {
    mostrarLoading(true);

    const response = await fetch(
      `${API_BASE_URL}/mapa-calor/${EMPRESA_ID}?metrica=${metrica}&dias=${dias}`
    );
    const data = await response.json();

    if (data.success && data.mapa_base64) {
      const container = document.getElementById("mapaContainer");
      // O backend já retorna com o prefixo data:image/png;base64, então usar diretamente
      const imagemSrc = data.mapa_base64.startsWith("data:")
        ? data.mapa_base64
        : `data:image/png;base64,${data.mapa_base64}`;
      container.innerHTML = `<img src="${imagemSrc}" alt="Mapa de Calor - ${metrica}" style="max-width: 100%; height: auto;">`;
      mostrarNotificacao("✅ Mapa de calor gerado com sucesso!", "success");
    } else {
      mostrarNotificacao(
        "❌ Nenhum dado disponível para gerar mapa",
        "warning"
      );
      console.log("Dados:", data);
    }
  } catch (error) {
    console.error("Erro ao gerar mapa:", error);
    mostrarNotificacao("❌ Erro ao conectar com o servidor", "error");
  } finally {
    mostrarLoading(false);
  }
}

async function gerarDashboardCompleto() {
  const dias = document.getElementById("diasAnalise").value;

  try {
    mostrarLoading(true);

    const response = await fetch(
      `${API_BASE_URL}/dashboard/${EMPRESA_ID}?dias=${dias}`
    );
    const data = await response.json();

    if (data.success && data.visualizacoes) {
      const container = document.getElementById("visualizacoesCompletas");
      const visualizacoes = data.visualizacoes;

      let html = "";

      if (visualizacoes.mapa_estresse) {
        html += `
                    <div class="visualizacao-item">
                        <h4>Mapa de Calor - Estresse</h4>
                        <img src="${visualizacoes.mapa_estresse}" alt="Mapa Estresse">
                    </div>
                `;
      }

      if (visualizacoes.mapa_felicidade) {
        html += `
                    <div class="visualizacao-item">
                        <h4>Mapa de Calor - Felicidade</h4>
                        <img src="${visualizacoes.mapa_felicidade}" alt="Mapa Felicidade">
                    </div>
                `;
      }

      if (visualizacoes.comparativo) {
        html += `
                    <div class="visualizacao-item">
                        <h4>Comparativo de Métricas</h4>
                        <img src="${visualizacoes.comparativo}" alt="Comparativo">
                    </div>
                `;
      }

      if (visualizacoes.barras) {
        html += `
                    <div class="visualizacao-item">
                        <h4>Análise por Setor</h4>
                        <img src="${visualizacoes.barras}" alt="Gráfico de Barras">
                    </div>
                `;
      }

      container.innerHTML = html;
      mostrarNotificacao("✅ Dashboard completo gerado!", "success");
    } else {
      mostrarNotificacao("❌ Erro ao gerar dashboard completo", "error");
    }
  } catch (error) {
    console.error("Erro ao gerar dashboard:", error);
    mostrarNotificacao("❌ Erro ao conectar com o servidor", "error");
  } finally {
    mostrarLoading(false);
  }
}

// =====================================================
// Utilitários
// =====================================================

function mostrarLoading(exibir) {
  const overlay = document.getElementById("loadingOverlay");
  if (exibir) {
    overlay.classList.remove("hidden");
  } else {
    overlay.classList.add("hidden");
  }
}

function mostrarNotificacao(mensagem, tipo = "info") {
  // Criar elemento de notificação
  const notif = document.createElement("div");
  notif.className = `notificacao notificacao-${tipo}`;
  notif.textContent = mensagem;
  notif.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${
          tipo === "success"
            ? "#2ecc71"
            : tipo === "error"
            ? "#e74c3c"
            : "#3498db"
        };
        color: white;
        border-radius: 5px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
    `;

  document.body.appendChild(notif);

  // Remover após 5 segundos
  setTimeout(() => {
    notif.style.animation = "slideOut 0.3s ease-out";
    setTimeout(() => notif.remove(), 300);
  }, 5000);
}

// Adicionar animações CSS
const style = document.createElement("style");
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// =====================================================
// Coach Virtual IA
// =====================================================

let historicoChat = [];

async function enviarMensagemCoach() {
  const input = document.getElementById("chatInput");
  const mensagem = input.value.trim();

  if (!mensagem) return;

  // Adicionar mensagem do usuário
  adicionarMensagemChat("user", mensagem);
  input.value = "";

  // Adicionar ao histórico
  historicoChat.push({ role: "user", content: mensagem });

  try {
    mostrarLoading(true);

    const response = await fetch(`${API_BASE_URL}/coach-virtual`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mensagem: mensagem,
        historico: historicoChat.slice(-10), // Últimas 5 interações
      }),
    });

    const result = await response.json();

    if (result.success) {
      adicionarMensagemChat("bot", result.resposta);
      historicoChat.push({ role: "assistant", content: result.resposta });
    } else {
      adicionarMensagemChat(
        "bot",
        "Desculpe, não consegui processar sua mensagem. Tente novamente."
      );
    }
  } catch (error) {
    console.error("Erro no coach:", error);
    adicionarMensagemChat(
      "bot",
      "Desculpe, o serviço está temporariamente indisponível."
    );
  } finally {
    mostrarLoading(false);
  }
}

function adicionarMensagemChat(tipo, texto) {
  const container = document.getElementById("chatMessages");
  const avatar = tipo === "bot" ? "🤖" : "👤";
  const classeTipo = tipo === "bot" ? "bot-message" : "user-message";

  const mensagemDiv = document.createElement("div");
  mensagemDiv.className = `chat-message ${classeTipo}`;
  mensagemDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${texto}</p>
        </div>
    `;

  container.appendChild(mensagemDiv);
  container.scrollTop = container.scrollHeight;
}

// =====================================================
// Relatório IA
// =====================================================

async function gerarRelatorioIA() {
  try {
    mostrarLoading(true);

    const response = await fetch(`${API_BASE_URL}/relatorio-ia/${EMPRESA_ID}`);
    const data = await response.json();

    if (data.success) {
      mostrarRelatorioIA(data.relatorio);
      mostrarNotificacao("✅ Relatório IA gerado com sucesso!", "success");
    } else {
      mostrarNotificacao("❌ Erro: " + data.error, "error");
    }
  } catch (error) {
    console.error("Erro ao gerar relatório IA:", error);
    mostrarNotificacao("❌ Erro ao conectar com IA", "error");
  } finally {
    mostrarLoading(false);
  }
}

function mostrarRelatorioIA(relatorio) {
  const container = document.getElementById("relatorioIAContainer");

  // Indicador de nível
  const nivelCor =
    relatorio.indicadores_chave.nivel_alerta === "verde"
      ? "indicador-verde"
      : relatorio.indicadores_chave.nivel_alerta === "amarelo"
      ? "indicador-amarelo"
      : "indicador-vermelho";

  let html = `
        <div class="relatorio-section">
            <h4>📊 Resumo Executivo</h4>
            <p>${relatorio.resumo_geral}</p>
            <p style="margin-top: 1rem;">
                <span class="indicador-nivel ${nivelCor}"></span>
                <strong>Status Geral:</strong> ${relatorio.indicadores_chave.tendencia.toUpperCase()}
            </p>
        </div>

        ${
          relatorio.setores_criticos.length > 0
            ? `
        <div class="relatorio-section">
            <h4>⚠️ Setores Críticos</h4>
            <ul class="relatorio-list">
                ${relatorio.setores_criticos
                  .map((setor) => `<li>${setor}</li>`)
                  .join("")}
            </ul>
        </div>
        `
            : ""
        }

        <div class="relatorio-section">
            <h4>✅ Pontos Positivos</h4>
            <ul class="relatorio-list">
                ${relatorio.pontos_positivos
                  .map((ponto) => `<li>${ponto}</li>`)
                  .join("")}
            </ul>
        </div>

        ${
          relatorio.riscos_identificados.length > 0
            ? `
        <div class="relatorio-section">
            <h4>🚨 Riscos Identificados</h4>
            <ul class="relatorio-list">
                ${relatorio.riscos_identificados
                  .map((risco) => `<li>${risco}</li>`)
                  .join("")}
            </ul>
        </div>
        `
            : ""
        }

        <div class="relatorio-section">
            <h4>🎯 Ações Recomendadas</h4>
            <ul class="relatorio-list">
                ${relatorio.acoes_recomendadas
                  .map(
                    (acao) => `
                    <li>
                        <strong>${acao.acao}</strong>
                        <span class="badge-prioridade badge-prioridade-${
                          acao.prioridade
                        }">
                            ${acao.prioridade.toUpperCase()}
                        </span>
                        <br><small>Setor: ${acao.setor}</small>
                    </li>
                `
                  )
                  .join("")}
            </ul>
        </div>
    `;

  container.innerHTML = html;
  container.classList.remove("hidden");
}

// =====================================================
// Export (se necessário)
// =====================================================

console.log("✅ Work Well carregado e pronto para uso!");
