---
name: model-router-advisor
description: Analise os requisitos de uma tarefa e o estado de cotas para recomendar deterministicamente o melhor executor (Codex ou Antigravity), modelo (Sol, Terra, Luna, Astra, Gemini 3.8, Claude Sonnet 4.6, Claude Opus 4.6 ou GPT-OSS 120B) e esforço de raciocínio. Use no planejamento de novas etapas e delegação bidirecional.
---

# Consultor de Roteamento de Modelos e Executores

Oriente a seleção técnica do executor, modelo e esforço de raciocínio para qualquer
etapa do portfólio. O roteamento é estritamente deliberado e opera sob simetria total
entre **Codex** (OpenAI) e **Antigravity** (Google Pro AI).

## Princípios Fundamentais

1. **Simetria Bidirecional:** Tanto o Codex quanto o Antigravity atuam como orquestradores
   e como executores delegados. A delegação pode partir de qualquer um e ter como destino
   qualquer modelo dos dois ecossistemas.
2. **Sem Substituição Silenciosa:** Cada execução declara nominalmente `executor`, `model`,
   `effort` e `fallback: none`. Uma troca entre modelos ou provedores encerra o worker
   anterior e requer pacote de passagem sanitizado.
3. **Um Escritor por Checkout:** O modelo selecionado para escrita opera de forma exclusiva
   na working tree autorizada.

## Catálogo de Modelos e Especialidades

### Ecossistema OpenAI (Executor: `codex`)
- `gpt-5.6-luna` (esforço `low`): Ultra-rápido e econômico. Tarefas mecânicas, skeletons,
  linting e ajustes simples de formatação.
- `gpt-5.6-terra` (esforço `medium`): Modelo padrão de trabalho no Codex. Equilíbrio ideal
  entre velocidade, precisão de código e consumo de cota.
- `gpt-5.6-sol` (esforço `high`): Raciocínio profundo para subsistemas complexos, grafos de
  dependência e depuração de concorrência/sandbox.
- `gpt-5.6-astra` (esforço `extreme`): Topo absoluto da fronteira de inteligência. **Reservado
  exclusivamente para exceções ultra-específicas** (impasses matemáticos, arquiteturais ou
  lógicos onde Sol e Opus comprovadamente falharem), devido ao altíssimo impacto na cota.

### Ecossistema Google Pro AI (Executor: `antigravity`)
- `gemini-3.8-flash-medium` / `-high` (esforço `medium` ou `high`): Orquestrador contínuo do
  Organizer. Janela de contexto massiva, custo computacional mínimo para leitura ampla de
  documentos `.md`, checagem de Git e geração de prompts.
- `claude-sonnet-4-6` (modo `Thinking`): Engenharia de software de elite. Produção de
  código limpo, refatorações cirúrgicas e testes unitários rigorosos (executor prioritário
  quando o Codex estiver com cota baixa ou por preferência).
- `claude-opus-4-6-thinking` (modo `Thinking`): Arquiteto sênior. Modelagem formal de
  segurança, desenho de contratos de integração inter-sistemas e gates de release críticos.
- `gpt-oss-120b-medium` (esforço `medium`): Auditoria independente e aberta para conferência
  neutra de robustez e ausência de viés comercial.

## Procedimento de Recomendação

Ao ser acionada, a skill executa 4 passos determinísticos:

1. **Avaliar Natureza da Tarefa:**
   - *Coordenação / Governança / Status:* `gemini-3.8-flash-medium` (Antigravity).
   - *Arquitetura Formal / Gate de Release Crítico:* `claude-opus-4-6-thinking` (Antigravity).
   - *Implementação de Código Modular no Codex:* `gpt-5.6-terra` (Codex).
   - *Implementação de Código Complexo no Codex:* `gpt-5.6-sol` (Codex).
   - *Implementação de Código no Antigravity / Alternativa Forte:* `claude-sonnet-4-6` (Antigravity).
   - *Tarefas Mecânicas / Skeletons:* `gpt-5.6-luna` (Codex).
   - *Auditoria Cruzada Aberta:* `gpt-oss-120b-medium` (Antigravity).
   - *Impasse Crítico Insolúvel:* `gpt-5.6-astra` (Codex, apenas com autorização explícita).

2. **Verificar Restrição de Cota Semanal:**
   - As cotas do Codex reiniciam semanalmente na segunda-feira.
   - Se a cota do Codex estiver baixa ou esgotada (ou em finais de semana), redirecionar
     automaticamente tarefas de implementação para `claude-sonnet-4-6` e tarefas de
     arquitetura para `claude-opus-4-6-thinking` no Antigravity, preservando o Codex.

3. **Verificar Ferramental Exclusivo:**
   - Se a tarefa exigir ferramentas ou automações exclusivas de um dos ambientes (ex:
     ambiente de execução do Codex vs. Antigravity IDE/CLI), priorizar o executor nativo
     correspondente.

4. **Emitir Recomendação Justificada:**
   - Perfil sugerido (ID exato no schema `orca-model-routing/v1`);
   - Executor e Modelo com IDs de runtime comprovados;
   - Nível de esforço e fallback (`none`);
   - Justificativa técnica (complexidade, cota e risco de retrabalho).
