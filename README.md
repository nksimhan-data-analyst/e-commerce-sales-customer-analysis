# E-Commerce Sales & Customer Analysis

## Project Overview

This project analyzes a synthetic e-commerce dataset covering orders, customers, products, locations, dates, revenue, discounts, profit, and shipping information from 2023 to 2025.

The objective is to transform raw transactional data into actionable business insights using Python, SQL, and Power BI.

The analysis focuses on:

- Revenue and profit performance
- Yearly and monthly sales trends
- Product and category performance
- Customer segment behavior and value
- Geographic sales distribution
- Discount and profitability relationships
- Shipping-method performance
- Data-quality validation and anomaly detection

The final deliverable is an interactive four-page Power BI dashboard containing 28 analytical visuals and page-level slicers for interactive exploration.

## Key Business Insights

- Recorded revenue increased substantially from 2023 to 2025, rising from approximately ₹9.42 crore in 2023 to ₹37.57 crore in 2025.
- Order volume increased from 3,323 orders in 2023 to 13,696 orders in 2025, while Average Order Value remained relatively stable at around ₹27,000–₹28,000.
- Electronics generated the highest recorded revenue among the product categories, while categories such as Beauty, Toys, and Fashion showed substantially higher profit margins.
- Premium customers had the highest revenue per customer among the defined customer segments, followed by Loyal and Regular customers.
- The South region generated the highest recorded revenue among the six regions in the dataset.
- Maharashtra recorded the highest state-level revenue, followed by Gujarat and Tamil Nadu.
- Recorded profit margin declined as discount levels increased, with the 25% and 30% discount groups showing negative recorded profit.
- Standard shipping accounted for the largest number of orders and had the longest average order-to-shipping interval, while Same Day shipping had an average interval of 0 days.
- A relatively small group of products contributed heavily to total recorded revenue, highlighting the importance of product-level performance monitoring.
- Data-quality validation identified three quantity outliers and three intentional revenue/profit discrepancies; these anomalies were preserved and flagged rather than overwritten.

## Methodology

The project followed a structured data analytics workflow:

1. **Data Inspection** — Examined the raw datasets, schemas, data types, missing values, duplicates, relationships, and foreign-key integrity.
2. **Data Cleaning** — Standardized text fields, removed exact duplicate order records, converted date fields, and identified data-quality anomalies.
3. **Exploratory Data Analysis** — Used Python and pandas to analyze revenue, profit, orders, customers, products, categories, geography, discounts, and shipping performance.
4. **SQL Business Analysis** — Used DuckDB to perform business-focused queries directly against the local CSV datasets.
5. **Data Modeling** — Built a relational Power BI model connecting orders, order items, customers, products, locations, and dates.
6. **DAX Analysis** — Created measures for revenue, profit, orders, ordering customers, Average Order Value, profit margin, category orders, and product profit margin.
7. **Dashboard Development** — Built a four-page Power BI report containing 28 visuals and interactive slicers.
8. **Validation & QA** — Cross-checked key metrics and tested filters/interactions across all report pages.

## Data Quality & Cleaning

The raw dataset was validated before analysis. The following issues were identified and handled:

| Issue | Count | Action |
|---|---:|---|
| Duplicate order records | 3 | Removed exact duplicate rows |
| Missing customer segments | 5 | Preserved as missing values; no unsupported segment was inferred |
| Customer-name whitespace issues | 15 | Removed leading/trailing whitespace |
| Inconsistent customer-segment casing | 10 | Standardized segment values |
| Inconsistent product-name casing | 8 | Standardized product names |
| Quantity outliers | 3 | Flagged for review; original values preserved |
| Revenue discrepancies | 3 | Flagged; original revenue values preserved |
| Profit discrepancies | 3 | Flagged; original profit values preserved |
| Invalid foreign-key relationships | 0 | No correction required |
| Invalid product pricing relationships | 0 | No correction required |
| Invalid shipping-date relationships | 0 | No correction required |
| Missing shipping dates | 2,506 | Preserved because they correspond to cancelled/processing orders |

### Data Quality Notes

The dataset contains intentionally introduced data-quality issues for analytical practice. Financial and quantity anomalies were not overwritten because their correct replacement values could not be reliably determined. Instead, they were identified and retained as documented data-quality exceptions.

Customer records with missing segments were also preserved rather than assigning segments based on assumptions.

The dataset is synthetic and intended for educational and portfolio purposes.

## Tools & Technology

- **Python** — Data cleaning, validation, exploratory data analysis, and anomaly detection
- **Pandas** — Data manipulation and analysis
- **DuckDB** — SQL-based business analysis directly over local CSV files
- **Power BI** — Data modeling, DAX measures, interactive dashboard development, and visualization
- **DAX** — KPI and analytical measure creation
- **Excel** — Initial data inspection and spreadsheet-based analysis
- **Cursor IDE** — Project development, code organization, documentation, and workflow management
- **Git / GitHub** — Version control and portfolio presentation

## Project Structure

```text
E-Commerce-Sales-Customer-Analysis/
│
├── data/
│   └── raw/
│       ├── customers.csv
│       ├── products.csv
│       ├── locations.csv
│       ├── orders.csv
│       ├── order_items.csv
│       └── dates.csv
│
├── python/
│   ├── 01_raw_data_inspection.py
│   ├── 02_data_cleaning.py
│   ├── 03_eda.py
│   └── 04_sql_analysis.py
│
├── sql/
│   └── 01_business_analysis.sql
│
├── powerbi/
│   └── E-Commerce_Sales_Customer_Analysis.pbix
│
├── docs/
│
├── PROJECT_SCOPE.md
└── README.md

## Business Questions

The analysis was designed to answer the following business questions:

1. How has revenue and profit changed over time?
2. Which product categories generate the most revenue and profit?
3. Which products are the strongest performers by revenue and profit margin?
4. How do different customer segments contribute to revenue and profitability?
5. Which customers generate the highest revenue?
6. Which regions and states contribute the most revenue?
7. How does discount level relate to recorded profit and profit margin?
8. Which shipping methods account for the most orders and revenue?
9. How long does each shipping method take from order date to shipping date?
10. What data-quality issues exist in the transactional dataset?

## Dashboard Overview

The final Power BI report contains four analytical pages with 28 visuals.

### Page 1 — Executive Overview

Provides a high-level view of overall business performance through:

- Total Revenue
- Total Profit
- Total Orders
- Ordering Customers
- Average Order Value
- Profit Margin
- Revenue by Year
- Revenue by Category
- Revenue by Region

### Page 2 — Product & Customer Performance

Focuses on product profitability, product revenue, customer segments, and monthly performance:

- Profit by Category
- Orders by Category
- Top 10 Products by Revenue
- Top 10 Products by Profit Margin
- Monthly Revenue Trend
- Revenue, Profit, and Profit Margin by Customer Segment
- Revenue, Orders, and Profit by Customer Segment

### Page 3 — Customer & Geographic Analysis

Examines customer value and geographic distribution:

- Revenue by Customer Segment
- Profit by Customer Segment
- Top 10 Customers by Revenue
- Revenue by Region
- Revenue by State using an India Shape Map
- Ordering Customers by Region

### Page 4 — Discount & Shipping Analysis

Analyzes the relationship between discounts, profitability, and shipping performance:

- Revenue by Discount Level
- Profit Margin by Discount Level
- Profit by Discount Level
- Revenue by Shipping Method
- Orders by Shipping Method
- Average Shipping Days by Shipping Method

### Interactive Filters

The report includes page-level slicers for:

- Year
- Customer Segment
- Region
- Category
- Discount Level
- Shipping Method

These allow users to explore the dashboard dynamically without changing the underlying analysis.

## Limitations & Assumptions

- The dataset is synthetic and was created for educational and portfolio purposes. The findings should not be interpreted as real-world e-commerce market results.
- Revenue and profit measures are based on the recorded transaction values in the dataset. Cancelled and returned orders are present in the source data, so these figures should not automatically be interpreted as realized net sales.
- Three quantity outliers with a quantity value of 99 were identified. They were flagged but not overwritten because the correct quantities could not be determined reliably.
- Three intentional revenue discrepancies and three corresponding profit discrepancies were identified and preserved as data-quality exceptions.
- Five customers have missing customer-segment values. These were retained as missing rather than assigning a segment without sufficient evidence.
- Shipping duration represents the number of days between the order date and shipping date, not the customer's actual delivery time.
- Relationships between discount levels and profitability are observational. The analysis does not establish that discounts directly caused changes in profit.
- Dashboard metrics depend on the available fields and business definitions in the synthetic dataset.

## How to Run

### 1. Clone the repository

git clone github.com/nksimhan-data-analyst/e-commerce-sales-customer-analysis
cd E-Commerce-Sales-Customer-Analysis

pip install pandas duckdb

python python/01_raw_data_inspection.py
python python/02_data_cleaning.py
python python/03_eda.py
python python/04_sql_analysis.py

powerbi/E-Commerce_Sales_Customer_Analysis.pbix

## Skills Demonstrated

- Data inspection and validation
- Data cleaning and preprocessing
- Missing-value and duplicate handling
- Data-quality and anomaly detection
- Exploratory Data Analysis (EDA)
- Business-oriented SQL analysis
- Relational data modeling
- DAX measure development
- KPI design
- Interactive Power BI dashboard development
- Business insight generation
- Analytical documentation
- Reproducible analytics workflow

## Project Outcome

This project demonstrates an end-to-end data analytics workflow, starting from raw transactional data and progressing through validation, cleaning, exploratory analysis, SQL-based business analysis, data modeling, DAX development, and interactive Power BI visualization.

The final deliverable combines technical analysis with business-oriented storytelling and provides an interactive framework for exploring sales, customers, products, geography, discounts, profitability, and shipping performance.