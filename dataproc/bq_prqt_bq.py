#!/usr/bin/env python

"""BigQuery I/O PySpark example."""

from pyspark.sql import SparkSession

spark = SparkSession \
  .builder \
  .master('yarn') \
  .appName('spark-bigquery-demo') \
  .getOrCreate()

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = "nvn-bucket/staging"
spark.conf.set('temporaryGcsBucket', bucket)

# Load data from BigQuery.
words = spark.read.format('bigquery') \
  .option('table', 'mlconsole-poc.nvn_dataset.annonymuspar') \
  .load()
words.createOrReplaceTempView('words')

# Perform Remove duplicate.
remove_dupl = spark.sql(
    'SELECT DISTINCT * FROM nvn_dataset.annonymuspar')
remove_dupl.show()
remove_dupl.printSchema()

# Saving the data to BigQuery
remove_dupl.write.format('bigquery') \
  .option('table', 'mlconsole-poc.nvn_dataset.annonymusparout') \
  .save()
