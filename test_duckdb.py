# test_duckdb.py
import duckdb

con = duckdb.connect()
results = con.execute("SELECT 42;").fetchall()
print(results)
