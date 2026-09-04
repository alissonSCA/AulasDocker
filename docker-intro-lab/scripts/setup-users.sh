#!/bin/bash
set -e

# Script para criar o usuário da equipe (roda como entrypoint, toda vez
# que o container sobe).
TEAM_NUMBER=${TEAM_NUMBER:-01}
TEAM_USER="team${TEAM_NUMBER}"
TEAM_PASSWORD=${TEAM_PASSWORD:-"team${TEAM_NUMBER}pass"}

if ! id -u ${TEAM_USER} > /dev/null 2>&1; then
    echo "Criando usuário: ${TEAM_USER}"
    useradd -m -s /bin/bash ${TEAM_USER}
    echo "${TEAM_USER}:${TEAM_PASSWORD}" | chpasswd
    usermod -aG sudo ${TEAM_USER}

    # sudo sem senha: é a primeira aula prática de Docker da turma, o
    # tempo é curto e não faz sentido pedir senha a cada "sudo apt
    # install" / "sudo dockerd". Cada equipe só tem acesso à própria VM
    # (container isolado), então o risco fica contido ali dentro.
    echo "${TEAM_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${TEAM_USER}
    chmod 440 /etc/sudoers.d/${TEAM_USER}

    mkdir -p /home/${TEAM_USER}/site
    chown -R ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}

    echo 'export PS1="\u@\h:\w\$ "' >> /home/${TEAM_USER}/.bashrc
    echo 'alias ll="ls -la"' >> /home/${TEAM_USER}/.bashrc
    chown ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/.bashrc
fi

# Garante que ~/site exista mesmo se o usuário já existia de um boot
# anterior (por exemplo, container recriado no meio do curso).
mkdir -p /home/${TEAM_USER}/site

# Cria um index.html inicial só se ainda não existir um — assim a
# equipe já tem algo pra ver no navegador antes de editar, mas se ela
# já editou o arquivo (volume persistente), não sobrescrevemos nada.
if [ ! -f /home/${TEAM_USER}/site/index.html ]; then
cat > /home/${TEAM_USER}/site/index.html << EOF
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Equipe ${TEAM_NUMBER}</title>
</head>
<body>
  <h1>Site da Equipe ${TEAM_NUMBER}</h1>
  <p>Ainda em construção... edite este arquivo com o nano e suba de novo!</p>
</body>
</html>
EOF
fi
chown -R ${TEAM_USER}:${TEAM_USER} /home/${TEAM_USER}/site

mkdir -p /var/log/${TEAM_USER}
chown ${TEAM_USER}:${TEAM_USER} /var/log/${TEAM_USER} 2>/dev/null || true

echo "Usuário ${TEAM_USER} configurado com sucesso!"
