# Databricks CI/CD with Vibe Coding

This project showcases how **Cursor** can be used for **vibe coding** together with **Databricks Asset Bundles (DAB)** and **GitHub Actions** to build and deploy Databricks workloads.

## What is Vibe Coding?

Vibe coding is an iterative, AI-assisted development style where you describe what you want in natural language and work alongside an AI assistant (like Cursor) to implement it. Instead of writing every line by hand, you focus on intent, structure, and review—letting the AI suggest code, config, and fixes while you steer the outcome.

## What This Repo Demonstrates

- **Cursor** – Using Cursor’s AI features to design and evolve Databricks bundles, notebooks, jobs, and pipelines through conversation and inline edits.
- **Databricks Asset Bundles (DAB)** – Defining Databricks resources (jobs, pipelines, notebooks, etc.) as code in a bundle that can be validated and deployed.
- **GitHub Actions** – Automating validation, testing, and deployment of the bundle on push or pull request (e.g., `databricks bundle validate`, `databricks bundle deploy`).

Together, this gives you a workflow where you can “vibe code” your Databricks assets in Cursor and have them automatically validated and deployed via GitHub Actions.

## Project Structure (Typical DAB Layout)

```
databricks_cicd_with_vibe/
├── README.md                 # This file
├── .github/
│   └── workflows/            # GitHub Actions for validate/deploy
│       └── databricks-bundle.yml
├── src/
│   └── <bundle_name>/        # Your DAB project
│       ├── databricks.yml    # Bundle configuration
│       ├── resources/        # Jobs, pipelines, etc.
│       └── ...
└── ...
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
   cd src/<bundle_name>
   databricks bundle validate -e <environment>
   ```

4. **Deploy via GitHub Actions**  
   Push to your branch; the workflow can run `databricks bundle validate` and optionally `databricks bundle deploy` (e.g. to dev on PR, to prod on merge to main).

## GitHub Actions Setup

Store these as repository secrets (or environment secrets):

- `DATABRICKS_HOST` – e.g. `https://<workspace>.cloud.databricks.com`
- `DATABRICKS_TOKEN` – token with access to deploy and run jobs/pipelines

Your workflow can:

- Run `databricks bundle validate -e <env>` on every push/PR.
- Run `databricks bundle deploy -e <env>` on specific branches or tags (e.g. `main` → production).

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
