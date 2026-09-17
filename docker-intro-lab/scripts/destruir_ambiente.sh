#!/bin/bash
# destruir_ambiente.sh — desmonta COMPLETAMENTE o laboratório
# docker-intro-lab depois da aula.
#
# O ambiente (10 VMs em container, redes e volumes de Docker-in-Docker)
# existe só para a prática em sala. Depois da aula ele deve ser
# destruído — não faz sentido deixar 10 containers privileged rodando
# indefinidamente na máquina.
#
# O que este script remove:
#   - os containers das 10 equipes (e o serviço-base "team-base");
#   - a rede "lab-network";
#   - os volumes nomeados teamNN_docker_data (o "disco" do Docker
#     aninhado de cada equipe — pode ser grande, já que cada equipe
#     baixou pelo menos a imagem do hello-world e do nginx);
#   - a imagem docker-intro-lab:latest construída localmente.
#
# O que este script NÃO remove por padrão:
#   - a pasta sites/teamNN (o index.html final de cada equipe) — é o
#     "resultado" da aula, então fica preservado para você revisar com
#     ./scripts/revisar_sites.sh depois. Use --purge-sites se também
#     quiser apagar isso (por exemplo, antes de reusar o laboratório
#     numa turma nova).
#
# Uso:
#   ./scripts/destruir_ambiente.sh                 # remove só o ambiente Docker
#   ./scripts/destruir_ambiente.sh --purge-sites    # também apaga sites/*
#   ./scripts/destruir_ambiente.sh -y               # não pergunta confirmação
#   ./scripts/destruir_ambiente.sh -y --purge-sites # combina as duas opções

set -euo pipefail

cd "$(dirname "$0")/.."

PURGE_SITES=0
SKIP_CONFIRM=0
for arg in "$@"; do
    case "$arg" in
        --purge-sites) PURGE_SITES=1 ;;
        -y|--yes) SKIP_CONFIRM=1 ;;
        *)
            echo "Opção desconhecida: $arg"
            echo "Uso: $0 [--purge-sites] [-y]"
            exit 1
            ;;
    esac
done

echo "============================================================"
echo " Destruir ambiente: docker-intro-lab"
echo "============================================================"
echo "Isto vai parar e remover:"
echo "  - todos os containers das 10 equipes (+ team-base)"
echo "  - a rede lab-network"
echo "  - os 10 volumes teamNN_docker_data"
echo "  - a imagem docker-intro-lab:latest"
if [ "$PURGE_SITES" -eq 1 ]; then
    echo "  - o conteúdo de sites/teamNN (index.html de cada equipe)"
else
    echo "sites/teamNN NÃO será apagado (use --purge-sites para isso também)."
fi
echo

if [ "$SKIP_CONFIRM" -ne 1 ]; then
    read -r -p "Confirma a destruição do ambiente? (s/N) " resp
    case "$resp" in
        s|S|sim|SIM) ;;
        *) echo "Cancelado."; exit 0 ;;
    esac
fi

echo
echo ">> Derrubando containers, rede e volumes (todos os profiles)..."
docker compose --profile nao-iniciar-diretamente down -v --remove-orphans

echo ">> Removendo a imagem docker-intro-lab:latest..."
docker rmi docker-intro-lab:latest 2>/dev/null || echo "   (imagem já não existia)"

if [ "$PURGE_SITES" -eq 1 ]; then
    echo ">> Apagando sites/*..."
    rm -rf sites/*
fi

echo
echo "Ambiente docker-intro-lab destruído."
