import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ftfy import fix_text #fix text encoding issues
import requests #to get data from api

#TODO: what predicts price of a house in Denmark? Is it size, region, house type, sale type, year built?
#could be year/quarter sold.


inpath = os.path.join(
    os.getcwd(),
    "Data",
    "DKHousingPricesSample100k.csv",
)

#load data

df = pd.read_csv(inpath)

print(df.columns)
print(df.head(10))

#how are quarters encoded?
print("unique quarters: ", df["quarter"].unique())
#reencode quarters to year and quarter
df["year"] = df["quarter"].str[:4].astype(int)
df["quarter_num"] = df["quarter"].str[5].astype(int)

#some of the city names and are malformed or empty, we make a function to clean them

#we inspect the rows with no city
df_no_city = df[df["city"].isnull()]
print("zip codes for houses with no city: ",df_no_city["zip_code"].value_counts())

#another irregularity is that zip code 2100 shows as "København A", but it should be "København Ø"
df_kobenhavn_a = df[df["zip_code"] == 2100]
print("city names for zip code 2100: ", df_kobenhavn_a["city"].value_counts())

#there is also an issue with some of the text encoding in the city and address fields
#an example is row 68978
print("example of bad encoding: ", df.loc[68978, ["city", "address"]])

#We fix the city issues by using Denmark's postal code API to get the correct city names
resp = requests.get("https://api.dataforsyningen.dk/postnumre", timeout=30)
resp.raise_for_status()
postnumre = resp.json()

zip_to_city = {item["nr"]: item["navn"] for item in postnumre}

df["zip_code_str"] = df["zip_code"].astype(str).str.zfill(4) #make sure zip codes are strings with 4 digits
df["city_from_zip"] = df["zip_code_str"].map(zip_to_city)

#select rows where city and city_from_zip are different and not null
mismatched_cities = df[(df["city"] != df["city_from_zip"]) & (df["city"].notnull())]
#show the two cols
print("mismatched cities: ", mismatched_cities[["zip_code", "city", "city_from_zip"]])

#we try to fix the address names. The encoding has replaced som Ø with A, these are not easily recoverable
#so we just fix the encoding as much as we can and leave it at that
df["address_fixed"] = df["address"].apply(fix_text)

#lets show the mismatched addresses as well
mismatched_addresses = df[df["address"] != df["address_fixed"]]
print("mismatched addresses: ", mismatched_addresses[["address", "address_fixed"]])

#everything seems in order now, we replace the old city and address columns with the fixed ones
df["city"] = df["city_from_zip"] #use city_from_zip where city is null
df["address"] = df["address_fixed"]
df = df.drop(columns=["city_from_zip", "zip_code_str", "address_fixed"])

#groupby region and get mean price
mean_prices = df.groupby("region")["purchase_price"].mean().reset_index()

#groupby region house type and plot
#include a line that shows average price for each house type
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



#make boxsplot without outliers
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x="region", y="purchase_price", showfliers=False)
plt.title("Purchase Price Distribution by Region (Without Outliers)")
plt.xlabel("Region")
plt.ylabel("Purchase Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#scatterplot of size vs price colored by region
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x="sqm", y="purchase_price", hue="region", alpha=0.6)
plt.title("Size vs Purchase Price Colored by Region")
plt.xlabel("Size (sqm)")
plt.ylabel("Purchase Price")
plt.legend(title="Region")
plt.tight_layout()
plt.show()

#scatterplot of size vs price colored by house type
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x="sqm", y="purchase_price", hue="house_type", alpha=0.6)
plt.title("Size vs Purchase Price Colored by House Type")
plt.xlabel("Size (sqm)")
plt.ylabel("Purchase Price")
plt.legend(title="House Type")
plt.tight_layout()
plt.show()

#same scatterplot for zealand only
df_zealand = df[df["region"] == "Zealand"]
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_zealand, x="sqm", y="purchase_price", hue="house_type", alpha=0.6)
plt.title("Size vs Purchase Price in Zealand Colored by House Type")
plt.xlabel("Size (sqm)")
plt.ylabel("Purchase Price")
plt.legend(title="House Type")
plt.tight_layout()
plt.show()


#boxplot of prices in most expensive cities with more than 100 entries, sorted median price
city_counts = df['city'].value_counts()
popular_cities = city_counts[city_counts > 100].index
df_popular_cities = df[df['city'].isin(popular_cities)]
mean_prices_by_city = df_popular_cities.groupby('city')['purchase_price'].median().reset_index()
mean_prices_by_city = mean_prices_by_city.sort_values(by='purchase_price', ascending=False).head(10)
top_cities = mean_prices_by_city['city'].tolist()
df_top_cities = df_popular_cities[df_popular_cities['city'].isin(top_cities)]
plt.figure(figsize=(12, 8))
sns.boxplot(data=df_top_cities, x='city', y='purchase_price', order=top_cities, palette='viridis')
plt.title('Purchase Price Distribution in Top 10 Most Expensive Cities (with > 100 entries)')
plt.xlabel('City')
plt.ylabel('Purchase Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#histogram of average prices by year
mean_prices_by_year = df.groupby('year')['purchase_price'].mean().reset_index()
plt.figure(figsize=(12, 8))
sns.barplot(data=mean_prices_by_year, x='year', y='purchase_price', palette='mako')
plt.title('Average Purchase Price by Year')
plt.xlabel('Year')
plt.ylabel('Average Purchase Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#boxplot of prices by year
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='year', y='purchase_price', palette='mako')
plt.title('Purchase Price Distribution by Year')
plt.xlabel('Year')
plt.ylabel('Purchase Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#show boxplot of house type
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x="house_type", y="purchase_price")
plt.title("Purchase Price Distribution by House Type")
plt.xlabel("House Type")
plt.ylabel("Purchase Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#show distribution of prize in sepate plots by house type
g = sns.FacetGrid(df, col="house_type", col_wrap=3, height=4)
g.map(sns.histplot, "purchase_price", bins=30, kde=True)
g.set_titles("{col_name}")
g.set_axis_labels("Purchase Price", "Count")
plt.subplots_adjust(top=0.9)
g.figure.suptitle("Purchase Price Distribution by House Type")
plt.show()

#show distribution of villas of 2021