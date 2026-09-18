---
name: local-integration-architect
description: Projete e revise contratos seguros entre projetos, agentes ou ferramentas locais, definindo responsabilidades, dados, versões, permissões, falhas, evidências e implantação gradual. Não implemente a integração sem autorização.
---

# Arquiteto de integração local

Produza um contrato verificável antes de conectar componentes. Classifique o pedido como
descoberta, desenho, revisão, implementação, implantação ou operação autônoma delimitada.
Os três primeiros modos são somente leitura.

## Fronteira

Para cada parte, confirme proprietário, papel, fonte de verdade, versão, entradas,
saídas, efeitos colaterais, permissões e responsável por iniciar, cancelar, aprovar e
recuperar. Use `local-project-orientation` para repositórios locais.

Defina transporte, schema, compatibilidade, autenticação, autorização, idempotência,
timeouts, cancelamento, repetição, logs, retenção, isolamento, rollback, critérios de
aceite e parada. Consulte [o modelo de contrato](references/integration-contract.md).

## Agentes e orquestradores

Trate Codex, Antigravity e outros workers como executores não confiáveis além do envelope.
Registre executor/modelo/esforço, skills efetivamente descobertas, projeto e checkout,
matriz de permissões, um escritor por checkout, limites, progresso, cancelamento e pacote
de evidências sanitizado. Preferir API, CLI e arquivos; GUI e credenciais pertencem a
Erick salvo autorização explícita e temporária.

Comece integrações em ambiente sintético. Escrita real, commit e publicação são gates
separados. Diante de lacuna crítica, decida **BLOQUEADO** ou **COMPLEMENTO NECESSÁRIO** e
indique a menor evidência seguinte. Atualize documentação e roadmap somente dentro de
autorização de escrita e sem reescrever histórico.
