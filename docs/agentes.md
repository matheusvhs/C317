# Desenvolvimento agêntico no projeto

Como o time usa **Claude Code** neste repositório. O objetivo é que qualquer pessoa clone o projeto
e tenha o mesmo contexto e as mesmas ferramentas, sem depender do que está configurado na máquina
de quem começou.

## O que já vem no repositório

| Arquivo | Papel |
|---|---|
| `CLAUDE.md` | Contexto do projeto carregado automaticamente em toda sessão: princípio de arquitetura, stack, estrutura, convenções e comandos. É o arquivo de maior impacto — mantenha-o atualizado. |
| `.claude/settings.json` | Configuração **compartilhada**: plugin do GitHub e lista de comandos pré-aprovados (reduz prompts de permissão para operações de leitura). Versionado. |
| `.claude/settings.local.json` | Configuração **pessoal** de cada pessoa. Está no `.gitignore` — não commitar. |
| `.claude/skills/drawio-skill/` | Skill de diagramas (MIT, de [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)), versionada para o time não precisar instalar nada. |
| `.claude/skills/diagramas-c317/` | Skill do projeto: identidade visual dos diagramas e fluxo de exportação usado nos relatórios de milestone. |

## Pré-requisitos

```bash
npm install -g @anthropic-ai/claude-code   # CLI
brew install --cask drawio                 # exportação de diagramas (macOS)
bash docs/setup-check.sh                   # confere o resto do ambiente
```

No VS Code, a extensão `hediet.vscode-drawio` abre os `.drawio` direto no editor.

## Como trabalhar

1. `claude` na raiz do repositório — o `CLAUDE.md` entra em contexto sozinho.
2. Trabalhe sempre em branch (`docs/...`, `feat/...`, `fix/...`), nunca na `main`.
3. Peça o que precisa em português mesmo; a documentação do projeto é em PT-BR.
4. Antes de aceitar uma mudança estrutural, confira se ela não contraria `docs/arquitetura.md` —
   depois do Milestone III a estrutura está congelada.

### Comandos úteis do Claude Code

| Comando | Uso |
|---|---|
| `/init` | Regenera o `CLAUDE.md` a partir do código (use com cuidado: o atual foi escrito à mão) |
| `/code-review` | Revisa o diff da branch antes de abrir o PR |
| `/artifacts` | Lista as páginas publicadas na sessão |
| `!<comando>` | Roda um comando do shell direto no prompt (ex.: `!git log --oneline -5`) |

## Skills

Skills são pacotes de instruções que o Claude carrega quando a tarefa combina com a descrição
delas. As duas do repositório são carregadas automaticamente — nada a instalar.

Para adicionar uma skill nova ao projeto, crie `.claude/skills/<nome>/SKILL.md` com o cabeçalho:

```markdown
---
name: <nome-em-kebab-case>
description: Use quando <situação concreta em que a skill deve disparar>.
---
```

A `description` é o que decide se a skill é carregada — descreva o **gatilho**, não a capacidade.

Skills externas podem ser instaladas na sua conta (valem para todos os seus projetos):

```bash
npx -y skills@latest add Agents365-ai/drawio-skill -g -a claude-code
npx -y skills@latest list -g
```

Só vale versionar no repositório uma skill que o time inteiro usa **neste** projeto.

## Boas práticas que já custaram retrabalho aqui

- **Contexto vence prompt longo**: informação estável (decisão de arquitetura, convenção, comando)
  vai para o `CLAUDE.md` ou para uma skill; não para o prompt de cada sessão.
- **Diagrama sempre exportado com `-e`** e passado pelo `repair_png.py` — o CLI do draw.io gera um
  PNG corrompido sem isso.
- **Não versionar `.venv/`**: o `apps/api/.gitignore` cuida disso, mas confira o `git status` antes
  do commit — são milhares de arquivos se escapar.
- **Revisar o que o agente escreveu antes do commit.** O trabalho é do time, e a banca vai
  perguntar o porquê de cada decisão para vocês, não para a ferramenta.
