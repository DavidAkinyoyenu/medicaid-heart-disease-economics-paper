import duckdb
from cdc_wonder import WonderQuery

# US adults 55-64 (men + women)
df = WonderQuery(
    dataset="mcd",
    group_by=["year", "state", "ten_year_age"],
    ten_year_age=["55-64"],
    years=range(1999, 2020),
    ucd_113_codes=["GR113-058"]  # Heart Disease I20-I25
).run()

df.to_csv("raw/cdc_wonder_adults_55_64_raw.csv", index=False)

conn = duckdb.connect()

conn.execute("""
    CREATE TABLE cdc_raw AS
    SELECT
        Year as year,
        State as state,
        "State Code" as state_code,
        Deaths as deaths,
        Population as population
    FROM read_csv('raw/cdc_wonder_adults_55_64_raw.csv', header=True)
""")

conn.execute("""
    CREATE TABLE cdc_wonder_adults_55_64 AS
    SELECT
        year,
        state,
        state_code,
        CASE WHEN COUNT(*) = COUNT(deaths) THEN SUM(deaths) ELSE NULL END AS deaths,
        CASE WHEN COUNT(*) = COUNT(population) THEN SUM(population) ELSE NULL END AS population,
        CASE WHEN COUNT(*) = COUNT(deaths)
             THEN SUM(deaths) / SUM(population) * 100000.0
             ELSE NULL END AS crude_rate
    FROM cdc_raw
    WHERE year IS NOT NULL AND state IS NOT NULL
    GROUP BY year, state, state_code
    ORDER BY state, year
""")

conn.execute("""
    COPY cdc_wonder_adults_55_64 TO 'intermediate/cdc_wonder_adults_55_64.parquet' (FORMAT parquet)
""")
conn.execute("""
    COPY cdc_wonder_adults_55_64 TO 'intermediate/cdc_wonder_adults_55_64.csv' (FORMAT csv, HEADER true)
""")

print(conn.execute("SELECT COUNT(*) FROM cdc_wonder_adults_55_64").fetchdf())
print(conn.execute("SELECT COUNT(*) FROM cdc_wonder_adults_55_64 WHERE deaths IS NULL").fetchdf())
print(conn.execute("SELECT * FROM cdc_wonder_adults_55_64 LIMIT 10").fetchdf())

conn.close()
