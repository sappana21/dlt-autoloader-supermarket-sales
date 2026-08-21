# Databricks notebook source
import dlt

def bronze_df():
    return dlt.read("bronze1")

@dlt.table(name="silver1")
def silver1():
    return(
        bronze_df()
        .select(
            "Invoice_ID",
            "Unit_price",
            "Tax5%",
            "gross_margin_percentage",
            "gross_income",
            "Product_line",
            "Customer_type"
        ).dropDuplicates(["Invoice_ID","Tax5%","Unit_price"])
    )