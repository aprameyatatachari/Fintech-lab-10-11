import pandas as pd
import mysql.connector as sql

# Connect to MySQL
mydb = sql.connect(
    host='localhost',
    user='root',
    password='#Audiq7#',
    database='aprameya'
)
query = "select language,country, count(customer_detail.id) from customer_detail join customer_address on customer_detail.id = customer_address.id group by country, language order by count(customer_detail.id) DESC"
df = pd.read_sql(query, mydb)
print(df.head())
mydb.close()
df.to_csv('customer_language_analytics.csv', index=False)
