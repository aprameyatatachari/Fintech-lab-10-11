import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('customer_language_analytics.csv')
plt.figure(figsize=(10, 6))
df['language'].value_counts().plot(kind='bar')
plt.title('Bar Chart of Your Column')
plt.xlabel('Languages')
plt.ylabel('Frequency')
plt.savefig('bar_chart.png')
plt.show()

