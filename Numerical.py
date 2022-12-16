import pandas as pd 
import numpy as np

def main():
    #read in pwt100 table csv and convert to dataframe, drop any rows with NaN values
    df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
    #df = df.loc[:,["countrycode", "country", "year", "cgdpo", "emp", "avh", "hc", "pop", "cn", "labsh", "ctfp"]] #filter table to only variables needed before discarding NaN rows
    df = df.dropna() #discard rows with NaN value

    #create table containing year and number of observations for that year
    print("Year-Observation table: \n")
    yearCountTable = df.groupby("year").apply(lambda x: x.count().sum())
    print(yearCountTable, "\n")

    #generate descriptive statistics for table, output year with highest observations
    print("Year-Observation table statistics: \n")
    yearCountTable.reset_index() #convert series to dataframe
    print(yearCountTable.describe(),"\n")
    print("Year with highest observations: ",yearCountTable.idxmax(), "n=", yearCountTable.max(), "\n\n")

    #we decided on using 2017 because it is the most recent year with highest number of observations
    print("2017: \n")
    df2017 = df.loc[df["year"] == 2017] #create dataframe for just 2017
    print(df2017, "\n\n")
    
main()
