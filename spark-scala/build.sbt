name := "R2DataCatalogDemo"

version := "1.0"

// A recent-ish version of Spark
val sparkVersion = "3.5.3"
val icebergVersion = "1.8.1"


// You need to use binaries of Spark compiled with either 2.12 or 2.13; and 2.12 is more common.
// If you download Spark with sdkman, then it comes with 2.12.18
scalaVersion := "2.12.18"

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-core" % sparkVersion,
    "org.apache.spark" %% "spark-sql" % sparkVersion,
    "org.apache.iceberg" % "iceberg-core" % icebergVersion,
    "org.apache.iceberg" % "iceberg-spark-runtime-3.5_2.12" % icebergVersion,
    "org.apache.iceberg" % "iceberg-aws-bundle" % icebergVersion,
)

// build a Fat JAR with all dependencies
assembly / assemblyMergeStrategy := {
    case PathList("META-INF", "services", xs @ _*) => MergeStrategy.concat
    case PathList("META-INF", xs @ _*) => MergeStrategy.discard
    case "reference.conf" => MergeStrategy.concat
    case "application.conf" => MergeStrategy.concat
    case x if x.endsWith(".properties") => MergeStrategy.first
    case x => MergeStrategy.first
}

// For Java  17 Compatability
Compile / javacOptions ++= Seq("--release", "17")