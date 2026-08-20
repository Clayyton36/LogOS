---
name: testar-app
description: Testa o LogOS de ponta a ponta rodando o app Qt de verdade (não a suíte de testes, não import isolado de função) sem abrir uma janela real, com screenshots pra conferir visualmente. Use quando o usuário pedir pra "testar o app", "testar pelo navegador" (LogOS não é web — ver nota abaixo), "ver se funciona na tela", ou depois de qualquer mudança em app/ui/.
metadata:
  author: clayton
  version: "1.0.0"
---

# testar-app

LogOS é um app desktop nativo (PySide6/Qt) — não roda em navegador, não tem
DOM/HTTP. Ferramentas de automação de browser (claude-in-chrome, Playwright
etc.) não se aplicam aqui. Se o usuário pedir pra "testar pelo navegador",
avise isso primeiro e use esta skill no lugar.

Rodar de verdade significa construir a `MainWindow` real e interagir com os
widgets reais (clicar em botões encontrados via `findChildren`, preencher
`QLineEdit`/`QComboBox` de verdade) — não chamar métodos internos das
páginas diretamente pulando a UI, e não só importar e checar um retorno.

## Passo a passo

1. **Nunca usar o banco real.** Antes de rodar, `rm -f database/logos.db`
   só se esse arquivo ainda não existir com dados reais do usuário — sempre
   checar com `ls database/*.db` antes. Depois do teste, `rm -f
   database/logos.db` de novo pra não deixar lixo no repo (o arquivo é
   gitignored, mas não deve sobreviver ao teste).

2. **Escrever um script de driver** (no diretório de scratchpad da sessão,
   nunca dentro do repo) que:
   - define `os.environ["QT_QPA_PLATFORM"] = "offscreen"` antes de importar
     `PySide6`;
   - cria a `QApplication`, chama `create_tables()`, instancia `MainWindow`
     e dá `.show()`;
   - navega entre páginas clicando nos botões reais do menu lateral
     (`findChildren(QPushButton)` filtrando por `objectName() ==
     "botaoNavegacao"` e pelo texto), não trocando o `QStackedWidget`
     manualmente;
   - acha as páginas com `janela.findChild(NovaDevolucaoPage)` (e as outras
     classes de `app/ui/`) — `findChild` acha widgets mesmo não visíveis no
     momento, então dá pra pegar todas as páginas de uma vez;
   - preenche campos e clica em botões reais (`botao(pagina, "texto").click()`),
     nunca chamando o método do slot diretamente;
   - tira screenshot com `widget.grab().save(caminho)` — da `janela` inteira
     pra telas normais, ou do próprio dialog (`app.activeModalWidget()`)
     pra modais.

3. **Diálogos modais bloqueiam** (`QMessageBox.exec()`, `QDialog.exec()`).
   Antes de disparar a ação que abre um, agendar
   `QTimer.singleShot(delay_ms, callback)` — o callback roda dentro do loop
   de eventos aninhado que o `.exec()` abre, pega o modal via
   `app.activeModalWidget()`, tira o screenshot dele se for o caso, e
   interage (clica no botão certo, ou `.accept()`/`.reject()`). Pra modais
   encadeados (ex.: confirmação dentro de confirmação), agendar o próximo
   `QTimer.singleShot` de dentro do callback anterior.

4. **Validar o que os screenshots não provam:** depois de cada ação de
   escrita, também confirmar via `DevolucaoController` (`consultar()`,
   `obter_indicadores()`) que o dado gravado é o esperado — screenshot
   mostra que renderizou, não que salvou certo.

5. **Cobrir o fluxo inteiro**, não só a tela que mudou: Nova Devolução →
   Análise → Decisão → Dashboard (cards clicáveis, lista por indicador,
   abrir/reabrir pedido finalizado) → Relatórios (coluna, filtro e botão de
   "lançado no sistema") → Consulta → Configurações. Cada mudança pode
   quebrar uma tela vizinha que consome o mesmo dado (ex.: mexer no SKU
   afeta o resumo da Análise e a tabela de Consulta).

6. **Olhar os screenshots de verdade** (Read na imagem), não só conferir que
   o script rodou sem exceção — uma tela em branco ou um layout quebrado
   não derruba o processo Python.

7. **Limpar ao final:** `rm -f database/logos.db`. Não commitar esse arquivo
   nem deixá-lo no working tree.

## Relacionado

- `.claude/skills/commit-push/` cobre o lado de git (commit + push) depois
  que o teste passar.
- Ver `CLAUDE.md`, seção "Verify visually", pra contexto de por que esse
  padrão existe (app desktop, não web).
