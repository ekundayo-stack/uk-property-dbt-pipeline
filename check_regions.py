import duckdb

con = duckdb.connect('dev.duckdb')

# Find any county in the sales data that has NO matching region in the seed
unmatched = con.sql("""
    SELECT DISTINCT s.county
    FROM avg_price_by_county_year s
    LEFT JOIN county_region r
        ON s.county = r.county
    WHERE r.region IS NULL
""").fetchall()

con.close()

if unmatched:
    print("UNMATCHED counties (no region found):")
    for row in unmatched:
        print(f"   - {row[0]}")
else:
    print("All counties matched to a region. Mapping is complete.")