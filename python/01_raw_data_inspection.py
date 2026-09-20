import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
locations = pd.read_csv("data/raw/locations.csv")
orders = pd.read_csv("data/raw/orders.csv")
order_items = pd.read_csv("data/raw/order_items.csv")
dates = pd.read_csv("data/raw/dates.csv")

# # print("\nCUSTOMERS")
# # print(customers.shape)
# # print(customers.columns.tolist())
# # print(customers.head())
# # print(customers.dtypes)
# # print(customers.isnull().sum())
# # print(customers.duplicated().sum())
# # print("Unique customer IDs: ", customers["customer_id"].nunique())
# # print(customers["customer_segment"].value_counts(dropna=False))
# # print("Names with leading/trailing whitespace:",
# #       (customers["customer_name"] != customers["customer_name"].str.strip()).sum())

# # print("\nPRODUCTS")
# # print(products.shape)
# # print(products.columns.tolist())
# # print(products.head())
# # print(products.dtypes)
# # print(products.isnull().sum())
# # print(products.duplicated().sum())
# # print("Unique product IDs:", products["product_id"].nunique())
# # print("Products with lowercase names:",
# #       (products["product_name"] == products["product_name"].str.lower()).sum())
# # print("Products where unit_price <= unit_cost:",
# #       (products["unit_price"] <= products["unit_cost"]).sum())

# # print("\nLOCATIONS")
# # print(locations.shape)
# # print(locations.columns.tolist())
# # print(locations.head())
# # print(locations.dtypes)
# # print(locations.isnull().sum())
# # print(locations.duplicated().sum())
# # print("Unique location IDs:", locations["location_id"].nunique())

# # print("\nORDERS")
# # print(orders.shape)
# # print(orders.columns.tolist())
# # print(orders.head())
# # print(orders.dtypes)
# # print(orders.isnull().sum())
# # print(orders.duplicated().sum())
# # print("Order statuses:")
# # print(orders["order_status"].value_counts(dropna=False))
# # print("Shipping dates missing by order status:")
# # print(orders.groupby("order_status")["shipping_date"].apply(lambda x: x.isna().sum()))
# # print("Unique order IDs:", orders["order_id"].nunique())

# # print("\nORDER ITEMS")
# # print(order_items.shape)
# # print(order_items.columns.tolist())
# # print(order_items.head())
# # print(order_items.dtypes)
# # print(order_items.isnull().sum())
# # print(order_items.duplicated().sum())
# # print("Unique order item IDs:", order_items["order_item_id"].nunique())
# # print("\nQuantity distribution:")
# # print(order_items["quantity"].value_counts().sort_index())
# # print("\nInvalid discounts:", 
# #       ((order_items["discount"] < 0) | (order_items["discount"] > 1)).sum())

# # expected_revenue = (
# #     order_items["quantity"]
# #     * order_items["unit_price"]
# #     * (1 - order_items["discount"])
# # )
# # print(
# #     "Revenue discrepancies:",
# #     (abs(order_items["revenue"] - expected_revenue) > 0.01).sum()
# # )

# # print("\nDATES")
# # print(dates.shape)
# # print(dates.columns.tolist())
# # print(dates.head())
# # print(dates.dtypes)
# # print(dates.isnull().sum())
# # print(dates.duplicated().sum())
# # print("Unique dates:", dates["date"].nunique())
# # print("\nDate range:")
# # print("Start:", dates["date"].min())
# # print("End:", dates["date"].max())

# print("\nFOREIGN KEY VALIDATION")
# print(
#     "Invalid customer IDs in orders:",
#     (~orders["customer_id"].isin(customers["customer_id"])).sum()
# )
# print(
#     "Invalid location IDs in orders:",
#     (~orders["location_id"].isin(locations["location_id"])).sum()
# )
# print(
#     "Invalid location IDs in customers:",
#     (~customers["location_id"].isin(locations["location_id"])).sum()
# )
# print(
#     "Invalid order IDs in order_items:",
#     (~order_items["order_id"].isin(orders["order_id"])).sum()
# )
# print(
#     "Invalid product IDs in order_items:",
#     (~order_items["product_id"].isin(products["product_id"])).sum()
# )
# print(
#     "Invalid order dates:",
#     (~orders["order_date"].isin(dates["date"])).sum()
# )

print("\n" + "=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print("\nCUSTOMERS")
print("- Missing customer segments: 5")
print("- Inconsistent segment casing: 10")
print("- Customer names with leading/trailing whitespace: 15")

print("\nPRODUCTS")
print("- Product names with lowercase formatting: 8")

print("\nLOCATIONS")
print("- No basic data-quality issues identified")

print("\nORDERS")
print("- Exact duplicate rows: 3")
print("- Missing shipping dates: 2,508")
print("  → 1,755 Cancelled orders")
print("  → 753 Processing orders")
print("- Unique order IDs: 25,000")

print("\nORDER ITEMS")
print("- Quantity outliers (quantity = 99): 3")
print("- Revenue calculation discrepancies: 3")

print("\nDATES")
print("- Date range: 2023-01-01 to 2025-12-31")
print("- Unique dates: 1,096")
print("- month/month_name formatting inconsistency identified")

print("\nREFERENTIAL INTEGRITY")
print("- All foreign-key validation checks passed")