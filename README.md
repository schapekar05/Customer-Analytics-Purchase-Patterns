# Customer Analytics & Purchase Pattern Analysis

A portfolio project demonstrating transaction-level analytics using a reproducible synthetic e-commerce dataset, Python, SQL and Power BI.

## Business objective
Understand customer purchasing behaviour, revenue performance, product/category contribution and repeat-purchase patterns to support commercial decisions.

## Dataset
- `data/transactions.csv`: 5,000 synthetic order records across 850 generated customer IDs.
- Coverage: 1 Jan–31 Dec 2025.
- Fields include order/customer IDs, date, category, product, quantity, unit price, discount, net revenue, order status, city, payment method and acquisition channel.
- This is **synthetic practice data**, not actual company/customer information. Revenue is set to zero for cancelled and returned orders.

## Project questions
1. What are total orders, net revenue, unique customers and average order value?
2. How does revenue trend month over month?
3. Which categories and products contribute most to revenue?
4. What share of customers purchase more than once?
5. Which customers are high-value based on recency, frequency and monetary value (RFM)?
6. How do payment methods, cities and acquisition channels differ?

## Repository structure
```text
Customer-Analytics-Purchase-Patterns/
├── data/transactions.csv
├── notebooks/customer_analysis.ipynb
├── sql/analysis_queries.sql
├── src/analyze.py
├── dashboard/powerbi_build_guide.md
├── visuals/
├── requirements.txt
└── README.md
```

## Run locally
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py
```
Open `notebooks/customer_analysis.ipynb` in Jupyter or VS Code to explore the analysis.

## Power BI
Import `data/transactions.csv`. Follow `dashboard/powerbi_build_guide.md` for suggested measures, visuals and interactions. Save your finished report as `dashboard/customer_analytics_dashboard.pbix`.

## Data quality and metric definitions
- **Net revenue:** sum of `net_revenue`; cancelled and returned orders contribute zero.
- **Completed orders:** orders with status `Delivered`.
- **AOV:** net revenue divided by delivered order count. State the denominator clearly when presenting this KPI.
- **Repeat customer:** customer with more than one delivered order.
- **RFM:** calculated using delivered orders only; snapshot date is one day after the maximum order date in the dataset.

## Important
The generated dataset and all findings are for portfolio demonstration only. Do not present synthetic metrics as real business results or claim business impact that was not measured.
