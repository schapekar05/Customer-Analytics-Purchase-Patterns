from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "transactions.csv", parse_dates=["order_date"])

delivered = df[df["order_status"].eq("Delivered")].copy()
net_revenue = df["net_revenue"].sum()
completed_orders = delivered["order_id"].nunique()
unique_customers = delivered["customer_id"].nunique()
aov = net_revenue / completed_orders if completed_orders else 0
customer_orders = delivered.groupby("customer_id")["order_id"].nunique()
repeat_customers = int((customer_orders > 1).sum())
repeat_rate = repeat_customers / unique_customers if unique_customers else 0

print("CUSTOMER ANALYTICS - EXECUTIVE KPIs")
print(f"Delivered orders: {completed_orders:,}")
print(f"Purchasing customers: {unique_customers:,}")
print(f"Net revenue: {net_revenue:,.2f}")
print(f"Average order value: {aov:,.2f}")
print(f"Repeat customers: {repeat_customers:,}")
print(f"Repeat customer rate: {repeat_rate:.1%}")

monthly = df.set_index("order_date").resample("MS")["net_revenue"].sum()
category = df.groupby("category", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=True)
product = df.groupby("product_name", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
customer = delivered.groupby("customer_id").agg(
    frequency=("order_id", "nunique"), monetary=("net_revenue", "sum"), last_purchase=("order_date", "max")
)
snapshot = df["order_date"].max() + pd.Timedelta(days=1)
customer["recency_days"] = (snapshot - customer["last_purchase"]).dt.days
customer["segment"] = pd.qcut(customer["monetary"].rank(method="first"), 4,
                              labels=["Low value", "Mid value", "High value", "Top value"])

print("\nCATEGORY PERFORMANCE")
print(category.sort_values("net_revenue", ascending=False).to_string(index=False))
print("\nCUSTOMER SEGMENTS")
print(customer["segment"].value_counts().to_string())

out = ROOT / "visuals"
out.mkdir(exist_ok=True)
plt.figure(figsize=(10, 5))
monthly.plot(marker="o")
plt.title("Monthly Net Revenue")
plt.xlabel("Month")
plt.ylabel("Net revenue")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(out / "monthly_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
plt.barh(category["category"], category["net_revenue"])
plt.title("Net Revenue by Category")
plt.xlabel("Net revenue")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(out / "category_revenue.png", dpi=160)
plt.close()

customer.reset_index().to_csv(out / "customer_segments.csv", index=False)
product.to_csv(out / "product_performance.csv", index=False)
print(f"\nAnalysis outputs saved to: {out}")
