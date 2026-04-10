import dlt

# Unity Catalog names are fixed for this demo bundle.
_CATALOG = "cicd_with_vibe"
_SCHEMA = "diagnostics"
# Matches CI upload: dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data/lab_results.csv
_CSV = f"/Volumes/{_CATALOG}/{_SCHEMA}/diagnostics_data/lab_results.csv"


@dlt.table(name="lab_results")
def lab_results():
    return (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(_CSV)
    )
