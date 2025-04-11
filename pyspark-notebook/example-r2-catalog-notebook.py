import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pyspark
    from pyspark.conf import SparkConf
    from pyspark.sql import SparkSession
    import pandas as pd
    import os

    # Setup App Environment Variables (set values in .env)
    token = os.getenv("TOKEN")
    catalog_uri = os.getenv("CATALOG_URI")
    warehouse = os.getenv("WAREHOUSE")
    namespace = "testnamespace"
    table = "test_table"

    # Setup the Spark Session
    # NOTE: You may see some red output while running this command, but this isn't an error message. It's just
    # Pyspark automatically setting up the JARs for Spark.
    spark = SparkSession.builder \
        .appName("R2CatalogDemo") \
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1,org.apache.iceberg:iceberg-aws-bundle:1.6.1") \
        .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.demo.type", "rest") \
        .config("spark.sql.catalog.demo.uri", catalog_uri) \
        .config("spark.sql.catalog.demo.warehouse", warehouse) \
        .config("spark.sql.catalog.demo.token", token) \
        .config("spark.sql.defaultCatalog", "demo") \
        .getOrCreate();
    spark.sql("USE demo")
    print("Setup Complete")
    return (
        SparkConf,
        SparkSession,
        catalog_uri,
        namespace,
        os,
        pd,
        pyspark,
        spark,
        table,
        token,
        warehouse,
    )


@app.cell
def _(namespace, spark):
    # Create (if not present) a new Namespace
    spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {namespace}")
    spark.sql("SHOW NAMESPACES").toPandas()
    return


@app.cell
def _(namespace, pd, spark, table):
    # Create a Pandas Data Frame with some test data
    data = pd.DataFrame([
        [1, 'a-string', 2.2],
        [2, 'a name', 42.0],
        [3, 'foo bar', -101.101],
        [4, 'fizz buzz', 0.2],
        [5, 'hello world', -10.0]
    ], columns=['id', 'name', 'num'])

    # Convert to a Spark Data Frame
    sparkDataFrame = spark.createDataFrame(data)

    # Write to Iceberg (WARN: this replaces the table if it already exists)
    sparkDataFrame.writeTo(f"{namespace}.{table}").createOrReplace();
    print("Done!")
    return data, sparkDataFrame


@app.cell
def _(namespace, spark, table):
    # Read the data we just wrote
    spark.sql(f"SELECT * FROM {namespace}.{table}").toPandas()
    return


@app.cell
def _(namespace, spark, table):
    # Show all the negative numbers
    spark.sql(f"SELECT id,name FROM {namespace}.{table} WHERE num < 0.0").toPandas()
    return


if __name__ == "__main__":
    app.run()
