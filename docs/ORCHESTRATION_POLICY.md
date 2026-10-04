# Política de orquestração

Atualizada em: 2026-10-04.

## Autoridade

| Pedido de Erick | Ação permitida |
| --- | --- |
| analisar, explicar, revisar ou diagnosticar | somente leitura |
| criar prompt | preparar, sem enviar ou iniciar |
| delegar ou criar tarefa | uma tarefa delimitada no projeto indicado |
| implementar | alterar somente a etapa e o projeto autorizados |
| commit ou publicar | somente quando pedido, após revisão |

Autonomia não inclui credenciais, login, instalação, rede pública, controle visual, ação
destrutiva, commit ou push. O coordenador preserva mudanças existentes, usa um escritor por
checkout e não amplia permissões quando troca executor.

## Ciclo obrigatório

1. Confirmar projeto, `AGENTS.md`, Git e modo de trabalho.
2. Para portfólio, ler `PROJECT_REGISTRY`, `SYSTEM_MAP`, esta política e `ROADMAP`.
3. Selecionar perfil em `orca-model-routing-profiles.json`, revalidando catálogo e
   capacidade no instante do lançamento.
4. Preparar contexto mínimo, objetivo, exclusões, permissões, validação e parada. Usar
   `DELEGATION_TEMPLATE.md` quando houver delegação.
5. Para coordenação supervisionada, usar a skill Orca `orchestration`: Run, Task, Dispatch,
   evidências, revisão e `worker-release` após conclusão aceita.
6. Atualizar documentação viva e roadmap somente para fatos comprovados; relatórios
   históricos não são reescritos.

## Perfis e custo

O catálogo atual possui 10 perfis. `gpt-5.6-luna` é o ponto de partida econômico no Codex;
Gemini Flash low/medium atende triagem e documentação; Sonnet 5.5 é indicado para código;
Opus 5.5 para arquitetura e gates; GPT-OSS é uma auditoria independente econômica. Essas
recomendações não são garantia de consumo, qualidade ou disponibilidade. `fallback: none`
impede troca automática.

Antigravity com modelo fixo só pode ser usado pelo caminho descrito em
`ORCA_WORKER_LIFECYCLE.md`, com revalidação por lançamento. Nunca alivie sandbox, permita
acesso externo ou use bypass para fazer uma sessão manual parecer um worker supervisionado.

## Paralelismo, evidência e gates

O coordenador decompõe trabalho não trivial em leitura, arquitetura, testes e auditoria.
Subagentes paralelos são somente leitura ou usam worktrees separados; um único responsável
integra as escritas. Cada relatório separa teste determinístico/mock, validação real,
proposta e desconhecido. Uma tarefa encerrada, terminal aberto ou commit isolado não prova
sucesso.

Projetos reais ficam bloqueados até gate específico. Em fixture descartável, o coordenador
pode administrar somente a subárvore autorizada e allowlists mínimas; são proibidos bypass,
curingas globais, acesso fora do workspace e persistência de argumentos globais.

## Colaboração Codex + Antigravity

O contrato `CODEX_ANTIGRAVITY_COLLABORATION.md` define a composição entre executores. Um
coordenador deve registrar executor, modelo, esforço, papel, checkout, permissões e condição
de parada de cada participante. Leitura e auditoria podem ser paralelas; escrita requer um
único responsável e integração sequencial. A troca de executor exige worker anterior
encerrado, Git verificado e pacote sanitizado; permissões, credenciais e contexto oculto não
são transferidos.
