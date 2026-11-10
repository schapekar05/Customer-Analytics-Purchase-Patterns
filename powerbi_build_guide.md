# Power BI Dashboard Build Guide

## Data model
Import `data/transactions.csv` and rename the table to `Transactions`.
Set `order_date` to Date, `net_revenue` and `unit_price` to Decimal Number, and `quantity` to Whole Number.

## DAX measures
```DAX
Delivered Orders =
CALCULATE(COUNTROWS(Transactions), Transactions[order_status] = "Delivered")

Net Revenue = SUM(Transactions[net_revenue])

Purchasing Customers =
CALCULATE(DISTINCTCOUNT(Transactions[customer_id]), Transactions[order_status] = "Delivered")

AOV = DIVIDE([Net Revenue], [Delivered Orders])

Repeat Customers =
COUNTROWS(
    FILTER(
        VALUES(Transactions[customer_id]),
        CALCULATE([Delivered Orders]) > 1
    )
)

Repeat Customer % = DIVIDE([Repeat Customers], [Purchasing Customers])
```

## Recommended report pages
1. **Executive Overview:** cards for Net Revenue, Delivered Orders, Purchasing Customers, AOV and Repeat Customer %; monthly revenue line chart; revenue by category bar chart.
2. **Customer Insights:** customer order frequency distribution, repeat vs one-time customer split, top customers by revenue, city performance.
3. **Product Performance:** category/product revenue, units sold, payment method and acquisition channel.

## Interactions
Add slicers for order date, city, category, acquisition channel and payment method. Enable cross-filtering and use informative titles/tooltips.

## Validation
Reconcile Power BI Net Revenue and Delivered Orders to the Python/SQL outputs. Explain that cancelled and returned orders have zero net revenue. Do not interpret synthetic results as real-world findings.
