import duckdb

print("=== COLUMN STRUCTURE ===")
print(duckdb.sql("DESCRIBE SELECT * FROM 'data/pp-2025.csv'"))

print("=== FIRST 5 ROWS ===")
print(duckdb.sql("SELECT * FROM 'data/pp-2025.csv' LIMIT 5"))

print("=== ROW COUNT ===")
print(duckdb.sql("SELECT COUNT(*) AS rows FROM 'data/pp-2025.csv'"))