import duckdb
from cdc_wonder import WonderQuery

# US men 45-64: fetch both age bands, then aggregate
df = WonderQuery(
    dataset="mcd",
    group_by=["year", "state", "ten_year_age", "sex"],
    ten_year_age=["45-54", "55-64"],
    sex=["M"],
    years=range(1999, 2020),
    ucd_113_codes=["GR113-058"]  # Heart Disease I20-I25
).run()

df.to_csv("raw/cdc_wonder_men_45_64_raw.csv", index=False)

conn = duckdb.connect()

# Load both age bands
conn.execute("""
    CREATE TABLE cdc_raw AS
    SELECT
        Year as year,
        State as state,
        "State Code" as state_code,
        Deaths as deaths,
        Population as population
    FROM read_csv('raw/cdc_wonder_men_45_64_raw.csv', header=True)
""")

# Sum deaths and population across 45-54 and 55-64, recompute crude rate per 100k
conn.execute("""
    CREATE TABLE cdc_wonder_men_45_64 AS
    SELECT
        year,
        state,
        state_code,
        SUM(deaths) AS deaths,
        SUM(population) AS population,
        SUM(deaths) / SUM(population) * 100000.0 AS crude_rate
    FROM cdc_raw
    GROUP BY year, state, state_code
    ORDER BY state, year
""")

conn.execute("""
    COPY cdc_wonder_men_45_64 TO 'intermediate/cdc_wonder_men_45_64.parquet' (FORMAT parquet)
""")
conn.execute("""
    COPY cdc_wonder_men_45_64 TO 'intermediate/cdc_wonder_men_45_64.csv' (FORMAT csv, HEADER true)
""")

print(conn.execute("SELECT COUNT(*) FROM cdc_wonder_men_45_64").fetchdf())
print(conn.execute("SELECT * FROM cdc_wonder_men_45_64 LIMIT 10").fetchdf())

conn.close()
