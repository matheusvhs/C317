# Casos de uso — item 2 do Milestone III

Diagrama: [`docs/diagramas/04_casos_de_uso.drawio.png`](diagramas/04_casos_de_uso.drawio.png)
(página 1 de `Casos_de_Uso_e_Modelo_de_Dados.drawio`).

O escopo foi mantido deliberadamente pequeno, como pede o enunciado: **doze casos de uso
essenciais** (UC01–UC08 e UC10–UC13), que cabem nos milestones 4–6, e **dois desejáveis**
(UC09 e UC14) que só entram se sobrar cronograma.

## Atores

| Ator | Tipo | Descrição |
|---|---|---|
| **Visitante do portal** | primário, anônimo | Cidadão, turista, empreendedor, gestor público ou pesquisador. Consulta sem login. |
| **Gestor SMCELT** | primário, autenticado | Equipe da Secretaria. Único perfil com credencial (JWT). Publica e valida dados. |
| **Estabelecimento** | primário, fase 2 | Hotel ou pousada que informa a própria ocupação por token, sem login. |
| **Pipeline analítico** | secundário (sistema) | GitHub Actions + dbt/DuckDB + publisher. Executa o processamento e devolve o status do run. |

## Catálogo de casos de uso

| # | Caso de uso | Ator | Escopo |
|---|---|---|---|
| UC01 | Consultar painel de indicadores | Visitante | essencial |
| UC02 | Filtrar indicadores por período e setor | Visitante | essencial |
| UC03 | Exportar dados do gráfico (CSV/JSON) | Visitante | essencial |
| UC04 | Consultar relatórios do Observatório | Visitante | essencial |
| UC05 | Baixar relatório em PDF | Visitante | essencial |
| UC06 | Autenticar no painel | Gestor SMCELT | essencial |
| UC07 | Enviar planilha de dados | Gestor SMCELT | essencial |
| UC08 | Publicar relatório em PDF | Gestor SMCELT | essencial |
| UC09 | Validar submissões dos estabelecimentos | Gestor SMCELT | **fase 2** |
| UC10 | Publicar dados (dispara o pipeline) | Gestor SMCELT · Pipeline | essencial |
| UC11 | Acompanhar execuções do pipeline | Gestor SMCELT · Pipeline | essencial |
| UC12 | Validar schema e regras de negócio | — (`«include»` de UC07) | essencial |
| UC13 | Registrar trilha de auditoria | — (`«include»` de UC08 e UC10) | essencial |
| UC14 | Enviar dados de ocupação do mês | Estabelecimento | **fase 2** |

Relações do diagrama:

- `UC07 «include» UC12` — toda planilha enviada passa pela validação de schema e regras.
- `UC08 «include» UC13` e `UC10 «include» UC13` — toda publicação grava quem publicou, quando e
  a partir de qual arquivo. É o que garante o histórico entre mudanças de gestão.
- Todos os casos de uso do painel exigem **UC06** (sessão JWT válida); a consulta pública é anônima.

## Descrição expandida dos dois casos de uso críticos

### UC10 — Publicar dados

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Gestor SMCELT |
| **Ator secundário** | Pipeline analítico (GitHub Actions + dbt) |
| **Pré-condições** | Usuário autenticado (UC06); existe um upload em `app.upload` com status `em_revisao` e validação de schema aprovada (UC07 + UC12). |
| **Pós-condições** | `serving.*` materializado em transação com a nova versão; `serving.versao` atualizado; `app.upload.status = publicado`; evento gravado em `app.auditoria`. |

**Fluxo principal**

1. O gestor abre a lista de uploads pendentes no painel.
2. Seleciona o upload revisado e confirma a publicação.
3. O sistema grava o arquivo na landing do object storage e dispara o pipeline
   (`workflow_dispatch`), criando um registro em `app.execucao_pipeline` com status `enfileirado`.
4. O pipeline executa bronze → silver → gold e roda os `dbt tests`.
5. Com os testes verdes, o publisher materializa `serving.*` em transação única e incrementa
   `serving.versao`.
6. O sistema registra a auditoria (UC13) e exibe "publicado" no painel.
7. O portal público passa a servir a nova versão.

**Fluxos alternativos**

- **A1 — testes de qualidade reprovados:** o pipeline não promove nada; `execucao_pipeline.status = falha`;
  o painel mostra o log e as linhas rejeitadas; `serving.*` permanece na versão anterior.
- **A2 — falha na materialização:** a transação sofre rollback; `serving.*` fica íntegro na versão
  anterior e o site continua no ar.
- **A3 — pipeline indisponível:** o upload fica `em_revisao` e é reprocessado no próximo ciclo de cron.

### UC02 — Filtrar indicadores por período e setor

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Visitante do portal (anônimo) |
| **Pré-condições** | Existe pelo menos uma publicação em `serving.serie`. |
| **Pós-condições** | Nenhuma — é uma consulta de leitura, sem efeito colateral. |

**Fluxo principal**

1. O visitante escolhe um indicador, um intervalo de períodos e, opcionalmente, um setor.
2. O front-end chama `GET /api/v1/series?indicador=&de=&ate=&setor=`.
3. A API lê `serving.serie` (formato longo) e devolve a série filtrada com fonte e data de
   atualização.
4. O gráfico é redesenhado exibindo fonte e "última atualização" (exigência de transparência de
   dado público).

**Fluxo alternativo**

- **A1 — sem dados no recorte:** a API devolve lista vazia e a interface explica que ainda não há
  publicação para o filtro escolhido, em vez de mostrar gráfico em branco.

**Por que este caso de uso importa para a arquitetura:** como `serving.serie` está em formato longo,
um indicador novo é uma linha em `serving.indicador` + o cálculo no gold — **sem alterar API nem
front-end**. É o que evita mudança brusca de estrutura depois do M3.
