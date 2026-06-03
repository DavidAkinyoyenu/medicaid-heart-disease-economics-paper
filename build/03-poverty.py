import requests
# import json
import duckdb

conn = duckdb.connect()

conn.execute("""
    CREATE TABLE poverty_output (
        year INTEGER,
        state VARCHAR,
        state_fips INTEGER,
        poverty_rate DOUBLE
    )
""")

for year in range(1999, 2020):
    url = (
        f"https://api.census.gov/data/timeseries/poverty/saipe"
        f"?get=NAME,SAEPOVRTALL_PT&for=state:*&YEAR={year}"
    )
    r = requests.get(url)
    data = r.json()
    header = data[0]
    rows = data[1:]

    idx_name = header.index("NAME")
    idx_rate = header.index("SAEPOVRTALL_PT")
    idx_fips = header.index("state")

    conn.executemany("""
        INSERT INTO poverty_output VALUES (?, ?, ?, ?)
    """, [(year, row[idx_name], int(row[idx_fips]), float(row[idx_rate])) for row in rows])

conn.execute("""
    COPY poverty_output TO 'intermediate/poverty_output.parquet' (FORMAT parquet)
""")

conn.execute("""
    COPY poverty_output TO 'intermediate/poverty_output.csv' (FORMAT csv, HEADER true)
""")

conn.close()
