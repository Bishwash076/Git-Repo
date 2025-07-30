from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder \
    .appName("LineageExample") \
    .getOrCreate()

df = spark.read.json("s3a://your-bucket/path/to/data.json")  # example input

df_gold = df.filter(F.length(F.col("text")) > 100).withColumn("text", F.lower(F.col("text")))

def emit_lineage(eventType, dataset, metadata):
    print(f"Emitting lineage: {eventType} on {dataset}, metadata: {metadata}")

emit_lineage("COMPLETE", "gold", {"rows": df_gold.count()})
