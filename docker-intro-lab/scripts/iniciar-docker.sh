#!/bin/bash
# iniciar-docker — inicia o daemon do Docker dentro desta VM (container
# privileged, Docker-in-Docker) de um jeito confiável e SEMPRE igual,
# não importa a velocidade da máquina de cada equipe.
#
# POR QUE ISSO EXISTE
# "sudo service docker start" usa o init.d clássico (não tem systemd
# aqui dentro) e retorna assim que dispara o processo em segundo
# plano — sem esperar o daemon terminar de subir de verdade. Isso
# causa o problema clássico: "docker --version" funciona na hora
# (é só o cliente, não fala com o daemon), mas "docker ps" ainda dá
# erro de conexão logo em seguida, porque o daemon ainda está de pé.
# Dependendo da velocidade da máquina, isso é imprevisível: às vezes
# dá tempo, às vezes não — o que é ruim numa aula em que todo mundo
# devia ter a mesma experiência.
#
# Este script inicia o daemon e só devolve o terminal depois de
# confirmar, de verdade (com "docker info"), que ele está pronto para
# receber comandos.
#
# Uso: depois de instalar o Docker, rode:
#   iniciar-docker
#
# Depois disso, "docker ps", "docker run hello-world" etc. já podem
# ser usados imediatamente. Use sempre com sudo (ex.: "sudo docker
# ps"), já que o usuário da equipe não faz parte do grupo "docker".

set -u

if sudo docker info > /dev/null 2>&1; then
    echo "Docker já estava rodando."
    exit 0
fi

if ! command -v dockerd > /dev/null 2>&1; then
    echo "Docker ainda não está instalado. Rode primeiro:"
    echo "  sudo apt update && sudo apt install -y docker.io"
    exit 1
fi

echo "Iniciando o Docker..."
sudo service docker start > /dev/null 2>&1 || true

# Se o init.d não conseguiu subir o daemon (comum em containers sem
# systemd), sobe manualmente em segundo plano como último recurso.
if ! pgrep -x dockerd > /dev/null 2>&1; then
    sudo bash -c 'dockerd > /var/log/dockerd.log 2>&1 &'
fi

echo -n "Aguardando o Docker ficar pronto"
for i in $(seq 1 30); do
    if sudo docker info > /dev/null 2>&1; then
        echo " -> pronto! (${i}s)"
        exit 0
    fi
    echo -n "."
    sleep 1
done

echo
echo "O Docker não respondeu em 30s. Verifique o log com:"
echo "  cat /var/log/dockerd.log"
exit 1
