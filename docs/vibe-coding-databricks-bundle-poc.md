# From a single prompt to a deployed pipeline: vibe coding with Databricks Asset Bundles and GitHub Actions

*A practical walkthrough for running a proof of concept with Cursor, Lakeflow Spark Declarative Pipelines, and CI/CD—without treating the pipeline run as part of CI unless you want it.*

---

If your team is exploring **AI-assisted development** on top of **Databricks**, the natural question is whether you can go from “describe the outcome” to “something running in a workspace” in one sitting—and still keep **infrastructure as code**, **reviewable diffs**, and a path to **automated deploys**.

This repository is built around that story. You use **Cursor** (or a similar assistant) to **vibe code**: you give a structured prompt, iterate on the bundle and pipeline code, then **push** so **GitHub Actions** can **validate** and **deploy** a **Databricks Asset Bundle**. The workflow in this repo also **uploads CSVs** from `data/` to a **Unity Catalog volume** path so your pipeline can read **`lab_results.csv`** (or your own files) the same way you would in a real project.

What this article gives you:

- A **Medium-style narrative** of what you are proving in a POC.
- **Step-by-step instructions** to run that POC using the **session demo prompt** from the README.
- Pointers back to the **[README](../README.md)** for authoritative details (secrets, CLI versions, path rules).

---

## What you are proving in the POC

In one sentence: **natural-language intent → bundle + pipeline as code → automated deploy + data on a volume → manual pipeline refresh in Databricks.**

| Layer | What the POC validates |
|--------|-------------------------|
| **Vibe coding** | You can steer an assistant with constraints (minimal DLT table, `.py` not notebook, `file` in YAML, paths relative to pipeline YAML, hardcoded catalog/schema for the demo). |
| **Databricks Asset Bundles** | Lakeflow Spark Declarative Pipeline resources live in Git and deploy with `databricks bundle deploy`. |
| **GitHub Actions** | CI **validates** and **deploys** the bundle and **uploads** CSVs; it does **not** run the pipeline by default (aligns with “no bundle run in CI unless asked”). |
| **Operations** | After deploy, a human triggers a **pipeline refresh** when you are ready to materialize tables—mirroring how many teams separate “ship definition” from “run now.” |

This is enough for a **time-boxed POC** with stakeholders: you can show the prompt, the repo layout, the Action run, and the pipeline in the workspace.

---

## Prerequisites

Before you start, confirm you have:

1. **Cursor** (or another AI-capable editor you use for the same workflow).
2. A **Databricks workspace** with **Unity Catalog**, and entitlements that match what you deploy—for **serverless** Lakeflow pipelines, **Lakeflow Advanced** is required (see the README deploy notes).
3. **Databricks CLI** with bundle support (`databricks bundle -h`), ideally **0.283.0 or newer** for Lakeflow Spark Declarative Pipelines in bundles.
4. A **GitHub** repository (fork or clone of this project) with **Actions** enabled.
5. **GitHub Environments** named **`dev`**, **`test`**, and **`prod`** (the workflow maps bundle targets to these names—see [.github/workflows/README.md](../.github/workflows/README.md)).

You will also need **Unity Catalog objects** that match what the bundle and workflow expect, or you will adjust names consistently. The README describes uploading to a volume path under **`cicd_with_vibe`** / **`diagnostics`**; **create the catalog, schema, and managed volume** in UC yourself (or align paths in your fork).

---

## Step 1 — Get the code and open it in Cursor

Clone your fork (or this repo), then open the folder in Cursor:

```bash
git clone <your-repo-url>
cd databricks_cicd_with_vibe
cursor .
```

Familiarize yourself with the layout: root **`databricks.yml`**, **`resources/pipelines/`** for pipeline bundle YAML, **`src/`** for pipeline Python, **`data/`** for CSVs the workflow uploads, and **`.github/workflows/`** for CI.

---

## Step 2 — Prepare Unity Catalog (POC baseline)

For a successful end-to-end story, your workspace should have:

- A **catalog** and **schema** your pipeline will target (the demo prompt assumes **hardcoded** names in code—keep them consistent with UC).
- A **managed volume** (or equivalent path) where CI can upload **`data/*.csv`**, and where the pipeline reads **`lab_results.csv`**.

The **[README](../README.md)** describes the volume path used by the **Deploy app bundle** workflow (`dbfs:/Volumes/...` style path). Create or align these objects **before** you rely on the upload step and the pipeline read.

---

## Step 3 — Paste the vibe prompt and iterate in Cursor

Open a chat (or composer) in Cursor and use the **session demo prompt** verbatim—this is the same block as in the README under **“Session demo prompt (vibe)”**:

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

**How to use this in a POC:**

- **Point the assistant** at `databricks.yml` and the intended folders (`resources/pipelines/`, `src/…`) so generated paths match your bundle layout.
- **Review every change**: YAML for the pipeline resource, Python for a single `@dlt.table`, and that **`libraries`** uses **`file`** with a path **relative to the pipeline YAML file’s directory** (not the bundle root).
- If something conflicts with your workspace (catalog name, volume path), **adjust in code** and keep the hardcoded-names rule intentional for the demo.

---

## Step 4 — Validate locally

With your Databricks profile configured:

```bash
databricks bundle validate -t dev --profile <your-profile>
```

Fix any validation errors before you depend on CI. The README **Deploy notes** section explains common pitfalls (CLI version, include globs, relative `file.path` resolution).

---

## Step 5 — Wire GitHub Actions

For each **GitHub Environment** (`dev`, `test`, `prod`) that you will use:

| Setting | Type |
|--------|------|
| `DATABRICKS_HOST` | Environment **variable** (workspace URL) |
| `DATABRICKS_TOKEN` | Environment **secret** |

Details and behavior (branch filters, manual runs) are in **[.github/workflows/README.md](../.github/workflows/README.md)**.

---

## Step 6 — Push and watch the workflow

Push to a branch that triggers **Deploy app bundle** (for example **`feature_*`** or **`release_*`**, depending on your workflow), or run the workflow **manually** and select the environment.

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

You can demonstrate:

1. The **prompt** and **constraints** you used in Cursor.
2. The **Git diff**: bundle YAML + minimal Python pipeline code.
3. A **successful GitHub Action** that deployed the bundle and uploaded data.
4. A **manual pipeline refresh** and a **table** visible in Unity Catalog (subject to your catalog/schema/table names).

That is a credible **half-day to one-day POC** for platform and data engineering audiences.

---

## Further reading

- **[README](../README.md)** — Full setup, deploy notes, and links to Databricks docs.
- **[docs/demo-session.md](demo-session.md)** — Short slide-style outline for a live session.

---

## License

This repository is released under the **MIT License**—see the [`LICENSE`](../LICENSE) file in the root of the project.
