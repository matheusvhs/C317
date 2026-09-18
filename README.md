# C317 — Plataforma Web do Observatório do Turismo de Santa Rita do Sapucaí

Projeto da disciplina **C317 (Projeto Orientado)** do Inatel, desenvolvido pelo programa
Working Life Connected em parceria com a **Secretaria Municipal de Cultura, Esporte, Lazer e
Turismo (SMCELT)** da Prefeitura de Santa Rita do Sapucaí — Edital HEIComp 2026.2.

## O problema

O Observatório do Turismo de SRS coleta dados turísticos e econômicos (hospedagem, leitos,
empresas, empregos, fluxo de visitantes) de forma manual e anual, com baixo retorno dos
estabelecimentos. O conteúdo produzido fica em arquivos internos, sem acesso público, e o
histórico se perde entre mudanças de gestão.

## O que a plataforma entrega

- Publicação organizada dos indicadores turísticos do município
- Acesso público aos relatórios e pesquisas do Observatório
- Dashboard visual com filtros por período e setor
- Painel administrativo para a SMCELT atualizar e publicar novos dados
- *(evolução futura, fora do escopo do protótipo)* Coleta autônoma pelos estabelecimentos,
  painel Cadastur/FNRH e Inventário Turístico

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/arquitetura.md`](docs/arquitetura.md) | Arquitetura completa: decisão do motor analítico (ADR-001), modelo de dados, contrato da API, governança/LGPD, mapa dos milestones e riscos |
| [`docs/casos-de-uso.md`](docs/casos-de-uso.md) | Atores, catálogo dos 9 casos de uso (escopo enxuto por decisão) e descrição expandida de UC06 (publicar dados) e UC01 (consultar painel) — item 2 do Milestone III |
| [`docs/modelo-dados.md`](docs/modelo-dados.md) | Estrutura do banco: schemas `app` (OLTP) e `serving` (espelho do gold), DDL PostgreSQL e regras de estado — item 3 do Milestone III |
| [`docs/agentes.md`](docs/agentes.md) | Como o time usa Claude Code neste repositório: `CLAUDE.md`, skills versionadas, convenções e boas práticas |
| [`docs/diagramas/`](docs/diagramas/) | Diagramas em `.drawio` + exportações `.drawio.png`: [visão de containers](docs/diagramas/01_visao_containers.drawio.png), [fluxo de publicação](docs/diagramas/02_fluxo_publicacao.drawio.png), [camada de publicação/API](docs/diagramas/03_camada_publicacao_api.drawio.png), [casos de uso](docs/diagramas/04_casos_de_uso.drawio.png) e [modelo de dados (ER)](docs/diagramas/05_modelo_dados_er.drawio.png) |

## Stack

Pipeline de dados em **dbt + DuckDB** (medalhão bronze/silver/gold) executado no GitHub Actions,
publicando em **PostgreSQL**; API em **FastAPI**; front-end a definir. Toda a stack é
Apache/MIT — sem custo recorrente e sem impedimento de licença para a Prefeitura operar,
auditar e evoluir a plataforma.

O princípio central: **o plano analítico é o cérebro, nunca o runtime do site**. Se o pipeline
falhar, o site continua no ar servindo a última versão publicada.
