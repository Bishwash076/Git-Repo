import duckdb

con = duckdb.connect()
results = con.execute("SELECT * FROM delta_scan('s3a://lake/gold') LIMIT 5").fetchall()
print(results)
