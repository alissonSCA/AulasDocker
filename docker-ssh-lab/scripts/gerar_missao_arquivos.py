#!/usr/bin/env python3
"""
gerar_missao_arquivos.py

FERRAMENTA OPCIONAL para o professor. Você NÃO precisa rodar isto para
subir o laboratório: os containers já geram os arquivos da própria
equipe sozinhos, automaticamente, no primeiro boot (veja
scripts/setup-users.sh e scripts/gerar_arquivos_equipe.py). Basta:

    docker compose up -d --build

Use este script apenas se quiser, pelo host (sem precisar entrar em
nenhum container):
  - pré-visualizar o conteúdo de data/teamNN/ antes da aula; ou
  - resetar manualmente uma equipe específica (apague o arquivo
    data/teamNN/.missao_gerada e rode este script de novo, ou apague a
    pasta data/teamNN inteira).

Assim como o gerador usado dentro dos containers, este script é
idempotente: se data/teamNN/.missao_gerada já existir, aquela equipe é
pulada (não sobrescreve progresso).

Uso:
    cd docker-ssh-lab
    python3 scripts/gerar_missao_arquivos.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from missao_dados import TEAMS  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MARKER_NAME = ".missao_gerada"


def main() -> None:
    from missao_dados import build_team_files

    os.makedirs(DATA_DIR, exist_ok=True)
    for team in TEAMS:
        dest = os.path.join(DATA_DIR, team["team"])
        marker = os.path.join(dest, MARKER_NAME)
        if os.path.exists(marker):
            print(f"[missao] {team['team']}: já gerado, pulando (apague {marker} para resetar).")
            continue
        os.makedirs(dest, exist_ok=True)
        build_team_files(team, dest)
        with open(marker, "w", encoding="utf-8") as f:
            f.write("Arquivos de missao gerados. Nao apague este arquivo se quiser preservar o progresso da equipe.\n")
        print(f"[missao] {team['team']}: arquivos gerados em {dest}")

    print(f"\nConcluído. Diretório: {DATA_DIR}")


if __name__ == "__main__":
    main()
