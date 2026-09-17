#!/bin/bash
# destruir_ambiente.sh — desmonta COMPLETAMENTE o laboratório
# docker-ssh-lab (Operação Nexus) depois da aula.
#
# O ambiente (10 VMs em container + rede) existe só para a prática em
# sala. Depois da aula ele deve ser destruído — não faz sentido deixar
# 10 servidores SSH rodando indefinidamente na máquina.
#
# O que este script remove:
#   - os containers das 10 equipes;
#   - a rede "lab-network";
#   - a imagem docker-ssh-lab:latest construída localmente.
#
# O que este script NÃO remove por padrão:
#   - data/teamNN (o workspace de cada equipe: sabotagem feita e
#     relatorio_missao.txt) — é o que você corrige com
#     scripts/corrigir_missao.py, então fica preservado até você
#     decidir apagar. Use --purge-data se também quiser apagar isso
#     (por exemplo, depois de já ter corrigido, ou antes de reusar o
#     laboratório numa turma nova);
#   - logs/teamNN — mesma lógica, incluído em --purge-data.
#
# Uso:
#   ./scripts/destruir_ambiente.sh                # remove só o ambiente Docker
#   ./scripts/destruir_ambiente.sh --purge-data    # também apaga data/* e logs/*
#   ./scripts/destruir_ambiente.sh -y              # não pergunta confirmação
#   ./scripts/destruir_ambiente.sh -y --purge-data # combina as duas opções

set -euo pipefail

cd "$(dirname "$0")/.."

PURGE_DATA=0
SKIP_CONFIRM=0
for arg in "$@"; do
    case "$arg" in
        --purge-data) PURGE_DATA=1 ;;
        -y|--yes) SKIP_CONFIRM=1 ;;
        *)
            echo "Opção desconhecida: $arg"
            echo "Uso: $0 [--purge-data] [-y]"
            exit 1
            ;;
    esac
done

echo "============================================================"
echo " Destruir ambiente: docker-ssh-lab (Operação Nexus)"
echo "============================================================"
echo "Isto vai parar e remover:"
echo "  - todos os containers das 10 equipes"
echo "  - a rede lab-network"
echo "  - a imagem docker-ssh-lab:latest"
if [ "$PURGE_DATA" -eq 1 ]; then
    echo "  - o conteúdo de data/teamNN e logs/teamNN (progresso da missão!)"
    echo "    -> se ainda não rodou 'python3 scripts/corrigir_missao.py',"
    echo "       faça isso ANTES de confirmar, ou a correção se perde."
else
    echo "data/teamNN e logs/teamNN NÃO serão apagados (use --purge-data)."
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
echo ">> Derrubando containers e rede..."
docker compose down -v --remove-orphans

echo ">> Removendo a imagem docker-ssh-lab:latest..."
docker rmi docker-ssh-lab:latest 2>/dev/null || echo "   (imagem já não existia)"

if [ "$PURGE_DATA" -eq 1 ]; then
    echo ">> Apagando data/* e logs/*..."
    rm -rf data/* logs/*
fi

echo
echo "Ambiente docker-ssh-lab destruído."
