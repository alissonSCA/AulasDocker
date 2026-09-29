# AulasDocker

Materiais de aula para uma disciplina de Docker e Linux/SSH em um curso técnico em informática: uma aula teórica, dois laboratórios práticos com Docker-in-Docker (10 VMs por turma, uma por equipe) e o material de revisão/avaliação (AP1) que cobre os dois laboratórios.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`aula-teorica-docker-linux/`](aula-teorica-docker-linux) | Slides e PDF da aula teórica de fundamentos (Docker + Linux) que antecede os laboratórios. |
| [`docker-intro-lab/`](docker-intro-lab) | Laboratório "Primeiro Contato com Docker": cada equipe conecta via SSH na própria VM, instala o Docker, testa com `hello-world` e sobe um site Nginx com volume persistente. |
| [`docker-ssh-lab/`](docker-ssh-lab) | "Operação Nexus": atividade de comandos Linux (`ls`, `cd`, `cat`, `nano`) em que cada equipe investiga pistas escondidas em nomes de arquivo e edita um arquivo para "sabotar" a missão. |
| [`AP1/`](AP1) | Plano de aula de revisão, slides, atividade de revisão, duas versões da prova (A/B) e os respectivos gabaritos (uso exclusivo do professor). |
| `Claude outputs/` | Cópias dos entregáveis gerados (PDFs, PPTX, gabaritos) da AP1 e da aula teórica, mantidas junto com os arquivos-fonte de cada pasta. |

## Ordem recomendada de uso

1. **Aula teórica** (`aula-teorica-docker-linux/`) — fundamentos de Docker e Linux antes da prática.
2. **`docker-intro-lab/`** — primeiro contato com Docker (pode rodar em outra aula, é independente do laboratório seguinte).
3. **`docker-ssh-lab/`** (Operação Nexus) — prática de comandos Linux via SSH.
4. **`AP1/`** — aula de revisão dos dois laboratórios, seguida da avaliação (prova A/B).

Cada laboratório (`docker-intro-lab/` e `docker-ssh-lab/`) tem seu próprio `README.md` com instruções detalhadas de como subir o ambiente, credenciais de cada equipe, estrutura de arquivos e solução de problemas.

## Requisitos gerais

- Docker e Docker Compose na máquina que vai hospedar os containers.
- Todos os computadores/celulares das equipes na mesma rede local dessa máquina.
- Portas livres no host: **2201–2210** (SSH, uma por equipe, convenção `22NN` usada nos dois laboratórios) e **8301–8310** (HTTP, exclusiva do `docker-intro-lab`).

Os dois laboratórios usam Docker-in-Docker (containers `privileged` simulando uma VM por equipe) — os detalhes técnicos e o passo a passo de teste antes da aula estão no README de cada laboratório.

## Autor

Alisson Sampaio de Carvalho Alencar
