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

    # Aviso de segurança exibido no login — simula o banner de um
    # servidor corporativo real. Não contém nenhuma pista da missão.
    cat > /home/${TEAM_USER}/aviso_seguranca.txt << 'EOF'
=======================================================================
  AVISO DE SEGURANCA - USO RESTRITO
=======================================================================
  Este sistema e monitorado. O acesso e restrito a pessoal autorizado.
  Atividades desta sessao podem ser registradas para fins de auditoria.

  Ultima verificacao de integridade: OK
  Politica de seguranca da informacao: v4.2
=======================================================================
EOF

    # Adiciona ao bashrc
    echo "cat ~/aviso_seguranca.txt" >> /home/${TEAM_USER}/.bashrc
    echo 'export PS1="\u@\h:\w\$ "' >> /home/${TEAM_USER}/.bashrc
    echo 'alias ll="ls -la"' >> /home/${TEAM_USER}/.bashrc
    echo 'alias workspace="cd ~/workspace"' >> /home/${TEAM_USER}/.bashrc

    # Configura permissões
    chown ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/.bashrc
    chown ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/aviso_seguranca.txt
fi

# Garante que o workspace exista mesmo se o bloco acima foi pulado
# (usuário já existia de um boot anterior do mesmo container).
mkdir -p /home/${TEAM_USER}/workspace

# Gera os arquivos da missão desta equipe dentro do workspace (que é o
# volume montado em ./data/teamNN no host, então o conteúdo sobrevive
# a reinícios do container). O script é idempotente: se os arquivos já
# existirem (marcador .missao_gerada), ele não sobrescreve nada — isso
# protege o progresso da equipe (relatório, sabotagem) caso o
# container seja recriado no meio da aula.
python3 /opt/missao/gerar_arquivos_equipe.py "${TEAM_NUMBER}" "/home/${TEAM_USER}/workspace"

# Garante que a equipe seja dona de tudo que foi gerado (o gerador
# roda como root), para que consigam editar com nano normalmente.
chown -R ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/workspace

# Cria diretório de logs
mkdir -p /var/log/team${TEAM_NUMBER}
chown ${TEAM_USER}:${TEAM_USER} /var/log/team${TEAM_NUMBER}

echo "Usuário ${TEAM_USER} configurado com sucesso!"
