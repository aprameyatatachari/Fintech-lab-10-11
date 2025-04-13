import pandas as pd
import mysql.connector as sql

# Connect to MySQL
mydb = sql.connect(
    host='localhost',
    user='root',
    password='root',
    database='aprameya'
)
lang = input("Enter the language you want to search for: ")
age_min = int(input("Enter the minimuim age you want to search for: "))
age_max = int(input("Enter the maximum age you want to search for: "))
query = '''SELECT cd.id, cn.first_name, cn.middle_name, cn.last_name, cd.date_of_birth, TIMESTAMPDIFF(YEAR, cd.date_of_birth, CURDATE()) as age, cd.language, cd.gender,  ca.city, ca.state, ca.country FROM customer_detail cd JOIN customer_names cn ON cd.name_id = cn.id LEFT JOIN customer_address ca ON cd.address_id = ca.id WHERE cd.language = %(language)s AND TIMESTAMPDIFF(YEAR, cd.date_of_birth, CURDATE()) BETWEEN %(age_min)s AND %(age_max)s ORDER BY cd.id;'''


df = pd.read_sql(query, mydb, params={'language': lang, 'age_min': age_min, 'age_max': age_max})
if(df.empty):
    print("No data found for the given criteria.")
else:
    print(df.head())
mydb.close()
df.to_csv('customer_details_'+lang+'_'+str(age_min)+'-'+str(age_max)+'.csv', index=False)
