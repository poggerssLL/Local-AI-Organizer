# Guia Descomplicado: Como Usar o Local AI Organizer com o Orca e suas IAs

Este guia foi feito para você que quer usar o sistema no dia a dia sem precisar ser um engenheiro de software avançado ou decorar comandos complicados.

Aqui você vai entender **o que é cada coisa**, **como abrir e usar** e **quem faz o quê** na sua equipe de inteligência artificial.

---

## 1. O que é cada coisa? (Em linguagem simples)

Pense neste projeto como uma pequena empresa ou oficina na sua máquina:

1. **Local AI Organizer (A Central de Regras):**
   - É o "gerente geral". Ele não fica escrevendo código à toa; ele guarda as regras, diz quem pode mexer em quê e não deixa nenhuma IA apagar seus arquivos pessoais ou fazer besteira.
2. **Orca ADE (O Painel de Controle):**
   - É como a cabine de um avião ou uma central cheia de botões e abas. Em vez de você ficar abrindo telas pretas de terminal estranhas, você abre o Orca e ele organiza os assistentes na sua tela.
3. **Codex e Antigravity (Os Dois Motores / As Empresas Parceiras):**
   - São as duas portas de entrada para as inteligências artificiais:
     - **Codex:** É a porta da OpenAI (onde moram os modelos GPT).
     - **Antigravity:** É a porta da Google Pro AI (onde moram o Gemini, o Claude e outros).
4. **Skills (Os Manuais de Treinamento):**
   - São como fichas de instrução que as IAs leem para saber como se comportar direito (por exemplo: como conferir se o código tem erros antes de te entregar).

---

## 2. Quem é quem na sua equipe de IAs?

Você tem à sua disposição 9 "perfis" de IA. Imagine que cada um é um funcionário com um talento diferente:

| Nome do Perfil | Quem é ele na prática? | Quando você deve chamar? |
| :--- | :--- | :--- |
| **Luna** (`organizer-codex-luna`) | **O Estagiário Rápido** | Para tarefas bobas, formatar textos rápidos ou criar esqueletos simples sem gastar sua cota. |
| **Terra** (`organizer-codex-economy`) | **O Operário Padrão** | É o faz-tudo do dia a dia no Codex. Bom, rápido e não gasta muita cota. |
| **Sol** (`organizer-codex-strong`) | **O Engenheiro Sênior** | Quando o código for difícil, tiver um bug misterioso ou precisar pensar muito. |
| **Astra** (`organizer-codex-astra`) | **O Cientista de Emergência** | Só deve ser usado em último caso extremo se todos os outros falharem, pois é caríssimo em cota. |
| **Gemini Flash** (`organizer-gemini-economy`) | **O Leitor Ágil** | Consegue ler centenas de páginas de texto e documentos em segundos sem cansar. Ótimo para organizar as coisas. |
| **Claude Sonnet** (`organizer-claude-sonnet`) | **O Especialista em Código** | Escreve códigos limpíssimos e testes excelentes. É o melhor substituto quando a cota do Codex estiver baixa! |
| **Claude Opus** (`organizer-claude-opus`) | **O Grande Arquiteto** | Pensa em segurança, planeja o futuro e desenha as regras de como os sistemas conversam. |
| **GPT-OSS** (`organizer-gpt-oss`) | **O Auditor Independente** | Modelo aberto para olhar de fora e conferir se o trabalho foi bem feito sem viés de grandes marcas. |

---

## 3. Como usar no dia a dia (Passo a Passo)

### Passo 1: Abrir o Orca
1. Dê dois cliques no aplicativo do **Orca ADE** no seu computador.
2. Na tela inicial, clique em **Open Project** (ou Abrir Projeto) e selecione a pasta do projeto:
   `Local AI` (que fica dentro dos seus Documentos).

---

### Passo 2: Descobrir qual IA chamar para o trabalho
Você não precisa adivinhar qual modelo é o melhor para o que você quer fazer. O sistema faz isso por você!

1. No chat ou terminal com a IA, digite apenas:
   ```text
   /model-router-advisor
   ```
2. A IA vai analisar a tarefa que você quer e vai te responder algo simples como:
   > *"Erick, para essa tarefa recomendo o **Claude Sonnet** no Antigravity, porque hoje é fim de semana e assim economizamos sua cota do Codex."*

---

### Passo 3: Onde ver o que as IAs andam conversando?
Você quer ver o histórico de uma conversa ou o resumo do que uma IA fez sem bagunçar seus arquivos principais?

1. Abra a pasta do projeto no Windows Explorer:
   `Local AI` -> pasta `runtime` -> pasta `chat_exchange`.
2. Lá dentro você vai ver arquivos como:
   - `claude-sonnet-4-6_exchange.md`
   - `gpt-5.6-terra_exchange.md`
3. Você pode abrir esses arquivos em qualquer bloco de notas. Eles mostram a última conversa limpa com cada IA.
4. **Fique tranquilo:** Essa pasta nunca é enviada para a internet e nem para o GitHub. É 100% privada no seu computador.

---

### Passo 4: Como pedir para fazerem o trabalho
Sempre que você for pedir algo sério, siga esta regrinha de ouro de 3 frases:
1. **O que fazer:** "Quero criar um script que faça X."
2. **O que NÃO fazer:** "Não altere os outros arquivos do projeto e não faça commit."
3. **Como provar:** "Me mostre os testes funcionando antes de terminar."

As nossas regras já impedem que a IA saia apagando arquivos ou enviando dados seus para a nuvem sem você mandar.

---

## 4. O que fazer se algo der errado? (Socorro rápido)

- **"Apareceu uma mensagem vermelha dizendo `os error 183` no Codex":**
  - *Calma!* Isso não é um erro real. Significa apenas que o Codex tentou criar a pasta de regras e ela já existia. Pode ignorar.
- **"O Codex pareceu travar e demorou muito":**
  - No Windows, às vezes o terminal tenta pedir permissão de administrador oculta. Nós já deixamos configurado para rodar com a opção segura `unelevated` que resolve isso.
- **"Minha cota do Codex acabou":**
  - Sem estresse! As cotas do Codex renovam toda **segunda-feira**. Enquanto isso, você simplesmente usa o **Claude Sonnet** ou o **Gemini** pelo Antigravity, que continuam funcionando com força total.
- **"Uma IA não sabe o que a outra fez":**
  - É normal, elas têm cérebros separados. Basta você pedir: *"Gere um pacote de passagem (handoff) para eu mandar para o outro modelo"*. A IA vai criar um resuminho perfeito para você passar para a próxima.

---

## 5. Regras de ouro para você nunca esquecer

1. **Você está no comando:** A IA só planeja. Mexer em código importante, fazer commit ou enviar para o GitHub só acontece quando você disser explicitamente: *"Autorizo"* ou *"Pode commitar"*.
2. **Privacidade sempre:** Seus documentos pessoais, áudios e arquivos privados nunca são enviados para fora do seu computador.
3. **Uma coisa de cada vez:** Deixe a IA terminar uma etapa e te mostrar o resultado antes de pedir a próxima.
