#!/usr/bin/env bash
# Verificação do ambiente de desenvolvimento — Observatório do Turismo de SRS (C317)
# Uso: bash docs/setup-check.sh
export PATH="/opt/homebrew/opt/postgresql@17/bin:$HOME/.local/bin:/opt/homebrew/bin:$PATH"

ver() { "$@" 2>/dev/null | head -1; }

printf '\n== Setup C317 — %s — %s ==\n\n' "$(whoami)@$(hostname -s)" "$(date '+%Y-%m-%d %H:%M')"
printf '%-14s | %-10s | %s\n' "COMPONENTE" "STATUS" "VERSÃO"
printf '%-14s-+-%-10s-+-%s\n' "--------------" "----------" "------------------------------"

check() { # nome, comando de versão...
  local nome="$1"; shift
  local out; out=$(ver "$@")
  if [ -n "$out" ]; then printf '%-14s | %-10s | %s\n' "$nome" "OK"     "$out"
  else                   printf '%-14s | %-10s | %s\n' "$nome" "FALTA"  "-"; fi
}

check "Git"         git --version
check "Node.js"     node --version
check "npm"         npm --version
check "Next.js"     sh -c 'cd apps/web 2>/dev/null && npx --no-install next --version || npm view next version 2>/dev/null | sed "s/^/disponivel no npm: /"'
check "Python"      python3 --version
check "FastAPI"     apps/api/.venv/bin/python -c "import fastapi;print('FastAPI',fastapi.__version__)"
check "PostgreSQL"  psql --version
check "dbt"         sh -c 'dbt --version 2>&1 | grep -m1 installed | sed "s/.*installed: */dbt-core /"; dbt --version 2>&1 | grep -m1 duckdb | sed "s/^ *- /+ dbt-/;s/ - .*//"'
check "DuckDB"      duckdb --version
check "VS Code"     code --version
check "GitHub CLI"  gh --version
check "Docker"      docker --version

printf '\n-- PostgreSQL: servidor e schemas --\n'
pg_isready 2>&1 | sed 's/^/  /'
psql -d otsrs -c "\dn" 2>&1 | sed 's/^/  /'

printf '\n-- Extensões do VS Code --\n'
code --list-extensions 2>/dev/null | grep -Ei 'python|ruff|eslint|prettier|drawio|dbt' | sed 's/^/  /'

printf '\n-- Repositório --\n'
git -C "$(dirname "$0")/.." log --oneline -1 2>/dev/null | sed 's/^/  /'
printf '\n'
