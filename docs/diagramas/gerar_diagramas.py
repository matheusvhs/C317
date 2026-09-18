#!/usr/bin/env python3
"""Gera o .drawio de casos de uso (item 2) e modelo de dados (item 3) do Milestone III.

Executar a partir da raiz do repositorio:

    python3 docs/diagramas/gerar_diagramas.py

Depois, exportar as paginas em PNG com o XML embutido (precisa do draw.io desktop):

    drawio -x -f png -e -s 2 -b 10 --page-index 1 \
      -o docs/diagramas/04_casos_de_uso.drawio.png \
      docs/diagramas/Casos_de_Uso_e_Modelo_de_Dados.drawio
    drawio -x -f png -e -s 2 -b 10 --page-index 2 \
      -o docs/diagramas/05_modelo_dados_er.drawio.png \
      docs/diagramas/Casos_de_Uso_e_Modelo_de_Dados.drawio

Edicoes pontuais podem ser feitas direto no .drawio (draw.io desktop ou
diagrams.net); mudancas estruturais valem mais a pena aqui, porque a
identidade visual do projeto fica centralizada nas constantes do topo.
"""
from html import escape

OUT = "docs/diagramas/Casos_de_Uso_e_Modelo_de_Dados.drawio"

AZUL, ROXO, MAGENTA = "#0A4AAD", "#6C5CE0", "#C750D6"
TXT, TXT2, BORDA = "#1F2733", "#5A6470", "#D8DCE4"
FONTE = "fontFamily=Helvetica;"

cells = []


def esc(s):
    return escape(s, quote=True)


def cell(cid, value, style, x, y, w, h, parent="1"):
    cells.append(
        f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )


def edge(cid, value, style, src, tgt, points=None, off=None):
    geo = '<mxGeometry relative="1" as="geometry">'
    if off:
        geo = f'<mxGeometry x="{off[0]}" relative="1" as="geometry"><mxPoint x="{off[1]}" y="{off[2]}" as="offset"/>'
    if points:
        geo += '<Array as="points">' + "".join(
            f'<mxPoint x="{px}" y="{py}"/>' for px, py in points
        ) + "</Array>"
    geo += "</mxGeometry>"
    cells.append(
        f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" edge="1" parent="1" '
        f'source="{src}" target="{tgt}">{geo}</mxCell>'
    )


def texto(cid, value, x, y, w, h, size=11, color=TXT, align="left", bold=False):
    v = f"<b>{value}</b>" if bold else value
    cell(
        cid, v,
        f"text;html=1;whiteSpace=wrap;align={align};verticalAlign=middle;fontSize={size};"
        f"fontColor={color};strokeColor=none;fillColor=none;{FONTE}labelPosition=center;"
        "verticalLabelPosition=middle;spacing=0;",
        x, y, w, h,
    )


def rotulo(cid, value, x, y, w=300, h=18):
    cell(
        cid, f'<span style="letter-spacing:1.2px;font-weight:600">{value}</span>',
        f"text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=10;fontColor={TXT2};"
        f"strokeColor=none;fillColor=none;{FONTE}labelPosition=center;verticalLabelPosition=middle;spacing=0;",
        x, y, w, h,
    )


def cabecalho(p, largura, titulo, subtitulo):
    meio = 40 + (largura - 80) // 2
    cell(f"{p}_hdr1", "", f"rounded=1;arcSize=6;fillColor={AZUL};gradientColor={ROXO};gradientDirection=east;strokeColor=none;", 40, 30, meio - 40 - 10, 92)
    cell(f"{p}_hdr2", "", f"fillColor={ROXO};strokeColor=none;", meio - 22, 30, 44, 92)
    cell(f"{p}_hdr3", "", f"rounded=1;arcSize=6;fillColor={ROXO};gradientColor={MAGENTA};gradientDirection=east;strokeColor=none;", meio + 10, 30, largura - 40 - (meio + 10), 92)
    cell(
        f"{p}_hdr4",
        '<div style="line-height:1.55;"><b style="font-size:21px">Observat&#243;rio do Turismo de Santa Rita do Sapuca&#237;</b>'
        f'<br/><span style="font-size:12.5px;opacity:0.92">{subtitulo}</span></div>',
        f"text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=21;fontColor=#FFFFFF;"
        f"strokeColor=none;fillColor=none;{FONTE}labelPosition=center;verticalLabelPosition=middle;spacing=0;",
        66, 38, 900, 76,
    )
    cell(
        f"{p}_hdr5",
        '<div style="line-height:1.5;opacity:0.92">SMCELT &#183; Prefeitura Municipal<br/>de Santa Rita do Sapuca&#237;</div>',
        f"text;html=1;whiteSpace=wrap;align=right;verticalAlign=middle;fontSize=11;fontColor=#FFFFFF;"
        f"strokeColor=none;fillColor=none;{FONTE}labelPosition=center;verticalLabelPosition=middle;spacing=0;",
        largura - 340, 38, 280, 76,
    )
    _ = titulo


def rodape(p, largura, y, pagina):
    cell(f"{p}_ft0", "", f"strokeColor={BORDA};strokeWidth=1;", 40, y, largura - 80, 1)
    texto(f"{p}_ft1", "Observat&#243;rio do Turismo de Santa Rita do Sapuca&#237; &#183; SMCELT / Prefeitura Municipal", 40, y + 12, 700, 20, 10, "#8A939E")
    texto(f"{p}_ft2", f"C317 &#183; HEIComp 2026.2 &#183; Milestone III &#183; {pagina}", largura - 740, y + 12, 700, 20, 10, "#8A939E", align="right")


# ---------------------------------------------------------------- PAGINA 1
P1_W, P1_H = 1920, 1160
p = "uc"
cabecalho(p, P1_W, "", "Diagrama de Casos de Uso (UML) &#183; Milestone III &#8212; Relat&#243;rio de Desenho")

# fronteira do sistema
cell("uc_sys", "", "rounded=1;arcSize=4;html=1;fillColor=#FFFFFF;strokeColor=#C3CAD6;strokeWidth=2;", 300, 180, 1320, 620)
texto("uc_sys_t", "Plataforma Web do Observat&#243;rio do Turismo", 322, 194, 700, 24, 14, TXT, bold=True)
texto("uc_sys_s", "escopo do prot&#243;tipo da C317 &#8212; 7 casos de uso de ator + 2 inclu&#237;dos", 322, 216, 700, 18, 10.5, TXT2)

# caixas de agrupamento
cell("uc_boxA", "", "rounded=1;arcSize=6;html=1;fillColor=#F5F9FE;strokeColor=#BBD3F0;strokeWidth=1;", 330, 250, 500, 250)
rotulo("uc_boxA_t", "PORTAL P&#218;BLICO &#183; ACESSO AN&#212;NIMO", 346, 262, 460)

cell("uc_boxB", "", "rounded=1;arcSize=6;html=1;fillColor=#F8F6FE;strokeColor=#CFC6F4;strokeWidth=1;", 870, 250, 720, 520)
rotulo("uc_boxB_t", "PAINEL ADMINISTRATIVO &#183; REQUER AUTENTICA&#199;&#195;O (JWT)", 886, 262, 680)

cell("uc_boxC", "", f"rounded=1;arcSize=6;html=1;fillColor=#FDF4FB;strokeColor={MAGENTA};strokeWidth=1;dashed=1;dashPattern=8 4;", 330, 540, 500, 200)
rotulo("uc_boxC_t", "FORA DO ESCOPO DO PROT&#211;TIPO &#183; EVOLU&#199;&#195;O FUTURA", 350, 556, 460)
texto("uc_boxC_c", '<div style="line-height:1.9">&#183; Coleta aut&#244;noma pelos estabelecimentos (formul&#225;rio com token)<br/>'
                  '&#183; Valida&#231;&#227;o das submiss&#245;es pela SMCELT<br/>'
                  '&#183; Exporta&#231;&#227;o dos dados do gr&#225;fico em CSV/JSON<br/>'
                  '&#183; Painel Cadastur/FNRH e Invent&#225;rio Tur&#237;stico</div>', 350, 582, 470, 140, 10.5, TXT2)

UC_PUB = f"ellipse;whiteSpace=wrap;html=1;fillColor=#E8F1FD;strokeColor={AZUL};strokeWidth=1.5;fontSize=11.5;fontColor=#10305E;{FONTE}"
UC_ADM = f"ellipse;whiteSpace=wrap;html=1;fillColor=#EFEAFB;strokeColor={ROXO};strokeWidth=1.5;fontSize=11.5;fontColor=#332178;{FONTE}"
UC_INC = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={ROXO};strokeWidth=1.5;dashed=1;dashPattern=6 4;fontSize=11;fontColor=#332178;{FONTE}"

publicos = [
    ("uc01", "UC01 &#183; Consultar painel de indicadores<br/><span style=\"font-size:10px\">com filtros por per&#237;odo e setor</span>"),
    ("uc02", "UC02 &#183; Consultar e baixar relat&#243;rios do Observat&#243;rio"),
]
for i, (cid, label) in enumerate(publicos):
    cell(cid, label, UC_PUB, 355, 300 + i * 88, 450, 64)

admins = [
    ("uc03", "UC03 &#183; Autenticar no painel"),
    ("uc04", "UC04 &#183; Enviar planilha de dados"),
    ("uc05", "UC05 &#183; Publicar relat&#243;rio em PDF"),
    ("uc06", "UC06 &#183; Publicar dados"),
    ("uc07", "UC07 &#183; Acompanhar execu&#231;&#245;es do pipeline"),
]
for i, (cid, label) in enumerate(admins):
    cell(cid, label, UC_ADM, 1250, 300 + i * 88, 310, 64)

cell("uc08", "UC08 &#183; Validar schema e regras de neg&#243;cio", UC_INC, 900, 388, 260, 64)
cell("uc09", "UC09 &#183; Registrar trilha de auditoria", UC_INC, 900, 520, 260, 64)

# atores
ATOR = f"shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;strokeWidth=2;fontSize=11.5;{FONTE}"
cell("uc_a1", '<b>Visitante do portal</b><br/><span style="font-size:10px;color:#5A6470">cidad&#227;o &#183; turista<br/>empreendedor &#183; pesquisador</span>',
     ATOR + f"strokeColor={AZUL};fontColor={TXT};", 150, 340, 46, 70)
cell("uc_a2", '<b>Gestor SMCELT</b><br/><span style="font-size:10px;color:#5A6470">equipe da Secretaria<br/>(usu&#225;rio autenticado)</span>',
     ATOR + f"strokeColor={ROXO};fontColor={TXT};", 1700, 400, 46, 70)
cell("uc_a3", '<div style="line-height:1.5"><span style="font-size:10px;color:#5A6470">&#171;sistema&#187;</span><br/><b>Pipeline anal&#237;tico</b><br/>'
              '<span style="font-size:10px;color:#5A6470">GitHub Actions + dbt<br/>publisher &#8594; serving</span></div>',
     f"rounded=1;arcSize=10;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={BORDA};strokeWidth=1;shadow=1;fontSize=12;fontColor={TXT};{FONTE}",
     1250, 830, 320, 90)

ASSOC = f"edgeStyle=none;html=1;endArrow=none;strokeColor={TXT2};strokeWidth=1.5;fontSize=10;fontColor={TXT};{FONTE}labelBackgroundColor=#FFFFFF;"
INC = (f"edgeStyle=none;html=1;endArrow=open;endSize=8;dashed=1;dashPattern=6 4;strokeColor={ROXO};strokeWidth=1.5;"
       f"fontSize=10;fontColor={ROXO};{FONTE}labelBackgroundColor=#FFFFFF;")
ORTO = ASSOC.replace("edgeStyle=none", "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto")

n = 0
for cid, _ in publicos:
    n += 1
    edge(f"uc_e{n}", "", ASSOC + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", "uc_a1", cid)
for cid, _ in admins:
    n += 1
    edge(f"uc_e{n}", "", ASSOC + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;", "uc_a2", cid)
n += 1
edge(f"uc_e{n}", "dispara o pipeline (workflow_dispatch)",
     ORTO + "exitX=0;exitY=0.8;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
     "uc06", "uc_a3", points=[(1210, 615), (1210, 875)], off=(0.55, 0, 0))
n += 1
edge(f"uc_e{n}", "status dos runs",
     ORTO + "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;", "uc_a3", "uc07")

edge("uc_i1", "&#171;include&#187;", INC + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;", "uc04", "uc08")
edge("uc_i2", "&#171;include&#187;", INC + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.3;entryDx=0;entryDy=0;", "uc05", "uc09", off=(-0.2, 0, -6))
edge("uc_i3", "&#171;include&#187;", INC + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.8;entryDx=0;entryDy=0;", "uc06", "uc09", off=(-0.2, 0, 6))

# legenda
LEG_Y = 960
rotulo("uc_leg", "LEGENDA", 300, LEG_Y, 200)
cell("uc_leg1", "", f"strokeColor={TXT2};strokeWidth=2;", 300, LEG_Y + 34, 34, 1)
texto("uc_leg1t", "associa&#231;&#227;o ator &#8212; caso de uso", 344, LEG_Y + 25, 230, 20, 10.5)
cell("uc_leg2", "", f"strokeColor={ROXO};strokeWidth=2;dashed=1;dashPattern=6 4;", 600, LEG_Y + 34, 34, 1)
texto("uc_leg2t", "&#171;include&#187; (comportamento obrigat&#243;rio)", 644, LEG_Y + 25, 260, 20, 10.5)
cell("uc_leg3", "", f"ellipse;fillColor=#E8F1FD;strokeColor={AZUL};strokeWidth=1.5;", 930, LEG_Y + 26, 34, 16)
texto("uc_leg3t", "caso de uso p&#250;blico", 974, LEG_Y + 25, 150, 20, 10.5)
cell("uc_leg4", "", f"ellipse;fillColor=#EFEAFB;strokeColor={ROXO};strokeWidth=1.5;", 1140, LEG_Y + 26, 34, 16)
texto("uc_leg4t", "caso de uso administrativo", 1184, LEG_Y + 25, 180, 20, 10.5)
cell("uc_leg5", "", f"strokeColor={MAGENTA};strokeWidth=2;dashed=1;dashPattern=8 4;", 1380, LEG_Y + 34, 34, 1)
texto("uc_leg5t", "fora do escopo do prot&#243;tipo", 1424, LEG_Y + 25, 200, 20, 10.5)

texto("uc_nota", '<div style="line-height:1.6"><b>Escopo do prot&#243;tipo da C317:</b> nove casos de uso, todos implementados nos milestones 4&#8211;6 &#8212; '
                 'escopo pequeno por decis&#227;o, para caber no semestre com folga. Todo caso de uso do painel exige UC03 (sess&#227;o JWT v&#225;lida); '
                 'a consulta p&#250;blica &#233; an&#244;nima. O que ficou de fora est&#225; registrado como evolu&#231;&#227;o futura, sem compromisso de entrega no semestre.</div>',
      300, LEG_Y + 58, 1320, 40, 11, TXT2)

rodape(p, P1_W, 1080, "p&#225;gina 1 de 2 &#183; item 2 do relat&#243;rio")

pag1 = "".join(cells)
cells = []

# ---------------------------------------------------------------- PAGINA 2
P2_W, P2_H = 2000, 1470
p = "er"
cabecalho(p, P2_W, "", "Estrutura do Banco de Dados (ER) &#183; Milestone III &#8212; Relat&#243;rio de Desenho")


def tabela(cid, x, y, w, nome, sub, cor, linhas, fase2=False):
    h = 54 + 22 * len(linhas)
    tracejado = "dashed=1;dashPattern=8 4;" if fase2 else ""
    cell(
        cid,
        f'<div style="line-height:1.35"><b>{nome}</b><br/><span style="font-size:9.5px;opacity:0.85">{sub}</span></div>',
        f"swimlane;html=1;whiteSpace=wrap;startSize=34;rounded=1;arcSize=6;fillColor={cor};swimlaneFillColor=#FFFFFF;"
        f"strokeColor={cor};strokeWidth=1.5;{tracejado}fontColor=#FFFFFF;fontSize=12.5;{FONTE}align=center;"
        "verticalAlign=middle;shadow=1;collapsible=0;",
        x, y, w, h,
    )
    corpo = '<div style="line-height:2.0">' + "<br/>".join(linhas) + "</div>"
    cell(
        cid + "_c", corpo,
        f"text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;fontColor={TXT};"
        f"strokeColor=none;fillColor=none;{FONTE}spacingLeft=0;",
        12, 40, w - 24, h - 48, parent=cid,
    )
    return h


def col(nome, tipo, marca=""):
    badge = ""
    if marca:
        cores = {"PK": AZUL, "FK": "#C6A700", "UQ": "#2E9E6B"}
        cor = cores.get(marca.split()[0], TXT2)
        badge = f' <span style="font-size:9px;font-weight:700;color:{cor}">{marca}</span>'
    peso = "font-weight:600" if "PK" in marca else ""
    return f'<span style="{peso}">{nome}</span> <span style="color:#8A939E;font-size:10px">{tipo}</span>{badge}'


# faixa app
cell("er_appbg", "", f"rounded=1;arcSize=3;html=1;fillColor=#F7F9FC;strokeColor=#DDE3EC;strokeWidth=1;", 40, 160, 1920, 740)
texto("er_appt", "schema <b>app</b> &#8212; OLTP transacional", 62, 176, 600, 22, 13.5, TXT)
texto("er_apps", "fonte da verdade da aplica&#231;&#227;o: usu&#225;rios, uploads, publica&#231;&#245;es e auditoria &#183; escrito pela API (FastAPI) &#183; nunca sobrescrito pelo pipeline",
      62, 198, 1200, 18, 10.5, TXT2)

tabela("er_relatorio", 90, 240, 320, "app.relatorio", "relat&#243;rios publicados pelo Observat&#243;rio", AZUL, [
    col("id", "bigserial", "PK"),
    col("numero", "int"),
    col("ano", "int"),
    col("titulo", "text"),
    col("resumo", "text"),
    col("tags", "text[]"),
    col("url_pdf", "text"),
    col("publicado_por", "bigint", "FK"),
    col("publicado_em", "timestamptz"),
])
tabela("er_usuario", 470, 240, 320, "app.usuario", "equipe da SMCELT (&#250;nico perfil com login)", AZUL, [
    col("id", "bigserial", "PK"),
    col("nome", "text"),
    col("email", "citext", "UQ"),
    col("senha_hash", "text"),
    col("papel", "text"),
    col("ativo", "boolean"),
    col("criado_em", "timestamptz"),
])
tabela("er_upload", 850, 240, 320, "app.upload", "planilha enviada pelo painel admin", AZUL, [
    col("id", "bigserial", "PK"),
    col("usuario_id", "bigint", "FK"),
    col("nome_arquivo", "text"),
    col("caminho_landing", "text"),
    col("hash_sha256", "text", "UQ"),
    col("tipo_dado", "text"),
    col("status", "text"),
    col("linhas_aceitas", "int"),
    col("linhas_rejeitadas", "int"),
    col("enviado_em", "timestamptz"),
])
tabela("er_exec", 1230, 240, 320, "app.execucao_pipeline", "run do GitHub Actions disparado pela API", AZUL, [
    col("id", "bigserial", "PK"),
    col("upload_id", "bigint", "FK"),
    col("run_id_gh", "text"),
    col("status", "text"),
    col("iniciado_em", "timestamptz"),
    col("finalizado_em", "timestamptz"),
    col("log_url", "text"),
    col("versao_publicada", "text"),
])
tabela("er_auditoria", 470, 620, 320, "app.auditoria", "trilha de quem publicou o qu&#234; e quando", AZUL, [
    col("id", "bigserial", "PK"),
    col("usuario_id", "bigint", "FK"),
    col("acao", "text"),
    col("entidade", "text"),
    col("entidade_id", "text"),
    col("detalhe", "jsonb"),
    col("ocorrido_em", "timestamptz"),
])
tabela("er_submissao", 850, 620, 320, "app.submissao", "coleta aut&#244;noma &#183; evolu&#231;&#227;o futura", MAGENTA, [
    col("id", "bigserial", "PK"),
    col("estabelecimento_id", "bigint", "FK"),
    col("periodo", "date"),
    col("payload", "jsonb"),
    col("status", "text"),
    col("recebido_em", "timestamptz"),
    col("validado_por", "bigint", "FK"),
], fase2=True)
tabela("er_estab", 1230, 620, 320, "app.estabelecimento", "hot&#233;is e pousadas &#183; evolu&#231;&#227;o futura", MAGENTA, [
    col("id", "bigserial", "PK"),
    col("cnpj", "text", "UQ"),
    col("nome_fantasia", "text"),
    col("setor", "text"),
    col("token_coleta", "text", "UQ"),
    col("ativo", "boolean"),
], fase2=True)

cell("er_nota1", "", f"rounded=1;arcSize=10;html=1;fillColor=#FFFFFF;strokeColor={BORDA};strokeWidth=1;shadow=1;", 1610, 620, 330, 194)
cell("er_nota1b", "", f"rounded=1;arcSize=40;fillColor={AZUL};strokeColor=none;", 1610, 620, 5, 194)
texto("er_nota1t", "Regras de estado", 1632, 636, 290, 20, 12.5, TXT, bold=True)
texto("er_nota1c", '<div style="line-height:1.7">&#183; <b>upload.status</b>: rascunho &#8594; em_revisao &#8594; publicado (ou rejeitado)<br/>'
                   '&#183; <b>execucao_pipeline.status</b>: enfileirado &#8594; executando &#8594; sucesso / falha<br/>'
                   '&#183; s&#243; run com <b>dbt tests</b> verdes materializa o schema <b>serving</b><br/>'
                   '&#183; nenhum dado pessoal de h&#243;spede &#233; armazenado (LGPD)</div>',
      1632, 660, 292, 140, 10.5, TXT2)

# faixa serving
cell("er_srvbg", "", f"rounded=1;arcSize=3;html=1;fillColor=#FAF8FE;strokeColor=#DFD8F6;strokeWidth=1;", 40, 930, 1920, 430)
texto("er_srvt", "schema <b>serving</b> &#8212; espelho de leitura do gold", 62, 946, 700, 22, 13.5, TXT)
texto("er_srvs", "reconstru&#237;do a cada publica&#231;&#227;o pelo publisher (dbt/DuckDB &#8594; PostgreSQL, em transa&#231;&#227;o) &#183; a API s&#243; l&#234; &#183; descart&#225;vel e sempre reproduz&#237;vel",
      62, 968, 1300, 18, 10.5, TXT2)

tabela("er_serie", 90, 1000, 320, "serving.serie", "formato longo: 1 linha por indicador/per&#237;odo/setor", ROXO, [
    col("indicador_id", "text", "PK FK"),
    col("periodo", "date", "PK"),
    col("setor", "text", "PK"),
    col("valor", "numeric"),
    col("fonte", "text"),
    col("atualizado_em", "timestamptz"),
])
tabela("er_indicador", 470, 1000, 320, "serving.indicador", "cat&#225;logo &#183; novo indicador = nova linha", ROXO, [
    col("indicador_id", "text", "PK"),
    col("nome", "text"),
    col("unidade", "text"),
    col("descricao", "text"),
    col("fonte", "text"),
    col("metodologia", "text"),
    col("periodicidade", "text"),
])
tabela("er_card", 850, 1000, 320, "serving.resumo_card", "cards do dashboard", ROXO, [
    col("indicador_id", "text", "PK FK"),
    col("valor_atual", "numeric"),
    col("variacao_pct", "numeric"),
    col("periodo_ref", "date"),
])
tabela("er_relpub", 1230, 1000, 320, "serving.relatorio", "espelho p&#250;blico de app.relatorio", ROXO, [
    col("id", "bigint", "PK"),
    col("numero", "int"),
    col("ano", "int"),
    col("titulo", "text"),
    col("resumo", "text"),
    col("tags", "text[]"),
    col("url_pdf", "text"),
])
tabela("er_versao", 1610, 1000, 320, "serving.versao", "carimbo da &#250;ltima publica&#231;&#227;o", ROXO, [
    col("versao", "text", "PK"),
    col("gerado_em", "timestamptz"),
    col("linhas", "bigint"),
    col("checksum", "text"),
])

REL = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={TXT2};strokeWidth=1.5;"
       f"startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;fontSize=10;fontColor={TXT};{FONTE}labelBackgroundColor=#FFFFFF;")
REL_OPC = REL.replace(f"strokeColor={TXT2}", "strokeColor=#9AA3AF") + "dashed=1;dashPattern=6 4;startArrow=ERzeroToOne;"
LIG = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={MAGENTA};strokeWidth=1.5;"
       f"dashed=1;dashPattern=6 4;endArrow=blockThin;endFill=1;endSize=6;fontSize=10;fontColor={TXT};{FONTE}labelBackgroundColor=#FFFFFF;")

edge("er_r1", "envia", REL + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.4;entryDx=0;entryDy=0;", "er_usuario", "er_upload")
edge("er_r2", "publica", REL + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.45;entryDx=0;entryDy=0;", "er_usuario", "er_relatorio")
edge("er_r3", "registra", REL + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;", "er_usuario", "er_auditoria")
edge("er_r4", "gera", REL + "exitX=1;exitY=0.4;exitDx=0;exitDy=0;entryX=0;entryY=0.35;entryDx=0;entryDy=0;", "er_upload", "er_exec")
edge("er_r5", "envia", REL + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;", "er_estab", "er_submissao")
edge("er_r6", "valida (opcional)", REL_OPC + "exitX=0.85;exitY=1;exitDx=0;exitDy=0;entryX=0.35;entryY=0;entryDx=0;entryDy=0;",
     "er_usuario", "er_submissao", points=[(742, 580), (962, 580)])
edge("er_r7", "descreve", REL + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;", "er_indicador", "er_serie")
edge("er_r8", "resume", REL + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", "er_indicador", "er_card")
edge("er_l1", "espelhado pelo publisher", LIG + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
     "er_relatorio", "er_relpub", points=[(250, 915), (1390, 915)])
edge("er_l2", "versao_publicada &#8594; serving.versao", LIG + "exitX=1;exitY=0.45;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;",
     "er_exec", "er_versao", points=[(1580, 347), (1580, 915), (1770, 915)], off=(0.85, 0, -12))

# legenda pagina 2
L2 = 1235
rotulo("er_leg", "LEGENDA", 90, L2, 200)
cell("er_leg1", "", f"strokeColor={TXT2};strokeWidth=2;", 90, L2 + 34, 34, 1)
texto("er_leg1t", "rela&#231;&#227;o 1:N obrigat&#243;ria (p&#233;-de-galinha)", 134, L2 + 25, 260, 20, 10.5)
cell("er_leg2", "", "strokeColor=#9AA3AF;strokeWidth=2;dashed=1;dashPattern=6 4;", 420, L2 + 34, 34, 1)
texto("er_leg2t", "rela&#231;&#227;o opcional (0:N)", 464, L2 + 25, 200, 20, 10.5)
cell("er_leg3", "", f"strokeColor={MAGENTA};strokeWidth=2;dashed=1;dashPattern=6 4;", 690, L2 + 34, 34, 1)
texto("er_leg3t", "materializa&#231;&#227;o feita pelo publisher (n&#227;o &#233; FK)", 734, L2 + 25, 280, 20, 10.5)
texto("er_leg4t", '<span style="font-weight:700;color:#0A4AAD">PK</span> chave prim&#225;ria &#160;&#160; '
                  '<span style="font-weight:700;color:#C6A700">FK</span> chave estrangeira &#160;&#160; '
                  '<span style="font-weight:700;color:#2E9E6B">UQ</span> &#237;ndice &#250;nico &#160;&#160; '
                  '<span style="color:#C750D6;font-weight:700">tabela tracejada</span> = fora do escopo do prot&#243;tipo', 1040, L2 + 25, 900, 20, 10.5)
texto("er_nota2", '<div style="line-height:1.6"><b>Por que dois schemas:</b> <b>app</b> guarda o estado transacional e nunca &#233; recalculado; '
                  '<b>serving</b> pode ser apagado e reconstru&#237;do a qualquer momento a partir do pipeline. '
                  'A API l&#234; <b>serving</b> nas rotas p&#250;blicas e escreve em <b>app</b> nas rotas administrativas &#8212; se o pipeline falhar, o site continua servindo a &#250;ltima vers&#227;o publicada.</div>',
      90, L2 + 58, 1850, 40, 11, TXT2)

rodape(p, P2_W, 1400, "p&#225;gina 2 de 2 &#183; item 3 do relat&#243;rio")

pag2 = "".join(cells)


def pagina(pid, nome, w, h, corpo):
    return (
        f'<diagram id="{pid}" name="{nome}"><mxGraphModel dx="1422" dy="798" grid="0" gridSize="10" guides="1" '
        f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" '
        f'background="#FFFFFF" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        f"{corpo}</root></mxGraphModel></diagram>"
    )


xml = (
    '<mxfile host="app.diagrams.net" agent="C317" type="device">'
    + pagina("pagUC", "1 &#183; Casos de uso (UML)", P1_W, P1_H, pag1)
    + pagina("pagER", "2 &#183; Modelo de dados (ER)", P2_W, P2_H, pag2)
    + "</mxfile>"
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(xml)
print("ok:", OUT, len(xml), "bytes")
