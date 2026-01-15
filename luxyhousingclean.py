import pandas as pd
import numpy as np
import mysql.connector

# ==========================================
# Reading the csv file
# ==========================================

original_data = pd.read_csv('./Luxury_Housing_Bangalore.csv')
data = pd.read_csv('./Luxury_Housing_Bangalore.csv')
# print(data.head(5))

# ==========================================
# STEP 1: HEADER CLEANING
# ==========================================

print(data.columns.tolist())
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
print("FIX APPLIED")
print(data.columns.tolist())

# ==========================================
# Info of csv file
# ==========================================

# print(data.info())
# RangeIndex: 101000 entries, 0 to 100999
# Data columns (total 18 columns):
#  #   Column                Non-Null Count   Dtype
# ---  ------                --------------   -----
#  0   property_id           101000 non-null  object
#  1   micro_market          101000 non-null  object
#  2   project_name          101000 non-null  object col2
#  3   developer_name        101000 non-null  object
#  4   unit_size_sqft        90954 non-null   float64 col4
#  5   configuration         101000 non-null  object
#  6   ticket_price_cr       90981 non-null   object
#  7   transaction_type      101000 non-null  object col 7
#  8   buyer_type            101000 non-null  object
#  9   purchase_quarter      101000 non-null  object
#  10  connectivity_score    101000 non-null  float64 
#  11  amenity_score         90910 non-null   float64
#  12  possession_status     101000 non-null  object
#  13  sales_channel         101000 non-null  object
#  14  nri_buyer             101000 non-null  object
#  15  locality_infra_score  101000 non-null  float64
#  16  avg_traffic_time_min  101000 non-null  int64
#  17  buyer_comments        82713 non-null   object

# ==========================================
# DROPPPING UNWANTED COLUNMS
# ==========================================

data.drop(columns=["project_name","transaction_type"], axis=1, inplace=True)
print("FIX APPLIED")

# ==========================================
# AFTER DROPPING INFO OF CSV FILE
# ==========================================

# print(data.info())
# RangeIndex: 101000 entries, 0 to 100999
# Data columns (total 16 columns):
#  #   Column                Non-Null Count   Dtype
# ---  ------                --------------   -----
#  0   property_id           101000 non-null  object
#  1   micro_market          101000 non-null  object
#  2   developer_name        101000 non-null  object
#  3   unit_size_sqft        90954 non-null   float64
#  4   configuration         101000 non-null  object
#  5   ticket_price_cr       90981 non-null   object
#  6   buyer_type            101000 non-null  object
#  7   purchase_quarter      101000 non-null  object
#  8   connectivity_score    101000 non-null  float64
#  9   amenity_score         90910 non-null   float64
#  10  possession_status     101000 non-null  object
#  11  sales_channel         101000 non-null  object
#  12  nri_buyer             101000 non-null  object
#  13  locality_infra_score  101000 non-null  float64
#  14  avg_traffic_time_min  101000 non-null  int64
#  15  buyer_comments        82713 non-null   object
# dtypes: float64(4), int64(1), object(11)
# memory usage: 12.3+ MB

# ==========================================
#  CATEGORICAL TYPOS (FUZZY LOGIC)
# ==========================================

print(data['micro_market'].unique())
print(data['developer_name'].unique())
print(data['configuration'].unique())
print(data['buyer_type'].unique())
print(data['possession_status'].unique())
print(data['sales_channel'].unique())
print(data['nri_buyer'].unique())

# ==========================================
#  ROW CLEANING
# ==========================================

data.micro_market =data.micro_market.str.strip().str.lower()
data.developer_name =data.developer_name.str.strip()
data.configuration =data.configuration.str.strip().str.upper().str.replace('+', '')
data.sales_channel =data.sales_channel.str.strip()
data.possession_status =data.possession_status.str.strip()
data.buyer_type =data.buyer_type.str.strip()
data.buyer_comments =data.buyer_comments.str.strip()
data['unit_size_sqft'] = data['unit_size_sqft'].replace(-1, np.nan)
print("FIX APPLIED")

# ==========================================
#  TYPE CONVERSION & CURRENCY CLEANING
# ==========================================

ticket_price_cr_mask = data['ticket_price_cr'].astype(str).str.contains(r'\₹')
print(data.loc[ticket_price_cr_mask,['property_id','ticket_price_cr']].head(3))
data['ticket_price_cr'] = data['ticket_price_cr'].astype(str).str.replace(r'[^\d.-]', '', regex=True)
data['ticket_price_cr'] = pd.to_numeric(data['ticket_price_cr'])
print(data.loc[ticket_price_cr_mask,['property_id','ticket_price_cr']].head(3))

# ==========================================
#  CHANGING DATE DATATYPE
# ==========================================

data['purchase_quarter'] = pd.to_datetime(data['purchase_quarter'])
print(data.info())
print(data.describe())

# ==========================================
#  DROPPING DUPLICATE VALUES
# ==========================================

dupes=data[data['property_id'].duplicated()]['property_id']
data[data['property_id'].isin(dupes)]
data = data.drop_duplicates(subset='property_id', keep='first')

# data.info()
# Index: 100000 entries, 0 to 99999
# Data columns (total 16 columns):
#  #   Column                Non-Null Count   Dtype         
# ---  ------                --------------   -----         
#  0   property_id           100000 non-null  object        
#  1   micro_market          100000 non-null  object        
#  2   developer_name        100000 non-null  object        
#  3   unit_size_sqft        89543 non-null   float64       
#  4   configuration         100000 non-null  object        
#  5   ticket_price_cr       90087 non-null   float64       
#  6   buyer_type            100000 non-null  object        
#  7   purchase_quarter      100000 non-null  datetime64[ns]
#  8   connectivity_score    100000 non-null  float64       
#  9   amenity_score         90000 non-null   float64       
#  10  possession_status     100000 non-null  object        
#  11  sales_channel         100000 non-null  object        
#  12  nri_buyer             100000 non-null  object        
#  13  locality_infra_score  100000 non-null  float64       
#  14  avg_traffic_time_min  100000 non-null  int64         
#  15  buyer_comments        81901 non-null   object        
# dtypes: datetime64[ns](1), float64(5), int64(1), object(9)
# memory usage: 13.0+ MB

# ==========================================
#  HANDLING NULL VALUES
# ==========================================

data["ticket_price_cr"].isnull().sum()
#np.int64(10019)
data["unit_size_sqft"].isnull().sum()
#np.int64(10551)
data["amenity_score"].isna().sum()
#np.int64(10090)

# Tracking NaN value & mask before median fill

mask_price = data["ticket_price_cr"].isna()
mask_size = data["unit_size_sqft"].isna()
mask_amenity = data["amenity_score"].isna()

# Median was used instead of mean due to skewed distributions and outliers

data["ticket_price_cr"].fillna(data["ticket_price_cr"].median(),inplace=True)
data["unit_size_sqft"].fillna(data["unit_size_sqft"].median(),inplace=True)
data["amenity_score"].fillna(data["amenity_score"].median(),inplace=True)
data["buyer_comments"].fillna("No Comments", inplace=True)

# ==========================================
#  OUTLINER HANDLING USING IQR
# ==========================================

def iqr_bounds(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return lower, upper

# Handle Outliers in Unit_Size_Sqft,ticket_price_cr,amenity_score& capping values

IQR_unit_size_sqft_low, IQR_unit_size_sqft_high = iqr_bounds(data["unit_size_sqft"])
print("unit_size_sqft =",IQR_unit_size_sqft_low, IQR_unit_size_sqft_high)
data["unit_size_sqft"] = data["unit_size_sqft"].clip(IQR_unit_size_sqft_low, IQR_unit_size_sqft_high)
# unit_size_sqft = 709.5 11305.5

IQR_ticket_price_cr_low, IQR_ticket_price_cr_high = iqr_bounds(data["ticket_price_cr"])
print("ticket_price_cr =",IQR_ticket_price_cr_low, IQR_ticket_price_cr_high)
data["ticket_price_cr"] = data["ticket_price_cr"].clip(IQR_ticket_price_cr_low, IQR_ticket_price_cr_high)
# ticket_price_cr = 4.915084288749999 19.17899967875

IQR_amenity_score_low, IQR_amenity_score_high = iqr_bounds(data["amenity_score"])
print("amenity_score =",IQR_amenity_score_low, IQR_amenity_score_high)
data["amenity_score"] = data["amenity_score"].clip(IQR_amenity_score_low, IQR_amenity_score_high)
# amenity_score = 3.0636149697500015 11.94760058575

# ============================================================
#  CHECKING THE DATA SET FOR MISSING VALUES OR DROPPED ROWS 
# ============================================================

missing_ids = set(original_data['Property_ID']) - set(data['property_id'])
print(missing_ids)
#set()

# print(data.info())
# Index: 100000 entries, 0 to 99999
# Data columns (total 16 columns):
#  #   Column                Non-Null Count   Dtype         
# ---  ------                --------------   -----         
#  0   property_id           100000 non-null  object        
#  1   micro_market          100000 non-null  object        
#  2   developer_name        100000 non-null  object        
#  3   unit_size_sqft        100000 non-null  float64       
#  4   configuration         100000 non-null  object        
#  5   ticket_price_cr       100000 non-null  float64       
#  6   buyer_type            100000 non-null  object        
#  7   purchase_quarter      100000 non-null  datetime64[ns]
#  8   connectivity_score    100000 non-null  float64       
#  9   amenity_score         100000 non-null  float64       
#  10  possession_status     100000 non-null  object        
#  11  sales_channel         100000 non-null  object        
#  12  nri_buyer             100000 non-null  object        
#  13  locality_infra_score  100000 non-null  float64       
#  14  avg_traffic_time_min  100000 non-null  int64         
#  15  buyer_comments        100000 non-null  object        
# dtypes: datetime64[ns](1), float64(5), int64(1), object(9)
# memory usage: 13.0+ MB

# ============================================================
#  FILLING MEAN VALUES IN MASKED NAN VALUES 
# ============================================================

data.loc[mask_price, "ticket_price_cr"] = data["ticket_price_cr"].mean()
data.loc[mask_size, "unit_size_sqft"] = data["unit_size_sqft"].mean()
data.loc[mask_amenity, "amenity_score"] = data["amenity_score"].mean()

# ============================================================
#  CHECKING SKEWNESS & DESCRIBING THE DATA 
# ============================================================

data["unit_size_sqft"].skew()
# np.float64(-0.0019221707056581176)

data["amenity_score"].skew()
# np.float64(0.0005731772341180994)

data["ticket_price_cr"].skew()
# np.float64(0.0766774747367327)

# as the skewness is 0 their are no possible outliners in the data 

print(data.describe())

# 	   unit_size_sqft	 ticket_price_cr	purchase_quarter	connectivity_score	amenity_score	locality_infra_score	avg_traffic_time_min
# count	101000.000000	  101000.000000	       101000	               101000.000000	101000.000000	  1 01000.000000	     101000.000000
# mean	6005.607358	       12.075382    2024-05-15 06:47:26.922772224  6.992619	        7.503617	      7.498426	             67.182921
# min	3000.000000	       4.915084	    2023-06-30 00:00:00	           4.000031         5.000224	      5.000013	             15.000000
# 25%	4683.000000	       10.264053	2023-09-30 00:00:00	           5.494526         6.395110	      6.247954	             41.000000
# 50%	6005.455327	       12.071976    2024-03-31 00:00:00	           6.985805	        7.503209	      7.495614	             67.000000
# 75%	7332.000000	       13.830031	2024-09-30 00:00:00            8.490000	        8.616106	      8.749824	             93.000000
# max	8999.000000	       19.179000	2025-03-31 00:00:00	           9.999970	        9.999865	      9.999956	             119.000000
# std	1638.522661	       2.865216	           NaN	                   1.731757	        1.366898	      1.443128	             30.271611

# ============================================================
#  SQL CONNECTION USING SQLALCHEMY
# ============================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="k.dybalasai",
    database="luxury_housing"
)

cursor = db.cursor()
insert_query = """
INSERT INTO luxury_properties (
    property_id, micro_market, developer_name, unit_size_sqft, configuration,
    ticket_price_cr, buyer_type, purchase_quarter, connectivity_score,
    amenity_score, possession_status, sales_channel, nri_buyer,
    locality_infra_score, avg_traffic_time_min, buyer_comments
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
for _, row in data.iterrows():
    cursor.execute(insert_query, (
        row['property_id'],
        row['micro_market'],
        row['developer_name'],
        row['unit_size_sqft'],
        row['configuration'],
        row['ticket_price_cr'],
        row['buyer_type'],
        row['purchase_quarter'],
        row['connectivity_score'],
        row['amenity_score'],
        row['possession_status'],
        row['sales_channel'],
        row['nri_buyer'],
        row['locality_infra_score'],
        row['avg_traffic_time_min'],
        row['buyer_comments']
    ))
db.commit()
print("DATA INSERTED")