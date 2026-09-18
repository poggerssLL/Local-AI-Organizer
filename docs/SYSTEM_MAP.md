# Mapa dos sistemas locais

## Visão geral

```text
                         Erick
                           |
                    autoriza e decide
                           |
            Local AI Organizer / coordenador
                    /      |       \
                   /       |        \
      Local Transcriber  Local File Agent  Jarvis Local
              |                 |                |
       transcrição fiel   organização segura   voz e ferramentas
              |                 |                |
              +---- Markdown ---+         Casa Inteligente
                         |
                resumo local futuro
```

As setas representam integrações planejadas ou possíveis. Elas não afirmam que os
componentes já estejam conectados.

## Responsabilidades

### `Local AI Organizer`

- mantém o contexto do portfólio;
- revisa evidências e baselines;
- decide qual projeto deve receber uma tarefa;
- gera prompts delimitados;
- seleciona skills disponíveis;
- acompanha resultados quando autorizado;
- não implementa silenciosamente trabalho em projetos irmãos.

Como camada operacional, o Organizer disponibiliza perfis explícitos de execução
materializados em `docs/orca-model-routing-profiles.json` e registrados no Orca como Quick
Commands escopados ao repositório:

```text
Erick escolhe um perfil nos Quick Commands do Orca
  -> Organizer fixa projeto, executor, modelo, esforço, contexto e permissões
  -> Orca inicia um único worker Codex ou Antigravity
  -> worker lê o contexto versionado e devolve evidências
  -> Organizer revisa o gate
```

A troca entre Codex e Antigravity ocorre entre execuções, nunca como substituição
silenciosa no meio de uma escrita. A memória comum pertence aos documentos versionados e
ao pacote de passagem; não à conversa privada de um provedor.

O antigo RAG de estudos não faz parte do organizador. Materiais e dados pessoais locais
remanescentes não devem ser tratados como contexto compartilhado do portfólio.

### `Local Transcriber`

- importa e transcreve mídia localmente;
- mantém transcrição, segmentos, palavras e timestamps;
- exporta formatos como Markdown;
- preserva a transcrição original como registro factual;
- pode receber futuramente uma camada separada de conteúdo gerado.

### `Local File Agent`

- inventaria diretórios autorizados;
- propõe classificação, nomes e destinos;
- exige validação determinística e aprovação humana;
- registra operações e oferece desfazer;
- nunca recebe autoridade para organizar o perfil inteiro do usuário.

### `Jarvis Local`

- recebe voz e produz uma interpretação estruturada;
- submete propostas a políticas determinísticas;
- executa apenas ferramentas permitidas;
- confirma ações sensíveis;
- não presume sucesso de uma ação residencial.

### `Casa Inteligente`

- permanece um projeto independente;
- só poderá ser integrado depois de uma revisão de contratos, autenticação, segurança e
  disponibilidade real dos dispositivos;
- não deve ser tratado como sinônimo de `Jarvis Local`.

## Integração planejada para transcrições e resumos

O fluxo desejado é:

```text
Local Transcriber
  -> exporta Markdown sanitizado
  -> Local File Agent sugere matéria e destino
  -> Erick aprova a organização
  -> um gerador local usa a transcrição como fonte
  -> resumo, tópicos e perguntas ficam separados do texto original
```

Invariantes:

- o Markdown original não é reescrito pelo resumo;
- o organizador de arquivos não interpreta o resumo como transcrição;
- conteúdo gerado registra modelo, prompt, parâmetros, data e versão da fonte;
- nenhum modelo é baixado silenciosamente;
- nenhum conteúdo pessoal é enviado à nuvem sem autorização explícita.

## Limites entre projetos

- cada projeto mantém seu próprio repositório, runtime, dados e documentação;
- bancos SQLite não são compartilhados entre computadores ou projetos;
- integrações futuras usam contratos versionados, arquivos controlados ou APIs locais;
- o coordenador compartilha contexto e prompts, não diretórios de runtime;
- uma falha em um projeto não deve impedir a operação local básica dos demais.
