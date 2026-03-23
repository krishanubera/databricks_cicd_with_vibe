# GitHub Actions

| Workflow | File | When it runs |
|----------|------|----------------|
| **Deploy app bundle** | `databricks-app.yml` | Push `feature_*` / `release_*`, PRs to `release_*`, or manual dispatch |

Secrets: `DATABRICKS_DEV_*`, `DATABRICKS_TEST_*`, `DATABRICKS_PROD_*` (host + token per environment).

The workflow deploys the root bundle and uploads `data/*.csv` to the configured `dbfs:/Volumes/...` path (ensure that volume exists in your workspace).
