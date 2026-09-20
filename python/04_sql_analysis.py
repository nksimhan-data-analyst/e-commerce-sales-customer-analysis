import duckdb

con = duckdb.connect()

with open("sql/01_business_analysis.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

con.execute(sql_script)

print("SQL business analysis executed successfully.")

con.close()