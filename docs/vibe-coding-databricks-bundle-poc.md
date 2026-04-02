# From a single prompt to a deployed pipeline: vibe coding with Databricks Asset Bundles and GitHub Actions

*A practical walkthrough for running a proof of concept with Cursor, Lakeflow Spark Declarative Pipelines, and CI/CD—without treating the pipeline run as part of CI unless you want it.*

---

If your team is exploring **AI-assisted development** on top of **Databricks**, the natural question is whether you can go from “describe the outcome” to “something running in a workspace” in one sitting—and still keep **infrastructure as code**, **reviewable diffs**, and a path to **automated deploys**.

This repository is **public** so you can **fork** it and run everything under your own GitHub account. You use **Cursor** (or a similar assistant) to **vibe code**: you give a structured prompt, iterate on the bundle and pipeline code, then **push** so **GitHub Actions** can **validate** and **deploy** a **Databricks Asset Bundle**. The workflow also **uploads CSVs** from `data/` to a **Unity Catalog volume** path so your pipeline can read **`lab_results.csv`** (or your own files) the same way you would in a real project.

Here’s what follows:

- What you’re actually proving in a POC (short version).
- **Step-by-step** instructions using the **session demo prompt** from the README.
- A clear **GitHub Environment + variable + secret** section (you’ll need this before deploy works).
- Pointers to the **[README](../README.md)** for CLI versions, path rules, and edge cases.

---

## What you are proving in the POC

In one sentence: **natural-language intent → bundle + pipeline as code → automated deploy + data on a volume → manual pipeline refresh in Databricks.**

| Layer | What the POC validates |
|--------|-------------------------|
| **Vibe coding** | You can steer an assistant with constraints (minimal DLT table, `.py` not notebook, `file` in YAML, paths relative to pipeline YAML, hardcoded catalog/schema for the demo). |
| **Databricks Asset Bundles** | Lakeflow Spark Declarative Pipeline resources live in Git and deploy with `databricks bundle deploy`. |
| **GitHub Actions** | CI **validates** and **deploys** the bundle and **uploads** CSVs; it does **not** run the pipeline by default (aligns with “no bundle run in CI unless asked”). |
| **Operations** | After deploy, a human triggers a **pipeline refresh** when you are ready to materialize tables—mirroring how many teams separate “ship definition” from “run now.” |

That’s enough for a **time-boxed POC** with stakeholders: prompt, repo layout, Action run, pipeline in the workspace.

---

## Prerequisites

Before you start:

1. **Cursor** (or another AI-capable editor).
2. A **Databricks workspace** with **Unity Catalog**, and entitlements that match what you deploy—for **serverless** Lakeflow pipelines, **Lakeflow Advanced** is required (see the README deploy notes).
3. **Databricks CLI** with bundle support (`databricks bundle -h`), ideally **0.283.0 or newer** for Lakeflow Spark Declarative Pipelines in bundles.
4. A **GitHub account** and a **fork** of this repo (recommended), with **Actions** enabled on the fork.
5. **GitHub Environments** named **`dev`**, **`test`**, and **`prod`** configured with **`DATABRICKS_HOST`** and **`DATABRICKS_TOKEN`**—see Step 5 below (don’t skip it).

You’ll also need **Unity Catalog objects** that match what the bundle and workflow expect, or you’ll adjust names consistently. The README describes uploading to a volume path under **`cicd_with_vibe`** / **`diagnostics`**; **create the catalog, schema, and managed volume** in UC yourself (or align paths in your fork).

---

## Step 1 — Fork the repo, clone your fork, open in Cursor

**Prefer a fork** over only creating a branch on someone else’s repo: your runs, secrets, and environments stay on **your** GitHub account, which is what you want for a POC.

1. On GitHub, open this **public** repository and click **Fork**. Create the fork under your user or org.
2. Clone **your fork** (not the upstream URL):

```bash
git clone <your-fork-url>
cd databricks_cicd_with_vibe
cursor .
```

Get comfortable with the layout: root **`databricks.yml`**, **`resources/pipelines/`** for pipeline bundle YAML, **`src/`** for pipeline Python, **`data/`** for CSVs the workflow uploads, and **`.github/workflows/`** for CI.

---

## Step 2 — Prepare Unity Catalog (POC baseline)

Your workspace should have:

- A **catalog** and **schema** your pipeline will target (the demo prompt assumes **hardcoded** names in code—keep them consistent with UC).
- A **managed volume** (or equivalent path) where CI can upload **`data/*.csv`**, and where the pipeline reads **`lab_results.csv`**.

The **[README](../README.md)** describes the volume path used by the **Deploy app bundle** workflow (`dbfs:/Volumes/...` style path). Create or align these objects **before** you rely on the upload step and the pipeline read.

---

## Step 3 — Paste the vibe prompt and iterate in Cursor

Open a chat (or composer) in Cursor and use the **session demo prompt** verbatim—the same block as in the README under **“Session demo prompt (vibe)”**:

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

**Practical tips:**

- **Point the assistant** at `databricks.yml` and the intended folders (`resources/pipelines/`, `src/…`) so generated paths match your bundle layout.
- **Review every change**: YAML for the pipeline resource, Python for a single `@dlt.table`, and that **`libraries`** uses **`file`** with a path **relative to the pipeline YAML file’s directory** (not the bundle root).
- If something conflicts with your workspace (catalog name, volume path), **adjust in code** and keep the hardcoded-names rule intentional for the demo.

---

## Step 4 — Validate locally

With your Databricks profile configured:

```bash
databricks bundle validate -t dev --profile <your-profile>
```

Fix validation errors before you rely on CI. The README **Deploy notes** section covers common pitfalls (CLI version, include globs, relative `file.path` resolution).

---

## Step 5 — Add GitHub Environments, variables, and secrets

The workflow **Deploy app bundle** does **not** read Databricks credentials from generic repo secrets alone. It expects each job to use a **GitHub Environment** named **`dev`**, **`test`**, or **`prod`** (matching the bundle target), and that environment must expose:

| Name | Where in the UI | Type |
|------|------------------|------|
| `DATABRICKS_HOST` | **Environment variables** | Variable (non-secret) |
| `DATABRICKS_TOKEN` | **Environment secrets** | Secret |

Do this on **your fork** (Settings apply to that repo):

1. Go to **Settings** → **Environments**.
2. Click **New environment**. Create **`dev`** first (exact name). Save.
3. Open the **`dev`** environment.
4. Under **Environment variables**, add:
   - **Name:** `DATABRICKS_HOST`
   - **Value:** your workspace URL, e.g. `https://dbc-xxxxxxxx.cloud.databricks.com`
5. Under **Environment secrets**, add:
   - **Name:** `DATABRICKS_TOKEN`
   - **Value:** a PAT or service principal token that can deploy the bundle and write to the paths your workflow uses.

Repeat steps 2–5 for **`test`** and **`prod`** if you will deploy to different workspaces or credentials. If you only POC against one workspace, configuring **`dev`** is enough—as long as the workflow run resolves to **`dev`** (see the workflow’s branch rules and manual dispatch).

Optional: configure **protection rules** (reviewers, wait timers) per environment if your org requires them.

Branch / trigger behavior (manual runs, `feature_*`, etc.) is summarized in **[.github/workflows/README.md](../.github/workflows/README.md)**.

---

## Step 6 — Push and watch the workflow

Push from **your fork** to a branch that triggers **Deploy app bundle** (for example **`feature_*`**), or use **Actions** → **Deploy app bundle** → **Run workflow** and pick the environment (`dev` / `test` / `prod`).

**Expect:**

- `databricks bundle validate`
- `databricks bundle deploy` (with `--auto-approve` in CI)
- Upload of **`data/*.csv`** to the configured volume path

**Do not expect** (with the stock workflow): a **pipeline run** or **`bundle run`** in CI—by design for this POC prompt.

---

## Step 7 — Refresh the pipeline in the workspace

After a green deploy:

1. Open **Databricks** → **Jobs & Pipelines** / **Pipelines**.
2. Find your pipeline (for example **`diagnostics_lab_results_pipeline`** if that is what the bundle defines).
3. Start a **refresh** so the table materializes in the **diagnostics** schema.

Use the job summary output (**`databricks bundle summary`**, **`databricks pipelines list-pipelines`**) if you need to confirm the pipeline exists before troubleshooting the UI.

---

## What “done” looks like for the POC

You can show:

1. The **prompt** and **constraints** you used in Cursor.
2. The **Git diff**: bundle YAML + minimal Python pipeline code.
3. A **successful GitHub Action** that deployed the bundle and uploaded data.
4. A **manual pipeline refresh** and a **table** visible in Unity Catalog (subject to your catalog/schema/table names).

That’s a solid **half-day to one-day POC** for platform and data engineering folks.

---

## Further reading

- **[README](../README.md)** — Full setup, deploy notes, and links to Databricks docs.
- **[docs/demo-session.md](demo-session.md)** — Short outline for a live session.

---

## License

This repository is released under the **MIT License**—see the [`LICENSE`](../LICENSE) file in the root of the project.
