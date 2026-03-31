# Databricks CI/CD with Vibe Coding

This project showcases how **Cursor** can be used for **vibe coding** together with **Databricks Asset Bundles (DAB)** and **GitHub Actions** to build and deploy Databricks workloads.

## What is Vibe Coding?

Vibe coding is an iterative, AI-assisted development style where you describe what you want in natural language and work alongside an AI assistant (like Cursor) to implement it. Instead of writing every line by hand, you focus on intent, structure, and review—letting the AI suggest code, config, and fixes while you steer the outcome.

## What This Repo Demonstrates

- **Cursor** – Using Cursor’s AI features to design and evolve Databricks bundles, notebooks, jobs, and pipelines through conversation and inline edits.
- **Databricks Asset Bundles (DAB)** – Defining Databricks resources (jobs, pipelines, notebooks, etc.) as code in a bundle that can be validated and deployed.
- **GitHub Actions** – **Deploy app bundle** (see `.github/workflows/README.md`).

Together, this gives you a workflow where you can “vibe code” your Databricks assets in Cursor and have them automatically validated and deployed via GitHub Actions.

## Project Structure

| Path | Bundle name | Purpose |
|------|-------------|---------|
| **`databricks.yml`** (root) | `databricks_cicd_with_vibe` | Jobs, pipelines, notebooks (`resources/`) |

```
databricks_cicd_with_vibe/
├── databricks.yml              # App bundle
├── resources/
│   ├── README.md
│   ├── jobs/
│   ├── pipelines/
│   └── …
├── .github/workflows/
│   ├── README.md
│   └── databricks-app.yml      # Deploy app + upload data/*.csv
├── data/                       # CSV files for upload step (path configured in workflow)
├── src/
└── tests/
```

## Prerequisites

- **Cursor** – [cursor.com](https://cursor.com)
- **Databricks workspace** – and a personal or service principal token for the CLI
- **Databricks CLI** – `databricks` CLI with Asset Bundles support (`databricks bundle -h`)
- **GitHub** – repo with Actions enabled and secrets (see below)

## Quick Start

1. **Clone and open in Cursor**
   ```bash
   git clone <your-repo-url>
   cd databricks_cicd_with_vibe
   cursor .
   ```

2. **Configure the bundle**  
   Root `databricks.yml` + `resources/` (jobs, pipelines, …).

3. **Validate locally**
   ```bash
   databricks bundle validate -t dev --profile <your-profile>
   ```

4. **Deploy via GitHub Actions**  
   **Deploy app bundle** — on `feature_*` / `release_*` pushes (see workflow), or run manually.

## GitHub Actions Setup

Add these **repository secrets** (host + token per workspace):

| Secret | Purpose |
|--------|---------|
| `DATABRICKS_DEV_HOST` / `DATABRICKS_DEV_TOKEN` | Dev |
| `DATABRICKS_TEST_HOST` / `DATABRICKS_TEST_TOKEN` | Test |
| `DATABRICKS_PROD_HOST` / `DATABRICKS_PROD_TOKEN` | Prod |

The workflow uploads `data/*.csv` to `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data` and deploys the bundle (including the `diagnostics_lab_results_pipeline` Lakeflow Declarative Pipeline definition). It does **not** trigger a pipeline run; start a refresh in the workspace when you want to materialize `cicd_with_vibe.diagnostics.lab_results`. **Create the catalog, schema, and managed volume in Unity Catalog yourself** (or change paths/catalog in bundle resources to match your environment).

### Deploy notes

- **Shared bundle path** (`/Workspace/Shared/.bundle/...`): the bundle sets `permissions` for `users` with `CAN_MANAGE` to match Databricks’ recommendation when using `/Shared`. For a stricter path, use a user-scoped `root_path` (see [bundle deployment modes](https://docs.databricks.com/en/dev-tools/bundles/deployment-modes.html)).
- **`--auto-approve`**: GitHub Actions runs `databricks bundle deploy ... --auto-approve` so the job does not hang (no interactive prompt). For local CLI, add `--auto-approve` when you intend to apply the deploy without confirmation.
- **Databricks CLI version**: [Develop pipelines with Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/pipelines-tutorial.html) requires **Databricks CLI 0.283.0 or above** for Lakeflow Spark Declarative Pipelines. Older CLIs can sync workspace files while not creating pipeline resources as expected. This repo’s GitHub workflow pins a compatible CLI; for local deploys, run `databricks -v` and upgrade if needed.
- **Finding the pipeline**: After deploy, use the sidebar **Jobs & Pipelines** (or **Workflows** → **Pipelines**, depending on workspace UI), apply the **Pipelines** filter, and look for **`diagnostics_lab_results_pipeline`**. The deploy job prints **`databricks bundle summary`** and **`databricks pipelines list-pipelines`** so you can confirm the pipeline exists in the workspace API (if the list does not include it, the UI will not show it either). The pipeline is defined under **`resources.pipelines`** in **`databricks.yml`** so `libraries` paths are relative to the **bundle root** (for example `src/pipelines/...`).

## Vibe Coding with Cursor

- **Describe the outcome**: e.g. “I need a job that runs at 2am and runs this notebook with these parameters.”
- **Point at the bundle**: Reference `databricks.yml`, `resources/jobs/`, or pipeline definitions.
- **Iterate**: Ask for “add retries,” “use a different cluster policy,” or “add a DLT pipeline.”
- **Let CI check**: Push your changes and use **Deploy app bundle**.

## Resources

- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- [Cursor](https://cursor.com)

## License

Use and adapt as needed for your organization.
