# Modelo de dados — item 3 do Milestone III

Diagrama ER: [`docs/diagramas/05_modelo_dados_er.drawio.png`](diagramas/05_modelo_dados_er.drawio.png)
(página 2 de `Casos_de_Uso_e_Modelo_de_Dados.drawio`).

Banco único **PostgreSQL**, com dois schemas de papéis opostos:

| Schema | Papel | Quem escreve | Quem lê | Pode ser apagado? |
|---|---|---|---|---|
| `app` | OLTP — estado transacional da aplicação | API (FastAPI), rotas administrativas | API | **não** — é a fonte da verdade |
| `serving` | espelho de leitura do gold | publisher (dbt/DuckDB → Postgres, em transação) | API, rotas públicas | **sim** — reconstruído a cada publicação |

Essa separação é a razão de a plataforma continuar no ar quando o pipeline falha: `serving` guarda
sempre a última versão publicada e a consulta pública nunca depende do processamento.

## Schema `app` (OLTP)

| Tabela | Conteúdo | Escopo |
|---|---|---|
| `usuario` | equipe da SMCELT — único perfil com login | essencial |
| `upload` | planilha enviada pelo painel, com hash e contagem de linhas | essencial |
| `execucao_pipeline` | run do GitHub Actions disparado pela API | essencial |
| `relatorio` | relatórios em PDF publicados pelo Observatório | essencial |
| `auditoria` | trilha de quem publicou o quê e quando | essencial |
| `estabelecimento` | hotéis e pousadas com token de coleta | fase 2 |
| `submissao` | dados informados pelo estabelecimento, aguardando validação | fase 2 |

## Schema `serving` (espelho do gold)

| Tabela | Conteúdo |
|---|---|
| `indicador` | catálogo: nome, unidade, fonte, metodologia, periodicidade |
| `serie` | **formato longo** — uma linha por indicador/período/setor |
| `resumo_card` | valores dos cards do dashboard (valor atual e variação) |
| `relatorio` | espelho público de `app.relatorio` |
| `versao` | carimbo da última publicação (versão, data, linhas, checksum) |

`serving.serie` em formato longo é a decisão que mantém API e front-end genéricos: indicador novo =
uma linha em `serving.indicador` + o cálculo no gold, sem tocar em código.

## DDL (esboço)

```sql
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS serving;

-- ---------------------------------------------------------------- app (OLTP)
CREATE TABLE app.usuario (
    id          bigserial PRIMARY KEY,
    nome        text        NOT NULL,
    email       text        NOT NULL UNIQUE,
    senha_hash  text        NOT NULL,                -- Argon2
    papel       text        NOT NULL DEFAULT 'editor'
                CHECK (papel IN ('admin', 'editor')),
    ativo       boolean     NOT NULL DEFAULT true,
    criado_em   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE app.upload (
    id                bigserial PRIMARY KEY,
    usuario_id        bigint      NOT NULL REFERENCES app.usuario (id),
    nome_arquivo      text        NOT NULL,
    caminho_landing   text        NOT NULL,
    hash_sha256       text        NOT NULL UNIQUE,   -- evita reenvio do mesmo arquivo
    tipo_dado         text        NOT NULL
                      CHECK (tipo_dado IN ('hospedagem', 'emprego', 'empresas', 'fluxo')),
    status            text        NOT NULL DEFAULT 'rascunho'
                      CHECK (status IN ('rascunho', 'em_revisao', 'publicado', 'rejeitado')),
    linhas_aceitas    integer     NOT NULL DEFAULT 0,
    linhas_rejeitadas integer     NOT NULL DEFAULT 0,
    enviado_em        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE app.execucao_pipeline (
    id               bigserial PRIMARY KEY,
    upload_id        bigint      REFERENCES app.upload (id),
    run_id_gh        text,                            -- id do run no GitHub Actions
    status           text        NOT NULL DEFAULT 'enfileirado'
                     CHECK (status IN ('enfileirado', 'executando', 'sucesso', 'falha')),
    iniciado_em      timestamptz NOT NULL DEFAULT now(),
    finalizado_em    timestamptz,
    log_url          text,
    versao_publicada text                             -- casa com serving.versao.versao
);

CREATE TABLE app.relatorio (
    id            bigserial PRIMARY KEY,
    numero        integer     NOT NULL,
    ano           integer     NOT NULL,
    titulo        text        NOT NULL,
    resumo        text,
    tags          text[]      NOT NULL DEFAULT '{}',
    url_pdf       text        NOT NULL,
    publicado_por bigint      REFERENCES app.usuario (id),
    publicado_em  timestamptz NOT NULL DEFAULT now(),
    UNIQUE (ano, numero)
);

CREATE TABLE app.auditoria (
    id          bigserial PRIMARY KEY,
    usuario_id  bigint      REFERENCES app.usuario (id),
    acao        text        NOT NULL,                -- publicou, rejeitou, editou...
    entidade    text        NOT NULL,                -- upload, relatorio, submissao
    entidade_id text        NOT NULL,
    detalhe     jsonb       NOT NULL DEFAULT '{}',
    ocorrido_em timestamptz NOT NULL DEFAULT now()
);

-- fase 2 -------------------------------------------------------------------
CREATE TABLE app.estabelecimento (
    id            bigserial PRIMARY KEY,
    cnpj          text    NOT NULL UNIQUE,
    nome_fantasia text    NOT NULL,
    setor         text    NOT NULL,
    token_coleta  text    NOT NULL UNIQUE,           -- acesso ao formulário sem login
    ativo         boolean NOT NULL DEFAULT true
);

CREATE TABLE app.submissao (
    id                 bigserial PRIMARY KEY,
    estabelecimento_id bigint      NOT NULL REFERENCES app.estabelecimento (id),
    periodo            date        NOT NULL,
    payload            jsonb       NOT NULL,          -- ocupação, leitos, diárias
    status             text        NOT NULL DEFAULT 'recebida'
                       CHECK (status IN ('recebida', 'aprovada', 'rejeitada')),
    recebido_em        timestamptz NOT NULL DEFAULT now(),
    validado_por       bigint      REFERENCES app.usuario (id),
    UNIQUE (estabelecimento_id, periodo)
);

-- ------------------------------------------------------------ serving (gold)
CREATE TABLE serving.indicador (
    indicador_id  text PRIMARY KEY,
    nome          text NOT NULL,
    unidade       text NOT NULL,
    descricao     text,
    fonte         text NOT NULL,
    metodologia   text,
    periodicidade text NOT NULL
);

CREATE TABLE serving.serie (
    indicador_id  text        NOT NULL REFERENCES serving.indicador (indicador_id),
    periodo       date        NOT NULL,
    setor         text        NOT NULL DEFAULT 'total',
    valor         numeric,
    fonte         text        NOT NULL,
    atualizado_em timestamptz NOT NULL,
    PRIMARY KEY (indicador_id, periodo, setor)
);

CREATE TABLE serving.resumo_card (
    indicador_id text PRIMARY KEY REFERENCES serving.indicador (indicador_id),
    valor_atual  numeric,
    variacao_pct numeric,
    periodo_ref  date
);

CREATE TABLE serving.relatorio (
    id      bigint PRIMARY KEY,                       -- espelho de app.relatorio.id
    numero  integer NOT NULL,
    ano     integer NOT NULL,
    titulo  text    NOT NULL,
    resumo  text,
    tags    text[]  NOT NULL DEFAULT '{}',
    url_pdf text    NOT NULL
);

CREATE TABLE serving.versao (
    versao     text PRIMARY KEY,
    gerado_em  timestamptz NOT NULL,
    linhas     bigint      NOT NULL,
    checksum   text        NOT NULL
);

CREATE INDEX ON serving.serie (indicador_id, periodo);
CREATE INDEX ON app.upload (status, enviado_em DESC);
```

## Regras que o diagrama registra

- **Estados do upload:** `rascunho → em_revisao → publicado` (ou `rejeitado`).
- **Estados da execução:** `enfileirado → executando → sucesso | falha`.
- Só um run com **`dbt tests` verdes** materializa `serving`; caso contrário a versão anterior
  permanece servindo o site.
- `app.execucao_pipeline.versao_publicada` aponta para `serving.versao.versao`. **Não é uma FK** —
  os dois schemas têm ciclos de vida independentes e `serving` é descartável.
- `serving.relatorio` é espelho de `app.relatorio`, materializado pelo publisher.
- **LGPD:** nenhum dado pessoal de hóspede entra no modelo. Da fase 2 só chega o agregado do
  estabelecimento; o contato do responsável fica restrito ao schema `app`.
