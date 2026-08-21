# Databricks notebook source
import dlt
from pyspark.sql.functions import sum, round

def silver_df():
    return dlt.read("silver1")

@dlt.table(name="gold1")
def gold1():
    return(
        silver_df()
        .groupBy("Customer_type")
        .agg(
            round(sum("Unit_price"),1).alias("total_unit_price")
    
        ).orderBy("total_unit_price")
    )