Hello, I explained my data engineering project to you in steps below.

![project-flow-diagram](https://github.com/EmreTUNCA/spark-kafka-elasticsearch-kibana-data-engineering-project/assets/77586627/bcdb1254-b66f-45fe-a095-b63de1960a12)

1 - We use the note book file from which we downloaded the data and then cleaned and converted it using Spark.
(data_clean_transform.ipynb)

2 - In the next step, our data will be produced to Kafka with the data generator. Therefore, beforehand, it should be checked that Kafka is running and that the topic (office-input) to be produced exists.
(You can use code like this to create the office-input topic:
/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic office-input --replication-factor 1 --partitions 1)

3 - We send the data we prepared using the data generator (https://github.com/erkansirin78/data-generator) to Kafka. In this way, the data is streamed with Kafka.
(For this, you can run the code like this in the console:
python dataframe_to_kafka.py -i /opt/examples/final/concat_keti_parq/part-00000-6be45915-e5c1-4823-b170-1c257a0b469c-c000.parquet -e parquet -t office-input -k 1 -b kafka:9092 )

4 - Since the consumed data will be written to elasticsearch in the next step, an appropriate index must be created on the elasticsearch side before this process. To do this, the code in the elasticsearch_index.md file must be run using elasticsearch dev tools.
(elasticsearch_index.md)

5 - We consume the data produced by Kafka using Spark and then write it to Elasticsearch.
(The console code that you can run by spark-submitting this py file should be as follows:
spark-submit --master local --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,io.delta:delta-core_2.12:2.4.0,org.elasticsearch:elasticsearch-spark-30_2.12:7.12.1,commons-httpclient:commons-httpclient:3.1 opt/examples/final/read_from_kafka.py)

6 - You can see the change of stream data on elasticsearch and kibana.
![elasticsearch_index_view](https://github.com/EmreTUNCA/spark-kafka-elasticsearch-kibana-data-engineering-project/assets/77586627/e655c1a9-ab37-4c1e-94f7-5f65986bb42e)
![kibana-realtime-dashboards](https://github.com/EmreTUNCA/spark-kafka-elasticsearch-kibana-data-engineering-project/assets/77586627/a13d3f41-7a1f-432c-a254-045ee622a2cf)
