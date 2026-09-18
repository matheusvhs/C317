# CLAUDE.md — contexto do projeto para agentes

Plataforma Web do **Observatório do Turismo de Santa Rita do Sapucaí**, disciplina **C317
(Projeto Orientado)** do Inatel, em parceria com a **SMCELT** da Prefeitura — Edital HEIComp
2026.2. Equipe de 4–5 alunos, 8 milestones quinzenais seguindo o SDLC.

## O princípio que decide as dúvidas de arquitetura

> **O plano analítico é o cérebro, nunca o runtime do site.**

O pipeline processa, versiona e publica; a aplicação lê de um espelho barato e rápido. Se o
pipeline cair, o site continua no ar servindo a última versão publicada. Qualquer proposta que
coloque o motor analítico no caminho de uma requisição do usuário está errada — não importa o
quanto simplifique o código.

## Stack

| Camada | Escolha | Observação |
|---|---|---|
| Front-end | Next.js (PWA) — decisão adiada | Contrato da API já congelado, então pode ser decidido depois |
| API | FastAPI + Pydantic + SQLAlchemy | `apps/api/` · OpenAPI é o contrato entre as duplas de front e back |
| Banco | PostgreSQL | schema `app` (OLTP) + schema `serving` (espelho de leitura) |
| Pipeline | dbt + DuckDB, tabelas Delta | roda no GitHub Actions (cron + `workflow_dispatch`), nunca em servidor próprio |
| Storage | Supabase Storage / Cloudflare R2 | PDFs, landing de uploads, tabelas Delta |

Toda a stack é Apache/MIT: a Prefeitura precisa poder operar, auditar e evoluir a plataforma sem
custo recorrente nem impedimento de licença. **Databricks foi avaliado e descartado** — a licença
não-comercial não sustenta uma plataforma que a SMCELT opera continuamente (o porquê completo está
no ADR-001, em `docs/arquitetura.md` §1; não reabrir essa decisão sem ler).

## Estrutura do repositório

```
apps/web/          front-end (a definir; contrato já congelado)
apps/api/          FastAPI — routers/ services/ models/ migrations/
data/              projeto dbt-duckdb: models/bronze|silver|gold, tests/, macros/
data/publish/      publisher: materialização gold → Postgres serving
docs/              arquitetura.md · casos-de-uso.md · modelo-dados.md · agentes.md
docs/diagramas/    .drawio + exportações .drawio.png + gerar_diagramas.py
docs/milestones/   enunciados e entregas dos milestones
.github/workflows/ ci.yml · pipeline.yml
```

## Documentos que valem ler antes de propor mudança

| Documento | Quando consultar |
|---|---|
| `docs/arquitetura.md` | Sempre que a mudança tocar motor analítico, serving, contrato da API ou governança |
| `docs/casos-de-uso.md` | Antes de alterar escopo de funcionalidade — o escopo é deliberadamente pequeno |
| `docs/modelo-dados.md` | Antes de mexer em tabela, coluna ou migração |
| `docs/agentes.md` | Como o time usa Claude Code neste repositório |

## Convenções

- **Idioma**: documentação, commits e comentários em **PT-BR**; identificadores de código,
  tabelas e colunas em **inglês/snake_case** (`upload`, `execucao_pipeline` seguem o domínio em
  PT-BR já fixado no modelo de dados — mantenha o que existe, não renomeie).
- **Commits**: mensagem no imperativo com prefixo (`docs:`, `feat:`, `fix:`, `chore:`) e um corpo
  que explica o *porquê*, não o *o quê* — o diff já mostra o quê.
- **Branches**: `docs/...`, `feat/...`, `fix/...`. Nunca commitar direto na `main`.
- **Schemas nunca se misturam**: `serving.*` é sempre reconstruível a partir do pipeline; `app.*`
  é a fonte da verdade transacional. Não criar FK entre os dois.
- **Estrutura congelada após o M3**: o professor proíbe mudança brusca de estrutura depois da
  especificação entregue. Indicador novo é uma linha em `serving.indicador` + o cálculo no gold —
  **sem tocar em back-end nem front-end**. Se uma proposta exige alterar API e front, provavelmente
  há um caminho pela camada de publicação.
- **LGPD**: nenhum dado pessoal entra no plano analítico. Dados de FNRH/hóspedes não são ingeridos.

## Comandos

```bash
bash docs/setup-check.sh                      # confere o ambiente de quem for desenvolver
cd apps/api && .venv/bin/uvicorn main:app --reload   # API local em http://127.0.0.1:8000/docs
python3 docs/diagramas/gerar_diagramas.py     # regenera o .drawio de casos de uso + ER
```

## Ao trabalhar neste repositório

- Diagramas seguem a identidade visual do projeto (gradiente `#0A4AAD → #6C5CE0 → #C750D6`,
  cartões brancos com barra de acento, Helvetica). Há uma skill de projeto em
  `.claude/skills/diagramas-c317/` com as regras e o fluxo de exportação.
- Exportar diagrama sempre como `.drawio.png` com XML embutido (`-e`): o PNG continua editável e
  vira anexo direto do relatório de milestone.
- Não commitar `.venv/`, `node_modules/`, `.DS_Store` nem `.claude/settings.local.json` — todos já
  estão no `.gitignore`.
