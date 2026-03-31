import dlt


@dlt.table(
    name="lab_results",
    comment="Lab results loaded from the diagnostics volume CSV file.",
)
def lab_results():
    return (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load("dbfs:/Volumes/cicd_with_vibe/diagnostics/diagnostics_data/lab_results.csv")
    )
