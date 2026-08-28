# Operação Nexus — Laboratório Docker SSH (10 VMs para equipes)

Atividade de comandos Linux para turmas de curso técnico em informática.
A turma é dividida em 10 equipes; cada equipe "invade" via SSH o
servidor de uma corporação diferente e usa apenas `ls`, `cd`, `cat` e
`nano` para:

1. descobrir qual empresa foi invadida;
2. descobrir qual ação (uma sabotagem inofensiva e bem-humorada, tipo
   "encher um estádio de patinhos de borracha") está sendo planejada;
3. descobrir qual é o alvo dessa ação;
4. **sabotar o ataque**: editar, com `nano`, o arquivo que registra as
   coordenadas do alvo, trocando-as pelas coordenadas da própria
   empresa invadida.

Nenhum arquivo entregue às equipes contém o nome da empresa ou do
alvo por escrito — só as coordenadas geográficas (latitude/longitude),
escondidas no **nome** dos arquivos. As equipes precisam deduzir o
que existe naquele ponto do mapa por conta própria.

O briefing da missão (contexto, tabela de conexão, comandos
permitidos, perguntas) é entregue às equipes em PDF:
`Operacao_Nexus_Briefing_Missao.pdf`. Esse PDF é a única orientação
que os alunos recebem — a máquina "invadida" não tem nenhuma dica.

---

## Como subir o laboratório

Requisitos: Docker e Docker Compose, portas 2201–2210 livres na
máquina que vai rodar os containers, e todos os computadores das
equipes na mesma rede local dessa máquina.

```bash
git clone <este-repositório>
cd docker-ssh-lab
docker compose up -d --build
```

Pronto. Não é preciso rodar nenhum script manualmente antes — cada
container, ao subir, cria o usuário da própria equipe e gera
automaticamente a árvore de arquivos daquela equipe dentro do
workspace (que é o volume montado em `data/teamNN`, então o conteúdo
já fica salvo no host). Isso é feito por
`scripts/gerar_arquivos_equipe.py`, chamado pelo entrypoint em
`scripts/setup-users.sh`.

**No dia da aula**, descubra o IP da máquina na rede local (`ip a` ou
`hostname -I` no Linux/Mac, `ipconfig` no Windows) e anote na lousa —
esse endereço não dá para saber com antecedência, então o PDF deixa o
campo em branco para você preencher à mão nas cópias impressas.

Cada equipe conecta com:

```bash
ssh teamNN@IP_DA_MAQUINA -p 22NN
```

| Equipe | Usuário | Porta | Senha padrão |
|---|---|---|---|
| 01 | team01 | 2201 | team01pass |
| 02 | team02 | 2202 | team02pass |
| 03 | team03 | 2203 | team03pass |
| 04 | team04 | 2204 | team04pass |
| 05 | team05 | 2205 | team05pass |
| 06 | team06 | 2206 | team06pass |
| 07 | team07 | 2207 | team07pass |
| 08 | team08 | 2208 | team08pass |
| 09 | team09 | 2209 | team09pass |
| 10 | team10 | 2210 | team10pass |

As senhas padrão vêm de `docker-compose.yml` (variável
`TEAM_PASSWORD` de cada serviço) — troque lá se quiser senhas
diferentes, antes de subir os containers.

---

## Estrutura do projeto

```
docker-ssh-lab/
├── docker-compose.yml          # define as 10 VMs (portas, usuários, volumes)
├── Dockerfile                  # imagem base (Ubuntu + SSH + as ferramentas permitidas)
├── data/teamNN/                 # workspace de cada equipe (volume, populado automaticamente)
├── logs/teamNN/                 # logs de cada equipe
├── scripts/
│   ├── setup-users.sh            # entrypoint: cria o usuário e dispara a geração da missão
│   ├── healthcheck.sh
│   ├── missao_dados.py           # GABARITO: empresas, alvos, coordenadas, textos (não vai pros alunos)
│   ├── gerar_arquivos_equipe.py  # gera os arquivos de UMA equipe (roda dentro do container)
│   ├── gerar_missao_arquivos.py  # ferramenta opcional: gera todas no host, sem Docker
│   └── corrigir_missao.py        # ferramenta de correção (roda no host, lê data/teamNN)
└── Operacao_Nexus_Briefing_Missao.pdf   # o que você imprime e entrega às equipes
```

`scripts/missao_dados.py` e `scripts/gerar_arquivos_equipe.py` também
são copiados para dentro da imagem, em `/opt/missao/`, com permissão
`700`/`600` e dono `root` — ou seja, **as equipes conectadas via SSH
não conseguem listar nem ler esses arquivos**, mesmo saindo do próprio
workspace. É assim que o "gabarito" (nomes reais de empresas e alvos)
fica fora do alcance delas mesmo estando dentro da mesma imagem
Docker. Isso foi testado manualmente (usuário sem privilégio recebe
"Permission denied" tanto para `ls` quanto para `cat` em `/opt/missao`).

---

## Como funciona a geração dos arquivos (e por que é segura contra reinícios)

Cada container, ao iniciar, roda:

```bash
python3 /opt/missao/gerar_arquivos_equipe.py "$TEAM_NUMBER" "/home/teamNN/workspace"
```

Esse script é **idempotente**: ele só gera os arquivos se ainda não
existir um marcador `.missao_gerada` dentro do workspace. Ou seja, se
você precisar rodar `docker compose up -d --build` de novo no meio do
curso (por exemplo, depois de um ajuste qualquer), os containers são
recriados mas **o progresso das equipes não é apagado** — o volume
`data/teamNN` já tem o marcador, então nada é sobrescrito.

Para resetar uma equipe específica (por exemplo, para reusar o
laboratório em outra turma), pare os containers e apague a pasta
`data/teamNN` inteira (ou só o arquivo `data/teamNN/.missao_gerada`,
se quiser manter alguma coisa); no próximo `docker compose up`, aquele
container gera tudo de novo do zero.

```bash
docker compose down
rm -rf data/team03      # exemplo: resetar só a equipe 03
docker compose up -d
```

---

## Como corrigir

Depois da aula (ou mesmo durante, se quiser acompanhar), rode a
partir da raiz do projeto, na máquina onde os containers estão
rodando:

```bash
python3 scripts/corrigir_missao.py
```

Não precisa dos containers ativos, nem SSH, nem `docker exec`:
como `data/teamNN` é volume montado, o script lê os arquivos
diretamente do host. Para cada equipe, ele mostra:

- a empresa e o alvo corretos (gabarito);
- se a sabotagem (pergunta 4) foi feita corretamente — ele lê o
  arquivo de coordenadas do alvo e compara com as coordenadas da
  empresa, tolerando pequenas variações de formatação (a equipe digita
  os números manualmente, então não é exigida uma correspondência
  byte-a-byte);
- o conteúdo do `relatorio_missao.txt` que a equipe escreveu com
  `nano` (perguntas 1-3, que são texto livre e por isso não são
  corrigidas automaticamente — mas ficam ali, lado a lado com o
  gabarito, para conferência rápida);
- um resumo final com todas as equipes.

---

## Como personalizar (outras turmas, outras empresas)

Toda a definição da missão está em `scripts/missao_dados.py`, numa
lista `TEAMS` com um dicionário por equipe:

```python
dict(
    team="team01",
    empresa="Google",
    empresa_coord="37.4220,-122.0841",   # lat,lon da sede/instalação
    alvo="Times Square, Nova York",
    alvo_coord="40.7580,-73.9855",        # lat,lon do alvo
    codinome="Operação Pato Amarelo",
    ataque="Assumir o controle dos painéis digitais do local-alvo...",
),
```

Para trocar uma empresa, um alvo ou o texto do "ataque", edite essa
lista (mantenha os nomes de campo). Depois de editar, se algum
container já tiver gerado os arquivos daquela equipe, apague a pasta
`data/teamNN` correspondente antes de subir de novo — do contrário o
marcador `.missao_gerada` faz o container preservar o conteúdo antigo.

Algumas regras para manter a mecânica funcionando:

- `empresa_coord` e `alvo_coord` sempre no formato `"lat,lon"` (duas
  casas decimais pra cima, sem espaço).
- O texto de `ataque` é a resposta da pergunta 2 e é lido em texto
  corrido pelas equipes — mantenha inofensivo (sem violência, sem
  nenhum detalhe tecnicamente reproduzível).
- Evite empresas/locais cujo nome apareça sem querer em outro lugar
  do texto (o gerador varre os arquivos de saída, mas vale conferir
  na hora de revisar).

---

## Ferramentas permitidas dentro do container

A imagem instala `ls`, `cd` (builtin do bash), `cat`, `nano` (e
outras ferramentas padrão do Ubuntu — o Dockerfile não bloqueia
comandos). A restrição a essas quatro ferramentas é uma regra da
atividade, reforçada no PDF, não um sandbox técnico: em uma sala de
aula supervisionada isso é suficiente, mas se quiser reforçar
tecnicamente (por exemplo, com um shell restrito), essa é uma
extensão que pode ser feita no `Dockerfile`/`setup-users.sh`.

---

## Solução de problemas

**Uma equipe não consegue conectar via SSH.** Confira se a porta
certa está livre no host (`docker compose ps`) e se o firewall da
máquina libera a faixa 2201–2210 na rede local.

**Quero reiniciar tudo do zero (outra turma, outro dia).**

```bash
docker compose down
rm -rf data/* logs/*
docker compose up -d --build
```

**Uma equipe travou dentro do `nano`.** `Ctrl+X` sai (perguntando se
quer salvar); se estiver realmente preso, feche a sessão SSH
(`Ctrl+D` ou `exit` em outro terminal) e reconecte — o processo do
`nano` daquela sessão morre junto.

**Quero pré-visualizar o conteúdo antes da aula sem subir o Docker.**

```bash
python3 scripts/gerar_missao_arquivos.py
```

Gera `data/teamNN` no host diretamente (mesma lógica, mesmo
idempotente). Totalmente opcional — o `docker compose up -d --build`
sozinho já é suficiente no dia da aula.
