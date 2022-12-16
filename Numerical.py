import pandas as pd 
import numpy as np

#calculate income per worker, cgdpo/emp
def IncomePerWorker(row):
    return row["cgdpo"] / row["emp"]

#calculate income per hour worked, cgdpo/(emp * avh)
def IncomePerHourWorked(row):
    return row["cgdpo"] / (row["emp"] * row["avh"])

#calculate income per unit of human capital, cgdpo/(emp * hc)
def IncomePerUnitOfHumanCapital(row):
    return row["cgdpo"] / (row["emp"] * row["hc"])

#calculate income per unit of human capital, cgdpo/(emp * avh * hc)
def IncomePerHourOfHumanCapital(row):
    return row["cgdpo"] / (row["emp"] * row["avh"] * row["hc"])

#returns a dataframe containing countries above a given quantile of a given variable
def GenerateQuantile(df, stat, quant):
    return df.loc[df[stat] >= df[stat].quantile(quant)]

#generates descriptive statistics of given dataframe, log-variance 95 90 10 05 quantiles, differences and ratios, returns dataframe
def CalcDifferencRatioStats(df):
    df_stats = df.describe([0.9, 0.1, 0.95, 0.05])

    #log-variance
    logStats = df_stats.apply(np.log, axis=0)
    df_stats.loc["log-variance"] = logStats.var()

    #min max calculations
    richest = df_stats.loc["max"]
    poorest = df_stats.loc["min"]
    df_stats.loc["max-min"] = richest.sub(poorest)
    df_stats.loc["max:min"] = richest.divide(poorest)
    
    #95-05 percentiles
    p95 = df_stats.loc["95%"]
    p05 = df_stats.loc["5%"]
    df_stats.loc["95%-05%"] = p95.sub(p05)
    df_stats.loc["95%:05%"] = p95.divide(p05)

    #90-10 percentiles
    p90 = df_stats.loc["90%"]
    p10 = df_stats.loc["10%"]
    df_stats.loc["90%-10%"] = p90.sub(p10)
    df_stats.loc["90%:10%"] = p90.divide(p10)
    
    return df_stats

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
    
    #create new columns for each of our gdp statistics
    df2017 = df2017.assign(ipw=df2017.apply(IncomePerWorker, axis=1),
                        iphw=df2017.apply(IncomePerHourWorked, axis=1),
                        ipuhc=df2017.apply(IncomePerUnitOfHumanCapital, axis=1),
                        iphhc=df2017.apply(IncomePerHourOfHumanCapital, axis=1))

    #create a new dataframe with only the required statistics for easier calculation
    df2017_income = df2017.loc[:, ["country", "ipw", "iphw", "ipuhc", "iphhc"]]
    df2017_income.set_index("country", inplace=True)
    
    #generate descriptive statistics and store in new table, print outcome
    df2017_income_stats = CalcDifferencRatioStats(df2017_income)
    print("2017 Income: \n\n", df2017_income, "\n\n")
    print("2017 Income Descriptive Statistics: \n\n", df2017_income_stats, "\n\n")
    
main()
