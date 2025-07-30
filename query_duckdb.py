import duckdb

# Load HTTPFS extension
con = duckdb.connect()
con.install_extension("httpfs")
con.load_extension("httpfs")

# If your MinIO or S3 is not public, you'll also need to set credentials
# con.execute("SET s3_access_key_id='<YOUR_MINIO_ACCESS_KEY>'")
# con.execute("SET s3_secret_access_key='<YOUR_MINIO_SECRET_KEY>'")
# con.execute("SET s3_endpoint='http://127.0.0.1:9000'")  # Change to your actual MinIO endpoint

# Run your query
result = con.execute("SELECT * FROM delta_scan('s3a://lake/gold') LIMIT 5").fetchdf()
print(result)
