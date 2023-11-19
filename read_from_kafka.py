from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder
.appName("Read From Kafka")
.getOrCreate())

spark.sparkContext.setLogLevel('ERROR')


# Read data from kafka source
lines = (spark
.readStream
.format("kafka")
.option("kafka.bootstrap.servers", "kafka:9092")
.option("subscribe", "office-input")
.load())


# deserialize key and value
lines2 = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)",
                          "topic", "partition", "offset", "timestamp")

lines3 = lines2.withColumn("time", F.trim(F.split(F.col("value"), ",")[0])) \
               .withColumn("room", F.split(F.col("value"), ",")[1]) \
               .withColumn("temperature", F.split(F.col("value"), ",")[2]) \
               .withColumn("pir", F.split(F.col("value"), ",")[3]) \
               .withColumn("light", F.split(F.col("value"), ",")[4]) \
               .withColumn("humidity", F.split(F.col("value"), ",")[5]) \
               .withColumn("co2", F.split(F.col("value"), ",")[6])

lines4 = lines3.drop("key","value","topic", "partition", "offset", "timestamp")

checkpoint_dir = "file:///tmp/streaming/read_from_kafka"

# write es
streamingQuery = (lines4
    .writeStream
    .format("org.elasticsearch.spark.sql")
    .outputMode("append") 
    .trigger(processingTime="1 second")
    .option("es.nodes", "es")
    .option("es.port","9200")
    .option("es.resource","office-input")
    .option("es.write.operation","index")
    .option("es.batch.write.refresh","false")
    .option("checkpointLocation", checkpoint_dir)
    .option("numRows",20)
    .option("truncate",False)
    .start())

# start streaming
streamingQuery.awaitTermination()