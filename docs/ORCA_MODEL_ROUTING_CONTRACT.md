# Contrato de roteamento de modelos no Orca

Atualizado em: 2026-10-04. Contrato: `orca-model-routing/v1`.

## Fonte de verdade e escopo

`docs/orca-model-routing-profiles.json` contém os 11 perfis materializados. Ele é a
fonte de verdade para ID, executor, esforço, `organizer-core-v2`, `fallback: none` e
`single_writer: true`. Antes de iniciar qualquer execução, confirme a disponibilidade no
executor; para Antigravity, execute `agy models`. A materialização não prova que todos os
perfis podem ser lançados pelo Orca nem libera escrita em projetos reais.

| Perfil | Executor | Modelo | Uso recomendado |
| --- | --- | --- | --- |
| `organizer-codex-luna` | Codex | `gpt-5.6-luna` / low | triagem, leitura e tarefas mecânicas |
| `organizer-codex-economy` | Codex | `gpt-5.6-terra` / medium | tarefas mecânicas, validações pontuais e testes usuais |
| `organizer-codex-sol-medium` | Codex | `gpt-6.1-sol` / medium | padrão para implementação de complexidade média, debugging delimitado e revisão técnica |
| `organizer-codex-strong` | Codex | `gpt-6.1-sol` / high | arquitetura, integração e depuração complexas |
| `organizer-gemini-low` | Antigravity | `gemini-3.8-flash-low` / low | classificação e sumarização curta |
| `organizer-gemini-economy` | Antigravity | `gemini-3.8-flash-medium` / medium | documentação e auditoria ampla |
| `organizer-gemini-strong` | Antigravity | `gemini-3.8-flash-high` / high | síntese e revisão técnica densa |
| `organizer-claude-sonnet` | Antigravity | `claude-sonnet-5-5-high` / high | implementação e cobertura de testes |
| `organizer-claude-opus` | Antigravity | `claude-opus-5-5-high` / high | arquitetura e gates críticos |
| `organizer-gpt-oss` | Antigravity | `gpt-oss-120b-medium` / medium | parecer independente e econômico |
| `organizer-openrouter-free` | OpenRouter | modelo gratuito configurado | opcional; exige autorização e validação própria |

Os seis IDs Antigravity acima foram observados em `agy models` nesta máquina em
2026-10-03. A disponibilidade futura, limite de uso e custo não são garantidos pelo
contrato. Os perfis Codex devem ser confirmados pelo recibo `launch.effective` do Orca;
em especial, a materialização de `gpt-6.1-sol` não é prova de disponibilidade até esse
recibo confirmar exatamente o modelo e o esforço solicitados.

## Contexto `organizer-core-v2`

1. `AGENTS.md`;
2. `docs/PROJECT_REGISTRY.md`, `docs/SYSTEM_MAP.md`, `docs/ORCHESTRATION_POLICY.md` e
   `docs/ROADMAP.md`, nessa ordem, quando houver coordenação de portfólio;
3. contrato, testes e documentação viva diretamente ligados à etapa;
4. `docs/DELEGATION_TEMPLATE.md` somente para delegação;
5. relatório histórico apenas quando citado por um documento vivo ou necessário para uma
   divergência.

O contexto não inclui todos os Markdown, transcript, memória privada, caminho pessoal,
credencial ou dados de runtime.

## Lançamento e falhas

- O modelo não concede permissões. Cada execução fixa `cwd`, escopo, leitura/escrita,
  rede, commit e push de forma independente.
- Um perfil inválido ou indisponível falha fechado; não há substituição automática.
- Codex com modelo fixo pode usar `worker-start` e precisa comprovar `launch.effective`.
- Antigravity com modelo fixo segue o contrato específico em
  `docs/ORCA_WORKER_LIFECYCLE.md`. O canário atual comprova o caminho supervisionado em
  fixture, mas cada Dispatch deve revalidar disponibilidade e registrar o modelo efetivo no
  recibo; um perfil do catálogo não é prova isolada de lançamento.
- Troca de executor exige término verificável do worker anterior, Git revisado e pacote
  sanitizado com objetivo, baseline, evidências e limitações — nunca transcript completo.

## Gate de promoção

Um perfil só pode passar de leitura sintética para escrita reversível após provar modelo
efetivo, contexto correto, permissões mínimas, resultado, limpeza de worker e Git. A
colaboração entre Codex e Antigravity segue `CODEX_ANTIGRAVITY_COLLABORATION.md` e não cria
um perfil híbrido nem autoriza dois escritores. Projetos reais, commit, push, credenciais,
instalação, rede pública e controle visual permanecem gates separados.

## Preflight de permissões além do modelo (2026-10-05)

permissions_profile é declarativo; launch.effective de modelo/effort não prova
sandbox nem allowlist. Na Etapa 4, o launcher padrão Codex abriu em YOLO e foi
cancelado antes do início; Gemini --sandbox recebeu revisão, mas check/done
foram bloqueados por EPERM. Sessão custom Codex --sandbox read-only iniciou,
mas seu shell não resolveu orca no PATH. A qualificação do MESMO executável
Orca, resolvido e verificado pelo coordenador, é resolução de comando explícita,
não substituição por outro binário nem fallback de executor. Se IPC continuar
negado, preservar falha, não habilitar bypass nem fingir worker_done.
Detalhes: [preflight restrito](ORCA_RELIABILITY_PREFLIGHT_2026-10-05.md).
