# Mapa dos sistemas locais

```text
Erick (autoriza e decide)
  -> Local AI Organizer (coordena, revisa e mantém contratos)
       -> Local Transcriber (transcrição local)
       -> Local File Agent (operações sob aprovação humana)
       -> Jarvis Local / Casa Inteligente (futuros e separados)
```

O Organizer não compartilha diretórios de runtime, bancos, transcrições ou memória privada
entre projetos. A integração futura usa contrato versionado e dados sanitizados.

## Execução assistida

```text
pedido autorizado -> perfil explícito -> contexto mínimo v2 -> um worker
  -> evidências, Git e limitações -> gate -> release ou retenção explícita
```

Codex e Antigravity são executores distintos. Gemini, Claude e GPT-OSS são modelos do
Antigravity; não são agentes independentes do Orca. O catálogo de perfis está em
`orca-model-routing-profiles.json`; o limite atual de lançamento Antigravity está em
`ORCA_WORKER_LIFECYCLE.md`. Não há fallback silencioso nem dois escritores por checkout.

Quando uma etapa exigir colaboração entre executores, ela segue o contrato
`CODEX_ANTIGRAVITY_COLLABORATION.md`: leitores e auditores podem trabalhar em paralelo
somente leitura ou em worktrees isolados; o pacote de passagem é sanitizado; um único
escritor integra mudanças sequencialmente; e um gate independente revisa as evidências.

## Invariantes de integração

- cada projeto mantém repositório, dados e documentação próprios;
- o coordenador encaminha prompts e evidências, não dados privados;
- escrita exige autorização explícita, validação proporcional e aprovação humana quando
  afetar arquivos reais;
- falha ou indisponibilidade de um executor não concede permissão a outro executor.
