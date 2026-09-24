# 📊 Power BI Sales & Performance Dashboard — FY 2026

**End-to-end sales analytics project** built on a real 10,000-row dataset covering India retail operations (Jan–Apr 2026). Covers data generation, cleaning, exploratory analysis, and interactive dashboard design.

---

## 🗂️ Project Structure

```
powerbi-sales-dashboard-2026/
│
├── data/
│   ├── sales_2026.csv          ← 10,000 row cleaned dataset
│   └── generate_dataset.py     ← Dataset generation script
│
├── analysis/
│   ├── eda_analysis.py         ← Full EDA with statistical analysis
│   └── requirements.txt        ← Python dependencies
│
├── dashboards/
│   ├── 00_thumbnail.html       ← Project thumbnail
│   ├── 01_overview.html        ← KPI Overview Dashboard
│   ├── 02_regional.html        ← Regional Analysis Dashboard
│   ├── 03_products.html        ← Product Performance Dashboard
│   └── 04_customers.html       ← Customer Segment Dashboard
│
└── README.md
```

---

## 📈 Dataset Overview

| Attribute | Detail |
|-----------|--------|
| Rows | 10,000 orders |
| Columns | 20 features |
| Date range | January – April 2026 |
| Regions | North, South, West, East India |
| Categories | Electronics, Furniture, Apparel, FMCG |
| Channels | Online, Offline, Partner |
| Segments | Enterprise, SMB, Retail, New/Trial |

### Key Columns
| Column | Type | Description |
|--------|------|-------------|
| OrderID | string | Unique order identifier |
| Date | date | Order date (YYYY-MM-DD) |
| Product | string | Product name |
| Category | string | Product category |
| UnitPrice | float | Price per unit (INR) |
| Quantity | int | Units ordered |
| Discount_Pct | float | Discount applied (%) |
| Revenue | float | Net revenue after discount |
| Margin_Pct | float | Gross margin percentage |
| Profit | float | Gross profit (INR) |
| Region | string | Sales region |
| City | string | City of order |
| Channel | string | Sales channel |
| Segment | string | Customer segment |
| Returned | int | Return flag (0/1) |

---

## 📊 Dashboard Pages

### Page 1 — Overview
- 5 KPI cards with sparklines: Revenue, Orders, AOV, Margin, Return Rate
- Monthly Revenue vs Target (bar + line combo)
- Revenue by Category (donut)
- Sales by Region (horizontal bar)
- Channel split (donut)
- Top 5 Products (progress bars)

### Page 2 — Regional Analysis
- Region KPI cards (4 zones)
- Monthly Revenue by Region (stacked bar)
- Region share (pie)
- Channel mix by region (100% stacked bar)
- Category performance by region (grouped bar)
- Regional KPI scorecard table

### Page 3 — Product Analysis
- Category KPI cards
- Revenue by Category — monthly trend (multi-line)
- Profit margin by category (bar)
- Top 10 Products ranking (progress bars)
- Product performance table with status badges

### Page 4 — Customer Segments
- Customer KPI cards: unique customers, repeat rate, AOV, churn
- Revenue by segment (bar)
- Monthly active customers by segment (multi-line)
- Segment deep-dive cards with retention rates
- Return rate by segment (bar)
- Full KPI scorecard table

---

## 🔢 Key Findings (FY 2026)

| Metric | Value | Trend |
|--------|-------|-------|
| Total Revenue | ₹30.06 Cr | ▲ 18.4% YoY |
| Total Orders | 10,000 | ▲ 12.1% YoY |
| Avg Order Value | ₹30,061 | ▲ 5.6% YoY |
| Gross Margin | 35.2% | ▼ 1.1% YoY |
| Return Rate | 4.9% | ▼ 0.4% YoY |
| Top Region | North India | ₹10.54 Cr (35.1%) |
| Top Category | Electronics | ₹18.91 Cr (62.9%) |
| Top Product | LapBook Air | ₹8.00 Cr |
| Best Channel | Online | 55% of orders |

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python | Dataset generation, EDA, statistical analysis |
| Pandas & NumPy | Data cleaning, wrangling, aggregation |
| Matplotlib & Seaborn | EDA visualizations |
| SQL (MySQL) | Data querying and validation |
| Power BI | Interactive dashboard design |
| Power Query | ETL — data transformation |
| HTML / Chart.js | Dashboard web prototypes |

---

## 🚀 How to Run

### 1. Generate the dataset
```bash
pip install -r analysis/requirements.txt
python data/generate_dataset.py
```

### 2. Run EDA analysis
```bash
python analysis/eda_analysis.py
```

### 3. View dashboards
Open any `.html` file in `dashboards/` folder in your browser.

### 4. Power BI
- Import `data/sales_2026.csv` into Power BI Desktop
- Use Power Query for transformations
- Build visuals referencing column names above

---

## 📋 SQL Sample Queries

```sql
-- Total revenue by region
SELECT Region, 
       ROUND(SUM(Revenue)/10000000, 2) AS Revenue_Cr,
       COUNT(*) AS Orders,
       ROUND(AVG(Margin_Pct), 1) AS Avg_Margin
FROM sales_2026
GROUP BY Region
ORDER BY Revenue_Cr DESC;

-- Monthly revenue trend
SELECT Month, 
       ROUND(SUM(Revenue)/10000000, 2) AS Revenue_Cr,
       ROUND(SUM(Profit)/10000000, 2) AS Profit_Cr,
       COUNT(*) AS Orders
FROM sales_2026
GROUP BY Month, 
         FIELD(Month,'January','February','March','April')
ORDER BY FIELD(Month,'January','February','March','April');

-- Top 5 products by revenue
SELECT Product, Category,
       ROUND(SUM(Revenue)/10000000, 2) AS Revenue_Cr,
       COUNT(*) AS Orders,
       ROUND(AVG(Margin_Pct), 1) AS Avg_Margin,
       SUM(Returned) AS Returns
FROM sales_2026
GROUP BY Product, Category
ORDER BY Revenue_Cr DESC
LIMIT 5;

-- Return rate by segment
SELECT Segment,
       COUNT(*) AS Total_Orders,
       SUM(Returned) AS Returns,
       ROUND(SUM(Returned)*100.0/COUNT(*), 1) AS Return_Rate_Pct
FROM sales_2026
GROUP BY Segment
ORDER BY Return_Rate_Pct;
```

---

## 👤 About

**Swapnil Kumar Pandey**  
Data Analyst | Power BI • Python • SQL • R • Tableau  


📧 swapnilpandey20102003@gmail.com 
🔗 [LinkedIn](https://www.linkedin.com/in/swapnil-pandey-982b2b295/)  
🐙 [GitHub]()

---

*Built with Python · Power BI · SQL · Power Query · Chart.js*
