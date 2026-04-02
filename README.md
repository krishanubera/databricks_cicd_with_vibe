# Databricks CI/CD with Vibe Coding

This repository is a **hands-on demo** of **vibe coding in Cursor** to produce a **Lakeflow Spark Declarative Pipeline** defined as a **Databricks Asset Bundle (DAB)**, then **deploying** it with **GitHub Actions**. The workflow **deploys the bundle and uploads CSVs to a volume**; it does **not** run the pipeline in CI by default—you **refresh the pipeline manually** in the workspace when you want to materialize tables.

**Session deck:** [docs/demo-session.md](docs/demo-session.md) · **POC walkthrough:** [docs/vibe-coding-databricks-bundle-poc.md](docs/vibe-coding-databricks-bundle-poc.md)

This repo is **public** so you can **fork** it and run the flow in your own GitHub account. Documentation here covers the demo story and setup only; it does **not** change application bundle YAML, Python, or workflow files.

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
├── LICENSE                     # MIT
├── databricks.yml              # App bundle
├── docs/
│   ├── demo-session.md         # Session presentation (this demo)
│   └── vibe-coding-databricks-bundle-poc.md  # Casual POC walkthrough
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
- **GitHub** – A **fork** of this repo (recommended), Actions enabled, and **Environments** with variables/secrets (see [GitHub Actions setup](#github-actions-setup))

## Quick Start

1. **Fork this repo (recommended), then clone your fork and open it in Cursor**
   ```bash
   git clone <your-fork-url>
   cd databricks_cicd_with_vibe
   cursor .
   ```
   Working from a **fork** keeps your tokens, branches, and workflow runs under your GitHub account. You can use a single branch on the fork (for example `feature_your_poc`) instead of contributing back to the upstream repo.

2. **Configure GitHub Environments** (needed before Actions can deploy)—see [GitHub Actions setup](#github-actions-setup) below.

3. **Configure the bundle** – Root [`databricks.yml`](databricks.yml) and files under `resources/` (including `resources/pipelines/`).

4. **Validate locally**
   ```bash
   databricks bundle validate -t dev --profile <your-profile>
   ```

5. **Deploy via GitHub Actions** – **Deploy app bundle** on `feature_*` / `release_*` pushes or PRs to `release_*`, or run manually (see [.github/workflows/README.md](.github/workflows/README.md)).

## GitHub Actions setup

The **Deploy app bundle** workflow reads **Databricks host and token** from **GitHub Environment** configuration—not from repository-level secrets alone. You need **one GitHub Environment per bundle target** the workflow will use: **`dev`**, **`test`**, and **`prod`** (names must match; the job sets `environment: ${{ needs.resolve.outputs.target }}`).

### Add each environment, variable, and secret

For **each** of `dev`, `test`, and `prod` that you plan to use:

1. In GitHub, open **your fork** (or repo) → **Settings** → **Environments**.
2. Click **New environment**, enter the name **`dev`**, **Save** (repeat for **`test`** and **`prod`** if you need them).
3. Open the environment (e.g. **`dev`**).
4. Under **Environment variables**, **Add environment variable**:
   - **Name:** `DATABRICKS_HOST`
   - **Value:** your Databricks workspace URL, e.g. `https://dbc-xxxxxxxx.cloud.databricks.com` (no trailing slash unless your org standardizes it—use the host your CLI uses).
5. Under **Environment secrets**, **Add secret**:
   - **Name:** `DATABRICKS_TOKEN`
   - **Value:** a personal access token or service principal token with rights to deploy bundles and upload files to the paths your workflow uses.

Repeat steps 3–5 for **`test`** and **`prod`** if those targets should deploy to different workspaces or credentials.

Optional: add **deployment protection rules** (required reviewers, wait timers) per environment if your org requires them.

Summary:

| Setting | Where | Type |
|---------|--------|------|
| `DATABRICKS_HOST` | Environment **variables** | Workspace URL |
| `DATABRICKS_TOKEN` | Environment **secrets** | PAT or service principal token |

More on when the workflow runs: [.github/workflows/README.md](.github/workflows/README.md).

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

This project is licensed under the [MIT License](LICENSE). You may use, copy, modify, and distribute the code and documentation under those terms.
