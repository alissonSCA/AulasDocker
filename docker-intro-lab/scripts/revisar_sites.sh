#!/bin/bash
# Mostra rapidamente o index.html que cada equipe deixou pronto.
# Roda no HOST (a máquina onde os containers estão), não precisa dos
# containers ativos nem de SSH: ./sites/teamNN é volume montado, então
# o conteúdo já está no host.
#
# Uso: ./scripts/revisar_sites.sh

cd "$(dirname "$0")/.." || exit 1

for n in $(seq -w 1 10); do
    f="sites/team${n}/index.html"
    echo "==================== Equipe ${n} ===================="
    if [ -f "$f" ]; then
        cat "$f"
    else
        echo "(sem index.html ainda — equipe não chegou a essa etapa)"
    fi
    echo
done
