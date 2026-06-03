import duckdb

conn = duckdb.connect()

conn.execute("""
    CREATE OR REPLACE TABLE bls_raw AS
    SELECT *
    FROM read_csv(
        'raw/raw_unemployment_staadata.csv',
        auto_detect = false,
        delim = ',',
        quote = '"',
        header = false,
        skip = 8,
        strict_mode = false,
        columns = {
            'fips':             'VARCHAR',
            'state':            'VARCHAR',
            'year_raw':         'VARCHAR',
            'population':       'VARCHAR',
            'labor_force':      'VARCHAR',
            'labor_force_rate': 'VARCHAR',
            'employment':       'VARCHAR',
            'employment_rate':  'VARCHAR',
            'unemployment':     'VARCHAR',
            'unemployment_rate':'VARCHAR'
        }
    )
""")

# Keep only state-level rows (exactly 2-digit numeric FIPS)
# Year column has footnotes like "2025(1)" — extract the 4-digit year
conn.execute("""
    CREATE OR REPLACE TABLE bls_laus AS
    SELECT
        trim(fips)  AS fips,
        trim(state) AS state,
        CAST(regexp_extract(trim(year_raw), '[0-9]{4}') AS INTEGER) AS year,
        CAST(replace(trim(unemployment_rate), ',', '') AS DOUBLE)   AS unemployment_rate
    FROM bls_raw
    WHERE trim(fips) IS NOT NULL
      AND trim(fips) <> ''
      AND length(trim(fips)) = 2
      AND try_cast(trim(fips) AS INTEGER) IS NOT NULL
      AND regexp_extract(trim(year_raw), '[0-9]{4}') <> ''
      AND CAST(regexp_extract(trim(year_raw), '[0-9]{4}') AS INTEGER) BETWEEN 1999 AND 2019

""")

conn.execute("""
    COPY bls_laus TO 'intermediate/bls_laus_output.parquet' (FORMAT parquet)
""")
conn.execute("""
    COPY bls_laus TO 'intermediate/bls_laus.csv' (FORMAT csv, HEADER true)
""")

print(conn.execute("SELECT COUNT(*) FROM bls_laus").fetchdf())
print(conn.execute("SELECT * FROM bls_laus LIMIT 10").fetchdf())

conn.close()
