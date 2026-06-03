import duckdb
from cdc_wonder import WonderQuery

# US adults 45-64 (men + women): fetch both age bands and both sexes, then aggregate
df = WonderQuery(
    dataset="mcd",
    group_by=["year", "state", "ten_year_age"],
    ten_year_age=["45-54", "55-64"],
    years=range(1999, 2020),
    ucd_113_codes=["GR113-058"]  # Heart Disease I20-I25
).run()

df.to_csv("raw/cdc_wonder_adults_45_64_raw.csv", index=False)

conn = duckdb.connect()

# Load both age bands (45-54 and 55-64, both sexes combined)
conn.execute("""
    CREATE TABLE cdc_raw AS
    SELECT
        Year as year,
        State as state,
        "State Code" as state_code,
        Deaths as deaths,
        Population as population
    FROM read_csv('raw/cdc_wonder_adults_45_64_raw.csv', header=True)
""")

# Sum deaths and population across both age bands, recompute crude rate per 100k
# If any band is suppressed, set the state-year to NULL rather than use an undercount
conn.execute("""
    CREATE TABLE cdc_wonder_adults_45_64 AS
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
    COPY cdc_wonder_adults_45_64 TO 'intermediate/cdc_wonder_adults_45_64.parquet' (FORMAT parquet)
""")
conn.execute("""
    COPY cdc_wonder_adults_45_64 TO 'intermediate/cdc_wonder_adults_45_64.csv' (FORMAT csv, HEADER true)
""")

print(conn.execute("SELECT COUNT(*) FROM cdc_wonder_adults_45_64").fetchdf())
print(conn.execute("SELECT COUNT(*) FROM cdc_wonder_adults_45_64 WHERE deaths IS NULL").fetchdf())
print(conn.execute("SELECT * FROM cdc_wonder_adults_45_64 LIMIT 10").fetchdf())

conn.close()
