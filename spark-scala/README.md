# R2 Data Catalog Spark Application Demo

This is a demo package demonstrating how to set up a Spark Application (using Scala) with R2 Data Catalog.

## Prerequisites

- Install Java 17
- Install `sbt` (build tool for Scala apps)
- Install `spark` 3.5.3

One way you can manage these dependencies is by using [SDK Man](https://sdkman.io/), which is a free, open source development kit manager for JVM-based projects.

Java 17:
```
sdk install java 17.0.14-amzn
```

SBT:
```
sdk install sbt 1.10.11
```

Spark
```
sdk install spark 3.5.3
```

*NOTE*: You may need to reload your shell after installing these tools so they are on the path. If that doesn't work, try running the following to set them on the path in your current shell

```
PATH=$PATH:"$(sdk home spark 3.5.3)/bin/"
PATH=$PATH:"$(sdk home sbt 1.10.11)/bin/"
```


## Run the Spark App

To run the project, compile the app
```
make build
```

Then set the following env variables in your shell session:


```
export CATALOG_URI=
export WAREHOUSE=
export TOKEN=
```

- **Catalog URI**: This is the URI your R2 Data Catalog. If you don't have this URI or forgot it, you can get it in the dash or in Wrangler. `wrangler r2 bucket catalog get <bucket>`. It will include a URI that looks like `https://catalog.cloudflarestorage.com/account_id/bucket_name`.
- **Warehouse**: This is the name of your catalog warehouse. This is your account identifer and bucket name, separated by an underscore. Both the account identifier and bucket name are in the path of your catalog URI.
- **Token**: This is a Cloudflare API token which should have permissions to both your R2 bucket and the R2 Data Catalog.


To run it in Spark, run the submit command.
```
make submit
```

After a few moments, you should see the query result in your terminal.
```
Records with age > 30:
+---+-------+---+
| id|   name|age|
+---+-------+---+
|  3|Charlie| 35|
|  4|  Diana| 40|
+---+-------+---+
```
