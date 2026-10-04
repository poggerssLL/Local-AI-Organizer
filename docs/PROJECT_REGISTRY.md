# Registro central de projetos

Atualizado em: 2026-10-04.

Este registro é um resumo de portfólio, não substitui o Git, os testes nem a documentação
viva de cada repositório. Não armazene caminhos pessoais, IDs de runtime, credenciais ou
dados privados.

| Projeto | Papel | Estado conhecido | Próximo passo seguro |
| --- | --- | --- | --- |
| `Local AI Organizer` | Coordenação, contratos e revisão | 7 skills portáteis; 10 perfis atualizados; ciclo de workers fail-closed. Em 2026-10-04, Orca 1.4.219 validou worker Antigravity em fixture e em um piloto reversível no Organizer: auditoria Codex somente leitura, um escritor Antigravity, testes determinísticos, `worker_done` e release. | Escolher uma etapa de projeto real com escopo e autorização explícitos; o próximo gate recomendado é a Etapa 3 do Local File Agent. |
| `Local Transcriber` | Transcrição local e offline | Informado por documentação anterior: MVP local, CUDA e resumos estruturados concluídos. Não revalidado nesta tarefa. | Manter operação local; reabrir apenas por necessidade medida. |
| `Local File Agent` | Inventário e organização segura | Informado: etapas 1 e 2 concluídas; etapa 3 depende de gate próprio. | Auditar fronteiras antes de hashes e duplicidades. |
| `Jarvis Local` | Assistente local por voz | Planejado. | Iniciar somente após a base segura do File Agent. |
| `Casa Inteligente` | Projeto residencial separado | Existência informada; arquitetura não inspecionada aqui. | Revisar contratos antes de integração. |

Classifique qualquer nova afirmação como confirmado agora, informado, planejado ou
desconhecido. Não converta relatórios históricos em baseline atual.
