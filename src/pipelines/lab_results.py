import dlt

# Path from pipeline configuration (bundle variable); default matches CI volume upload.
_CSV = "/Volumes/cicd_with_vibe/diagnostics/diagnostics_data/lab_results.csv"


@dlt.table(name="lab_results")
def lab_results():
    path = spark.conf.get("pipelines.lab_results_csv", _CSV)
    return spark.read.format("csv").option("header", "true").load(path)
