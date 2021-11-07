import pandas as pd
import matplotlib.pyplot as plt
% matplotlib inline

# Assessing data
df_08 = pd.read_csv('all_alpha_08.csv')
df_08.info()
df_18 = pd.read_csv('all_alpha_18.csv')
df_18.info()

sum(df_08.duplicated())
sum(df_18.duplicated())

#__________________________________________________________________

# Cleaning Column Labels

# view 2008 dataset
df_08.head(1)
# view 2018 dataset
df_18.head(1)

# drop columns from 2008 dataset
df_08.drop(['Stnd', 'Underhood ID', 'FE Calc Appr', 'Unadj Cmb MPG'], axis=1, inplace=True)
# confirm changes
df_08.head(1)

# drop columns from 2018 dataset
df_18.drop(['Stnd', 'Stnd Description', 'Underhood ID', 'Comb CO2'], axis=1, inplace=True)
# confirm changes
df_18.head(1)

# rename Sales Area to Cert Region
df_08.rename(columns={'Sales Area' : 'Cert Region' }, inplace = True)
# confirm changes
df_08.head(1)

# replace spaces with underscores and lowercase labels for 2008 dataset
df_08.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)
# confirm changes
df_08.head(1)

# replace spaces with underscores and lowercase labels for 2018 dataset
df_18.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)
# confirm changes
df_18.head(1)

# confirm column labels for 2008 and 2018 datasets are identical
df_08.columns == df_18.columns
# make sure they're all identical like this
(df_08.columns == df_18.columns).all()

# save new datasets for next section
df_08.to_csv('data_08_v1.csv', index=False)
df_18.to_csv('data_18_v1.csv', index=False)

#__________________________________________________________________

# Filter, Drop Nulls, Dedupe

# load datasets
df_08 = pd.read_csv('data_08_v1.csv')
df_18 = pd.read_csv('data_18_v1.csv')
# view dimensions of dataset
df_08.shape
# view dimensions of dataset
df_18.shape

## Filter by Certification Region
# filter datasets for rows following California standards
df_08 = df_08.query('cert_region == "CA"')
df_18 = df_18.query('cert_region == "CA"')
# confirm only certification region is California
df_08['cert_region'].unique()
# confirm only certification region is California
df_18['cert_region'].unique()
# drop certification region columns form both datasets
df_08.drop('cert_region', axis=1, inplace=True)
df_18.drop('cert_region', axis=1, inplace=True)
df_08.shape
df_18.shape

## Drop Rows with Missing Values
# view missing value count for each feature in 2008
df_08.isnull().sum()
# view missing value count for each feature in 2018
df_18.isnull().sum()
# drop rows with any null values in both datasets
df_08.dropna(inplace = True)
df_18.dropna(inplace = True)
# checks if any of columns in 2008 have null values - should print False
df_08.isnull().sum().any()
# checks if any of columns in 2018 have null values - should print False
df_18.isnull().sum().any()

## Dedupe Data
# print number of duplicates in 2008 and 2018 datasets
df_08.duplicated().sum()
df_18.duplicated().sum()
# drop duplicates in both datasets
df_08.drop_duplicates(inplace = True)
df_18.drop_duplicates(inplace = True)
# print number of duplicates again to confirm dedupe - should both be 0
df_08.duplicated().sum()
df_18.duplicated().sum()
# save progress for the next section
df_08.to_csv('data_08_v2.csv', index=False)
df_18.to_csv('data_18_v2.csv', index=False)

#__________________________________________________________________

# Fixing `cyl` Data Type

# load datasets
df_08 = pd.read_csv('data_08_v2.csv')
df_18 = pd.read_csv('data_18_v2.csv')
# check value counts for the 2008 cyl column
df_08['cyl'].value_counts()
# Extract int from strings in the 2008 cyl column
df_08['cyl'] = df_08['cyl'].str.extract('(\d+)').astype(int)
# Check value counts for 2008 cyl column again to confirm the change
df_08['cyl'].value_counts()
# convert 2018 cyl column to int
df_18['cyl'] = df_18['cyl'].astype(int)
df_08.to_csv('data_08_v3.csv', index=False)
df_18.to_csv('data_18_v3.csv', index=False)

#__________________________________________________________________

# Fixing `air_pollution_score` Data Type

# load datasets
df_08 = pd.read_csv('data_08_v3.csv')
df_18 = pd.read_csv('data_18_v3.csv')

# try using pandas' to_numeric or astype function to convert the
# 2008 air_pollution_score column to float -- this won't work
df_08['air_pollution_score'].astype(float)

# It's not just the air pollution score!
#The mpg columns and greenhouse gas scores also seem to have the same problem
#maybe that's why these were all saved as strings!
# First, let's get all the hybrids in 2008
hb_08 = df_08[df_08['fuel'].str.contains('/')]
hb_08
# hybrids in 2018
hb_18 = df_18[df_18['fuel'].str.contains('/')]
hb_18
# create two copies of the 2008 hybrids dataframe
df1 = hb_08.copy()  # data on first fuel type of each hybrid vehicle
df2 = hb_08.copy()  # data on second fuel type of each hybrid vehicle

# Each one should look like this
df1
# columns to split by "/"
split_columns = ['fuel', 'air_pollution_score', 'city_mpg', 'hwy_mpg', 'cmb_mpg', 'greenhouse_gas_score']

# apply split function to each column of each dataframe copy
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("/")[0])
    df2[c] = df2[c].apply(lambda x: x.split("/")[1])
# this dataframe holds info for the FIRST fuel type of the hybrid
# aka the values before the "/"s
df1
# this dataframe holds info for the SECOND fuel type of the hybrid
# aka the values after the "/"s
df2
# combine dataframes to add to the original dataframe
new_rows = df1.append(df2)

# now we have separate rows for each fuel type of each vehicle!
new_rows
# drop the original hybrid rows
df_08.drop(hb_08.index, inplace=True)

# add in our newly separated rows
df_08 = df_08.append(new_rows, ignore_index=True)
# check that all the original hybrid rows with "/"s are gone
df_08[df_08['fuel'].str.contains('/')]
df_08.shape

# Repeat this process for the 2018 dataset
# create two copies of the 2018 hybrids dataframe, hb_18
df1 = hb_18.copy()
df2 = hb_18.copy()

# list of columns to split
split_columns = ['fuel', 'city_mpg', 'hwy_mpg', 'cmb_mpg']

# apply split function to each column of each dataframe copy
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("/")[0])
    df2[c] = df2[c].apply(lambda x: x.split("/")[1])
# append the two dataframes
new_rows = df1.append(df2)

# drop each hybrid row from the original 2018 dataframe
# do this by using pandas' drop function with hb_18's index
df_18.drop(hb_18.index, inplace=True)

# append new_rows to df_18
df_18 = df_08.append(new_rows, ignore_index=True)

# convert string to float for 2008 air pollution column
df_08['air_pollution_score'] = df_18['air_pollution_score'].astype(float)
# convert int to float for 2018 air pollution column
df_18['air_pollution_score'] = df_18['air_pollution_score'].astype(float)
df_08.to_csv('data_08_v4.csv', index=False)
df_18.to_csv('data_18_v4.csv', index=False)

#__________________________________________________________________

# Fix `city_mpg`, `hwy_mpg`, `cmb_mpg` datatypes

# load datasets
df_08 = pd.read_csv('data_08_v4.csv')
df_18 = pd.read_csv('data_18_v4.csv')

# convert mpg columns to floats
mpg_columns = ['city_mpg','hwy_mpg','cmb_mpg']
for c in mpg_columns:
    df_18[c] = df_18[c].astype(float)
    df_08[c] = df_08[c].astype(float)
    
## Fix `greenhouse_gas_score` datatype
    #2008: convert from float to int
    
# convert from float to int
df_08['greenhouse_gas_score'] = df_08['greenhouse_gas_score'].astype(int) 
## All the dataypes are now fixed! Take one last check to confirm all the changes.
df_08.dtypes
df_18.dtypes
df_08.dtypes == df_18.dtypes

# Save your final CLEAN datasets as new files!
df_08.to_csv('clean_08.csv', index=False)
df_18.to_csv('clean_18.csv', index=False)

#__________________________________________________________________

# # Drawing Conclusions

# load datasets
df_08 = pd.read_csv('clean_08.csv')
df_18 = pd.read_csv('clean_18.csv')

### Q1: Are more unique models using alternative sources of fuel? By how much?
alt_08 = df_08.query('fuel in ["CNG", "ethanol"]').model.nunique()
alt_08
alt_18 = df_18.query('fuel in ["Ethanol","Electricity"]').model.nunique()
alt_18
plt.bar(['2008', '2018'], [alt_08, alt_18])
plt.title('Number of Unique Models Using Alternative Fuels')
plt.xlabel('year')
plt.ylabel('Number of Unique Models')

### Q2: How much have vehicle classes improved in fuel economy?  

veh_08 = df_08.groupby(['veh_class']).cmb_mpg.mean() 
veh_18 = df_18.groupby(['veh_class']).cmb_mpg.mean()
inc = veh_18 - veh_08
inc.dropna(inplace=True)
inc
plt.subplots(figsize=(8, 5))
plt.bar(inc.index, inc)
plt.title('Improvements in Fuel Economy from 2008 to 2018 by Vehicle Class')
plt.xlabel('Vehicle Class')
plt.ylabel('Increase in Average Combined MPG');

### Q3: What are the characteristics of SmartWay vehicles? Have they changed over time?
df_08.smartway.value_counts()
df_18.smartway.value_counts()
df_18.smartway.unique()
smart_08 = df_08.query('smartway == "no"')
smart_08.describe()
smart_18 = df_18.query('smartway == "Elite"')
smart_18.describe()

### Q4: What features are associated with better fuel economy?
df_08.describe()
df_18.describe()

#__________________________________________________________________

# Merging Datasets

# rename 2008 columns
df_08.rename(columns=lambda x: x[:10] + "_2008", inplace=True)
# view to check names
df_08.head()
# merge datasets
df_combined = df_08.merge(df_18, left_on='model_2008', right_on='model',
how='inner')
# view to check merge
df_combined.head()
df_combined.to_csv('combined_dataset.csv', index=False)

#__________________________________________________________________

# Results with Merged Dataset

# load dataset
df = pd.read_csv('combined_dataset.csv')

# 1. Create a new dataframe, `model_mpg`, that contain the mean
#combined mpg values in 2008 and 2018 for each unique model
model_mpg = df.groupby(['model_2008']).mean()
model_mpg.head()
model_mpg = df.groupby(['model_2008']).mean()
new_df = model_mpg.filter(['cmb_mpg_2008','cmb_mpg'], axis=1)
mpg_change = new_df['cmb_mpg'] - new_df['cmb_mpg_2008']
new_df['mpg_change'] = mpg_change
new_df.head()
max(new_df['mpg_change'])
df_max = new_df.query('mpg_change == "16.533333333333339"')
df_max
