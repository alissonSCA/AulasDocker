# Plano de Aula — Revisão para a AP1

**Curso:** Técnico em Informática
**Unidade temática:** Docker — primeiros passos e prática com SSH/Linux
**Pré-requisito:** turma já concluiu os dois laboratórios práticos (`docker-intro-lab` e `docker-ssh-lab` / Operação Nexus)
**Duração sugerida:** 50 minutos (ajuste livremente conforme o tempo de aula da sua instituição)
**Objetivo da aula:** consolidar os comandos e conceitos praticados nos dois laboratórios antes da AP1, tirar dúvidas e simular o formato da prova.

---

## 1. Objetivos específicos

Ao final da aula, o aluno deve ser capaz de:

- explicar o que `docker run hello-world` testa e por que essa etapa existe;
- descrever o que cada uma das flags `-d`, `-p` e `-v` faz em `docker run`;
- explicar por que o conteúdo de um arquivo dentro de um volume sobrevive à recriação do container;
- montar corretamente o comando de conexão SSH (`ssh usuario@IP -p porta`);
- listar os quatro comandos permitidos no `docker-ssh-lab` (`ls`, `cd`, `cat`, `nano`) e para que serve cada um;
- explicar a lógica de "pistas escondidas no nome do arquivo" usada na Operação Nexus.

## 2. Conteúdos revisados

| Origem | Tópicos |
|---|---|
| `docker-intro-lab` | instalação do Docker (`apt install docker.io`), inicialização confiável (`iniciar-docker`), teste com `hello-world`, `docker run -d -p -v --name`, persistência de dados via volume, publicação de site com Nginx |
| `docker-ssh-lab` (Operação Nexus) | conexão SSH (usuário/porta/senha por equipe), os quatro comandos permitidos (`ls`, `cd`, `cat`, `nano`), leitura sistemática de diretórios, interpretação de pistas no **nome** dos arquivos (não só no conteúdo), edição de arquivo com `nano` para "sabotar" as coordenadas |

## 3. Materiais necessários

- Quadro ou projetor
- `Slides_Revisao.pptx` (nesta mesma pasta) — apoio visual para conduzir a aula
- Cópia (impressa ou na tela) dos dois PDFs de briefing já entregues nas aulas práticas: `Aula_Docker_Intro_Briefing.pdf` e `OPERAÇÃO NEXUS.pdf`
- `Atividade_Revisao.pdf` (impressa ou na tela) para a prática guiada/individual dos alunos
- Lista de perguntas de recapitulação oral (seção 5 deste plano)
- Provas impressas para o dia da AP1 (`Prova_A.pdf` e `Prova_B.pdf`, nesta mesma pasta) — **não distribuir nesta aula de revisão**, apenas no dia da avaliação

## 4. Roteiro da aula

| Tempo | Etapa | Descrição |
|---|---|---|
| 0–5 min | Abertura | Relembrar o objetivo da aula e avisar a data/formato da AP1 (prova individual, 10 questões de múltipla escolha, sem consulta). |
| 5–20 min | Recapitulação guiada — `docker-intro-lab` | Perguntas orais rápidas (ver seção 5), alternando entre equipes. Reforçar especialmente: para que serve o `hello-world`, o que significa cada flag do `docker run`, e por que o volume garante persistência. |
| 20–35 min | Recapitulação guiada — `docker-ssh-lab` | Idem, focando na sintaxe do SSH, nos quatro comandos permitidos e na ideia de "pista no nome do arquivo, não só no conteúdo". Vale reencenar rapidamente a lógica da sabotagem (por que trocar as coordenadas funciona). |
| 35–45 min | Simulado relâmpago | Escolher 3 a 5 perguntas de estilo parecido com o da prova (podem ser adaptadas das seções 5 ou das próprias provas, trocando os números/nomes) e resolver **em conjunto**, no quadro, pedindo que os alunos justifiquem a resposta em voz alta. |
| 45–50 min | Dúvidas e fechamento | Perguntas abertas da turma. Reforçar a lista de "o que estudar" (seção 6). |

## 5. Perguntas de recapitulação oral (uso do professor)

Use estas perguntas na etapa de recapitulação — são propositalmente **diferentes** das perguntas da prova escrita, para reforçar o conteúdo sem entregar as respostas do exame.

**Sobre o `docker-intro-lab`:**

1. O que o comando `docker run hello-world` verifica?
2. Antes do `hello-world`, que comando instala o Docker na VM?
3. Por que às vezes `docker --version` funciona mas `docker ps` dá erro logo em seguida? (dica: o daemon leva um tempo para ficar pronto — por isso criamos o `iniciar-docker`)
4. No comando `docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx`, o que aconteceria se a gente tirasse o `-v`?
5. Se eu editar o `index.html` e reiniciar o container do Nginx, o site continua com a edição? Por quê?
6. Por que cada equipe publica o Nginx sempre na porta 8080 *dentro* da VM, mesmo tendo portas públicas diferentes (83NN)?

**Sobre o `docker-ssh-lab` (Operação Nexus):**

7. Quais são os quatro comandos que a missão permite usar?
8. Por que a missão não deixa usar comandos como `rm` ou `mv`?
9. Se um arquivo se chama `geo_37.4220,-122.0841.log`, que tipo de pista isso pode ser, mesmo sem nenhuma empresa escrita no conteúdo?
10. Por que a "sabotagem" (trocar as coordenadas do alvo) precisa ser feita com as coordenadas certas, e não com qualquer número?
11. O que `ls -la` mostra que um `ls` simples não mostra?

## 6. O que estudar antes da prova (repassar para a turma)

- Reler os dois PDFs de briefing entregues nas aulas práticas.
- Praticar de cabeça o comando de conexão SSH (`ssh usuario@IP -p porta`) e o comando de publicar o site com Nginx.
- Saber explicar, com as próprias palavras, o que cada flag do `docker run` faz (`-d`, `-p`, `-v`, `--name`).
- Entender *por que* o volume garante persistência (não decorar só que "persiste").
- Lembrar os quatro comandos permitidos na Operação Nexus e a lógica de procurar pistas no nome dos arquivos.

## 7. Sobre a avaliação (AP1)

- Duas versões da prova (`Prova_A.pdf` e `Prova_B.pdf`) — mesma cobertura de conteúdo e mesma distribuição de dificuldade (4 questões muito fáceis, 4 fáceis, 2 médias), com perguntas e ordem diferentes, para reduzir cola entre alunos vizinhos.
- Pontuação: as 10 questões valem o mesmo, 1,0 pt cada — total 10,0 pts. A dificuldade varia só para equilibrar a prova, não a pontuação.
- As questões testam o conteúdo (comandos, conceitos, boas práticas) e não fazem referência direta às práticas/laboratórios em si — não citam nomes de equipe, de missão ou de laboratório.
- O gabarito comentado das duas provas está em `gabarito.md`, nesta mesma pasta (uso exclusivo do professor).

## 8. Slides e atividade de revisão

- `Slides_Revisao.pptx` — apresentação de apoio para conduzir esta aula (20 slides): roteiro, objetivos, os dois blocos de conteúdo (Docker e SSH/Linux) e um resumo do que cai na prova.
- `Atividade_Revisao.pdf` — atividade prática que pode ser aplicada durante ou ao final da aula (associação de comandos, comando para completar, verdadeiro/falso e duas questões abertas). Não vale nota; o gabarito está em `Atividade_Revisao_Gabarito.md` (uso exclusivo do professor).
