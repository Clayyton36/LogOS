# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

LogOS is a desktop application (PySide6/Qt) for controlling product returns ("devoluções") for Aeromaxx, a company selling across multiple marketplaces (`plataforma` field: e.g. Mercado Livre, Shopee). The codebase, UI text, and domain terms are in Portuguese (Brazil); keep new code, identifiers, and UI strings consistent with this convention.

**Product vision:** the returns module is the first module of a planned modular **Hub Logístico** (logistics platform) — future modules could cover invoices, stock, supplier integrations, marketplace integrations, barcode scanning. The explicit strategy is to *not* build the Hub upfront: prove the returns module end-to-end first, then expand. Don't propose work on future-Hub modules (stock, invoices, integrations) unless the user asks — the returns module isn't done yet.

**Business flow the domain model must respect:** physical return arrives → recebimento (receiving) registered → análise (product condition assessed) → baixa (write-off in system) → nota de devolução (return note) issued → destino (destination) decided: `ESTOQUE` (back to stock, only if condition is adequate) / `TROCA` (defect → supplier exchange claim) / `DESCARTE` (discard, unusable). The UI is deliberately split one page per step of this flow (Recebimento, Análise, Decisão, Consulta, Dashboard, Relatórios, Configurações) rather than one large screen.

**Build order (don't skip ahead without being asked):** 1) Recebimento (receiving form → first end-to-end write), 2) Consulta (search/filter/view), 3) Análise (condition assessment), 4) Decisão (destino: ESTOQUE/TROCA/DESCARTE), 5) Dashboard (KPIs), 6) Relatórios (export via `openpyxl`), 7) integrations/Hub expansion.

Steps 1–6 are done — the full returns flow (Recebimento → Análise → Decisão), Consulta, Dashboard and Relatórios are implemented end-to-end, each with its own Controller and going through `DevolucaoRepository`/SQLite. Step 7 (integrations/Hub expansion) hasn't started; don't propose work there unless asked. Within the returns module, remaining gaps are incremental refinement (field-level validation, UX polish), not missing pages — check with the user before assuming a whole new page/flow is needed.

A `Devolucao` is not fully immutable once "Finalizada": the Dashboard's pedido-detail dialog (`DetalheDevolucaoDialog`) has a "Reabrir" action that reverts `status` back to `"Analisada"` and clears `destino`/`observacoes_decisao`/`data_decisao`, so it can go through Decisão again. There is also a `lancado_sistema` field (`"SIM"`/`"NAO"`, default `"NAO"`) tracked on Relatórios, independent of the flow status — it just marks whether the pedido was keyed into an external system, toggled manually from that screen.

## Commands

There is no build system, linter, formatter, or test suite configured yet (no `pytest`, no `pyproject.toml`, no CI). When adding tooling, check with the user first since none currently exists.

```bash
# Set up environment (venv already exists at .venv/)
source .venv/bin/activate
pip install -r requirements.txt

# Run the app
python main.py
```

Running `main.py` calls `create_tables()` on startup, which creates `database/logos.db` (a SQLite file) and the `devolucoes` table if they don't already exist. The DB file is gitignored (`*.db`) — never delete a `database/logos.db` that already contains data without checking with the user first (there's no automated backup; see the "verify visually" note below for how to test without touching real data).

**Verify visually, since this is a desktop app, not a web app.** LogOS is a native PySide6/Qt window — browser automation tools (claude-in-chrome, Playwright, etc.) don't apply here, there's no DOM/HTTP involved. To smoke-test a change without popping a real window, drive the app with `QT_QPA_PLATFORM=offscreen`: construct `MainWindow`, interact with the real widgets (`findChild(...)`, set combo/line-edit values, `.click()` real buttons — not calling internal methods directly), and call `widget.grab().save(path)` to capture screenshots to look at. Modal dialogs (`QMessageBox`, `QDialog.exec()`) block, so schedule `QTimer.singleShot(...)` callbacks before triggering them to interact with/dismiss the modal from inside its nested event loop. Always use a throwaway `database/logos.db` for this (delete it before and after), never the user's real one. The project's `/commit-push` skill (`.claude/skills/commit-push/`) has the git side of this workflow (selective staging, commit message style, push); if the offscreen-driver pattern above gets used often, consider recommending `/run-skill-generator` to turn it into a proper project skill.

## Architecture

Layered structure, small but intentional:

- **`main.py`** — entry point. Initializes the DB schema, then boots the `QApplication` and shows `MainWindow`.
- **`database/`** — raw SQLite access.
  - `connection.py`: `get_connection()` opens a sqlite3 connection to `database/logos.db` (path resolved relative to repo root) with `row_factory = sqlite3.Row`.
  - `schema.py`: `create_tables()` — idempotent `CREATE TABLE IF NOT EXISTS` DDL for `devolucoes` and `condicoes_produto`. This is the single source of truth for the DB schema; there is no migration framework. **New columns are additive and safe on existing local `.db` files** — the established pattern (see the `colunas_novas` loop and the `lancado_sistema` check right after it) is `ALTER TABLE devolucoes ADD COLUMN ... [DEFAULT ...]` guarded by a `PRAGMA table_info` check, so a column added to `CREATE TABLE` also needs a matching `ALTER TABLE ADD COLUMN` for it to reach databases created before the column existed — don't just edit the `CREATE TABLE` and assume old `.db` files pick it up. Deleting the local `.db` is only a fallback for renaming/removing a column, not for adding one.
- **`app/models/`** — plain `@dataclass` models mirroring DB tables (`Devolucao` mirrors the `devolucoes` table 1:1, including a `data_criacao`/`data_atualizacao` audit pair).
- **`app/repositories/`** — data access objects that translate between models and SQL. Each method opens its own connection via `get_connection()` and closes it before returning (no shared/pooled connection, no ORM). Follow this per-call-connection pattern for new repository methods. Two repositories exist: `DevolucaoRepository` (recebimento/análise/decisão/consulta/indicadores/reabertura/lançado-no-sistema) and `CondicaoProdutoRepository` (CRUD for the user-editable "condição do produto" list used in Análise).
- **`app/controllers/`** — exists and is the required entry point for all writes: `DevolucaoController` (validation, the returns flow, and the fixed-choice constants consumed directly by the UI — `PLATAFORMAS_VALIDAS`, `OBSERVACOES_RECEBIMENTO_VALIDAS`, `ACESSORIOS_VALIDOS`, `AVARIA_VALIDOS`, `DESTINOS_VALIDOS`, `LANCADO_SISTEMA_VALIDOS`) and `ConfiguracoesController` (condições do produto CRUD). Repository methods are not called directly from UI code — route new writes/reads through a controller.
- **`app/ui/`** — one `QWidget` subclass per page (`DashboardPage`, `NovaDevolucaoPage`, `ConsultaPage`, `AnalisePage`, `DecisaoPage`, `RelatoriosPage`, `ConfiguracoesPage`), plus `DetalheDevolucaoDialog` (a `QDialog`, not a page — read-only detail + "Reabrir" for a finalized pedido) and `MainWindow`, which owns a `QStackedWidget` and switches between pages. `MainWindow` builds the side menu and page instances directly in `__init__`; there's still no router/navigation abstraction, but pages that need to jump to a specific record on another page expose a `selecionar_devolucao(id)` method, and `MainWindow` wires cross-page callbacks after construction (see `DashboardPage.definir_navegacao(...)`, called from `MainWindow` with closures over `navegar_para`/`paginas`) rather than pages reaching into `QStackedWidget` themselves.

### Data flow

Layering is UI → Controllers → Repositories → SQLite, consistently, for both writes and reads. A Services layer is still reserved for once business rules (e.g. auto-suggesting ESTOQUE/TROCA/DESCARTE from condição+avaria) get more complex than "user picks from a fixed list" — `app/services/` hasn't been created yet. Repository methods should not be called directly from UI code; route new writes/reads through a controller.

Fixed-choice fields (Plataforma, Observações de recebimento, Acessórios, Avaria, Destino, Lançado no sistema) are backed by plain tuple constants in `devolucao_controller.py`, imported directly by the UI to populate `QComboBox`es — not stored in a DB table. That's different from "Condição do produto" (Configurações), which the user can add/remove at runtime via `condicoes_produto` in the DB. Use the tuple-constant pattern for genuinely fixed enumerations the user didn't ask to make editable; use the DB-table pattern only when there's an explicit need for the user to manage the list themselves.

A broader target directory layout was agreed with the user. `app/{controllers,models,repositories,ui}/` exist and are in active use; `app/{assets,services,utils}/` and the top-level `config/`, `docs/`, `logs/`, `reports/`, `tests/` don't exist yet. Create these lazily as needed rather than scaffolding them upfront.
