import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# data was originall from https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data taken 
# around september 10th
# the data was cleaned to reflect crimes that would impact pedestrians more than anything else. 
# thing like cyber crimes and car thefts were removed, as one could fairly assume that doesn't invovle a pedestrian being hurt 
# the main connection is still walkability and how crime is correlated with it 
df = pd.read_csv('https://raw.githubusercontent.com/sbsutton98/data/main/Crime_Data_20_to_Present_cleaned.csv')

df_cleaner = df.drop(columns=['Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Status', 'Vict Age', 'Date Rptd',
'DATE OCC','Part 1-2','Weapon Used Cd','Weapon Desc', 'Status Desc'])
# dropped some columns, that I assumed would come to be helpful later on, but they did not. 

df2 = df_cleaner.groupby(['AREA'])['Crm Cd'].count()
# found the number of crimes that occured in the different areas

df_area = df_cleaner.groupby(['AREA'])

dfs = {name: group for name, group in df_area}
central = dfs[1]
central_count = pd.DataFrame(central["Crm Cd"].value_counts())
central_count
# gives us a count of which crime codes are reported on the most in the Central area 


d = {'AREA': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
     'Count':[8894,5635,5106,3593,2936,5240,3101,2273,2155,2140,2776,7989,6334,2683,2944,1993,1716,6077,2275,4783,1695]}
area_counts = pd.DataFrame(data=d)
area_counts
# making a count for each area to be compared to one another 
# mean count for crimes overall is 3921. 


order = df_cleaner["Crm Cd"].value_counts().index

count_plot = sns.countplot(x=df_cleaner["Crm Cd"], order=order)
count_plot.set_xticklabels(count_plot.get_xticklabels(), rotation=45, horizontalalignment="right")
count_plot.get_figure().savefig("Crime Code Counts1.png", dpi=600, bbox_inches="tight")
count_plot.set_xlabel("Crime Code")
count_plot.set_ylabel("Number of Crimes")

_ = count_plot.set_title("Number of Crimes by Type")
#this is where plotting came in, and creation of visualizations 
# above is the number of different crimes 

bar_crime_count = sns.barplot(x=area_counts["AREA"], y=area_counts["Count"], palette="deep")
bar_crime_count.set_xlabel("Police Department Areas")
bar_crime_count.set_ylabel("Number of Crimes")
t = bar_crime_count.set_title("Number of Crimes by Area")
# this is a chart of crimes by area, showing the differences for areas specifically 

# cleaned up empty categories "X" and "H"
vict_sex = ["M", "F"]
df_cleaner1 = df[df["Vict Sex"].isin(vict_sex)]
gender_scatter = sns.boxplot(x=area_counts["Count"], y=df_cleaner1["Vict Sex"], boxprops={"alpha": 0.7})

scatter_title = gender_scatter.set_title("Number of Crimes by Sex")
_ = gender_scatter.set_xlabel("Number of Crimes")
__ = gender_scatter.set_ylabel("Sex of Victim")
# wanted to see if gender had any effect on crimes being comitted


# exploring times when crimes occured 
df_hours = df_cleaner
df_hours['TIME OCC'] = df_hours['TIME OCC'].astype(str)
df_hours['TIME OCC'] = df_hours['TIME OCC'].str[:-2]
df_hours.loc[df_hours["TIME OCC"] == "", "TIME OCC"] = '00'
# one issue was that the 12am hour was just 2 digits
# replaced the empty values with 00, following military time still
df_hours["TIME OCC"].unique()
# got us our what we can group by
df_hours_1 = df_hours.groupby(['TIME OCC'])['Crm Cd'].count()
df_hours_1 = df_hours_1.to_frame()

time_code = ['0000','0100','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','0200','2000','2100','2200','2300','0300','0400','0500','0600','0700','0800','0900']
df_hours_1["Hour Code"] = time_code
df_hours_1 = df_hours_1.sort_values(by=['Hour Code'])
# sets everything to military time 

time_line = sns.scatterplot(x=df_hours_1['Hour Code'], y=df_hours_1['Crm Cd'])
time_line.set_xticklabels(time_line.get_xticklabels(), rotation=45)
____= time_line.set_xlabel("Time of Day"), time_line.set_ylabel("Amount of Crimes")
_____ = time_line.set_title("Crime by Hour")


