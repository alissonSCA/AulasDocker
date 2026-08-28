FROM ubuntu:22.04

# Variáveis de ambiente
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

# Instala serviços essenciais
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    vim \
    nano \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    net-tools \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Configura SSH
RUN mkdir /var/run/sshd && \
    echo 'root:root123' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Script de setup de usuários (cria o usuário da equipe e dispara a
# geração dos arquivos da missão daquela equipe)
COPY scripts/setup-users.sh /usr/local/bin/setup-users.sh
RUN chmod +x /usr/local/bin/setup-users.sh

# Script de healthcheck
COPY scripts/healthcheck.sh /usr/local/bin/healthcheck.sh
RUN chmod +x /usr/local/bin/healthcheck.sh

# Dados da missão (o "gabarito": nomes reais de empresas/alvos e o
# gerador que popula o workspace de cada equipe). Fica fora do PATH,
# em pasta só de root, com permissão 600 -- as equipes conectam como
# usuários sem privilégio e não conseguem ler nem listar este
# diretório, então não há como "ler o gabarito" pelo SSH delas.
RUN mkdir -p /opt/missao
COPY scripts/missao_dados.py /opt/missao/missao_dados.py
COPY scripts/gerar_arquivos_equipe.py /opt/missao/gerar_arquivos_equipe.py
RUN chown -R root:root /opt/missao && \
    chmod 700 /opt/missao && \
    chmod 600 /opt/missao/*.py

# Porta SSH
EXPOSE 22

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh

# Entrypoint
CMD ["/bin/bash", "-c", "/usr/local/bin/setup-users.sh && /usr/sbin/sshd -D"]
