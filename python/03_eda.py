import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
locations = pd.read_csv("data/raw/locations.csv")
orders = pd.read_csv("data/raw/orders.csv")
order_items = pd.read_csv("data/raw/order_items.csv")
dates = pd.read_csv("data/raw/dates.csv")

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

customers["customer_name"] = customers["customer_name"].str.strip()
customers["customer_segment"] = customers["customer_segment"].str.title()

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["shipping_date"] = pd.to_datetime(orders["shipping_date"])

dates["date"] = pd.to_datetime(dates["date"])

total_revenue = order_items["revenue"].sum()
print("\nTotal Revenue:", total_revenue)

total_profit = order_items["profit"].sum()
print("Total Profit:", total_profit)

total_orders = orders["order_id"].nunique()
print("Total Orders:", total_orders)

total_customers = customers["customer_id"].nunique()
print("Total Customers:", total_customers)

average_order_value = total_revenue / total_orders
print("Average Order Value:", average_order_value)

orders_status = orders[["order_id", "order_status"]].drop_duplicates()

order_items_status = order_items.merge(
    orders_status,
    on="order_id",
    how="left"
)

status_summary = (
    order_items_status
    .groupby("order_status")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nRevenue and Profit by Order Status:")
print(status_summary)

orders["order_date"] = pd.to_datetime(orders["order_date"])

order_items_year = order_items.merge(
    orders[["order_id", "order_date"]].drop_duplicates(),
    on="order_id",
    how="left"
)

order_items_year["year"] = order_items_year["order_date"].dt.year

yearly_summary = (
    order_items_year
    .groupby("year")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
)

print("\nRevenue and Profit by Year:")
print(yearly_summary)

yearly_summary["aov"] = (
    yearly_summary["revenue"]
    / yearly_summary["order_count"]
)

print("\nAverage Order Value by Year:")
print(yearly_summary[["revenue", "order_count", "aov"]])

order_items_year["year_month"] = (
    order_items_year["order_date"]
    .dt.to_period("M")
)

print("\nYear-Month column created:")
print(order_items_year[["order_date", "year_month"]].head())

monthly_summary = (
    order_items_year
    .groupby("year_month")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .reset_index()
)

print("\nMonthly Revenue, Profit and Orders:")
print(monthly_summary)

order_items_product = order_items.merge(
    products[[
        "product_id",
        "product_name",
        "category",
        "subcategory"
    ]],
    on="product_id",
    how="left"
)

print("\nOrder items connected with product information:")
print(
    order_items_product[
        ["product_id", "product_name", "category", "subcategory"]
    ].head()
)

category_summary = (
    order_items_product
    .groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nRevenue, Profit and Orders by Category:")
print(category_summary)

category_summary["profit_margin"] = (
    category_summary["profit"]
    / category_summary["revenue"]
    * 100
)

print("\nCategory Profit Margin:")
print(
    category_summary[
        ["revenue", "profit", "profit_margin"]
    ].sort_values("profit_margin", ascending=False)
)

product_summary = (
    order_items_product
    .groupby(
        ["product_id", "product_name", "category", "subcategory"]
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nProduct Revenue, Profit and Orders:")
print(product_summary.head(10))

product_summary["profit_margin"] = (
    product_summary["profit"]
    / product_summary["revenue"]
    * 100
)

product_margin_summary = (
    product_summary
    .reset_index()
    .sort_values("profit_margin", ascending=False)
)

print("\nProduct Profit Margin:")
print(
    product_margin_summary[
        ["product_name", "category", "revenue", "profit", "profit_margin"]
    ].head(10)
)

order_items_customer = (
    order_items
    .merge(
        orders[["order_id", "customer_id"]].drop_duplicates(),
        on="order_id",
        how="left"
    )
    .merge(
        customers[["customer_id", "customer_segment"]],
        on="customer_id",
        how="left"
    )
)

print("\nOrder items connected with customer information:")
print(
    order_items_customer[
        ["order_id", "customer_id", "customer_segment", "revenue", "profit"]
    ].head()
)

segment_summary = (
    order_items_customer
    .groupby("customer_segment")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique"),
        customer_count=("customer_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nRevenue, Profit, Orders and Customers by Segment:")
print(segment_summary)

segment_summary["revenue_per_customer"] = (
    segment_summary["revenue"]
    / segment_summary["customer_count"]
)

segment_summary["profit_per_customer"] = (
    segment_summary["profit"]
    / segment_summary["customer_count"]
)

print("\nCustomer Value by Segment:")
print(
    segment_summary[
        [
            "revenue",
            "profit",
            "customer_count",
            "revenue_per_customer",
            "profit_per_customer"
        ]
    ]
)

customer_summary = (
    order_items_customer
    .groupby(["customer_id", "customer_segment"])
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(customer_summary.head(10))

print("\nTop 10 Customers by Profit:")
print(
    customer_summary
    .sort_values("profit", ascending=False)
    .head(10)
)

order_items_location = (
    order_items
    .merge(
        orders[["order_id", "location_id"]].drop_duplicates(),
        on="order_id",
        how="left"
    )
    .merge(
        locations[
            ["location_id", "city", "state", "region"]
        ],
        on="location_id",
        how="left"
    )
)

print("\nGeographic data preview:")
print(order_items_location.head())

region_summary = (
    order_items_location
    .groupby("region")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nRevenue and Profit by Region:")
print(region_summary)

state_summary = (
    order_items_location
    .groupby("state")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nTop 10 States by Revenue:")
print(state_summary.head(10))

print("\nDiscount Distribution:")
print(
    order_items["discount"]
    .value_counts()
    .sort_index()
)

discount_summary = (
    order_items
    .groupby("discount")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        order_count=("order_id", "nunique"),
        item_count=("order_item_id", "count")
    )
    .sort_index()
)

discount_summary["profit_margin"] = (
    discount_summary["profit"]
    / discount_summary["revenue"]
    * 100
)

print("\nRevenue and Profit by Discount Level:")
print(discount_summary)

shipping_method_summary = (
    orders["shipping_method"]
    .value_counts()
    .sort_index()
)

print("\nShipping Method Distribution:")
print(shipping_method_summary)

shipping_analysis = orders[
    orders["shipping_date"].notna()
].copy()

shipping_analysis["delivery_days"] = (
    shipping_analysis["shipping_date"]
    - shipping_analysis["order_date"]
).dt.days

print("\nDelivery Time Preview:")
print(
    shipping_analysis[
        ["order_id", "shipping_method", "order_date",
         "shipping_date", "delivery_days"]
    ].head()
)

shipping_summary = (
    shipping_analysis
    .groupby("shipping_method")
    .agg(
        order_count=("order_id", "nunique"),
        average_delivery_days=("delivery_days", "mean"),
        minimum_delivery_days=("delivery_days", "min"),
        maximum_delivery_days=("delivery_days", "max")
    )
    .sort_values("average_delivery_days")
)

print("\nDelivery Time by Shipping Method:")
print(shipping_summary)

items_per_order = (
    order_items
    .groupby("order_id")
    .agg(
        total_items=("quantity", "sum"),
        item_lines=("order_item_id", "count")
    )
)

print("\nItems per Order Summary:")
print(items_per_order.describe())

normal_order_items = order_items[
    order_items["quantity"] != 99
]

normal_items_per_order = (
    normal_order_items
    .groupby("order_id")
    .agg(
        total_items=("quantity", "sum"),
        item_lines=("order_item_id", "count")
    )
)

print("\nNormal Items per Order Summary:")
print(normal_items_per_order.describe())

order_items["quantity_outlier"] = order_items["quantity"] == 99

expected_revenue = (
    order_items["quantity"]
    * order_items["unit_price"]
    * (1 - order_items["discount"])
)

order_items["revenue_check"] = (
    abs(order_items["revenue"] - expected_revenue) <= 0.01
)

order_items_with_cost = order_items.merge(
    products[["product_id", "unit_cost"]],
    on="product_id",
    how="left"
)

expected_profit = (
    order_items_with_cost["revenue"]
    - (
        order_items_with_cost["quantity"]
        * order_items_with_cost["unit_cost"]
    )
    - order_items_with_cost["shipping_cost"]
)

order_items["profit_check"] = (
    abs(order_items["profit"] - expected_profit) <= 0.01
)

anomaly_summary = order_items[
    (order_items["quantity_outlier"]) |
    (~order_items["revenue_check"]) |
    (~order_items["profit_check"])
]

print("\nFinal Anomaly Summary:")
print("Anomalous order-item records:", len(anomaly_summary))

print("\nAnomalous Records:")
print(
    anomaly_summary[
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "revenue",
            "profit",
            "quantity_outlier",
            "revenue_check",
            "profit_check"
        ]
    ]
)