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

# Script de setup de usuários
COPY scripts/setup-users.sh /usr/local/bin/setup-users.sh
RUN chmod +x /usr/local/bin/setup-users.sh

# Script de healthcheck
COPY scripts/healthcheck.sh /usr/local/bin/healthcheck.sh
RUN chmod +x /usr/local/bin/healthcheck.sh

# Porta SSH
EXPOSE 22

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh

# Entrypoint
CMD ["/bin/bash", "-c", "/usr/local/bin/setup-users.sh && /usr/sbin/sshd -D"]
