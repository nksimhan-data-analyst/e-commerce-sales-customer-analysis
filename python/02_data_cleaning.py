import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
locations = pd.read_csv("data/raw/locations.csv")
orders = pd.read_csv("data/raw/orders.csv")
order_items = pd.read_csv("data/raw/order_items.csv")
dates = pd.read_csv("data/raw/dates.csv")

customers["customer_name"] = customers["customer_name"].str.strip()
customers["customer_segment"] = customers["customer_segment"].str.title()
print("Customer segment capitalization standardized.")
missing_segments = customers[customers["customer_segment"].isna()]
print("\nCustomers with missing segments:")
print(missing_segments)
missing_customer_ids = missing_segments["customer_id"]
missing_customer_orders = orders[
    orders["customer_id"].isin(missing_customer_ids)
]
print("Order history for customers with missing segments:")
print(
    missing_customer_orders[
        ["order_id", "customer_id", "order_date", "order_status"]
    ].sort_values(["customer_id", "order_date"])
)
print(
    "\nMissing customer segments after cleaning:",
    customers["customer_segment"].isna().sum()
)

lowercase_products = products[
    products["product_name"] == products["product_name"].str.lower()
]

print("\nProducts with lowercase names:")
print(lowercase_products[["product_id", "product_name"]])

products["product_name"] = products["product_name"].str.title()
print(
    "Lowercase product names after cleaning:",
    (products["product_name"] == products["product_name"].str.lower()).sum()
)
duplicate_orders = orders[orders.duplicated(keep=False)]

print("\nDuplicate order rows:")
print(duplicate_orders)

orders = orders.drop_duplicates()

print("Rows after removing duplicates:", len(orders))
print("Unique order IDs:", orders["order_id"].nunique())
print("\nMissing shipping dates after cleaning:")
print(orders["shipping_date"].isna().sum())

print("\nMissing shipping dates by order status:")
print(
    orders.groupby("order_status")["shipping_date"]
    .apply(lambda x: x.isna().sum())
)

quantity_outliers = order_items[order_items["quantity"] == 99]

print("\nQuantity outliers:")
print(quantity_outliers)

outlier_products = products[
    products["product_id"].isin(quantity_outliers["product_id"])
]

print("\nProducts associated with quantity outliers:")
print(
    outlier_products[
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "unit_cost",
            "unit_price"
        ]
    ]
)

quantity_outliers = order_items[order_items["quantity"] == 99].copy()

quantity_outliers["expected_revenue"] = (
    quantity_outliers["quantity"]
    * quantity_outliers["unit_price"]
    * (1 - quantity_outliers["discount"])
)

print("\nQuantity outliers with revenue validation:")
print(
    quantity_outliers[
        [
            "order_item_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "revenue",
            "expected_revenue"
        ]
    ]
)

order_items_with_cost = order_items.merge(
    products[["product_id", "unit_cost"]],
    on="product_id",
    how="left"
)

order_items_with_cost["expected_profit"] = (
    order_items_with_cost["revenue"]
    - (
        order_items_with_cost["quantity"]
        * order_items_with_cost["unit_cost"]
    )
    - order_items_with_cost["shipping_cost"]
)

profit_discrepancies = order_items_with_cost[
    abs(
        order_items_with_cost["profit"]
        - order_items_with_cost["expected_profit"]
    ) > 0.01
]

print("\nProfit discrepancies:")
print(
    profit_discrepancies[
        [
            "order_item_id",
            "product_id",
            "quantity",
            "revenue",
            "unit_cost",
            "shipping_cost",
            "profit",
            "expected_profit"
        ]
    ]
)

print("\nNumber of profit discrepancies:", len(profit_discrepancies))

order_items["quantity_outlier"] = order_items["quantity"] == 99

expected_revenue = (
    order_items["quantity"]
    * order_items["unit_price"]
    * (1 - order_items["discount"])
)

order_items["revenue_check"] = (
    abs(order_items["revenue"] - expected_revenue) <= 0.01
)

print(
    "\nQuantity outliers flagged:",
    order_items["quantity_outlier"].sum()
)

print(
    "Revenue discrepancies flagged:",
    (~order_items["revenue_check"]).sum()
)

order_items["profit_check"] = order_items_with_cost["profit"].sub(
    order_items_with_cost["expected_profit"]
).abs() <= 0.01

print(
    "Profit discrepancies flagged:",
    (~order_items["profit_check"]).sum()
)

dates["date"] = pd.to_datetime(dates["date"])

print("\nDate column type after conversion:")
print(dates["date"].dtype)

print("\nMonth representations:")
print(dates[["date", "month", "month_number", "month_name"]].head(15))

print(
    "Month consistency:",
    (
        dates["month_number"]
        == dates["date"].dt.month
    ).all()
)

print(
    "Full month-name consistency:",
    (
        dates["month"]
        == dates["date"].dt.month_name()
    ).all()
)

print(
    "Abbreviated month-name consistency:",
    (
        dates["month_name"]
        == dates["date"].dt.strftime("%b")
    ).all()
)

expected_days = (
    dates["date"].max() - dates["date"].min()
).days + 1

print("\nExpected number of days:", expected_days)
print("Actual number of dates:", dates["date"].nunique())

print(
    "Continuous date range:",
    expected_days == dates["date"].nunique()
)

customers["signup_date"] = pd.to_datetime(customers["signup_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["shipping_date"] = pd.to_datetime(orders["shipping_date"])

print("\nDate column types:")
print("Customer signup_date:", customers["signup_date"].dtype)
print("Order order_date:", orders["order_date"].dtype)
print("Order shipping_date:", orders["shipping_date"].dtype)

print("\n" + "=" * 60)
print("FINAL CLEANING VALIDATION")
print("=" * 60)

print("\nCustomers")
print("Missing segments:", customers["customer_segment"].isna().sum())
print(
    "Whitespace issues:",
    (customers["customer_name"] != customers["customer_name"].str.strip()).sum()
)

print("\nProducts")
print(
    "Lowercase product names:",
    (products["product_name"] == products["product_name"].str.lower()).sum()
)

print("\nOrders")
print("Rows:", len(orders))
print("Unique order IDs:", orders["order_id"].nunique())
print("Duplicate rows:", orders.duplicated().sum())
print("Missing shipping dates:", orders["shipping_date"].isna().sum())

print("\nOrder Items")
print("Quantity outliers:", order_items["quantity_outlier"].sum())
print("Revenue discrepancies:", (~order_items["revenue_check"]).sum())
print("Profit discrepancies:", (~order_items["profit_check"]).sum())

print("\nDates")
print("Unique dates:", dates["date"].nunique())
print("Date range:", dates["date"].min(), "to", dates["date"].max())