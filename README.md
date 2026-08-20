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
- *(fase 2)* Coleta autônoma pelos estabelecimentos, painel Cadastur/FNRH e Inventário Turístico

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/arquitetura.md`](docs/arquitetura.md) | Arquitetura completa: decisão do motor analítico (ADR-001), modelo de dados, contrato da API, governança/LGPD, mapa dos milestones e riscos |
| [`docs/diagramas/`](docs/diagramas/) | Diagramas em `.drawio` — visão de containers (C4), fluxo de publicação e camada de publicação |

## Stack

Pipeline de dados em **dbt + DuckDB** (medalhão bronze/silver/gold) executado no GitHub Actions,
publicando em **PostgreSQL**; API em **FastAPI**; front-end a definir. Toda a stack é
Apache/MIT — sem custo recorrente e sem impedimento de licença para a Prefeitura operar,
auditar e evoluir a plataforma.

O princípio central: **o plano analítico é o cérebro, nunca o runtime do site**. Se o pipeline
falhar, o site continua no ar servindo a última versão publicada.
