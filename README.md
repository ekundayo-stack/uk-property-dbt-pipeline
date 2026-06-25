# UK Property Price Pipeline (dbt + DuckDB)

An analytics-engineering pipeline that transforms six years of UK property
sale records from HM Land Registry into a clean, tested dimensional model
using dbt and DuckDB.

## What it does

Raw Land Registry "Price Paid" data (2020 to 2025, 5.9 million
transactions) flows through three layers:

- **Source** — six yearly CSVs, read together via a wildcard and declared
  as a single dbt source
- **Staging** (`stg_price_paid`) — columns renamed and typed, light cleaning
- **Marts** — a dimensional model plus business-ready aggregates:
  - `fct_sales` — sales fact table, one row per transaction, joined to its
    property type dimension
  - `dim_property_type` — property type dimension, mapping Land Registry
    codes to readable labels
  - `avg_price_by_county` — average and median sale price by region
  - `monthly_sales_trend` — sales volume and average price by month

## Pipeline

![Lineage Graph](images/lineage_graph.png)

The graph shows a star schema: raw data cleaned once in staging, then
modelled into a fact table that references its dimension, alongside two
aggregate marts.

## Data quality

Fourteen dbt tests run on every build, including:

- uniqueness and not-null on transaction keys
- not-null on price and date
- accepted-values checks on property type and old/new fields
- a relationships test confirming every sale links to a valid property
  type (referential integrity across the full dataset)

All tests passing across all records.

## Tech stack

dbt Core, dbt-duckdb, DuckDB.

## Running it locally

1. Download one or more yearly Price Paid CSVs from
   https://www.gov.uk/guidance/about-the-price-paid-data
2. Place them in a `data/` folder, named `pp-YYYY.csv` (the files are
   gitignored due to size).
3. Update the `external_location` path in `models/staging/_sources.yml`
   to point to your `data/` folder.
4. Run `dbt run` to build, then `dbt test` to validate.


## AI Report Generator

On top of the pipeline, an AI layer (in `ai_reporting/`) generates written
property market briefings from the modelled data using Google's Gemini API.

The interesting engineering is the guardrails against hallucination:

- A strict system prompt constrains the model to use only the real figures
  it is given, and forbids it from describing recorded data as forecasts.
- After generation, an automated verification step extracts every number
  from the AI's output and checks it against the source data. If the model
  states any figure not present in the pipeline, the report is flagged and
  refused.
- Reports are only saved if verification passes. A verified report or none.

Run `dbt run` first to build the data, then:
`python ai_reporting/generate_report.py "London"` (or any region).