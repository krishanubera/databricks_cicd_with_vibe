# GitHub Actions

Each workflow has its **own** `workflow_dispatch` (manual **Run workflow** in the Actions UI). There are two separate workflows → two manual entry points.

| Workflow | File | When it runs |
|----------|------|----------------|
| **Deploy app bundle** | `databricks-app.yml` | **Manual** (workflow_dispatch), or push `feature_*` / `release_*`, or PRs to `release_*` |
| **Deploy Unity Catalog bundle** | `unity-catalog.yml` | **Manual** (workflow_dispatch), or push/PR when **`bundles/unity-catalog/**`** changes (same branch rules) |

**Where to run manually:** **Actions** → left sidebar → open **Deploy app bundle** or **Deploy Unity Catalog bundle** → green **Run workflow** → pick branch and environment.

Secrets (both workflows): `DATABRICKS_DEV_*`, `DATABRICKS_TEST_*`, `DATABRICKS_PROD_*` (host + token per environment).

- **Unity Catalog bundle** — validates and deploys [`bundles/unity-catalog`](../../bundles/unity-catalog) (`databricks_cicd_with_vibe_uc`): catalog `cicd_with_vibe`, schema `diagnostics`, managed volume `diagnostics_data`. Sets `DATABRICKS_BUNDLE_ENGINE=direct` (required for catalog resources). Uses `defaults.run.working-directory: bundles/unity-catalog` for CLI commands.
- **App bundle** — deploys the root bundle and uploads `data/*.csv` to `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data`. For a **new** workspace, run the UC workflow first so the volume exists.
