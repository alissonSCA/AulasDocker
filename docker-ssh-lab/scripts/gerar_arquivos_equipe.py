#!/usr/bin/env python3
"""
gerar_arquivos_equipe.py <numero_equipe> <diretorio_destino>

Gera a arvore de arquivos da missao para UMA equipe dentro do diretorio
de destino informado. E chamado automaticamente pelo entrypoint de cada
container (veja scripts/setup-users.sh), uma vez por equipe, usando o
workspace daquela equipe como destino.

IDEMPOTENTE: se o destino ja contiver o arquivo marcador
".missao_gerada", o script nao faz nada -- isso preserva qualquer
edicao feita pela equipe (o relatorio, a sabotagem das coordenadas
etc.) caso o container seja recriado (ex.: "docker compose up --build"
de novo no meio do curso). Para forcar a regeneracao de uma equipe
especifica, apague o marcador (ou a pasta inteira) e suba o container
de novo.

Uso tipico dentro do container:
    python3 /opt/missao/gerar_arquivos_equipe.py 01 /home/team01/workspace
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from missao_dados import TEAMS_BY_KEY, build_team_files  # noqa: E402

MARKER_NAME = ".missao_gerada"


def main() -> None:
    if len(sys.argv) != 3:
        print("uso: gerar_arquivos_equipe.py <numero_equipe ex: 01> <diretorio_destino>")
        sys.exit(1)

    numero = sys.argv[1]
    dest = sys.argv[2]
    team_key = f"team{numero}"

    team = TEAMS_BY_KEY.get(team_key)
    if team is None:
        print(f"[missao] equipe desconhecida: {team_key} (verifique missao_dados.py)")
        sys.exit(1)

    marker = os.path.join(dest, MARKER_NAME)
    if os.path.exists(marker):
        print(f"[missao] {team_key}: arquivos ja existem (marcador encontrado), preservando conteudo.")
        return

    os.makedirs(dest, exist_ok=True)
    build_team_files(team, dest)
    with open(marker, "w", encoding="utf-8") as f:
        f.write("Arquivos de missao gerados. Nao apague este arquivo se quiser preservar o progresso da equipe.\n")

    print(f"[missao] {team_key}: arquivos de missao gerados em {dest}")


if __name__ == "__main__":
    main()
