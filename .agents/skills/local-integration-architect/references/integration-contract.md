# Modelo de contrato de integração

Registre somente valores confirmados; marque o restante como informado, proposto ou
desconhecido.

## Identificação e objetivo

- contrato, versão, participantes, proprietários e estado;
- baselines verificados, problema, resultado observável, escopo e parada;
- envelope: capacidades permitidas, reservadas, duração e limites.

## Partes, fluxo e dados

Para cada parte, registre responsabilidade, fonte de verdade, dados, operações, efeitos e
proibições. Descreva fluxo normal, aprovações, cancelamento, timeout, falha parcial e
resultado desconhecido. Defina transporte, schema, encoding, limites, correlação,
idempotência, exemplo sanitizado, retenção e compatibilidade.

## Segurança e operação

Documente leitura, escrita, terminal, rede, instalação, GUI, gestão de ambiente
descartável e Git, com padrão negado ou delimitado, forma de autorização e evidência.
Inclua segredos, isolamento, auditoria, concorrência, custo, logs, rollback e desligamento.

## Evidências e rollout

Separe diff, Git, testes determinísticos, mocks, validação real e limitações. Promova por
gates: descoberta, simulação, leitura sintética, escrita descartável, escrita real e,
somente com autorização, commit/publicação. Registre decisões, incógnitas e próximo passo.
