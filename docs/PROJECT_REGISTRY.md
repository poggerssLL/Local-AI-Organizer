# Registro central de projetos

Atualizado em: 2026-10-05.

Este registro é um resumo de portfólio, não substitui o Git, os testes nem a documentação
viva de cada repositório. Não armazene caminhos pessoais, IDs de runtime, credenciais ou
dados privados.

| Projeto | Papel | Estado conhecido | Próximo passo seguro |
| --- | --- | --- | --- |
| `Local AI Organizer` | Coordenação, contratos e revisão | Preflight real Orca 1.4.219 com Gemini Flash high sandbox e Codex Sol 6.1 high readonly. Revisões textuais úteis, mas lifecycle bloqueado: Gemini EPERM no IPC; Codex CommandNotFoundException inclusive caminho qualificado. Launcher padrão Codex abriu YOLO/draft e foi cancelado antes do início. Quatro Tasks failed operacionalmente, sem worker_done durável; zero workers ativos/reclaimable. | [Preflight e limites atuais](ORCA_RELIABILITY_PREFLIGHT_2026-10-05.md). Manter Gemini high prioritário e fallback none. Sandbox/integração de IPC e resolução do Orca precisam solução suportada; não habilitar bypass nem confundir aprovação técnica com lifecycle completo. |
| `Local Transcriber` | Transcrição local e offline | Manutenção 8C integrada sobre baseline local `5d58eeb`, preservando alterações 8/8B. Suíte 142/142 em checkout isolado; Ruff global e formatação de 28 arquivos aprovados também no checkout principal. Clock controlado no teste de retries e regressão separada da expiração; código de produção da fila inalterado. | Sem commit/push; inferência real não reexecutada. Aviso pip de distribuição inválida permanece sem repair. Consulte relatório 8C do projeto; Etapa 9 não iniciada. |
| `Local File Agent` | Inventário e organização segura | Etapa 3 publicada em `49c7dbe`; Etapa 4 publicada em main `9db3c44`: regras por extensão/nome/UTC, sugestões auditáveis sem I/O/planos/LLM. Suíte isolada 90/89/1 skip legado; 20 testes novos também aprovados no principal. Gate técnico Codex readonly aprovado via transcript após complemento de duplicatas com metadata inválida, aceito pelo coordenador; lifecycle Orca failed. | Push confirmado pelo servidor; main local e origin/main em `9db3c44`, árvore limpa. Etapa 5 não iniciada. Dados reais fora do escopo. Relatório 4 do projeto documenta limites e fixture oculta legada ausente em clones limpos. |
| `Jarvis Local` | Assistente local por voz | Planejado. | Iniciar somente após a base segura do File Agent. |
| `Casa Inteligente` | Projeto residencial separado | Existência informada; arquitetura não inspecionada aqui. | Revisar contratos antes de integração. |

Classifique qualquer nova afirmação como confirmado agora, informado, planejado ou
desconhecido. Não converta relatórios históricos em baseline atual.
