# Contrato de Integração do OpenRouter

Atualizado em: 2026-09-18.
Schema: `openrouter-integration/v1`

## 1. Finalidade e Estado

Este contrato formaliza as regras de arquitetura, segurança, privacidade e operação para a utilização do provedor **OpenRouter** no ecossistema do `Local AI Organizer`.

- **Estado atual:** **ESPECIFICAÇÃO E ADAPTADOR INICIAIS (Fase Experimental Sintética)**.
- **Papel no Portfólio:** Camada de experimentação e processamento auxiliar baseada em modelos abertos (*open-weights*) e camadas gratuitas (*free tier*).

---

## 2. Futuros Usos do OpenRouter (Ampliando Possibilidades)

Além de testar sistemas básicos, a integração com o OpenRouter destrava 5 capacidades estratégicas para o portfólio:

### 2.1. Testes de Robustez e Tolerância de Prompts
Modelos proprietários topo de linha (Sol, Opus, Gemini High) compensam falhas de ambiguidade nas instruções. Modelos abertos menores (ex.: Llama 3 8B, Mistral 7B, Qwen) funcionam como o "teste de estresse definitivo": se um prompt, schema JSON ou pipeline de extração produzir o formato esperado nesses modelos, significa que a arquitetura do prompt é robusta e à prova de falhas.

### 2.2. Avaliação e Auditoria Cruzada Neutra (*LLM-as-a-Judge*)
Permite configurar um modelo aberto e independente para auditar o código gerado pelo Codex ou pelo Antigravity, procurando bugs, regressões, vulnerabilidades de segurança ou desvios de escopo, sem consumir um único token das cotas semanais do desenvolvedor.

### 2.3. Geração em Massa de Dados Sintéticos e Fixtures
Alimentação de ambientes de teste com centenas de arquivos fictícios, logs falsos, transcrições sintéticas e cenários de estresse para os projetos irmãos (`Local File Agent` e `Local Transcriber`), mantendo o custo financeiro e de cotas em zero.

### 2.4. Triagem e Pré-processamento de Baixo Custo
Classificação preliminar de arquivos, verificação se um texto é prosa ou código, extração de palavras-chave brutas e sumarização não-crítica antes de o material refinado ser entregue ao modelo principal.

### 2.5. Preservação Estratégica de Cotas Semanais
Garante que as cotas do Codex (OpenAI) e limites do Antigravity (Google Pro AI) sejam preservados integralmente para arquitetura densa, refatorações complexas e revisão de releases críticas.

---

## 3. Diretrizes Rígidas de Privacidade e Governança de IA Local

> [!CAUTION]
> **INVARIANTE DE OURO SOBRE DADOS:**
> Provedores gratuitos em nuvem e nós de inferência comunitários frequentemente retêm requisições para telemetria, análise de abuso ou retreinamento.

1. **Apenas Dados 100% Sintéticos:** É terminantemente proibido enviar documentos pessoais, gravações de áudio do `Local Transcriber`, caminhos absolutos do usuário (`C:\Users\...`) ou informações confidenciais para o OpenRouter.
2. **Isolamento de Credenciais:** A chave de API nunca deve ser salva em arquivos de configuração, commits ou documentação. O adaptador deve ler exclusivamente a variável de ambiente `$env:OPENROUTER_API_KEY`.
3. **Modo Dry-Run / Mock Nativo:** O adaptador deve conter suporte a testes simulados (mock) para validação determinística sem depender de conexão de rede externa ou de chaves ativas.
4. **Sem Fallback Silencioso:** Falhas de conexão, limites de taxa (HTTP 429) ou instabilidade do provedor devem retornar erro explícito, sem chavear silenciosamente para modelos locais ou outros executores.

---

## 4. Catálogo de Modelos Gratuitos Selecionados

| Identificador no OpenRouter | Especialidade Principal | Caso de Uso Recomendado |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | Raciocínio geral equilibrado | Geração de dados de teste e auditoria cruzada |
| `qwen/qwen-2.5-72b-instruct:free` | Código e raciocínio lógico | Testes de robustez de refatoração |
| `mistralai/mistral-7b-instruct:free` | Ultra-rápido e leve | Triagem preliminar e classificação mecânica |
| `deepseek/deepseek-r1:free` | Raciocínio profundo (Thinking) | Validação cruzada de hipóteses arquiteturais |

---

## 5. Especificação Técnica do Adaptador (`openrouter_client.py`)

- **Localização:** `src/adapters/openrouter_client.py`
- **Protocolo:** REST API HTTPS compatível com o padrão OpenAI (`https://openrouter.ai/api/v1/chat/completions`).
- **Autenticação:** `Bearer $OPENROUTER_API_KEY`
- **Cabeçalhos Obrigatórios:**
  - `HTTP-Referer`: Identificador local do projeto (`http://localhost/local-ai-organizer`)
  - `X-Title`: `Local AI Organizer`
- **Tratamento de Rate Limit:** Detecção do código HTTP 429 e espera com backoff exponencial limitado a no máximo 3 tentativas.
- **Filtro de Salvaguarda:** Bloqueio local pré-envio caso o texto de entrada contenha caminhos do perfil do usuário ou padrões de dados privados.
