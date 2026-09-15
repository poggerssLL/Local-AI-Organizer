# Roadmap central

Atualizado em: 2026-09-15.

## Regra de sequência

O roadmap orienta a próxima decisão, mas não autoriza implementação. Trabalhe em uma
entrega por vez e só avance depois de revisar o resultado anterior.

## Fundação do coordenador

1. **Concluído:** criar e validar a skill pessoal `local-project-orientation`.
2. **Concluído:** consolidar o contexto central em `PROJECT_REGISTRY.md`,
   `SYSTEM_MAP.md`, `ORCHESTRATION_POLICY.md`, `ROADMAP.md` e
   `DELEGATION_TEMPLATE.md`.
3. **Concluído:** validar em um novo chat do projeto `Local AI` a recuperação do
   portfólio, das regras de autorização e do próximo passo a partir da documentação
   central.
4. **Concluído:** criar e validar a skill `phase-gate-reviewer`.
5. **Concluído:** criar e validar a skill `implementation-prompt-builder`, incluindo a
   recomendação justificada de modelo e esforço para cada nova tarefa.
6. **Concluído:** confirmar a descoberta de `implementation-prompt-builder` e criar e
   validar a skill `local-ai-release-review`.
7. **Próximo:** confirmar em novo chat a descoberta de `local-ai-release-review` e criar
   `local-project-coordinator` depois que os fluxos básicos estiverem estáveis.
8. Criar `local-integration-architect` somente quando dois projetos reais precisarem de
   um contrato comum.

## Local Transcriber

1. Receber o resultado final da Etapa 7B.
2. Revisar a instalação, a validação CUDA real, o fallback em CPU, a documentação e o Git.
3. Corrigir na mesma tarefa qualquer bloqueador da 7B.
4. Considerar o MVP local encerrado depois da aprovação.
5. Postergar as Etapas 8A e 8B de processamento remoto enquanto o uso local atender Erick.
6. Avaliar separadamente uma extensão de resumos locais, preservando a transcrição
   original e registrando a proveniência do conteúdo gerado.

## Local File Agent

Iniciar em repositório separado e por etapas:

1. fundação e política de segurança;
2. inventário somente leitura;
3. hashes e duplicidades;
4. classificação determinística;
5. integração local com modelo usando saída estruturada;
6. plano de operações;
7. prévia e aprovação;
8. execução transacional;
9. diário de auditoria;
10. desfazer;
11. validação em diretório controlado com arquivos sintéticos.

O primeiro prompt deve tratar somente da fundação. Nenhuma organização real de arquivos
é autorizada por este roadmap.

## Jarvis Local

Começar somente depois de o `Local File Agent` estabelecer políticas seguras para
ferramentas e aprovação:

1. arquitetura e threat model;
2. microfone e detecção de fala;
3. STT local de baixa latência;
4. TTS local;
5. conversa sem ferramentas;
6. planner estruturado;
7. catálogo de ferramentas permitido;
8. confirmação de ações sensíveis;
9. integração local revisada com Home Assistant ou `Casa Inteligente`;
10. wake word, memória local e dispositivos distribuídos.

## Processamento remoto

As Etapas 8A e 8B do `Local Transcriber` estão adiadas, não canceladas. Retome somente se
medições reais mostrarem que o computador atual não atende ao uso desejado ou se Erick
quiser explicitamente usar outra máquina.

## Próximo marco

O próximo marco aplicável é confirmar a descoberta de `local-ai-release-review` em novo
chat e, se estiver disponível, criar `local-project-coordinator`. Mantenha uma skill por
vez e não antecipe `local-integration-architect`.
