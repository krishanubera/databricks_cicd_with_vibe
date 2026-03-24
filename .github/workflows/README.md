# GitHub Actions

| Workflow | File | When it runs |
|----------|------|----------------|
| **Deploy app bundle** | `databricks-app.yml` | **Manual** (workflow_dispatch), or push `feature_*` / `release_*`, or PRs to `release_*` |

**Manual run:** **Actions** → **Deploy app bundle** → **Run workflow** → pick branch and environment.

Secrets: `DATABRICKS_DEV_*`, `DATABRICKS_TEST_*`, `DATABRICKS_PROD_*` (host + token per environment).

The workflow deploys the root bundle and uploads `data/*.csv` to `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data`. **Create the catalog, schema, and managed volume in Unity Catalog yourself** (or match that path) so the upload step can write files.
