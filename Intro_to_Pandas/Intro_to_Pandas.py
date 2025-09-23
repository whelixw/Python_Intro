import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


inpath = os.path.join(
    os.getcwd(),
    "Data",
    "DKHousingPricesSample100k.csv",
)

#load data

df = pd.read_csv(inpath)

print(df.head(10))

#groupby region and get mean price
mean_prices = df.groupby("region")["purchase_price"].mean().reset_index()

#groupby region house type and plot
mean_prices_by_type = df.groupby(["region", "house_type"])["purchase_price"].mean().reset_index()
print(mean_prices_by_type)

plt.figure(figsize=(12, 8))
sns.barplot(data=mean_prices_by_type, x="region", y="purchase_price", hue="house_type")
plt.title("Average Purchase Price by Region and House Type")
plt.xlabel("Region")
plt.ylabel("Average Purchase Price")
plt.legend(title="House Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#make a boxplot of prices by region
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x="region", y="purchase_price")
plt.title("Purchase Price Distribution by Region")
plt.xlabel("Region")
plt.ylabel("Purchase Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
