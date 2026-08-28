#!/usr/bin/env python3
"""
corrigir_missao.py

Ferramenta de correção para o professor. Lê diretamente as pastas
data/teamNN/ no host (não precisa dos containers rodando, nem SSH,
nem docker exec — como data/ é volume montado, o conteúdo já está
aqui) e, para cada equipe, mostra:

  - a empresa e o alvo corretos (gabarito);
  - se a "sabotagem" (pergunta 4) foi feita corretamente, checando o
    conteúdo do arquivo de coordenadas do alvo;
  - o relatorio_missao.txt que a equipe escreveu, se existir, para
    você conferir as perguntas 1-3 de próprio punho;
  - um resumo final com todas as equipes.

Uso:
    cd docker-ssh-lab
    python3 scripts/corrigir_missao.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from missao_dados import TEAMS  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

COORD_TAG_RE = re.compile(r"<coordinates>\s*([\-0-9.]+)\s*,\s*([\-0-9.]+)")


def parse_coord_str(s: str):
    lat_str, lon_str = s.split(",")
    return float(lat_str), float(lon_str)


def find_kml(team_dir: str):
    conf_dir = os.path.join(team_dir, "documentos", "projetos", "confidencial")
    if not os.path.isdir(conf_dir):
        return None
    for fn in sorted(os.listdir(conf_dir)):
        if fn.endswith(".kml"):
            return os.path.join(conf_dir, fn)
    return None


def parse_kml_pair(path: str):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return None
    m = COORD_TAG_RE.search(content)
    if not m:
        return None
    n1, n2 = float(m.group(1)), float(m.group(2))
    return (n1, n2)


def pair_matches(pair, expected_lat_lon, tol=0.01):
    """True se `pair` (em qualquer ordem: lon,lat ou lat,lon) bate com
    as coordenadas esperadas, dentro de uma tolerância (equipes digitam
    os números manualmente, então toleramos pequenas diferenças de
    formatação — o que importa é se são os números certos)."""
    a, b = pair
    lat, lon = expected_lat_lon
    direct = abs(a - lat) < tol and abs(b - lon) < tol
    swapped = abs(a - lon) < tol and abs(b - lat) < tol
    return direct or swapped


def main() -> None:
    print("=" * 78)
    print("CORREÇÃO — OPERAÇÃO NEXUS")
    print("=" * 78)

    if not os.path.isdir(DATA_DIR):
        print(f"Diretório de dados não encontrado: {DATA_DIR}")
        sys.exit(1)

    resumo = []

    for team in TEAMS:
        team_dir = os.path.join(DATA_DIR, team["team"])
        print(f"\n--- {team['team'].upper()} ---")
        print(f"  Empresa correta  : {team['empresa']}")
        print(f"  Ação (codinome)  : {team['codinome']}")
        print(f"  Alvo correto     : {team['alvo']}")

        if not os.path.isdir(team_dir):
            print("  [!] Pasta da equipe não encontrada — os containers já subiram alguma vez?")
            resumo.append((team["team"], "N/D", "N/D"))
            continue

        empresa_coord = parse_coord_str(team["empresa_coord"])
        alvo_coord = parse_coord_str(team["alvo_coord"])

        kml_path = find_kml(team_dir)
        if kml_path is None:
            sabotagem_status = "ARQUIVO NÃO ENCONTRADO"
        else:
            pair = parse_kml_pair(kml_path)
            if pair is None:
                sabotagem_status = "ARQUIVO SEM COORDENADAS LEGÍVEIS (conferir manualmente)"
            elif pair_matches(pair, empresa_coord):
                sabotagem_status = "SIM — coordenadas trocadas para a empresa (sabotagem OK)"
            elif pair_matches(pair, alvo_coord):
                sabotagem_status = "NÃO — ainda aponta para o alvo original"
            else:
                sabotagem_status = f"COORDENADAS DIFERENTES DE AMBAS ({pair[0]:.4f}, {pair[1]:.4f}) — conferir manualmente"
        print(f"  Sabotagem (Q4)   : {sabotagem_status}")

        relatorio_path = os.path.join(team_dir, "relatorio_missao.txt")
        relatorio_existe = os.path.isfile(relatorio_path)
        if relatorio_existe:
            print("  Relatório entregue: SIM")
            print("  " + "-" * 50)
            with open(relatorio_path, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    print("  | " + line.rstrip())
            print("  " + "-" * 50)
        else:
            print("  Relatório entregue: NÃO (relatorio_missao.txt não encontrado em ~/workspace)")

        resumo.append((
            team["team"],
            "OK" if sabotagem_status.startswith("SIM") else "--",
            "OK" if relatorio_existe else "--",
        ))

    print("\n" + "=" * 78)
    print("RESUMO")
    print("=" * 78)
    print(f"{'Equipe':<10}{'Sabotagem':<12}{'Relatório':<10}")
    print("-" * 32)
    for team_id, sabotou, entregou in resumo:
        print(f"{team_id:<10}{sabotou:<12}{entregou:<10}")


if __name__ == "__main__":
    main()
