import duckdb

conn = duckdb.connect()

conn.execute("""
    CREATE OR REPLACE TABLE cdc AS
    SELECT * FROM read_parquet('intermediate/cdc_wonder_adults_25_44_all_cause.parquet')
""")

conn.execute("""
    CREATE OR REPLACE TABLE expansion AS
    SELECT * FROM read_parquet('intermediate/expansion_dates.parquet')
""")

conn.execute("""
    CREATE OR REPLACE TABLE bls AS
    SELECT * FROM read_parquet('intermediate/bls_laus_output.parquet')
""")

conn.execute("""
    CREATE OR REPLACE TABLE poverty AS
    SELECT * FROM read_parquet('intermediate/poverty_output.parquet')
""")

conn.execute("""
    CREATE OR REPLACE TABLE cigarette AS
    SELECT * FROM read_parquet('intermediate/cigarette_tax_output.parquet')
""")

conn.execute("""
    CREATE OR REPLACE TABLE panel AS
    SELECT
        c.year,
        c.state,
        c.state_code,
        c.deaths,
        c.population,
        c.crude_rate,
        b.unemployment_rate,
        p.poverty_rate,
        cig.cigarette_tax_per_pack,
        e.expansion_year,
        CASE WHEN c.year >= e.expansion_year THEN 1 ELSE 0 END AS treat_post
    FROM cdc AS c
    LEFT JOIN bls AS b
        ON c.year  = b.year
        AND c.state = b.state
    LEFT JOIN expansion AS e
        ON c.state = e.state
    LEFT JOIN poverty AS p
        ON c.year  = p.year
        AND c.state = p.state
    LEFT JOIN cigarette AS cig
        ON c.year  = cig.year
        AND c.state = cig.state
    WHERE c.state IS NOT NULL
      AND c.year  IS NOT NULL
    ORDER BY c.state, c.year
""")

OUT = 'panel_adults_25_44_all_cause_unemployment_poverty_cigarette'

conn.execute(f"COPY panel TO 'output/{OUT}.parquet' (FORMAT parquet)")
conn.execute(f"COPY panel TO 'output/{OUT}.csv' (FORMAT csv, HEADER true)")

df = conn.execute("SELECT * FROM panel").fetchdf()
print(f"Rows: {len(df)}")
print(df.head(10))

conn.close()

df.to_stata(f"output/{OUT}.dta", write_index=False, version=118)
