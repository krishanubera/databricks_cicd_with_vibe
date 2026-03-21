# Databricks CI/CD with Vibe Coding

This project showcases how **Cursor** can be used for **vibe coding** together with **Databricks Asset Bundles (DAB)** and **GitHub Actions** to build and deploy Databricks workloads.

## What is Vibe Coding?

Vibe coding is an iterative, AI-assisted development style where you describe what you want in natural language and work alongside an AI assistant (like Cursor) to implement it. Instead of writing every line by hand, you focus on intent, structure, and review—letting the AI suggest code, config, and fixes while you steer the outcome.

## What This Repo Demonstrates

- **Cursor** – Using Cursor’s AI features to design and evolve Databricks bundles, notebooks, jobs, and pipelines through conversation and inline edits.
- **Databricks Asset Bundles (DAB)** – Defining Databricks resources (jobs, pipelines, notebooks, etc.) as code in a bundle that can be validated and deployed.
- **GitHub Actions** – Automating validation, testing, and deployment of the bundle on push or pull request (e.g., `databricks bundle validate`, `databricks bundle deploy`).

Together, this gives you a workflow where you can “vibe code” your Databricks assets in Cursor and have them automatically validated and deployed via GitHub Actions.

## Project Structure (Option A – bundle at repo root)

```
databricks_cicd_with_vibe/
├── README.md                 # This file
├── databricks.yml            # Bundle configuration (main entry)
├── .github/
│   └── workflows/
│       └── databricks-bundle.yml   # GitHub Actions validate/deploy
├── resources/
│   ├── jobs/                 # Job definitions (*.yml)
│   ├── pipelines/           # DLT pipeline definitions
│   ├── apps/                 # App definitions
│   ├── models/               # Model definitions
│   └── catalogs/             # Unity Catalog (catalogs, schemas, etc.)
├── src/
│   ├── notebooks/            # Notebooks used by jobs/pipelines
│   └── python/               # Shared Python modules
└── tests/                    # Local unit tests
```

## Prerequisites

- **Cursor** – [cursor.com](https://cursor.com)
- **Databricks workspace** – and a personal or service principal token for the CLI
- **Databricks CLI** – `databricks` CLI with Asset Bundles support (`databricks bundle -h`)
- **GitHub** – repo with Actions enabled and secrets for your Databricks host and token (and optionally storage/config)

## Quick Start

1. **Clone and open in Cursor**
   ```bash
   git clone <your-repo-url>
   cd databricks_cicd_with_vibe
   cursor .
   ```

2. **Configure the bundle**  
   In Cursor, describe what you need (e.g. “add a job that runs this notebook daily” or “add a pipeline for this DLT flow”). Use the bundle’s `databricks.yml` and `resources/` so the AI can suggest or edit the right YAML and code.

3. **Validate locally**
   ```bash
   databricks bundle validate -t dev --profile <your-profile>
   ```

4. **Deploy via GitHub Actions**  
   Push to your branch; the workflow can run `databricks bundle validate` and optionally `databricks bundle deploy` (e.g. to dev on PR, to prod on merge to main).

## Unity Catalog

The bundle deploys the **`diagnostics`** schema in catalog **`cicd_with_vibe`**. Create the catalog **once** in your workspace (Data Explorer UI with Default Storage, or `CREATE CATALOG ... MANAGED LOCATION '...'`). The bundle does **not** create the catalog, because API-created catalogs often need an explicit managed location when your metastore has no default storage root.

## GitHub Actions Setup

The workflow deploys to **three bundle targets** (`dev`, `test`, `prod`), each intended to use a **different Databricks workspace**. Add these **repository secrets** (host + personal access token per workspace):

| Secret | Purpose |
|--------|---------|
| `DATABRICKS_DEV_HOST` | Dev workspace URL, e.g. `https://<dev-workspace>.cloud.databricks.com` |
| `DATABRICKS_DEV_TOKEN` | Token for dev workspace |
| `DATABRICKS_TEST_HOST` | Test workspace URL |
| `DATABRICKS_TEST_TOKEN` | Token for test workspace |
| `DATABRICKS_PROD_HOST` | Production workspace URL |
| `DATABRICKS_PROD_TOKEN` | Token for production workspace |

Create the Unity Catalog catalog (e.g. `cicd_with_vibe`) in **each** workspace if you deploy bundle resources there.

Your workflow runs `databricks bundle validate` / `deploy` with the target that matches the branch or manual choice (see `.github/workflows/databricks-bundle.yml`).

## Vibe Coding with Cursor

- **Describe the outcome**: e.g. “I need a job that runs at 2am and runs this notebook with these parameters.”
- **Point at the bundle**: Reference `databricks.yml`, `resources/jobs/`, or pipeline definitions so Cursor can propose concrete YAML and Python/SQL.
- **Iterate**: Ask for “add retries,” “use a different cluster policy,” or “add a DLT pipeline” and apply the suggested changes.
- **Let CI check**: Push your changes and use GitHub Actions to validate and deploy, so the bundle stays consistent and deployable.

## Resources

- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- [Cursor](https://cursor.com)

## License

Use and adapt as needed for your organization.
