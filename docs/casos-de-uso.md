# Casos de uso — item 2 do Milestone III

Diagrama: [`docs/diagramas/04_casos_de_uso.drawio.png`](diagramas/04_casos_de_uso.drawio.png)
(página 1 de `Casos_de_Uso_e_Modelo_de_Dados.drawio`).

O enunciado da disciplina pede escopo pequeno, para o time conseguir cumprir o planejado com
tranquilidade. São **nove casos de uso**: sete de ator e dois incluídos. Todos entram nos
milestones 4–6 — não existe caso de uso "desejável" no diagrama, porque item que talvez não seja
entregue não é escopo, é intenção.

## Atores

| Ator | Tipo | Descrição |
|---|---|---|
| **Visitante do portal** | primário, anônimo | Cidadão, turista, empreendedor, gestor público ou pesquisador. Consulta sem login. |
| **Gestor SMCELT** | primário, autenticado | Equipe da Secretaria. Único perfil com credencial (JWT). Publica e acompanha. |
| **Pipeline analítico** | secundário (sistema) | GitHub Actions + dbt/DuckDB + publisher. Executa o processamento e devolve o status do run. |

## Catálogo de casos de uso

| # | Caso de uso | Ator |
|---|---|---|
| UC01 | Consultar painel de indicadores (com filtros por período e setor) | Visitante |
| UC02 | Consultar e baixar relatórios do Observatório | Visitante |
| UC03 | Autenticar no painel | Gestor SMCELT |
| UC04 | Enviar planilha de dados | Gestor SMCELT |
| UC05 | Publicar relatório em PDF | Gestor SMCELT |
| UC06 | Publicar dados (dispara o pipeline) | Gestor SMCELT · Pipeline analítico |
| UC07 | Acompanhar execuções do pipeline | Gestor SMCELT · Pipeline analítico |
| UC08 | Validar schema e regras de negócio | — (`«include»` de UC04) |
| UC09 | Registrar trilha de auditoria | — (`«include»` de UC05 e UC06) |

Relações do diagrama:

- `UC04 «include» UC08` — toda planilha enviada passa pela validação de schema e regras.
- `UC05 «include» UC09` e `UC06 «include» UC09` — toda publicação grava quem publicou, quando e a
  partir de qual arquivo. É o que garante o histórico entre mudanças de gestão.
- Todos os casos de uso do painel exigem **UC03** (sessão JWT válida); a consulta pública é anônima.

### Cobertura das funcionalidades essenciais do SRS

| Funcionalidade essencial | Casos de uso |
|---|---|
| Dashboard visual com filtros por período e setor | UC01 |
| Acesso público aos relatórios e pesquisas | UC02, UC05 |
| Publicação organizada dos indicadores | UC04, UC06, UC08 |
| Painel administrativo para atualização contínua | UC03, UC06, UC07 |
| Continuidade entre gestões (histórico auditável) | UC09 |

## Fora do escopo do protótipo — evolução futura

Registrado no diagrama como quadro tracejado, **sem ator associado e sem compromisso de entrega no
semestre**:

- Coleta autônoma pelos estabelecimentos (formulário com token)
- Validação das submissões pela SMCELT
- Exportação dos dados do gráfico em CSV/JSON
- Painel Cadastur/FNRH e Inventário Turístico

O modelo de dados já prevê as tabelas `app.estabelecimento` e `app.submissao` para a coleta
autônoma — desenhar não custa cronograma, implementar custa. Elas aparecem tracejadas no ER pelo
mesmo motivo.

## Descrição expandida dos dois casos de uso críticos

### UC06 — Publicar dados

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Gestor SMCELT |
| **Ator secundário** | Pipeline analítico (GitHub Actions + dbt) |
| **Pré-condições** | Usuário autenticado (UC03); existe um upload em `app.upload` com status `em_revisao` e validação de schema aprovada (UC04 + UC08). |
| **Pós-condições** | `serving.*` materializado em transação com a nova versão; `serving.versao` atualizado; `app.upload.status = publicado`; evento gravado em `app.auditoria`. |

**Fluxo principal**

1. O gestor abre a lista de uploads pendentes no painel.
2. Seleciona o upload revisado e confirma a publicação.
3. O sistema grava o arquivo na landing do object storage e dispara o pipeline
   (`workflow_dispatch`), criando um registro em `app.execucao_pipeline` com status `enfileirado`.
4. O pipeline executa bronze → silver → gold e roda os `dbt tests`.
5. Com os testes verdes, o publisher materializa `serving.*` em transação única e incrementa
   `serving.versao`.
6. O sistema registra a auditoria (UC09) e exibe "publicado" no painel.
7. O portal público passa a servir a nova versão.

**Fluxos alternativos**

- **A1 — testes de qualidade reprovados:** o pipeline não promove nada; `execucao_pipeline.status = falha`;
  o painel mostra o log e as linhas rejeitadas; `serving.*` permanece na versão anterior.
- **A2 — falha na materialização:** a transação sofre rollback; `serving.*` fica íntegro na versão
  anterior e o site continua no ar.
- **A3 — pipeline indisponível:** o upload fica `em_revisao` e é reprocessado no próximo ciclo de cron.

### UC01 — Consultar painel de indicadores

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Visitante do portal (anônimo) |
| **Pré-condições** | Existe pelo menos uma publicação em `serving.serie`. |
| **Pós-condições** | Nenhuma — é uma consulta de leitura, sem efeito colateral. |

**Fluxo principal**

1. O visitante abre o painel e vê os cards com os indicadores mais recentes.
2. Escolhe um indicador, um intervalo de períodos e, opcionalmente, um setor.
3. O front-end chama `GET /api/v1/series?indicador=&de=&ate=&setor=`.
4. A API lê `serving.serie` (formato longo) e devolve a série filtrada com fonte e data de
   atualização.
5. O gráfico é redesenhado exibindo fonte e "última atualização" (exigência de transparência de
   dado público).

**Fluxo alternativo**

- **A1 — sem dados no recorte:** a API devolve lista vazia e a interface explica que ainda não há
  publicação para o filtro escolhido, em vez de mostrar gráfico em branco.

**Por que este caso de uso importa para a arquitetura:** como `serving.serie` está em formato longo,
um indicador novo é uma linha em `serving.indicador` + o cálculo no gold — **sem alterar API nem
front-end**. É o que evita mudança brusca de estrutura depois do M3 e o que permite o escopo
continuar pequeno sem fechar a porta para crescer.
