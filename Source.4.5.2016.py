import pandas as pd

%pwd 
%cd 'Z:\\Data Academy'
%ls 

#import data
Source = pd.read_csv('SBO Startup Acquisition Source Clean.csv')

#check dataframe 
Source.head(3)
Source.tail(3)

#drop all rows where CBGROUP_TTL is "Publicy held and other firms not classifiable"
Source = Source[~Source["CBGROUP_TTL"].str.contains("Publicly held")]

#confirm new shape of dataframe 
Source.shape

#check column variables 
Source.columns

#isolate demographic characteristics 
Source.CBGROUP_TTL.head(5)
Source.CBGROUP_TTL.tail(5)
