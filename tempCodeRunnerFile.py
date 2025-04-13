import pandas as pd
import mysql.connector as sql

# Connect to MySQL
mydb = sql.connect(
    host='localhost',
    user='root',
    password='#Audiq7#',
    database='aprameya'
)
query = "select gender, count(gender) from customer_detail group by gender having gender in('male','female');"
df = pd.read_sql(query, mydb)
print(df.head())
mydb.close()
df.to_csv('customer_gender_ratio.csv', index=False)
