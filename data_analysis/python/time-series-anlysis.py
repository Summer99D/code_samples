## I will be importing libraries to use 
import pandas as pd
import datetime
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from pandas_datareader import wb
import requests
from bs4 import BeautifulSoup

pd.options.display.float_format = '{:.2f}'.format

#South korea- FRED
start_skGDP = datetime.date(year=2008, month=1,  day=1)
end_skGDP   = datetime.date(year=2020, month=12, day=31)
series_sk = ['MKTGDPKRA646NWDB', #this is annual GDP but not seaosnally adjusted
             'LFWA64TTKRQ647S'] #this is quarterly working population, seasonally adjusted
source = 'fred'

SK_df = web.DataReader(series_sk, source, start_skGDP, end_skGDP)
SK_df.head()

##this series is not consistent date-wise with my other df so I will be changing it to quarterly to allow for comparison
SK_df= SK_df.resample('Y').mean()

##now I need to change the index form date to year  to allow 
SK_df['year'] = SK_df.index.year
## I am going to rename the cols to understand what is going on
SK_df.rename(columns={'MKTGDPKRA646NWDB': 'GDP'}, inplace=True) #GDP in millions
SK_df.rename(columns={'LFWA64TTKRQ647S':'Working_Pop'}, inplace=True) #working pop in tohusands
SK_df['country']= 'South Korea'
SK_df.head()
##need to see Dtypes for merging later on
SK_df.dtypes
SK_df.reset_index()['year']



#world bank- Italy
indicator = ['NY.GDP.MKTP.CD', #annual GDP (USD)
             'SL.TLF.TOTL.IN'] #annual working pop(thousands)
country = 'ITA'

ITA_df = wb.download(indicator=indicator, 
                 country=country, 
                 start=2008, end=2020)

ITA_df.head()
ITA_df.reset_index()['year']
# Reset the index of the ITA_df DataFrame
ITA_df.reset_index(inplace=True)



##renaming the columns to understnad what is oging on:
ITA_df.rename(columns={"NY.GDP.MKTP.CD": 'GDP'}, inplace=True)
ITA_df.rename(columns={'SL.TLF.TOTL.IN': 'Working_Pop'}, inplace=True)
# Convert the data type of the 'year' column in one of the DataFrames
ITA_df['year'] = ITA_df['year'].astype(int) 

##I don't know why the GDP for Italy is funky, I made sure to look for 

Merged_df= pd.merge(SK_df, ITA_df, on= ['year', 'Working_Pop', 'GDP', 'country'], how='outer')
Merged_df.rename(columns={'year':'Year'}, inplace=True)
Merged_df.rename(columns={'country':'Country'}, inplace=True)
Merged_df.set_index('Year', inplace=True)
print(Merged_df)

#   b) Adjust the data so that all four are at the same frequency (you'll have
#      to look this up), then do any necessary merge and reshaping to put
#      them together into one long (tidy) format dataframe.




#   c) Finally, go back and change your earlier code so that the
#      countries and dates are set in variables at the top of the file. Your
#      final result for parts a and b should allow you to (hypothetically) 
#      modify these values easily so that your code would download the data
#      and merge for different countries and dates.
#      - You do not have to leave your code from any previous way you did it
#        in the file. If you did it this way from the start, congrats!
#      - You do not have to account for the validity of all the possible 
#        countries and dates, e.g. if you downloaded the US and Canada for 
#        1990-2000, you can ignore the fact that maybe this data for some
#        other two countries aren't available at these dates.
#   d) Clean up any column names and values so that the data is consistent
#      and clear, e.g. don't leave some columns named in all caps and others
#      in all lower-case, or some with unclear names, or a column of mixed 
#      strings and integers. Write the dataframe you've created out to a 
#      file named q1.csv, and commit it to your repo.

# Clean up column names
Merged_df.columns = ['GDP', 'Working Pop', 'Country']

# Write the DataFrame to a CSV file
Merged_df.to_csv('q1.csv', index=False)

# Print the first few rows of the cleaned DataFrame
print(Merged_df.head())