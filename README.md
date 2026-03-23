# Databricks CI/CD with Vibe Coding

This project showcases how **Cursor** can be used for **vibe coding** together with **Databricks Asset Bundles (DAB)** and **GitHub Actions** to build and deploy Databricks workloads.

## What is Vibe Coding?

Vibe coding is an iterative, AI-assisted development style where you describe what you want in natural language and work alongside an AI assistant (like Cursor) to implement it. Instead of writing every line by hand, you focus on intent, structure, and review—letting the AI suggest code, config, and fixes while you steer the outcome.

## What This Repo Demonstrates

- **Cursor** – Using Cursor’s AI features to design and evolve Databricks bundles, notebooks, jobs, and pipelines through conversation and inline edits.
- **Databricks Asset Bundles (DAB)** – Defining Databricks resources (jobs, pipelines, notebooks, etc.) as code in a bundle that can be validated and deployed.
- **GitHub Actions** – **Deploy app bundle** and **Deploy Unity Catalog bundle** (see `.github/workflows/README.md`).

Together, this gives you a workflow where you can “vibe code” your Databricks assets in Cursor and have them automatically validated and deployed via GitHub Actions.

## Project Structure

| Path | Bundle name | Purpose |
|------|-------------|---------|
| **`databricks.yml`** (root) | `databricks_cicd_with_vibe` | Jobs, pipelines, notebooks (`resources/`) |
| **`bundles/unity-catalog/databricks.yml`** | `databricks_cicd_with_vibe_uc` | Unity Catalog: catalog, schema, volume for CSV uploads |

```
databricks_cicd_with_vibe/
├── databricks.yml              # App bundle
├── bundles/
│   └── unity-catalog/          # UC bundle (separate from app)
│       ├── databricks.yml
│       ├── README.md
│       └── resources/
├── resources/
│   ├── README.md
│   ├── jobs/
│   ├── pipelines/
│   └── …
├── .github/workflows/
│   ├── README.md
│   ├── databricks-app.yml      # Deploy app + upload data/*.csv
│   └── unity-catalog.yml       # Deploy UC bundle only
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

   For the Unity Catalog bundle (from `bundles/unity-catalog`), set `DATABRICKS_BUNDLE_ENGINE=direct` and use the same command there (see [`bundles/unity-catalog/README.md`](bundles/unity-catalog/README.md)).

4. **Deploy via GitHub Actions**  
   - **Deploy Unity Catalog bundle** — when `bundles/unity-catalog/**` changes on `feature_*` / `release_*`, or run manually. Use this **before** (or once prior to) the app workflow if the volume does not exist yet.  
   - **Deploy app bundle** — on `feature_*` / `release_*` pushes (see workflow), or run manually.

## GitHub Actions Setup

Add these **repository secrets** (host + token per workspace):

| Secret | Purpose |
|--------|---------|
| `DATABRICKS_DEV_HOST` / `DATABRICKS_DEV_TOKEN` | Dev |
| `DATABRICKS_TEST_HOST` / `DATABRICKS_TEST_TOKEN` | Test |
| `DATABRICKS_PROD_HOST` / `DATABRICKS_PROD_TOKEN` | Prod |

The workflow uploads `data/*.csv` to `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data`. **Create that path** by deploying the **`bundles/unity-catalog`** bundle (CLI or **Deploy Unity Catalog bundle** workflow) before relying on the upload step in a new workspace.

### Deploy notes

- **Shared bundle path** (`/Workspace/Shared/.bundle/...`): each bundle sets `permissions` for `users` with `CAN_MANAGE` to match Databricks’ recommendation when using `/Shared`. For a stricter path, use a user-scoped `root_path` (see [bundle deployment modes](https://docs.databricks.com/en/dev-tools/bundles/deployment-modes.html)).
- **Destructive UC actions / `--auto-approve`**: if a previous deploy created Unity Catalog resources (catalogs, schemas, volumes) that are **no longer** in the UC bundle, the next UC bundle deploy may **delete** them to match the bundle. GitHub Actions runs `databricks bundle deploy ... --auto-approve` so the job does not hang. For local CLI: add `--auto-approve` when you intend to apply that sync (or manage UC only in the workspace and keep it out of the bundle).

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
