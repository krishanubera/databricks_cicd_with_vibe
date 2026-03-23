# Unity Catalog bundle (`databricks_cicd_uc`)

Defines UC resources that are deployed **before** the app bundle in CI (volume path, future grants, etc.).

- **Deploy (local):** `cd bundles/unity-catalog && databricks bundle deploy -t dev --profile <profile>`
- **Validate:** `databricks bundle validate -t dev`
- **Engine:** set `DATABRICKS_BUNDLE_ENGINE=direct` for UC resources (GitHub Actions sets this).

App jobs/pipelines live in the **repo root** bundle (`databricks_cicd_with_vibe`).
