import duckdb
from cdc_wonder import WonderQuery

# US men 55-64
df = WonderQuery(
    dataset="mcd",
    group_by=["year", "state", "ten_year_age", "sex"],
    ten_year_age=["55-64"],
    sex=["M"],
    years=range(1999, 2020),
    ucd_113_codes=["GR113-058"]  # Heart Disease I20-I25
).run()

df.to_csv("raw/cdc_wonder_output_raw.csv", index=False)

conn = duckdb.connect()
conn.execute("""
    CREATE TABLE cdc_wonder_output AS
    SELECT
        Year as year,
        State as state,
        "State Code" as state_code,
        "Ten-Year Age Groups" as ten_year_age,
        "Sex Code" as sex_code,
        Deaths as deaths,
        Population as population,
        "Crude Rate" as crude_rate
    FROM read_csv('raw/cdc_wonder_output_raw.csv', header=True)
""")

conn.execute("""
    COPY cdc_wonder_output TO 'intermediate/cdc_wonder_output.parquet' (FORMAT parquet)
""")
conn.execute("""
    COPY cdc_wonder_output TO 'intermediate/cdc_wonder_output.csv' (FORMAT csv, HEADER true)
""")

conn.close()
