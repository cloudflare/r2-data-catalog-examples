package com.example

import org.apache.spark.sql.SparkSession

object R2DataCatalogDemo {
    def main(args: Array[String]): Unit = {

        val uri = sys.env("CATALOG_URI")
        val warehouse = sys.env("WAREHOUSE")
        val token = sys.env("TOKEN")

        val spark = SparkSession.builder()
            .appName("My R2 Data Catalog Demo")
            .master("local[*]")
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.mydemo", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.mydemo.type", "rest")
            .config("spark.sql.catalog.mydemo.uri", uri)
            .config("spark.sql.catalog.mydemo.warehouse", warehouse)
            .config("spark.sql.catalog.mydemo.token", token)
            .getOrCreate()

        import spark.implicits._

        val data = Seq(
            (1, "Alice", 25),
            (2, "Bob", 30),
            (3, "Charlie", 35),
            (4, "Diana", 40)
        ).toDF("id", "name", "age")

        spark.sql("USE mydemo")

        spark.sql("CREATE NAMESPACE IF NOT EXISTS demoNamespace")

        data.writeTo("demoNamespace.demotable").createOrReplace()

        val readResult = spark.sql("SELECT * FROM demoNamespace.demotable WHERE age > 30")
        println("Records with age > 30:")
        readResult.show()
    }
}