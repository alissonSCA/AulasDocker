FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Fortaleza

# Ferramentas do "sistema operacional" da VM de cada equipe.
# Docker NÃO é instalado aqui de propósito — é o que os alunos vão
# instalar durante a aula.
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    nano \
    vim \
    curl \
    wget \
    ca-certificates \
    git \
    net-tools \
    iproute2 \
    iputils-ping \
    dnsutils \
    less \
    && rm -rf /var/lib/apt/lists/*

# Configura SSH
RUN mkdir /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Pré-configura o Docker que os alunos ainda vão instalar: storage-driver
# "vfs" evita problemas de overlay-em-overlay (Docker dentro de Docker) e
# "iptables": false evita erros de permissão ao mexer nas regras de
# iptables do host a partir de dentro do container aninhado. Os alunos
# não precisam saber disso nem fazer nada — quando eles rodarem
# "sudo apt install docker.io" e iniciarem o serviço, o daemon já vai
# ler esse arquivo sozinho.
RUN mkdir -p /etc/docker && \
    printf '{\n  "storage-driver": "vfs",\n  "iptables": false\n}\n' > /etc/docker/daemon.json

COPY scripts/setup-users.sh /usr/local/bin/setup-users.sh
RUN chmod +x /usr/local/bin/setup-users.sh
COPY scripts/healthcheck.sh /usr/local/bin/healthcheck.sh
RUN chmod +x /usr/local/bin/healthcheck.sh

# Helper que os alunos rodam depois de instalar o Docker
# ("iniciar-docker"): garante que o daemon suba e fique pronto de
# forma determinística para todo mundo, em vez de depender do timing
# de "sudo service docker start" (ver comentários no próprio script).
COPY scripts/iniciar-docker.sh /usr/local/bin/iniciar-docker
RUN chmod +x /usr/local/bin/iniciar-docker

# 22 = SSH da equipe. 8080 = porta onde a equipe vai publicar o próprio
# container Nginx lá dentro (mapeada por fora em docker-compose.yml).
EXPOSE 22 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh

CMD ["/bin/bash", "-c", "/usr/local/bin/setup-users.sh && /usr/sbin/sshd -D"]
