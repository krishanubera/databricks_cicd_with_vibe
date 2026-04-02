# Databricks CI/CD with Vibe Coding

This repository is a **hands-on demo** of **vibe coding in Cursor** to produce a **Lakeflow Spark Declarative Pipeline** defined as a **Databricks Asset Bundle (DAB)**, then **deploying** it with **GitHub Actions**. The workflow **deploys the bundle and uploads CSVs to a volume**; it does **not** run the pipeline in CI by default—you **refresh the pipeline manually** in the workspace when you want to materialize tables.

**Session deck:** [docs/demo-session.md](docs/demo-session.md)

Documentation in this repo covers the demo story and setup only; it does **not** change application bundle YAML, Python, or workflow files.

## What is Vibe Coding?

Vibe coding is an iterative, AI-assisted development style where you describe what you want in natural language and work alongside an AI assistant (like Cursor) to implement it. You focus on intent, structure, and review—letting the AI suggest code, config, and fixes while you steer the outcome.

## What This Repo Demonstrates

End-to-end flow:

1. **Cursor** – Natural-language iteration to design and evolve the bundle and pipeline as code.
2. **Databricks Asset Bundles** – Jobs, pipelines, and related resources defined in YAML and deployed to a workspace.
3. **GitHub Actions** – **Deploy app bundle** validates, deploys, and uploads `data/*.csv` to the configured volume path (see [.github/workflows/README.md](.github/workflows/README.md)).

Together: **vibe code in Cursor** → **commit** → **Actions: validate + deploy + CSV upload** → **manual pipeline refresh** in Databricks to load data into Unity Catalog.

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

## Project Structure

The **demo** centers on the **pipeline resource YAML** under `resources/pipelines/` and the **pipeline Python** module under the designated `src/…` path (see deploy notes for relative path examples).

| Path | Bundle name | Purpose |
|------|-------------|---------|
| **`databricks.yml`** (root) | `databricks_cicd_with_vibe` | Bundle root; includes `resources/` |

```
databricks_cicd_with_vibe/
├── databricks.yml              # App bundle
├── docs/
│   └── demo-session.md         # Session presentation (this demo)
├── resources/
│   ├── jobs/
│   ├── pipelines/              # Pipeline bundle YAML (e.g. diagnostics pipeline)
│   └── …
├── .github/workflows/
│   ├── README.md
│   └── databricks-app.yml      # Validate + deploy; upload data/*.csv (no pipeline run)
├── data/                       # CSV files (e.g. lab_results.csv) for the upload step
├── src/                        # Pipeline Python and other source layout
└── tests/
```

## Prerequisites

- **Cursor** – [cursor.com](https://cursor.com)
- **Databricks workspace** – and a personal or service principal token for the CLI
- **Databricks CLI** – `databricks bundle` support (`databricks bundle -h`)
- **GitHub** – Actions enabled; **Environments** configured (see below)

## Quick Start

1. **Clone and open in Cursor**
   ```bash
   git clone <your-repo-url>
   cd databricks_cicd_with_vibe
   cursor .
   ```

2. **Configure the bundle** – Root [`databricks.yml`](databricks.yml) and files under `resources/` (including `resources/pipelines/`).

3. **Validate locally**
   ```bash
   databricks bundle validate -t dev --profile <your-profile>
   ```

4. **Deploy via GitHub Actions** – **Deploy app bundle** on `feature_*` / `release_*` pushes or PRs to `release_*`, or run manually (see [.github/workflows/README.md](.github/workflows/README.md)).

## GitHub Actions setup

The **Deploy app bundle** workflow uses a **GitHub Environment** per bundle target (`dev`, `test`, `prod`). For each environment, configure:

| Setting | Type | Purpose |
|---------|------|---------|
| `DATABRICKS_HOST` | Environment **variable** | Workspace URL (e.g. `https://xxx.cloud.databricks.com`) |
| `DATABRICKS_TOKEN` | Environment **secret** | Personal access token or service principal token |

Create the **dev**, **test**, and **prod** environments before runs that resolve to each target. Details: [.github/workflows/README.md](.github/workflows/README.md).

### What CI does (and does not do)

- **Does:** `databricks bundle validate`, `databricks bundle deploy`, and upload of `data/*.csv` to `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data`.
- **Does not:** Run the pipeline (`bundle run` / pipeline refresh) unless you add that explicitly to the workflow.

After deploy, start a **pipeline refresh** in the workspace when you want to materialize **`cicd_with_vibe.diagnostics.lab_results`** (or the table name your bundle defines). **Create the catalog, schema, and managed volume in Unity Catalog yourself** (or align bundle paths/catalog with your environment).

### Deploy notes

- **Shared bundle path** (`/Workspace/Shared/.bundle/...`): the bundle sets `permissions` for `users` with `CAN_MANAGE` to match Databricks’ recommendation when using `/Shared`. For a stricter path, use a user-scoped `root_path` (see [bundle deployment modes](https://docs.databricks.com/en/dev-tools/bundles/deployment-modes.html)).
- **`--auto-approve`**: GitHub Actions runs `databricks bundle deploy ... --auto-approve` so the job does not hang. For local CLI, add `--auto-approve` when you intend to apply the deploy without confirmation.
- **Databricks CLI version**: [Develop pipelines with Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/pipelines-tutorial.html) requires **Databricks CLI 0.283.0 or above** for Lakeflow Spark Declarative Pipelines. This repo’s workflow pins a compatible CLI; locally, run `databricks -v` and upgrade if needed.
- **Finding the pipeline**: After deploy, use **Jobs & Pipelines** / **Pipelines** and look for **`diagnostics_lab_results_pipeline`**. The deploy job prints **`databricks bundle summary`** and **`databricks pipelines list-pipelines`**. Pipeline definitions live under **`resources/pipelines/`** (e.g. **`diagnostics_lab_results_pipeline.yml`**). Root [`databricks.yml`](databricks.yml) uses **`include: resources/*.yml`** and **`resources/pipelines/*.yml`** (single-level globs); avoid **`resources/pipelines/**/*.yml`** here if you hit deploy `Rel` errors ([CLI issue #4831](https://github.com/databricks/cli/issues/4831)). For pipeline `libraries` `file.path` in **included** YAML, paths resolve **relative to that YAML file** ([Databricks CLI PR #3225](https://github.com/databricks/cli/pull/3225)). From `resources/pipelines/`, use **`../../src/pipelines/...`**; from `resources/`, use **`../src/pipelines/...`**.
- **Serverless pipelines and edition**: **Advanced** edition is required when `serverless: true`. If your workspace does not include Lakeflow Advanced, enable it or use **classic compute** (`serverless: false` and a `clusters` block per the [bundle pipeline resource](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#pipeline)).

## Vibe coding with Cursor

- **Describe the outcome** – e.g. the session demo prompt above.
- **Point at the bundle** – `databricks.yml`, `resources/pipelines/`, `resources/jobs/`.
- **Iterate** – retries, policies, or pipeline tweaks in conversation.
- **Let CI deploy** – Push and rely on **Deploy app bundle** for validate + deploy + CSV upload.

## Resources

- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- [Cursor](https://cursor.com)

## License

Use and adapt as needed for your organization.
