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

## Troubleshooting

| Symptom | What to check |
|--------|----------------|
| **Catalog exists but schema/volume missing** | Open the workflow log for **Deploy Unity Catalog bundle** and search for `Error` / `FAILED`. Invalid **volume** grant privileges (e.g. `READ_FILES` instead of `READ_VOLUME`) can cause the volume step to fail. This bundle uses `READ_VOLUME` / `WRITE_VOLUME` per the [bundles volume schema](https://databricks.github.io/cli/python/databricks.bundles.volumes.html). |
| **Grants fail on `users`** | Some accounts use a different default group name. Temporarily remove `grants:` blocks in `resources/uc.yml`, redeploy, then add grants in the Catalog UI or SQL. |
| **Nothing created** | Confirm `DATABRICKS_BUNDLE_ENGINE=direct` and CLI **≥ 0.236.0** for volumes. The deploy identity needs UC rights to create a catalog (often metastore admin or `CREATE CATALOG`). |
| **Re-run after fixing YAML** | Run **Deploy Unity Catalog bundle** again (or `databricks bundle deploy ... --auto-approve` locally). |
