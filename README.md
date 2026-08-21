# Supermarket Sales - Databricks Autoloader Pipeline (Bronze-Silver-Gold)

This project implements a **Medallion Architecture (Bronze → Silver → Gold)** data pipeline in **Databricks**, built using **Delta Live Tables (DLT)** and **Auto Loader (`cloudFiles`)** for incremental ingestion of supermarket sales data.

## Dataset

`supermarket_sales.csv` — transactional sales data with the following columns:

`Invoice_ID, Branch, City, Customer_type, Gender, Product_line, Unit_price, Quantity, Tax5%, Total, Date, Time, Payment, cogs, gross_margin_percentage, gross_income, Rating`

## Pipeline Overview

```
Volume (CSV files)
      │
      ▼
  ┌─────────┐
  │ Bronze  │  Raw ingestion via Auto Loader (cloudFiles)
  └─────────┘
      │
      ▼
  ┌─────────┐
  │ Silver  │  Cleaned & deduplicated subset of columns
  └─────────┘
      │
      ▼
  ┌─────────┐
  │  Gold   │  Aggregated business metrics
  └─────────┘
```

### 1. Bronze Layer (`practicebronze.py`)

- Ingests raw CSV files using **Auto Loader** (`spark.readStream.format("cloudFiles")`).
- Source path: `/Volumes/workspace/practicep/practicep`
- Options used: `cloudFiles.format = csv`, `header = true`, `inferSchema = true`
- Adds an `ingestion_time` column (`current_timestamp()`) to track when each record was ingested.
- Table: **`bronze1`**, created with `delta.columnMapping.mode = name`.

### 2. Silver Layer (`practicesilver.py`)

- Reads from `bronze1` using `dlt.read()`.
- Selects a curated subset of columns:
  `Invoice_ID, Unit_price, Tax5%, gross_margin_percentage, gross_income, Product_line, Customer_type`
- Removes duplicate records based on `Invoice_ID`, `Tax5%`, and `Unit_price`.
- Table: **`silver1`**.

### 3. Gold Layer (`practicegold.py`)

- Reads from `silver1` using `dlt.read()`.
- Aggregates total `Unit_price` grouped by `Customer_type`, rounded to 1 decimal place.
- Result sorted by `total_unit_price`.
- Table: **`gold1`**.

## Tech Stack

- **Databricks** (Delta Live Tables / DLT framework)
- **Auto Loader** (`cloudFiles`) for incremental, schema-inferred streaming ingestion
- **Delta Lake** for storage (with column mapping enabled)
- **PySpark** for transformations

## Project Structure

```
├── practicebronze.py   # Bronze: raw ingestion via Auto Loader
├── practicesilver.py   # Silver: cleaned, deduplicated data
├── practicegold.py     # Gold: aggregated metrics
├── supermarket_sales.csv
└── README.md
```

## How to Run

1. Upload the notebooks (`practicebronze.py`, `practicesilver.py`, `practicegold.py`) to a Databricks workspace.
2. Place `supermarket_sales.csv` in the Unity Catalog volume: `/Volumes/workspace/practicep/practicep`.
3. Create a **Delta Live Tables pipeline** in Databricks, adding all three notebooks as source files (in Bronze → Silver → Gold order).
4. Start the pipeline. Auto Loader will incrementally pick up new files dropped into the source volume.

## Notes

- Since this uses **Auto Loader with streaming reads**, new files added to the source volume are automatically picked up in subsequent pipeline runs — no manual reprocessing needed.
- Schema is inferred automatically (`inferSchema = true`); for production use, consider defining an explicit schema and enabling `cloudFiles.schemaLocation` for schema evolution tracking.
