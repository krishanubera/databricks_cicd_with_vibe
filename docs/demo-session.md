# Cursor, vibe coding, and CI/CD for Databricks ETL

**Session purpose:** Show how to use **Cursor** to develop **Databricks ETL** processes through **vibe coding** (iterative, AI-assisted development), then **package and deploy** that code into Databricks environments using **Databricks Asset Bundles** and **GitHub Actions**.

**Hands-on demo:** Lakeflow Spark Declarative Pipelines as the ETL example.

---

## Agenda

- Session goals: develop with Cursor → ship with bundles and CI
- What vibe coding means here
- End-to-end flow: Cursor → Git → GitHub Actions → Databricks
- Demo goal: pipeline from volume CSV to diagnostics table
- The demo prompt and constraints
- Repo layout and what CI does
- After deploy: refresh and Q&A

---

## Session goals (two parts)

### 1. Develop ETL with Cursor (vibe coding)

- Use **natural language** in Cursor to shape pipelines, bundle config, and Python
- **Iterate quickly**: describe outcomes, review generated code, steer until it matches your data and standards
- Typical artifacts: `databricks.yml`, pipeline YAML under `resources/pipelines/`, ETL logic in `src/`

### 2. Package and deploy with Databricks Asset Bundles + GitHub Actions

- **Databricks Asset Bundles** define the deployable unit (resources, paths, targets) so the same repo represents what runs in each environment
- **GitHub Actions** automate **validate**, **deploy**, and supporting steps (e.g. uploading seed data to a volume)
- Result: committed code flows from PR/main into a **Databricks workspace** in a repeatable way

---

## What is vibe coding?

- Iterative, AI-assisted development in **Cursor**
- Describe ETL outcomes in natural language; **review and steer** the assistant
- Bundle YAML and Python evolve through conversation until production-ready

---

## End-to-end flow

1. **Cursor** — Vibe coding: natural-language iteration on bundle and ETL/pipeline code
2. **Git repository** — `databricks.yml`, `resources/pipelines/`, `src/`
3. **GitHub Actions** — `bundle validate`, `bundle deploy`, CSV upload to volume
4. **Databricks workspace** — **Manual** pipeline refresh to materialize tables (unless you add automation)

```mermaid
flowchart LR
  Cursor[Cursor_vibe_coding]
  Repo[Git_repo]
  GHA[GitHub_Actions_DAB]
  WS[Databricks_workspace]
  Cursor -->|develop_ETL| Repo
  Repo -->|validate_deploy| GHA
  GHA -->|bundle_deploy_upload| WS
  WS -->|manual_refresh| Table[UC_table]
```

---

## Demo goal

- **Lakeflow Spark Declarative Pipeline** (Databricks Asset Bundle) as a concrete ETL pattern
- Load **`lab_results.csv`** into a table in the **`diagnostics`** schema
- Source file: read from **Unity Catalog volume** (CSV uploaded from `data/` by CI)

---

## Session demo prompt (vibe)

Use this prompt (or equivalent) when driving the live demo in Cursor:

```
Create a Databricks Asset Bundle pipeline from scratch for Lakeflow Spark Declarative Pipelines to load lab_results.csv into a table in the diagnostics schema. The lab result to be taken from the volume.

Constraints
No bundle run in CI unless asked.
use Serverless with advance edition
Keep code minimal: one @dlt.table that loads the CSV once.
Keep the code in py file not notebook
Make sure the yml file config uses 'file' not notebook
keep the py file and yml file in their designated directories in current folder structures.
Define the python code path in yml in so that it resolves the path relative to that YAML file's directory

don't search online
keep the catalog and schema name hardcoded
```

### Constraints (as given to the assistant)

- **No `bundle run` in CI** unless you explicitly ask for it.
- **Serverless** pipeline with **Lakeflow Advanced** edition (required for serverless pipelines).
- **Minimal code:** a single `@dlt.table` that loads the CSV once.
- **Python module (`.py`)**, not a notebook; pipeline `libraries` use **`file`**, not `notebook`, in YAML.
- **Conventional layout:** pipeline bundle YAML under `resources/pipelines/`, pipeline Python under the repo’s `src/…` layout; **`file.path`** in included YAML resolves **relative to that YAML file’s directory** (not the bundle root).
- **No web search** during the demo (assistant should not search online).
- **Catalog and schema names hardcoded** in code as specified for the demo.

---

## Repo layout at a glance

| Area | Role |
|------|------|
| `databricks.yml` | Bundle root (packaging / targets) |
| `resources/pipelines/` | Pipeline resource YAML |
| `src/` | ETL / pipeline Python (paths resolve from pipeline YAML) |
| `data/` | CSV files for workflow upload |
| `.github/workflows/` | Validate, deploy bundle, upload data to volume |

---

## What CI does (and does not)

**Does**

- `databricks bundle validate`
- `databricks bundle deploy`
- Upload `data/*.csv` to the configured volume path

**Does not**

- Run the pipeline or `bundle run` by default

---

## After deploy

- Find the pipeline under **Jobs & Pipelines** / **Pipelines** (e.g. `diagnostics_lab_results_pipeline`)
- Confirm via **`databricks bundle summary`** and **`databricks pipelines list-pipelines`** in the workflow log
- Start a **pipeline refresh** in the workspace to materialize the table

---

## Q&A and links

- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- [Cursor](https://cursor.com)
- [POC walkthrough](vibe-coding-databricks-bundle-poc.md)

---

*Session notes — see root [README.md](../README.md) for fork/setup and GitHub Actions configuration.*
