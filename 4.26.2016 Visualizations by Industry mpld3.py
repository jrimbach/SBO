import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
%pwd

%cd 'Z:\\Data Academy'

%ls

#import source data
Source = pd.read_csv('Source Clean.csv')

#for industries get rid of "Total for all Sectors" and "Industries not Classified"
droplist = ['Total for all sectors','Industries not classified']
IndustryClean = Source[~Source['NAICS.display-label'].isin(droplist)]

#for sources of capital get rid of "All firms", "None needed", "Total reporting", "Item not reported"
droplist = ['All firms','None needed','Total reporting','Item not reported',"Don't know"]
SourceIndustryClean = IndustryClean[~IndustryClean['STRTSRCE.display-label'].isin(droplist)]

SourceIndustryClean.rename(columns = {'NAICS.display-label':'industry','CBGROUP.display-label':'dem','STRTSRCE.display-label':'source','FIRMALL':'firms'}, inplace = True)

#delete all rows in 'CBGROUP.display-label' unless it says exactly 'Minority' and 'Nonminority' 
droplist = ['Minority','Nonminority']
DemSourceIndustry = SourceIndustryClean[SourceIndustryClean.dem.isin(droplist)]

#rename/rewrite industry categories in DemSourceIndustry dataframe
#replace "(60[6-9])" with nothing (delete "(60[6-9]) appearing anywhere in the dataframe) by using regex method 
DemSourceIndustry = DemSourceIndustry.replace(r'\(60[6-9]\)', '', regex=True)

#subset data by each minority groups (two datasets)

#create new dataframe with just minority 
droplist = ['Minority']
Minority = DemSourceIndustry[DemSourceIndustry.dem.isin(droplist)]

#create new dataframe with just nonminority 
droplist = ['Nonminority']
Nonminority = DemSourceIndustry[DemSourceIndustry.dem.isin(droplist)]

#subset minority in agriculture by using 'Minority' dataframe and dropping all industries except agriculture
droplist = ['Agriculture, forestry, fishing and hunting']
MinorityAgriculture = Minority[Minority['industry'].isin(droplist)]

#check new dataframe 
MinorityAgriculture.shape

#subset nonminority in agriculture 
droplist = ['Mining, quarrying, and oil and gas extraction']
NonminorityAgriculture = Nonminority[Nonminority['industry'].isin(droplist)]
'''
-------------------------------------------------------------------------------
'''
#create bar chart for number of minority agriculture firms by funding source

#create new subset dataframe with only source and firm for minority firms in agriculture
MinorityAgriculture2 = MinorityAgriculture.drop('industry', axis=1)
MinorityAgriculture3 = MinorityAgriculture2.drop('dem', axis=1)

#convert objects in firms column to integers
Firms2 = pd.to_numeric(MinorityAgriculture3.firms)
Firms2.dtypes
MinorityAgriculture3.firms = pd.to_numeric(MinorityAgriculture3.firms)

#confirm firms data type is integer 
MinorityAgriculture3.dtypes

#create bar chart for number of minority agriculture firms by funding source
MinAgPlot = MinorityAgriculture3.plot(x=MinorityAgriculture3.source, kind='bar')
MinAgFig = MinAgPlot.get_figure()

#create bar chart for number of minority agriculture firms by funding source in HTML
mpld3.show(MinAgFig)

#mpld3.show()
#mpld3.fig_to_html(template_type="simple")
'''
-------------------------------------------------------------------------------
'''
#create bar chart for number of nonminority agriculture firms by funding source

#create new subset dataframe with only source and firm for nonminority firms in agriculture
NonminorityAgriculture.shape
NonminorityAgriculture2 = NonminorityAgriculture.drop('industry', axis=1)
NonminorityAgriculture3 = NonminorityAgriculture2.drop('dem', axis=1)

#convert objects in firms column to integers
Firms3 = pd.to_numeric(NonminorityAgriculture3.firms)
Firms3.dtypes
NonminorityAgriculture3.firms = pd.to_numeric(NonminorityAgriculture3.firms)

#confirm firms data type is integer 
NonminorityAgriculture3.dtypes

#create bar chart for number of nonminority agriculture firms by funding source
NonminAgPlot = NonminorityAgriculture3.plot(x=MinorityAgriculture3.source, kind='bar')
NonminAgFig = NonminAgPlot.get_figure()

#create bar chart for number of nonminority agriculture firms by funding source in HTML
mpld3.show(NonminAgFig)

#mpld3.css(f)
'''
-------------------------------------------------------------------------------
'''
#compare minority and nonminority using stacked bar plot 

fig = plt.figure()

#create ax1 for array of minority firm counts for each funding source
ax1 = MinorityAgriculture3.firms

#create ax2 for array of nonminority firm counts for each funding source
ax2 = NonminorityAgriculture3.firms

N = len(ax1) ## length of ax1
ind = np.arange(N)    # the x locations for the groups, number of groups
width = 0.5       # the width of each bar -- play with this to fit it onto the screen

#set up stacked bar plot with 12 bins 
p1 = plt.bar(ind, ax1, width, color='slateblue')  #Top value
p2 = plt.bar(ind, ax2, width, color='salmon', bottom=ax1) #Bottom Value

#ind + width/2 states that within each bin (ind), the tick mark goes at position width/2
#In this case it's 0.5/2 = 0.25
plt.xticks(ind + width/2., NonminorityAgriculture3.source, rotation='vertical')

#Tick intervals (yaxis)-- from 0 to 45000 by interval of 5000
plt.yticks(np.arange(0, 45000, 5000)) 

#create x- and y-axis labels and stacked bar plot title 
plt.title('Comparison of Minority and Nonminority Funding Sources in Agriculture')
plt.xlabel('Funding Sources')
plt.ylabel('Number of Firms')
plt.legend(['Number of Minority Firms', 'Number of Nonminority Firms'])
plt.show()           

#create stacked bar chart comparing number of minority and nonminority agriculture firms by funding source in HTML
mpld3.show(fig)                
'''
-------------------------------------------------------------------
'''
import flask
from flask import *
import pandas as pd
app = Flask(__name__)

@app.route("/tables")
def show_tables():
    data = pd.read_excel('dummy_data.xlsx)                       