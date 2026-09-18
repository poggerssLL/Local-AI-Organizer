# Registro central de projetos

Atualizado em: 2026-09-18.

## Finalidade

Este arquivo oferece uma visão curta do portfólio local de Erick. Ele não substitui a
documentação, o Git ou os testes de cada projeto. Antes de delegar trabalho, o coordenador
deve localizar o projeto salvo no Codex e verificar seu estado real.

Não registre aqui caminhos absolutos pessoais, IDs de tarefas, IDs de host, credenciais ou
outros identificadores de runtime. Esses valores devem ser resolvidos apenas durante a
ação que realmente precisar deles.

## Classificação das informações

- **Confirmado:** observado diretamente no projeto correspondente durante uma tarefa
  atual.
- **Informado:** relatado por Erick ou por outra tarefa, ainda sem nova verificação neste
  projeto.
- **Planejado:** intenção aprovada, ainda não implementada.
- **Desconhecido:** não inspecionado ou sem evidência suficiente.

## Projetos principais

| Projeto | Papel | Estado conhecido | Próximo passo seguro |
| --- | --- | --- | --- |
| `Local AI Organizer` | Central de arquitetura, revisão e coordenação dos projetos locais | Confirmado neste repositório: documentação central e seis skills portáteis em `.agents/skills/`. Descoberta e canário somente leitura (`local-project-orientation`) aprovados no Antigravity em 2026-09-18. Os 4 perfis Codex/Gemini e o piloto sintético permanecem materializados, mas leitura de sentinelas Codex, handoff e PTY ainda não estão homologados. Planejado: adicionar primeiro Claude Opus, Claude Sonnet e GPT-OSS como modelos do executor Antigravity; depois admitir outros executores por adaptadores próprios. OpenRouter é opção futura separada. Projetos reais permanecem bloqueados | Homologar PTY/handoff interativo; depois inventariar e validar um perfil adicional por vez |
| `Local Transcriber` | Transcrição local e offline de gravações | Informado: Etapa 7 concluída; Etapa 7B de CUDA está em finalização por outra tarefa. O baseline final da 7B ainda não foi revisado aqui | Receber e revisar o resultado da 7B antes de planejar qualquer extensão |
| `Local File Agent` | Inventário e organização segura de arquivos com aprovação humana | Planejado; ainda não constava como projeto local salvo na verificação de 2026-09-14 | Criar projeto e repositório separados; começar somente pela fundação e política de segurança |
| `Jarvis Local` | Assistente local por voz, ferramentas permitidas e futura integração residencial | Planejado; projeto ainda não iniciado | Começar somente depois de o `Local File Agent` possuir uma base segura |
| `Casa Inteligente` | Projeto residencial existente e separado | Confirmada apenas a existência como projeto Git salvo; arquitetura e compatibilidade não foram inspecionadas nesta etapa | Revisar seus contratos antes de propor qualquer integração com `Jarvis Local` |

## Projetos auxiliares

Outros projetos acadêmicos e pessoais podem aparecer na lista de projetos salvos do
Codex. Eles não entram automaticamente no roadmap de IA local. O coordenador deve listar
os projetos disponíveis no momento da delegação, selecionar o rótulo exato e não inferir
relações apenas por semelhança de nome.

## Regras de atualização

1. Atualize um estado somente com evidência identificada.
2. Marque relatos ainda não verificados como **Informado**.
3. Não copie para cá transcrições, documentos pessoais, credenciais ou resultados
   privados.
4. Não transforme commits históricos em baseline atual.
5. Quando um novo projeto for criado, registre apenas seu papel, estado e dependências;
   detalhes técnicos pertencem ao próprio repositório.
