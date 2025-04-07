#!/bin/sh

# We need to set these "--add-opens" so that Spark can run on Java 17 (it needs access to
# parts of the JVM which have been modularized and made internal).
JAVA_17_COMPATABILITY="--add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED"

spark-submit \
--conf "spark.log.level=WARN" \
--conf "spark.driver.extraJavaOptions=$JAVA_17_COMPATABILITY" \
--conf "spark.executor.extraJavaOptions=$JAVA_17_COMPATABILITY" \
--class com.example.R2DataCatalogDemo target/scala-2.12/R2DataCatalogDemo-assembly-1.0.jar