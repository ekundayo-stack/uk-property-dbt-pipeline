import os
import re
import sys
import duckdb
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Choose the region (default to London if none given) ---
region = sys.argv[1] if len(sys.argv) > 1 else "London"

# --- Stage 1 & 2: pull that region's real numbers ---
# Find dev.duckdb relative to this script's own location, not where it's run from
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'dev.duckdb')
con = duckdb.connect(db_path)

rows = con.sql(f"""
    SELECT sale_year, total_sales, avg_price
    FROM avg_price_by_region_year
    WHERE region = ?
    ORDER BY sale_year
""", params=[region]).fetchall()

con.close()

if not rows:
    print(f"No data found for region '{region}'. Check the spelling.")
    sys.exit()

data_block = f"Property market figures for {region}, by year:\n"
allowed_numbers = set()
for year, sales, price in rows:
    data_block += f"- {year}: {sales:,} sales, average price GBP {price:,.0f}\n"
    allowed_numbers.add(int(year))
    allowed_numbers.add(int(sales))
    allowed_numbers.add(int(price))

# --- Stage 3: hand to Gemini with guardrails ---
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_rules = f"""You are a UK property market analyst writing a short briefing about {region}.

STRICT RULES:
- Use ONLY the figures provided in the data. Do not invent, estimate, or add any number that is not explicitly given.
- If you mention a figure, it must match the data exactly.
- Do not reference any year, region, or statistic that is not in the data.
- All figures provided are ACTUAL RECORDED sales, not forecasts. Never describe any year as a projection, forecast, or estimate.
- Do not speculate about the future or use phrases like "looking ahead" or "projections indicate".
- This briefing is specifically about {region}. Do not compare to other regions, as you do not have their data here.
- Write in clear, professional prose. No bullet points.
- Keep it to three short paragraphs.
- If you cannot support a claim with the provided data, do not make the claim."""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Here is the data:\n\n{data_block}\n\nWrite the briefing.",
    config=types.GenerateContentConfig(
        system_instruction=system_rules,
        temperature=0.2,
    ),
)

report_text = response.text
print(f"=== AI BRIEFING: {region} ===\n")
print(report_text)

# --- Stage 4: automated number verification ---
def verify_numbers(text, allowed):
    found = re.findall(r'\d[\d,]*', text)
    flagged = [t for t in found if int(t.replace(',', '')) not in allowed]
    return flagged

flagged = verify_numbers(report_text, allowed_numbers)

print("\n=== NUMBER VERIFICATION ===")
if flagged:
    print("VERIFICATION FAILED. These numbers are NOT in the source data:")
    for f in flagged:
        print(f"   - {f}")
else:
    print("VERIFICATION PASSED. Every number matches the source data.")

# --- Stage 5: save to Markdown (only if verified) ---
if not flagged:
    timestamp = datetime.now().strftime("%Y-%m-%d")
    safe_region = region.replace(" ", "_")
    filename = f"report_{safe_region}_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Property Market Briefing: {region}\n\n")
        f.write(f"*Generated {timestamp} from HM Land Registry data (2020 to 2025).*\n\n")
        f.write("*Every figure was automatically verified against the source pipeline.*\n\n")
        f.write("---\n\n")
        f.write(report_text)
    print(f"\nReport saved to {filename}")
else:
    print("\nReport NOT saved (verification failed).")