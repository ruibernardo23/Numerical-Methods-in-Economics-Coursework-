import pandas as pd 
import numpy as np

def main():
    #read in pwt100 table csv and convert to dataframe, drop any rows with NaN values
    df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")

main()
