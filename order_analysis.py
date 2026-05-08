import kaggle
#extract file from zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip') 
zip_ref.extractall() # extract file to dir
zip_ref.close() # close file

import pandas as pd
df = pd.read_csv('orders.csv',na_values=['Not Available','unknown'])
(df.head(20))
(df['Ship Mode'].unique())

#rename columns names ..make them lower case and replace space with underscore
#df.rename(columns={'Order Id':'order_id', 'City':'city'})
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
(df.head(5))

#derive new columns discount , sale price and profit
df['discount']=df['list_price']*df['discount_percent']*.01
df['sale_price']= df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']

df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")

#drop cost price list price and discount percent columns
df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)

#load the data into sql server using replace option

import sqlalchemy as sal

# 🔹 Create connection
engine = sal.create_engine(
    "mysql+mysqlconnector://root:sonu%25123@127.0.0.1:3306/orders_data"
)

# 🔹 Test connection + fetch data
try:
    query_result = pd.read_sql("SELECT 1", engine)
    print("✅ Connection successful")
except Exception as e:
    print("❌ Error:", e)

#load the data into sql server using append option
df.to_sql('df_orders', con=engine , index=False, if_exists = "replace",)



df = pd.read_csv("orders.csv")
print(df.shape)