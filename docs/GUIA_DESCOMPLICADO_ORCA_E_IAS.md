# Guia descomplicado: Orca e perfis de IA

Este guia explica os perfis do Local AI Organizer sem substituir o `AGENTS.md`, o
catálogo de modelos nem a confirmação de disponibilidade no momento do lançamento.

## O que é cada componente

1. **Local AI Organizer:** guarda contratos, critérios de segurança e o roteiro dos
   projetos; não autoriza alterações sozinho.
2. **Orca ADE:** coordena sessões e workers supervisionados.
3. **Codex e Antigravity:** são executores diferentes. Os modelos Gemini, Claude e
   GPT-OSS são modelos expostos pelo Antigravity, não agentes independentes.
4. **Skills:** instruções versionadas que definem como orientar, rotear, testar e revisar.

## Perfis atuais

| Perfil | Papel prático | Quando escolher |
| --- | --- | --- |
| **Luna** (`organizer-codex-luna`) | Triagem rápida | leitura curta e tarefas repetitivas |
| **Terra** (`organizer-codex-economy`) | Perfil econômico | testes usuais, validações pontuais e tarefas mecânicas |
| **Sol 6.1 médio** (`organizer-codex-sol-medium`) | Desenvolvedor padrão | implementação, debugging delimitado e revisão técnica de complexidade média |
| **Sol 6.1 alto** (`organizer-codex-strong`) | Engenheiro sênior | arquitetura, integração e bugs complexos |
| **Gemini Flash baixo** (`organizer-gemini-low`) | Classificador rápido | triagem e síntese curta |
| **Gemini Flash médio** (`organizer-gemini-economy`) | Leitor ágil | documentação e auditoria ampla |
| **Gemini Flash alto** (`organizer-gemini-strong`) | Revisor técnico | síntese e revisão técnica densa |
| **Claude Sonnet** (`organizer-claude-sonnet`) | Especialista em código | implementação e cobertura de testes |
| **Claude Opus** (`organizer-claude-opus`) | Arquiteto | arquitetura e gates críticos |
| **GPT-OSS** (`organizer-gpt-oss`) | Auditor independente | segunda opinião econômica |
| **OpenRouter** (`organizer-openrouter-free`) | Perfil opcional | somente após autorização específica de custo, credencial e privacidade |

O perfil não é uma autorização nem uma garantia de qualidade, consumo ou disponibilidade.
Cada execução preserva `fallback: none`: se o modelo exato não estiver disponível, ela deve
parar de forma explícita, sem trocar de modelo por conta própria.

## Uso no dia a dia

1. Abra o projeto correto no Orca.
2. Peça ao coordenador para usar `model-router-advisor`, explicando objetivo, limites e
   como o resultado será validado.
3. Antes de uma tarefa com escrita, confirme o repositório, o `AGENTS.md`, o Git e se há
   somente um escritor no checkout.
4. Para workers supervisionados, confirme o modelo efetivo no recibo de lançamento;
   para Antigravity, também consulte `agy models`. Uma sessão manual não equivale a
   Dispatch supervisionado.
5. Exija evidências: diff revisado, testes relevantes e limitações declaradas. Commit e
   push só ocorrem quando você pedir explicitamente.

## Quando algo der errado

- **Modelo indisponível:** não aceite uma troca automática. Escolha outro perfil de forma
  explícita ou aguarde a disponibilidade.
- **Cota limitada:** prefira Luna para tarefas claras e repetitivas, Terra para validações
  pontuais e os perfis Antigravity já autorizados para seus papéis próprios.
- **Um executor não recebeu contexto:** gere um pacote de passagem sanitizado com baseline,
  escopo, exclusões, validação e condição de parada; não envie transcrições, credenciais ou
  dados privados.
- **Precisa de maior qualidade:** comece no Sol 6.1 médio para implementação normal;
  eleve para Sol 6.1 alto apenas diante de arquitetura difícil, integrações ou falhas que
  resistirem às validações usuais.

## Regras de ouro

1. Erick continua no comando: uma IA não faz commit, push, instalação, login ou controle
   visual sem autorização específica.
2. Dados pessoais, documentos e mídias não devem entrar em prompts, artefatos versionados
   ou serviços externos sem autorização.
3. Trabalhe uma etapa por vez e não prossiga para a seguinte apenas porque uma sessão
   terminou; revise as evidências primeiro.
