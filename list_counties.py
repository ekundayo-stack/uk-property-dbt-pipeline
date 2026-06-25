import duckdb

con = duckdb.connect('dev.duckdb')

rows = con.sql("""
    SELECT county, SUM(number_of_sales) AS total_sales
    FROM avg_price_by_county_year
    GROUP BY county
    ORDER BY county
""").fetchall()

con.close()

for county, sales in rows:
    print(f"{county} | {sales:,}")

print(f"\nTotal counties: {len(rows)}")