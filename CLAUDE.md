# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

LogOS is a desktop application (PySide6/Qt) for controlling product returns ("devoluções") for Aeromaxx, a company selling across multiple marketplaces (`plataforma` field: e.g. Mercado Livre, Shopee). The codebase, UI text, and domain terms are in Portuguese (Brazil); keep new code, identifiers, and UI strings consistent with this convention.

**Product vision:** the returns module is the first module of a planned modular **Hub Logístico** (logistics platform) — future modules could cover invoices, stock, supplier integrations, marketplace integrations, barcode scanning. The explicit strategy is to *not* build the Hub upfront: prove the returns module end-to-end first, then expand. Don't propose work on future-Hub modules (stock, invoices, integrations) unless the user asks — the returns module isn't done yet.

**Business flow the domain model must respect:** physical return arrives → recebimento (receiving) registered → análise (product condition assessed) → baixa (write-off in system) → nota de devolução (return note) issued → destino (destination) decided: `ESTOQUE` (back to stock, only if condition is adequate) / `TROCA` (defect → supplier exchange claim) / `DESCARTE` (discard, unusable). The UI is deliberately split one page per step of this flow (Recebimento, Análise, Decisão, Consulta, Dashboard, Relatórios, Configurações) rather than one large screen.

**Build order (don't skip ahead without being asked):** 1) Recebimento (receiving form → first end-to-end write), 2) Consulta (search/filter/view), 3) Análise (condition assessment), 4) Decisão (destino: ESTOQUE/TROCA/DESCARTE), 5) Dashboard (KPIs), 6) Relatórios (export, `openpyxl` planned), 7) integrations/Hub expansion.

The project is early-stage: most UI pages are placeholder widgets with just a title label, and only the "create return" write path exists in the repository layer (no read/update/delete yet). Current sprint: implement Recebimento end-to-end — `NovaDevolucaoPage` form (número do pedido, plataforma, cliente, SKU, produto, responsável pelo recebimento, observações) → validation → a new Controller layer (doesn't exist yet) → `Devolucao` → `DevolucaoRepository` → SQLite, auto-setting `status = "Recebida"` and `data_recebimento = now`.

## Commands

There is no build system, linter, formatter, or test suite configured yet (no `pytest`, no `pyproject.toml`, no CI). When adding tooling, check with the user first since none currently exists.

```bash
# Set up environment (venv already exists at .venv/)
source .venv/bin/activate
pip install -r requirements.txt

# Run the app
python main.py
```

Running `main.py` calls `create_tables()` on startup, which creates `database/logos.db` (a SQLite file) and the `devolucoes` table if they don't already exist. The DB file is gitignored (`*.db`).

## Architecture

Layered structure, small but intentional:

- **`main.py`** — entry point. Initializes the DB schema, then boots the `QApplication` and shows `MainWindow`.
- **`database/`** — raw SQLite access.
  - `connection.py`: `get_connection()` opens a sqlite3 connection to `database/logos.db` (path resolved relative to repo root) with `row_factory = sqlite3.Row`.
  - `schema.py`: `create_tables()` — idempotent `CREATE TABLE IF NOT EXISTS` DDL. This is the single source of truth for the DB schema; there is no migration framework, so schema changes are made by editing the `CREATE TABLE` statement directly (and, since it's `IF NOT EXISTS`, existing local `.db` files won't pick up column changes — delete the local `.db` to pick up schema edits during development).
- **`app/models/`** — plain `@dataclass` models mirroring DB tables (e.g. `Devolucao` mirrors the `devolucoes` table 1:1, including a `data_criacao`/`data_atualizacao` audit pair).
- **`app/repositories/`** — data access objects that translate between models and SQL. Each method opens its own connection via `get_connection()` and closes it before returning (no shared/pooled connection, no ORM). Follow this per-call-connection pattern for new repository methods.
- **`app/ui/`** — one `QWidget` subclass per page (`DashboardPage`, `NovaDevolucaoPage`, `ConsultaPage`, `RecebimentoPage`, `RelatoriosPage`, `ConfiguracoesPage`), plus `MainWindow`, which owns a `QStackedWidget` and switches between pages. `MainWindow` currently builds the side menu and page instances directly in `__init__`; there's no router/navigation abstraction — new pages are wired in by constructing the widget and calling `conteudo.addWidget(...)`.

### Data flow

Target layering is UI → Controllers → Repositories → SQLite, with a Services layer reserved for once business rules (e.g. the ESTOQUE/TROCA/DESCARTE decision logic) get more complex. Only UI → Repository → SQLite exists today — `app/controllers/` and `app/services/` haven't been created yet and are expected to appear as the Recebimento flow (and later steps) get built out. Repository methods should not be called directly from UI code going forward; route new writes through a controller.

A broader target directory layout was agreed with the user (not all present yet): `app/{assets,controllers,models,repositories,services,ui,utils}/`, plus top-level `config/`, `docs/`, `logs/`, `reports/`, `tests/`. Create these lazily as needed rather than scaffolding them upfront.
