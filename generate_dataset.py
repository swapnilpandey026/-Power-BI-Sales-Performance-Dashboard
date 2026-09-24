import csv, random, math
from datetime import date, timedelta

random.seed(42)

products = [
    ("Galaxy Pro X1","Electronics",24999),
    ("SmartWatch S5","Electronics",12999),
    ("AirBuds Ultra","Electronics",5999),
    ("LapBook Air","Electronics",54999),
    ("TabMax 12","Electronics",32999),
    ("Cotton Slim Fit Shirt","Apparel",1299),
    ("Running Shoes Pro","Apparel",3499),
    ("Formal Trousers","Apparel",1899),
    ("Winter Jacket","Apparel",4599),
    ("Sports Backpack","Apparel",1599),
    ("Instant Noodles Pack","FMCG",120),
    ("Protein Powder 1kg","FMCG",1899),
    ("Face Wash 200ml","FMCG",299),
    ("Hair Oil 500ml","FMCG",249),
    ("Sanitizer 500ml","FMCG",199),
    ("Office Chair","Furniture",8999),
    ("Study Table","Furniture",5999),
    ("Bookshelf 5-Tier","Furniture",3499),
    ("Sofa 3-Seater","Furniture",24999),
    ("Wardrobe 4-Door","Furniture",18999),
]

regions = {
    "North India": ["Delhi","Noida","Gurugram","Agra","Lucknow","Chandigarh","Jaipur"],
    "South India": ["Bengaluru","Chennai","Hyderabad","Kochi","Mysuru","Coimbatore"],
    "West India":  ["Mumbai","Pune","Ahmedabad","Surat","Nagpur","Nashik"],
    "East India":  ["Kolkata","Bhubaneswar","Patna","Guwahati","Ranchi"],
}
channels = ["Online","Offline","Partner"]
segments = ["Enterprise","SMB","Retail","New/Trial"]
seg_weights = [5,20,50,25]

rows = []
start = date(2026,1,1)
for i in range(10000):
    d = start + timedelta(days=random.randint(0,99))
    prod,cat,price = random.choice(products)
    region = random.choices(list(regions.keys()),weights=[35,25,30,10])[0]
    city = random.choice(regions[region])
    channel = random.choices(channels,weights=[55,30,15])[0]
    segment = random.choices(segments,weights=seg_weights)[0]
    qty = random.randint(1,5)
    discount = round(random.choice([0,0,0,5,10,15,20]),0)
    base = price*qty
    disc_amt = round(base*discount/100,2)
    revenue = round(base - disc_amt,2)
    margin_pct = round(random.uniform(22,48),1)
    profit = round(revenue*margin_pct/100,2)
    returned = random.choices([0,1],weights=[95,5])[0]
    rows.append([
        f"ORD-{100000+i}",
        d.strftime("%Y-%m-%d"),
        d.strftime("%B"), d.year, f"Q{math.ceil(d.month/3)}",
        prod, cat, price, qty, discount, disc_amt, revenue, margin_pct, profit,
        region, city, channel, segment,
        returned, f"CUST-{random.randint(1000,9999)}"
    ])

headers = [
    "OrderID","Date","Month","Year","Quarter",
    "Product","Category","UnitPrice","Quantity","Discount_Pct","Discount_Amt",
    "Revenue","Margin_Pct","Profit",
    "Region","City","Channel","Segment",
    "Returned","CustomerID"
]

with open("/home/claude/powerbi_project/data/sales_2026.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(headers)
    w.writerows(rows)

print(f"Generated {len(rows)} rows")
