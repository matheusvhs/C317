---
name: diagramas-c317
description: Use ao criar ou editar qualquer diagrama do Observatório do Turismo de SRS (arquitetura, casos de uso, ER, fluxo) para aplicar a identidade visual do projeto e o fluxo de exportação usado nos relatórios de milestone. Complementa a skill drawio-skill com as decisões já tomadas neste repositório.
---

# Diagramas do Observatório do Turismo (C317)

Aplica a identidade visual do projeto aos diagramas e mantém as exportações no formato que os
relatórios de milestone esperam. Para a mecânica do XML do draw.io e do CLI, use a skill
`drawio-skill` (versionada em `.claude/skills/drawio-skill/`); esta skill traz **o que já foi
decidido aqui** e não deve ser reaberto a cada diagrama novo.

## Arquivos existentes

| Arquivo | Conteúdo |
|---|---|
| `docs/diagramas/Arquitetura_Observatorio_Turismo_SRS.drawio` | 3 páginas: visão de containers (C4 nível 2), fluxo de publicação, camada de publicação/API |
| `docs/diagramas/Casos_de_Uso_e_Modelo_de_Dados.drawio` | 2 páginas: casos de uso (UML) e modelo de dados (ER) |
| `docs/diagramas/gerar_diagramas.py` | Gera o segundo arquivo por código — a identidade visual está nas constantes do topo |

Numeração das exportações continua a sequência existente: `01_`…`05_` já estão em uso.

## Identidade visual

```
Gradiente do cabeçalho   #0A4AAD → #6C5CE0 → #C750D6  (azul → roxo → magenta)
Texto principal          #1F2733      Texto secundário   #5A6470
Bordas / divisores       #D8DCE4      Rodapé             #8A939E
Fonte                    Helvetica
```

Regras que mantêm as páginas coerentes entre si:

- **Cabeçalho** em três peças sobrepostas (faixa azul→roxo, divisor sólido, faixa roxo→magenta),
  altura 92px, começando em `y=30`. As peças precisam se sobrepor ~10px, senão os cantos
  arredondados abrem uma emenda branca visível.
- **Cartões**: retângulo branco `rounded=1;arcSize=10`, borda `#D8DCE4`, `shadow=1`, com uma barra
  de acento de 5px de largura na borda esquerda (`arcSize=40`).
- **Rótulos de seção** em caixa alta, `fontSize=10`, `letter-spacing:1.2px`, cor `#5A6470`.
- **Rodapé** em toda página: linha `#D8DCE4`, identificação do projeto à esquerda e
  `C317 · HEIComp 2026.2 · <milestone> · página N de M` à direita.
- **Fora do escopo do protótipo** sempre em magenta `#C750D6` com traço tracejado — deixa explícito
  na banca o que o time se comprometeu a entregar e o que é evolução futura.
- **Legenda** obrigatória quando a página usa 3+ cores semânticas.

## Fluxo de trabalho

1. Mudança estrutural (novos nós, nova página) → editar `gerar_diagramas.py` e rodar
   `python3 docs/diagramas/gerar_diagramas.py`. Ajuste pontual de posição → editar o `.drawio`
   direto no draw.io desktop.
2. Rascunho para conferência visual (sem `-e`, largura limitada para caber na visão do modelo):

   ```bash
   drawio -x -f png --width 2000 -b 10 --page-index 1 -o /tmp/rascunho.png <arquivo>.drawio
   ```

3. Ler o PNG e conferir: rótulos cortados, arestas atravessando formas, linhas empilhadas,
   sobreposição de texto.
4. Exportação final, **sempre com `-e`** (XML embutido, PNG continua editável) e nome
   `NN_nome.drawio.png`:

   ```bash
   drawio -x -f png -e -s 2 -b 10 --page-index N -o docs/diagramas/NN_nome.drawio.png <arquivo>.drawio
   python3 .claude/skills/drawio-skill/scripts/repair_png.py docs/diagramas/NN_nome.drawio.png
   ```

   O `repair_png.py` é obrigatório: o CLI do draw.io trunca o chunk IEND em PNGs com `-e`.

5. Registrar o diagrama novo na tabela de documentação do `README.md`.

## Conteúdo: o que cada diagrama precisa mostrar

- Diagramas de arquitetura separam visualmente **plano de aplicação** e **plano analítico**, com as
  três integrações numeradas entre eles (grava na landing · dispara pipeline · materializa serving).
  Essa separação é o argumento central do projeto na banca — não dilua.
- Casos de uso: atores primários à esquerda, ator-sistema (pipeline) à direita ou abaixo, fronteira
  do sistema explícita, `«include»` tracejado em roxo.
- ER: tabelas agrupadas por schema (`app` e `serving`), pé-de-galinha nas FKs, marcação PK/FK/UQ por
  coluna e — importante — as ligações entre schemas em tracejado magenta, porque são materializações
  do publisher e **não** chaves estrangeiras.
