# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 21:50:05 2018
@author: Deepali
%matplotlib inline
"""

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import CSS4_COLORS
#import seaborn as sns

# File to Load (Remember to change these)
city_data_to_load = "data/city_data.csv"
ride_data_to_load = "data/ride_data.csv"

# Read the City and Ride Data
df_city = pd.read_csv("data/city_data.csv")
df_ride = pd.read_csv("data/ride_data.csv")
#df_city.head()
#df_ride.head()

# Combine the data into a single dataset
df_pyber = df_ride.set_index("city").join(df_city[['city','type','driver_count']].set_index("city"),how="inner")
df_pyber = df_pyber.reset_index(drop=False)
df_pyber.head()

# analyze
average_fare = df_pyber.groupby("city").mean()['fare']
average_fare = pd.DataFrame(average_fare)
total_drivers = df_pyber.groupby("city").mean()['driver_count']
total_drivers = pd.DataFrame(total_drivers)
total_rides = df_pyber.groupby("city").count()["ride_id"]
total_rides = pd.DataFrame(total_rides).rename(columns={"ride_id":"total rides"})
city_type = df_pyber.groupby(['city','type']).count().reset_index(drop=False)[["city","type"]].set_index("city")
df_summary = ((average_fare.join(total_drivers)).join(total_rides)).join(city_type)

# Display the data table for preview
df_summary.head()

#Scatter Bubble plot
df_summary['color'] = df_summary['type'].replace("Urban",CSS4_COLORS['coral'],
	regex=True).replace("Suburban",CSS4_COLORS['lightblue'],
	regex=True).replace("Rural",CSS4_COLORS['gold'],regex=True)
list_type_pyber = ['Urban','Suburban','Rural']
#sns.set()
#sns.set_context("talk")
#sns.set_style("whitegrid")
paths_list = []
for cityType in list_type_pyber:
    I = df_summary.type==cityType
    colorLabel = df_summary[I].color[0]
    dummy = plt.scatter(x=df_summary[I]['total rides'],y=df_summary[I]['fare'],s=3.0*df_summary[I]['driver_count'],color=colorLabel,label=cityType,alpha=0.7)
    paths_list.append(dummy)
plt.xlim(0,40)
plt.ylim(15,55)
plt.xlabel("Total Number of Rides Per City")
plt.ylabel("Average Fare ($) Per City")
plt.title("Scatter Plot - Pyber")
plt.legend(tuple(paths_list),
           tuple(list_type_pyber))
plt.savefig("images/PyberScatterPlot.png")
plt.show()
	
# Pie Chart 1
percent_total_rides = list(df_summary.reset_index().groupby('type').sum()['total rides']/df_summary.reset_index().groupby('type').sum()['total rides'].sum()*100)
type_labels = list(df_summary.reset_index().groupby('type').sum()['total rides'].index)
plt.pie(percent_total_rides,
        colors=(CSS4_COLORS['gold'],
                CSS4_COLORS['lightblue'],
                CSS4_COLORS['coral']),
        labels=type_labels,
        explode=[0.05,0.05,0.05],
        shadow=True,
        autopct='{:5.2f}%'.format)
plt.title("% Total Rides by City Type")
plt.savefig("images/PyberTotalRidesbyCity.png")
plt.show()

# Pie Chart 2
percent_total_fare = list(df_summary.reset_index().groupby('type').sum()['fare']/df_summary.reset_index().groupby('type').sum()['fare'].sum()*100)
type_labels = list(df_summary.reset_index().groupby('type').sum()['fare'].index)
plt.pie(percent_total_fare,
        colors=(CSS4_COLORS['gold'],
                CSS4_COLORS['lightblue'],
                CSS4_COLORS['coral']),
        labels=type_labels,
        explode=[0.05,0.05,0.05],
        shadow=True,
        autopct='{:5.2f}%'.format)
plt.title("% Total Fares by City Type")
plt.savefig("images/PyberTotalFaresbyCity.png")
plt.plot()

# Pie Chart 3
percent_total_farepercent_  = list(df_summary.reset_index().groupby('type').sum()['driver_count']/df_summary.reset_index().groupby('type').sum()['driver_count'].sum()*100)
type_labels = list(df_summary.reset_index().groupby('type').sum()['driver_count'].index)
plt.pie(percent_total_fare,
        colors=(CSS4_COLORS['gold'],
                CSS4_COLORS['lightblue'],
                CSS4_COLORS['coral']),
        labels=type_labels,
        explode=[0.05,0.05,0.05],
        shadow=True,
        autopct='{:5.2f}%'.format)
plt.title("% Total Drivers by City Type")
plt.savefig("images/PyberTotalDriversbyCity.png")
plt.plot()












