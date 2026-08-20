---
name: commit-push
description: Commita as mudanças pendentes do LogOS no padrão do projeto e envia (push) pra origin/main. Use quando o usuário pedir "commit e push", "sobe pro github", "salva e envia", ou variações do tipo "commita isso e manda pro repositório".
metadata:
  author: clayton
  version: "1.0.0"
---

# commit-push

Atalho para o fluxo de commit + push do LogOS, seguindo os padrões já
estabelecidos no histórico do repositório.

## Passo a passo

1. **Rodar em paralelo**: `git status`, `git diff` (staged e unstaged) e
   `git log --oneline -10` pra entender o que mudou e o estilo de mensagem
   já usado no projeto (verbo no imperativo, em português, ex.: "Adiciona",
   "Implementa", "Corrige", "Ajusta").

2. **Selecionar o que entra no commit.** Neste repositório é comum
   `README.md`, `database/connection.py` e `main.py` aparecerem como
   modificados só por causa de bit de permissão de arquivo (modo
   `100644` → `100755`), sem mudança de conteúdo — isso é ruído de
   ambiente (Windows/WSL), não trabalho feito. Antes de dar `git add`,
   rode `git diff -- <arquivo>` nesses três arquivos e exclua do commit
   qualquer um que mostre só `old mode`/`new mode` sem diff de conteúdo.
   Do contrário, adicione tudo que for conteúdo de código relevante,
   preferindo listar os arquivos por nome a `git add -A`/`git add .`.

3. **Escrever a mensagem de commit** no mesmo estilo do histórico:
   linha de assunto curta em português, verbo no imperativo, sem ponto
   final. Se o commit cobrir mais de uma tela/funcionalidade, usar corpo
   com bullets (um por área alterada), como em commits anteriores do tipo
   "Completa a revisao geral: campo NF, referencias e dados obsoletos".
   Usar HEREDOC pra preservar formatação, e sempre terminar com:
   ```
   Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
   ```

4. **Commitar** com os arquivos selecionados no passo 2. Nunca usar
   `--no-verify`. Se um hook de pre-commit falhar, corrigir o problema e
   criar um novo commit — não usar `--amend` nesse caso.

5. **Verificar o remote antes de empurrar**: `git remote -v` deve apontar
   pra `git@github.com:Clayyton36/LogOS.git` (SSH, "C" maiúsculo — o
   GitHub já indicou que o antigo `clayyton36` minúsculo foi renomeado).
   Se o remote ainda estiver como HTTPS ou com o `c` minúsculo antigo,
   avisar o usuário e corrigir com
   `git remote set-url origin git@github.com:Clayyton36/LogOS.git` antes
   de prosseguir.

6. **Dar `git push origin main`.** Se falhar por falta de credencial SSH
   (`Permission denied (publickey)` ou similar), não tentar contornar —
   avisar o usuário que a chave SSH precisa estar configurada/associada
   à conta GitHub e pedir pra ele resolver no terminal dele.

7. **Reportar ao usuário**: hash do commit, arquivos incluídos, arquivos
   deixados de fora (e por quê), e confirmação do push (`git log --oneline
   -1` local vs. o que foi enviado).

## Regras que continuam valendo (não são exclusivas desta skill)

- Só commitar/empurrar o que o usuário pediu — não é permissão geral pra
  sempre commitar/empurrar sozinho em qualquer situação futura.
- Nunca `git push --force` sem pedido explícito.
- Revisar o conteúdo do que foi staged antes de commitar; se algo parecer
  segredo/credencial, avisar antes de prosseguir.
- Preferir `git add <arquivo>` nomeado a `git add -A`/`.`.
