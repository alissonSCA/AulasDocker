#!/bin/bash

# Script para criar usuário da equipe
TEAM_NUMBER=${TEAM_NUMBER:-01}
TEAM_USER="team${TEAM_NUMBER}"
TEAM_PASSWORD=${TEAM_PASSWORD:-"team${TEAM_NUMBER}pass"}

# Cria usuário se não existir
if ! id -u ${TEAM_USER} > /dev/null 2>&1; then
    echo "Criando usuário: ${TEAM_USER}"
    useradd -m -s /bin/bash ${TEAM_USER}
    echo "${TEAM_USER}:${TEAM_PASSWORD}" | chpasswd
    usermod -aG sudo ${TEAM_USER}
    
    # Configuração do ambiente do usuário
    mkdir -p /home/${TEAM_USER}/workspace
    mkdir -p /home/${TEAM_USER}/.ssh
    chown -R ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}
    chmod 700 /home/${TEAM_USER}/.ssh
    
    # Cria arquivo de boas-vindas
    cat > /home/${TEAM_USER}/welcome.txt << EOF
===========================================
  Bem-vindo(a) Equipe ${TEAM_NUMBER}!
===========================================

Informações do ambiente:
- Hostname: $(hostname)
- Usuário: ${TEAM_USER}
- Workspace: ~/workspace

Comandos úteis:
- ssh team${TEAM_NUMBER}@$(hostname -I | awk '{print $1}') -p 22
- Para sair: exit

Bons estudos!
===========================================
EOF

    # Adiciona ao bashrc
    echo "cat ~/welcome.txt" >> /home/${TEAM_USER}/.bashrc
    echo 'export PS1="\u@\h:\w\$ "' >> /home/${TEAM_USER}/.bashrc
    echo 'alias ll="ls -la"' >> /home/${TEAM_USER}/.bashrc
    echo 'alias workspace="cd ~/workspace"' >> /home/${TEAM_USER}/.bashrc
    
    # Configura permissões
    chown ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/.bashrc
fi

# Cria diretório de logs
mkdir -p /var/log/team${TEAM_NUMBER}
chown ${TEAM_USER}:${TEAM_USER} /var/log/team${TEAM_NUMBER}

echo "Usuário ${TEAM_USER} configurado com sucesso!"
