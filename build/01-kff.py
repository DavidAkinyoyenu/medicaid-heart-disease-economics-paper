import duckdb

conn = duckdb.connect()

conn.execute("""
    CREATE OR REPLACE TABLE expansion_raw AS
    SELECT *
    FROM read_csv(
        'raw/raw_expansion_date.csv',
        auto_detect = false,
        delim = ',',
        quote = '"',
        escape = '"',
        header = true,
        skip = 2,
        null_padding = true,
        strict_mode = false,
        columns = {
            'Location': 'VARCHAR',
            'Status of Medicaid Expansion Decision': 'VARCHAR',
            'Expansion Implementation Date': 'VARCHAR',
            'Expansion Adopted Through Ballot Initiative': 'VARCHAR',
            'Trigger Law In Place': 'VARCHAR',
            'Footnotes': 'VARCHAR'
        }
    )
""")

conn.execute("""
    CREATE OR REPLACE TABLE expansion_dates AS
    SELECT
        trim(Location) AS state,
        CASE
            WHEN trim("Expansion Implementation Date") IS NULL
                 OR trim("Expansion Implementation Date") = ''
                 OR trim("Expansion Implementation Date") = 'N/A'
            THEN 3000
            ELSE year(try_strptime(trim("Expansion Implementation Date"), '%m/%d/%Y'))
        END AS expansion_year
    FROM expansion_raw
    WHERE trim(Location) IS NOT NULL
      AND trim(Location) <> ''
      AND trim(Location) <> 'United States'
      AND trim(Location) NOT IN ('Notes', 'Sources', 'Footnotes')
      AND trim(Location) NOT LIKE '%1.%'
      AND length(trim(Location)) <= 50
""")

conn.execute("""
    COPY expansion_dates TO 'intermediate/expansion_dates.parquet' (FORMAT parquet)
""")

conn.execute("""
    COPY expansion_dates TO 'intermediate/expansion_dates.csv' (FORMAT csv, HEADER true)
""")


print(conn.execute("SELECT COUNT(*) FROM expansion_dates").fetchdf())
print(conn.execute("SELECT * FROM expansion_dates ORDER BY state").fetchdf())
