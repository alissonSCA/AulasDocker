#!/usr/bin/env python3
"""
missao_dados.py

Fonte única de verdade dos dados da missão (Operação Nexus): as 10
equipes, as empresas "invadidas", os alvos e as ações planejadas, além
das funções que geram o conteúdo de cada arquivo da árvore de pastas.

Este módulo é importado por:
  - gerar_arquivos_equipe.py  (roda dentro de cada container, gera só a
    equipe correspondente ao TEAM_NUMBER daquele container)
  - gerar_missao_arquivos.py  (ferramenta opcional para o professor
    rodar no host, fora do Docker, para pré-visualizar ou resetar)
  - corrigir_missao.py        (lê os arquivos já gerados para conferir
    as respostas de cada equipe)

IMPORTANTE: este arquivo contém os nomes reais das empresas e dos
alvos. Nenhum desses nomes é escrito nos arquivos entregues às
equipes -- só as coordenadas aparecem lá. Dentro da imagem Docker,
este arquivo fica em /opt/missao com permissão 600 (só root lê), então
as equipes não têm como abrir este "gabarito" pelo SSH delas.

PARA PERSONALIZAR A ATIVIDADE (outro professor reproduzindo):
Edite a lista TEAMS abaixo. Cada equipe precisa de:
  team           -> "team01".."team10" (deve bater com o docker-compose.yml)
  empresa        -> nome real da empresa (só aparece aqui, nunca nos arquivos)
  empresa_coord  -> "lat,lon" da sede/instalação da empresa
  alvo           -> nome real do alvo (só aparece aqui, nunca nos arquivos)
  alvo_coord     -> "lat,lon" do alvo
  codinome       -> nome fantasia da operação (aparece no memorando)
  ataque         -> descrição da ação planejada (aparece no memorando,
                     é a resposta da pergunta 2 -- mantenha inofensivo
                     e sem nenhum detalhe tecnicamente reproduzível)
"""

import os
import textwrap

TEAMS = [
    dict(
        team="team01",
        empresa="Google",
        empresa_coord="37.4220,-122.0841",
        alvo="Times Square, Nova York",
        alvo_coord="40.7580,-73.9855",
        codinome="Operação Pato Amarelo",
        ataque=(
            "Assumir o controle dos paineis digitais do local-alvo e "
            "programa-los para exibir, em loop continuo, uma animacao de "
            "patinhos de borracha gigantes dancando ao som de 'Rubber "
            "Duckie'. Sincronizar o efeito com a liberacao de 5 mil "
            "patinhos infláveis sobre o publico."
        ),
    ),
    dict(
        team="team02",
        empresa="Amazon",
        empresa_coord="47.6205,-122.3493",
        alvo="Wembley Stadium, Londres",
        alvo_coord="51.5560,-0.2795",
        codinome="Operação Chuva de Confete",
        ataque=(
            "Redirecionar a frota de entregas automatizadas para "
            "sobrevoar o local-alvo durante o evento principal e "
            "liberar, ao mesmo tempo, milhares de bolinhas de confete e "
            "purpurina biodegradavel sobre o gramado."
        ),
    ),
    dict(
        team="team03",
        empresa="Microsoft",
        empresa_coord="47.6423,-122.1390",
        alvo="Aeroporto Internacional de Dubai",
        alvo_coord="25.2532,55.3657",
        codinome="Operação Elevador Fedorento",
        ataque=(
            "Reprogramar o sistema de som do local-alvo para tocar "
            "apenas musicas de elevador em volume baixo e, "
            "simultaneamente, liberar pelos dutos de ventilacao uma "
            "nuvem de bolhas de sabao com forte cheiro de repolho."
        ),
    ),
    dict(
        team="team04",
        empresa="Apple",
        empresa_coord="37.3349,-122.0090",
        alvo="Estádio do Maracanã, Rio de Janeiro",
        alvo_coord="-22.9121,-43.2302",
        codinome="Operação Maçã Dourada",
        ataque=(
            "Sincronizar o som de notificacao de celular mais famoso do "
            "mundo em todos os teloes e alto-falantes do local-alvo, "
            "seguido da liberacao de confete em formato do logotipo de "
            "uma maca mordida."
        ),
    ),
    dict(
        team="team05",
        empresa="Tesla",
        empresa_coord="30.2207,-97.6187",
        alvo="Golden Gate Bridge, São Francisco",
        alvo_coord="37.8199,-122.4783",
        codinome="Operação Freio de Bolha",
        ataque=(
            "Fazer com que toda a frota de veiculos autonomos da regiao "
            "pare simultaneamente sobre o local-alvo e abra os tetos "
            "solares, liberando uma chuva de bolhas de sabao coloridas "
            "sobre pedestres e turistas."
        ),
    ),
    dict(
        team="team06",
        empresa="Meta (Facebook)",
        empresa_coord="37.4847,-122.1477",
        alvo="Torre Eiffel, Paris",
        alvo_coord="48.8584,2.2945",
        codinome="Operação Balão Azul",
        ataque=(
            "Publicar, em massa e ao mesmo tempo, uma noticia falsa nas "
            "redes sociais anunciando que o local-alvo foi comprado por "
            "uma rede social, provocando uma enxurrada de curiosos "
            "carregando baloes azuis."
        ),
    ),
    dict(
        team="team07",
        empresa="Samsung",
        empresa_coord="37.2581,127.0564",
        alvo="Cruzamento de Shibuya, Tóquio",
        alvo_coord="35.6595,139.7005",
        codinome="Operação Bipe Global",
        ataque=(
            "Disparar, em volume maximo e ao mesmo tempo, o som de "
            "notificacao de smartphone mais reconhecivel do mercado em "
            "todas as telas do cruzamento mais movimentado do "
            "local-alvo, liberando tambem uma nuvem de bolhas de sabao "
            "coloridas."
        ),
    ),
    dict(
        team="team08",
        empresa="Petrobras",
        empresa_coord="-22.9095,-43.1815",
        alvo="Refinaria REDUC, Duque de Caxias",
        alvo_coord="-22.7199,-43.2727",
        codinome="Operação Repolho Industrial",
        ataque=(
            "Alterar remotamente o fluxo de um dos dutos industriais do "
            "local-alvo para que, em vez de vapor, seja liberada uma "
            "nuvem de bolhas de sabao com forte cheiro de repolho."
        ),
    ),
    dict(
        team="team09",
        empresa="Coca-Cola",
        empresa_coord="33.7695,-84.3964",
        alvo="SoFi Stadium, Los Angeles",
        alvo_coord="33.9535,-118.3392",
        codinome="Operação Sabor Surpresa",
        ataque=(
            "Reprogramar todas as maquinas automaticas de bebida do "
            "local-alvo para servir, durante dez minutos, apenas uma "
            "edicao limitada e nada convencional: refrigerante sabor "
            "repolho."
        ),
    ),
    dict(
        team="team10",
        empresa="Toyota",
        empresa_coord="35.0833,137.1561",
        alvo="Terminal do Eurotúnel, Folkestone",
        alvo_coord="51.0946,1.1616",
        codinome="Operação Maré de Patinhos",
        ataque=(
            "Liberar cerca de 20 mil patinhos de borracha dentro do "
            "sistema de ventilacao do local-alvo, fazendo-os flutuar "
            "lentamente ao lado dos trilhos durante a operacao."
        ),
    ),
]

TEAMS_BY_KEY = {t["team"]: t for t in TEAMS}

# ---------------------------------------------------------------------------
# Conteudo "de disfarce" (decoys) -- iguais em todas as equipes, so servem
# para dar volume realista de arquivos de escritorio.
# ---------------------------------------------------------------------------

POLITICA_USO = """\
POLITICA DE USO ACEITAVEL - TI CORPORATIVO
Documento interno - revisao anual

1. O uso dos sistemas corporativos e destinado exclusivamente a
   atividades profissionais autorizadas.
2. E proibido compartilhar credenciais de acesso com terceiros.
3. Todo acesso remoto e registrado para fins de auditoria de seguranca.
4. Duvidas devem ser encaminhadas ao Service Desk de TI (ramal 4040).

Ultima atualizacao: revisao automatica do sistema de compliance.
"""

COMUNICADO_FERIAS = """\
COMUNICADO - RECURSOS HUMANOS
Assunto: Ferias coletivas

Prezados colaboradores,

Informamos que o periodo de ferias coletivas do setor administrativo
sera definido conforme calendario interno, a ser divulgado pelo RH em
ate 30 dias. Duvidas sobre saldo de ferias podem ser tratadas
diretamente no portal do colaborador.

Atenciosamente,
Recursos Humanos
"""

PONTO_ELETRONICO = """\
data;colaborador;entrada;saida;observacao
2026-07-01;COL-0231;08:02;17:58;
2026-07-02;COL-0231;08:11;18:04;
2026-07-03;COL-0231;07:59;12:00;meio periodo
2026-07-04;COL-0231;08:05;18:01;
2026-07-06;COL-0231;08:00;17:55;
"""

FECHAMENTO_MENSAL = """\
centro_custo;previsto;realizado;variacao_pct
CC-1002;184500.00;179320.50;-2.8
CC-1010;92300.00;95810.00;3.8
CC-1044;41200.00;40990.00;-0.5
CC-1078;15800.00;16110.00;2.0
"""

CHAMADOS_ABERTOS = """\
[HELPDESK] Fila de chamados abertos - TI

#4471 - Impressora do 3o andar sem toner - Prioridade: baixa
#4472 - Solicitacao de acesso a VPN - Prioridade: media
#4473 - Notebook nao liga (bateria) - Prioridade: media
#4474 - Atualizacao de antivirus pendente em 12 estacoes - Prioridade: alta
"""

STATUS_REDE = """\
[MONITORAMENTO DE REDE]
Uptime do link primario: 99.97%
Uptime do link secundario (failover): 99.81%
Pacotes perdidos (ultimas 24h): 0.02%
Nenhum incidente critico registrado.
"""

ROADMAP = """\
ROADMAP INTERNO - INICIATIVAS 2027 (rascunho)

- Revisao da politica de home office
- Consolidacao de fornecedores de nuvem
- Programa de mentoria entre equipes
- Atualizacao do parque de notebooks

Documento sujeito a alteracoes ate aprovacao final da diretoria.
"""


def datacenter_log() -> str:
    # O conteudo NAO repete as coordenadas -- a pista esta no nome do
    # arquivo, nao no texto.
    return textwrap.dedent("""\
        [LOG DE INFRAESTRUTURA - DATACENTER PRIMARIO]
        Ultima sincronizacao: 03:12:07
        Status dos nos: 128/128 ONLINE
        Latencia media (no local -> matriz): 4ms
        Backup incremental concluido as 02:00.
        Verificacao de integridade: OK.
        Nenhuma acao necessaria.

        (arquivo de log gerado automaticamente pelo agente de monitoramento
        de geolocalizacao de instalacoes)
        """)


def waypoint_kml(coord: str) -> str:
    lat, lon = coord.split(",")
    return textwrap.dedent(f"""\
        <!-- Waypoint marcado pela equipe de reconhecimento de campo -->
        <!-- Ponto de interesse: prioridade ALTA -->
        <!-- Confirmar coordenadas antes de prosseguir com a operacao -->
        <Placemark>
          <name>Ponto de execucao</name>
          <status>alvo confirmado</status>
          <coordinates>{lon},{lat},0</coordinates>
        </Placemark>
        """)


def memo_operacional(codinome: str, ataque: str) -> str:
    return textwrap.dedent(f"""\
        MEMORANDO INTERNO - CONFIDENCIAL
        De: Comite de Operacoes Especiais
        Para: Equipe de Campo
        Assunto: {codinome}

        Prezada equipe,

        A operacao segue confirmada. Resumo do plano de acao:

        {ataque}

        O ponto exato de execucao foi demarcado pela equipe de
        reconhecimento e consta no arquivo de coordenadas anexo a esta
        mesma pasta. Confira antes de prosseguir.

        Este documento e confidencial. Nao compartilhe fora do canal
        seguro.

        -- Comite de Operacoes Especiais
        """)


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_team_files(team: dict, root: str) -> None:
    """Gera a arvore de arquivos da missao de UMA equipe dentro de `root`.

    `root` deve ser o diretorio que faz o papel de workspace da equipe
    (dentro do container: /home/teamNN/workspace ; no host, para uso
    opcional do professor: ./data/teamNN).
    """
    # Arquivo de disfarce na raiz do workspace
    _write(os.path.join(root, "politica_uso_aceitavel.txt"), POLITICA_USO)

    # documentos/rh
    _write(os.path.join(root, "documentos", "rh", "comunicado_ferias_coletivas.txt"), COMUNICADO_FERIAS)
    _write(os.path.join(root, "documentos", "rh", "ponto_eletronico_julho.csv"), PONTO_ELETRONICO)

    # documentos/financeiro
    _write(os.path.join(root, "documentos", "financeiro", "fechamento_mensal.csv"), FECHAMENTO_MENSAL)

    # documentos/ti/manutencao (decoy)
    _write(os.path.join(root, "documentos", "ti", "manutencao", "chamados_abertos.log"), CHAMADOS_ABERTOS)

    # documentos/ti/infraestrutura (decoy + pista da EMPRESA)
    _write(os.path.join(root, "documentos", "ti", "infraestrutura", "status_rede.log"), STATUS_REDE)
    _write(
        os.path.join(root, "documentos", "ti", "infraestrutura", f"geo_{team['empresa_coord']}.log"),
        datacenter_log(),
    )

    # documentos/projetos (decoy)
    _write(os.path.join(root, "documentos", "projetos", "roadmap_2027.txt"), ROADMAP)

    # documentos/projetos/confidencial (pista do ATAQUE + do ALVO, alvo do "sabotagem")
    _write(
        os.path.join(root, "documentos", "projetos", "confidencial", "memo_operacional.txt"),
        memo_operacional(team["codinome"], team["ataque"]),
    )
    _write(
        os.path.join(root, "documentos", "projetos", "confidencial", f"geo_{team['alvo_coord']}.kml"),
        waypoint_kml(team["alvo_coord"]),
    )
