# Primeiro Contato com Docker — Laboratório SSH (10 VMs para equipes)

Aula prática de introdução ao Docker para turmas de curso técnico em
informática. A turma é dividida em 10 equipes; cada equipe conecta via
SSH numa VM própria (um container isolado), onde ela mesma:

1. instala o Docker (`sudo apt install docker.io`);
2. inicia o serviço e testa a instalação (`docker run hello-world`);
3. escreve um `index.html` próprio com `nano`;
4. sobe um servidor Nginx publicando essa página;
5. edita a página e "sobe de novo" para confirmar que o conteúdo
   persiste.

Este laboratório é **independente** do laboratório `docker-ssh-lab`
(Operação Nexus) — pode rodar antes dele, em outra aula, como
preparação. As portas usadas aqui (2301–2310 para SSH, 8301–8310 para
HTTP) foram escolhidas de propósito para não colidir com as portas
2201–2210 da Operação Nexus, caso um dia você precise subir os dois ao
mesmo tempo na mesma máquina.

---

## Como isso funciona por baixo dos panos (Docker-in-Docker)

Cada VM de equipe já É um container Docker rodando na sua máquina.
Para que dentro dele o aluno consiga instalar e usar o Docker de
verdade, o container da equipe roda em modo `privileged` — é isso que
dá a ele acesso ao kernel necessário para rodar outro daemon Docker
"dentro". É a mesma técnica usada por serviços como o Play with Docker
da própria Docker Inc.

Duas configurações já vêm pré-prontas na imagem (o aluno não precisa
saber disso nem fazer nada) para essa técnica funcionar de forma
confiável em qualquer host:

- **`storage-driver: vfs`** — evita incompatibilidades de rodar
  overlay2 "em cima" do overlay2 do seu host.
- **`iptables: false`** — evita erros de permissão ao Docker aninhado
  tentar mexer nas regras de iptables do host; a publicação de portas
  (`-p`) continua funcionando via *userland proxy* do próprio Docker.

Isso é mais lento que uma instalação normal do Docker, mas para uma
turma de 10 equipes rodando um único Nginx cada, a diferença é
imperceptível.

---

## Como subir o laboratório

Requisitos: Docker e Docker Compose na máquina que vai rodar os
containers, portas 2301–2310 e 8301–8310 livres nela, e os
computadores/celulares das equipes na mesma rede local dessa máquina.

```bash
cd docker-intro-lab
docker compose up -d --build
```

No dia da aula, descubra o IP da máquina na rede local (`ip a` ou
`hostname -I` no Linux, `ipconfig` no Windows) e anote na lousa — esse
endereço muda de rede para rede, então avise a turma verbalmente ou
escreva no quadro (os slides têm um espaço reservado para isso).

Cada equipe conecta com:

```bash
ssh teamNN@IP_DA_MAQUINA -p 23NN
```

| Equipe | Usuário | Porta SSH | Senha padrão | Porta HTTP (pra ver o site no navegador) |
|---|---|---|---|---|
| 01 | team01 | 2301 | team01pass | 8301 |
| 02 | team02 | 2302 | team02pass | 8302 |
| 03 | team03 | 2303 | team03pass | 8303 |
| 04 | team04 | 2304 | team04pass | 8304 |
| 05 | team05 | 2305 | team05pass | 8305 |
| 06 | team06 | 2306 | team06pass | 8306 |
| 07 | team07 | 2307 | team07pass | 8307 |
| 08 | team08 | 2308 | team08pass | 8308 |
| 09 | team09 | 2309 | team09pass | 8309 |
| 10 | team10 | 2310 | team10pass | 8310 |

As senhas padrão vêm de `docker-compose.yml` (variável `TEAM_PASSWORD`
de cada serviço) — troque lá se quiser senhas diferentes, antes de
subir os containers.

Dentro da VM, cada equipe deve publicar o próprio container Nginx na
porta **8080** (`docker run -d -p 8080:80 ...`) — é essa porta 8080
*interna* que o `docker-compose.yml` já mapeia para a porta pública
83NN de cada equipe. Isso está nos slides, mas vale reforçar
verbalmente durante a aula.

---

## ⚠️ TESTE ISSO ANTES DA AULA

Docker-in-Docker depende de detalhes do kernel/host que eu não
consigo testar por você nesta conversa (não tenho acesso a um
terminal na sua máquina neste momento). Faça este teste com
**pelo menos 1-2 dias de antecedência**, não na véspera:

```bash
cd docker-intro-lab
docker compose up -d --build team01
docker compose logs -f team01        # espera "Usuário team01 configurado com sucesso!"

ssh team01@localhost -p 2301         # senha: team01pass
# dentro da VM da equipe 01:
sudo apt update && sudo apt install -y docker.io
sudo service docker start            # se der erro, ver "Troubleshooting" abaixo
docker run hello-world               # tem que rodar sem erro
nano ~/site/index.html               # edite qualquer coisa e salve
docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx
curl localhost:8080                  # tem que devolver o HTML editado
exit
```

E de fora (no navegador ou com `curl`, na própria máquina host):

```bash
curl localhost:8301                  # tem que devolver o mesmo HTML
```

Se tudo isso funcionou, pode confiar no laboratório para a turma
inteira. Se algo falhou, veja a seção de Troubleshooting abaixo antes
de repetir para as outras 9 equipes.

Depois do teste, se quiser resetar a equipe 01 para o dia da aula:

```bash
docker compose down
rm -rf sites/team01
docker compose up -d --build
```

---

## Estrutura do projeto

```
docker-intro-lab/
├── docker-compose.yml          # define as 10 VMs (portas, privileged, volumes)
├── Dockerfile                  # imagem base (Ubuntu + SSH + sudo, sem Docker)
├── sites/teamNN/                # index.html de cada equipe (volume, sobrevive a restart)
├── scripts/
│   ├── setup-users.sh            # entrypoint: cria o usuário e o index.html inicial
│   ├── healthcheck.sh
│   └── revisar_sites.sh          # mostra o index.html de todas as equipes (roda no host)
└── README.md
```

---

## Como revisar depois da aula

```bash
./scripts/revisar_sites.sh
```

Mostra o `index.html` final de cada equipe direto do host — não
precisa dos containers ativos nem de SSH, porque `sites/teamNN` é
volume montado.

---

## Troubleshooting

**`sudo service docker start` não funciona / "Unit docker.service not
found" ou parecido.** O container não tem systemd, então use o
comando alternativo ensinado nos slides:

```bash
sudo dockerd > /tmp/dockerd.log 2>&1 &
sleep 3
docker version
```

Se aparecer erro de cgroup ("cgroups: cgroup mountpoint does not
exist" ou similar), o host provavelmente está em cgroup v1 e a chave
`cgroup: host` do `docker-compose.yml` não resolveu. Tente remover a
linha `cgroup: host` de cada serviço no `docker-compose.yml` e suba de
novo (`docker compose up -d --build`).

**`docker compose` reclama da chave `cgroup: host` ao subir.** Sua
versão do Docker Compose é mais antiga. Apague a linha `cgroup: host`
dos serviços em `docker-compose.yml` — o laboratório funciona sem ela
na maioria dos hosts modernos, só fica um pouco mais frágil em cgroup
v2.

**Uma equipe não consegue conectar via SSH.** Confira se a porta certa
está livre no host (`docker compose ps`) e se o firewall da máquina
libera as faixas 2301–2310 e 8301–8310 na rede local.

**O site não abre no navegador (porta 83NN), mas `curl localhost:8080`
funciona dentro da VM.** A equipe provavelmente publicou o Nginx numa
porta diferente de 8080 (por exemplo, `-p 80:80`). Peça pra conferir
com `docker ps` e refazer o `docker run` com `-p 8080:80`.

**`docker run hello-world` trava ou dá timeout tentando baixar a
imagem.** A VM da equipe não tem internet — confira a rede da máquina
host e se o firewall não está bloqueando a saída dos containers.

**Quero reiniciar tudo do zero (outra turma, outro dia).**

```bash
docker compose down -v      # o -v também apaga os volumes de dados do Docker aninhado
rm -rf sites/*
docker compose up -d --build
```

**Quero resetar só uma equipe.**

```bash
docker compose stop team03
docker compose rm -f team03
docker volume rm docker-intro-lab_team03_docker_data
rm -rf sites/team03
docker compose up -d --build team03
```
