import requests
import duckdb

# Download CDC STATE System cigarette tax data
url = "https://data.cdc.gov/api/views/7nwe-3aj9/rows.csv?accessType=DOWNLOAD"
r = requests.get(url)

with open("raw/cigarette_tax_raw.csv", "wb") as f:
    f.write(r.content)

conn = duckdb.connect()

conn.execute("""
    CREATE TABLE cigarette_tax_output AS
    SELECT
        LocationDesc AS state,
        LocationAbbr AS state_abbr,
        CAST(Year AS INTEGER) AS year,
        CAST(Data_Value AS DOUBLE) AS cigarette_tax_per_pack
    FROM read_csv('raw/cigarette_tax_raw.csv', header=True)
    WHERE SubMeasureDesc = 'State Tax per pack'
      AND CAST(Year AS INTEGER) BETWEEN 1999 AND 2019
      AND LocationDesc NOT IN ('United States')
    ORDER BY state, year
""")

conn.execute("""
    COPY cigarette_tax_output TO 'intermediate/cigarette_tax_output.parquet' (FORMAT parquet)
""")

conn.execute("""
    COPY cigarette_tax_output TO 'intermediate/cigarette_tax_output.csv' (FORMAT csv, HEADER true)
""")

conn.close()
