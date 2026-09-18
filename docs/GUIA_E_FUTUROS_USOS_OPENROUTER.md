# Guia de Uso e Futuros Usos do OpenRouter no Portfólio

Este documento orienta detalhadamente como utilizar a nova integração com o **OpenRouter** no `Local AI Organizer` e cataloga os **casos de uso futuros automatizados** para quando você desejar expandir ou avaliar os sistemas.

---

## 1. Como Usar o Sistema do OpenRouter (Manual e Prático)

O sistema foi desenhado para ser simples, autônomo e seguro. Você tem controle total sobre quais modelos usar e nunca precisa expor suas chaves de API.

### 1.1. Onde fica a Chave de API?
A sua chave de API pode ser configurada de duas formas (ambas 100% protegidas contra o Git pelo `.gitignore`):

1. **No arquivo local `API_KEY.env`:**
   - Basta ter o arquivo `API_KEY.env` na pasta do projeto com a linha:
     ```text
     OPENROUTER_API_KEY=sua_chave_aqui
     ```
   - O sistema lê esse arquivo automaticamente antes de qualquer chamada.
2. **Ou na variável de ambiente do Windows:**
   - No PowerShell:
     ```powershell
     $env:OPENROUTER_API_KEY = "sua_chave_aqui"
     ```

---

### 1.2. Como Consultar os Modelos Gratuitos Disponíveis em Tempo Real?
Você não precisa adivinhar quais modelos estão sem custo. Execute no terminal:

```powershell
python src/adapters/openrouter_client.py --list-free
```

O comando se conecta à API pública do OpenRouter e lista todos os modelos gratuitos ativos no momento (ex.: `qwen/qwen3.8-27b:free`, `deepseek/deepseek-v4-flash-0731:free`, `nvidia/nemotron-3.5-lightning:free`, `google/gemma-4-31b-it:free`, `openrouter/free`, etc.).

---

### 1.3. Como Rodar o Chat de Exemplo (`exemplo_chat.py`)
Criamos um script pronto na raiz do projeto chamado [`exemplo_chat.py`](file:///C:/Users/erick/OneDrive/Documentos/Local%20AI/exemplo_chat.py).

Para usar:
1. Abra o arquivo no editor;
2. Altere o modelo ou a pergunta se desejar:
   ```python
   MODELO_ESCOLHIDO = "qwen/qwen3.8-27b:free"
   MENSAGEM = "Sua pergunta ou instrução aqui"
   ```
3. Execute no terminal:
   ```powershell
   python exemplo_chat.py
   ```

---

### 1.4. Como Usar o Cliente em seus Próprios Scripts Python
Basta importar a classe `OpenRouterClient`:

```python
from src.adapters.openrouter_client import OpenRouterClient

# Inicializa o cliente (busca automaticamente do API_KEY.env ou do ambiente)
client = OpenRouterClient()

# Faz a chamada com o modelo desejado
resposta = client.chat_completion(
    messages=[{"role": "user", "content": "Gere uma lista de 5 nomes de arquivos falsos para teste."}],
    model="qwen/qwen3.8-27b:free",
    temperature=0.7
)

conteudo = resposta["choices"][0]["message"]["content"]
print(conteudo)
```

---

## 2. Futuros Usos Automatizados nos Projetos do Portfólio

A integração com o OpenRouter foi homologada para operar como **camada auxiliar de alta velocidade e custo zero**. Abaixo estão os 5 casos de uso arquitetados para ativação futura:

```text
                                  OpenRouter no Portfólio
                                             │
      ┌──────────────────┬───────────────────┼───────────────────┬──────────────────┐
      ▼                  ▼                   ▼                   ▼                  ▼
[1. Gerador de    [2. Auditor         [3. Estresse de    [4. Triagem        [5. Roteador de
   Fixtures]         LLM-as-Judge]       Prompts/JSON]      Anonimizada]       Emergência]
Para o File Agent   Para Releases       Para novas skills   Para arquivos      Fallback leve
```

### Caso 1: Fábrica Automática de Fixtures para o `Local File Agent`
- **Problema:** Para testar a organização e renomeação de arquivos no `Local File Agent`, precisamos de diretórios cheios de arquivos simulados (ex.: PDFs de contas falsas, relatórios fictícios, fotos de férias simuladas).
- **Como a Automação Funcionará:**
  - Um script de preparação (ex.: `src/tools/generate_test_data.py`) aciona o OpenRouter com o modelo `qwen/qwen3.8-27b:free` solicitando a criação de 50 estruturas de pastas e arquivos fictícios.
  - O script cria esses arquivos falsos em uma pasta temporária `%TEMP%` para o `Local File Agent` treinar seus algoritmos sem encostar em nenhum arquivo real seu.

### Caso 2: Auditoria Cruzada Automática no Release Gate (*LLM-as-a-Judge*)
- **Problema:** Quando o Codex ou Antigravity terminam de codificar uma tarefa, a revisão de código consome tokens valiosos dos modelos principais.
- **Como a Automação Funcionará:**
  - Durante a execução da skill `local-ai-release-review`, um hook automatizado extrai o `git diff` da etapa e envia para um modelo aberto e neutro (como `deepseek/deepseek-r1:free` ou `meta-llama/llama-3.3-70b-instruct:free`).
  - O modelo aberto gera um parecer neutro destacando:
    1. Possíveis bugs ou variáveis não declaradas;
    2. Divergências em relação ao que foi pedido;
    3. Riscos de segurança.
  - O parecer é exibido na tela para você decidir se aprova o commit.

### Caso 3: Bateria Automática de Estresse e Estabilidade de Prompts
- **Problema:** Modelos proprietários gigantes (Sol, Opus) compensam prompts mal escritos porque adivinham a intenção do usuário. Quando o prompt é usado em outro sistema, ele falha.
- **Como a Automação Funcionará:**
  - Sempre que criarmos uma nova skill ou contrato, um teste de estresse dispara o mesmo prompt para 3 modelos gratuitos distintos no OpenRouter (ex.: Llama, Mistral e Qwen).
  - Se os 3 modelos retornarem o formato esperado (ex.: JSON estrito), o prompt é considerado **à prova de falhas e universal**.

### Caso 4: Triagem e Extração Rasa de Metadados Anonimizados
- **Problema:** Ler e resumir milhares de metadados consome muitas cotas.
- **Como a Automação Funcionará:**
  - O sistema sanitiza localmente nomes e caminhos de arquivos (substituindo nomes reais por tokens abstratos como `arquivo_001.txt`).
  - O OpenRouter processa esses metadados anonimizados em lote para sugerir categorias genéricas (ex.: "Finanças", "Acadêmico", "Fotos").

### Caso 5: Roteador de Preservação e Fallback de Cotas
- **Problema:** Fins de semana ou momentos de esgotamento de cotas semanais do Codex.
- **Como a Automação Funcionará:**
  - A skill `model-router-advisor` pode sugerir o perfil `organizer-openrouter-free` para tarefas mecânicas ou scaffolds preliminares, preservando 100% da sua cota para quando os dias úteis começarem.

---

## 3. Salvaguardas e Princípios Inegociáveis de Privacidade

Para manter a conformidade com a política do portfólio de IA local:

1. **Apenas Dados Sintéticos e Código Aberto:** Nunca automatizar o envio de documentos confidenciais, dados bancários ou gravações de áudio do `Local Transcriber`.
2. **Proteção Ativa em Código:** O adaptador possui o método `check_privacy_guardrail()` que aborta automaticamente requisições que contenham caminhos do tipo `C:\Users\...` ou credenciais.
3. **Resiliência contra Rate Limits:** Automações com modelos gratuitos devem ser **não-bloqueantes**. Se o OpenRouter retornar `HTTP 429` (muitas requisições), a automação registra o aviso e o sistema continua normalmente sem travar.
