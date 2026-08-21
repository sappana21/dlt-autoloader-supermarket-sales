# Databricks notebook source
import dlt

from pyspark.sql.functions import current_timestamp

@dlt.table(
    name="bronze1",
    table_properties={
        "delta.columnMapping.mode": "name"
    }
)
def bronze1():
    return(
      spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format","csv")
        .option("header","true")
        .option("inferschema","true")
        .load("/Volumes/workspace/practicep/practicep")
        .withColumn("ingestion_time",current_timestamp())
    )
