# Unity Catalog bundle

This bundle declares **Unity Catalog** objects used by the root app workflow’s CSV upload:

- **Catalog** `cicd_with_vibe`
- **Schema** `diagnostics`
- **Managed volume** `diagnostics_data` → `dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data`

The app bundle at the repo root does **not** include these resources so UC and app lifecycles stay independent.

## Prerequisites

- **Databricks CLI** with bundles support (`databricks bundle -h`), **≥ 0.236.0** recommended for volume resources.
- **Direct deployment engine** — required for `catalogs` in bundles. Set before validate/deploy:
  - **PowerShell:** `$env:DATABRICKS_BUNDLE_ENGINE = "direct"`
  - **bash:** `export DATABRICKS_BUNDLE_ENGINE=direct`
- **Permissions** — the identity running deploy needs rights to create catalogs/schemas/volumes (often metastore admin or equivalent in your account). Grant failures are usually workspace policy, not YAML.

## Local commands

From this directory (`bundles/unity-catalog`):

```bash
databricks bundle validate -t dev --profile <profile>
databricks bundle deploy -t dev --profile <profile> --auto-approve
```

Use targets `test` or `prod` to match your workspaces.

## Deploy order

For a **new** workspace, deploy **this bundle first** (or run the **Deploy Unity Catalog bundle** GitHub workflow), then deploy the app bundle so the volume path exists before `data/*.csv` upload.
