#!/usr/bin/env python
# coding: utf-8

# In[63]:


#import the useful libraries.
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
#import the warnings.
import warnings
warnings.filterwarnings('ignore', '.*do not.*', )
warnings.warn('DelftStack')
warnings.warn('Do not show this message')


# In[64]:


# import the data
df = pd.read_csv("Uber Request Data.csv")


# In[65]:


# Cross checking the data
df.head()


# In[66]:


# FInding the shape of data
df.shape


# In[67]:


# finding the details pertaining to various coloumns
df.info()


# In[68]:


# To get an idea of distribution of trips across the city
df["Pickup point"].value_counts()


# In[70]:


# To find out the Trip Status across the various values
df.Status.value_counts()


# In[268]:


# Converting the date data into proper date time format
df['Request timestamp'] = pd.to_datetime(df['Request timestamp'])
df["Drop timestamp"]= pd.to_datetime(df['Drop timestamp'])


# In[269]:


df.info()


# In[270]:


# Creating a new coloumn for the hour of the trip when its getting initiated
df["hour"] = df['Request timestamp'].dt.hour


# In[79]:


# Performing a simple check for the new coloumn hour how it is appearing in data set
df.head()


# In[80]:


# Cross checking the coloumn info 
df.info()


# In[81]:


# Hourly disctribution of data which will show all trips across data set
df.hour.value_counts()


# ## Created a function to split the hour into sessions viz - Late Night,Early Morning,Morning,Afternoon,Evening and Night which will be used for visualization purpose.

# In[92]:



def session(hour):
    if hour > 0 and hour <= 4:
        return ('Late Night')
    elif hour > 4 and hour <= 7:
        return ('Early Morning')
    elif hour > 7 and hour <= 12:
        return('Morning')
    elif hour > 12 and hour <= 16:
        return('Afternoon')
    elif hour > 16 and hour <= 19:
        return('Evening')
    else:
        return('Night')


# In[93]:


# Creating a new coloumn for session and applying the above session function
df["session"]=df["hour"].apply(session)


# In[119]:


df.head()


# ## Question - 1 : Visually identify the most pressing problems for Uber. 
# Hint: Create plots to visualize the frequency of requests that get canceled or show 'no cars available'; identify the most problematic types of requests (city to airport/airport to city etc.) and the time slots (early mornings, late evenings etc.) using plots

# In[120]:


df.session.value_counts()


# In[121]:


df['Status'].value_counts()


# In[122]:


df[df['Status']=='Trip Completed'].session.value_counts()


# # Visual representation of Status of the trip

# In[134]:


plot = sns.catplot(x="Status", kind="count", data=df);


# # Visual representation of trips across Pickup points

# In[135]:


sns.countplot(x="Pickup point", data=df)
plt.show()


# # Visual Represenation of Status of trip across the pick up points

# In[286]:


plt.figure(figsize=(15,10))
sns.catplot(x="Pickup point", hue="Status", kind="count", data=df)
plt.show()


# #  Above plot tells us that
# # 1) No Cars Available status count is very high at Airport.
# # 2) Cancelled status count is more in city.

# # Grouping by the pickup points and check the status of the trip

# In[282]:


df.groupby(['Pickup point']).Status.value_counts().unstack(0).plot.bar()
plt.show();


# In[267]:


# CHecking the cancelled trips across all the time slots
df[df['Status']=='Cancelled'].session.value_counts().plot.bar()


# In[288]:


#plot of no. of requests from city to airport/airport to city
plt.figure(figsize=(12,10))
sns.barplot(x='hour', y='Request id', hue='Pickup point',data=df, estimator=len)
plt.title("frequency of request from city-airport/airport-city")
plt.ylabel("count of Request id")
plt.show()


# ### As we can see in the above plot that most of the people requests for the car in the Morning or Evening.
# ### Morning and Evening are the time when there is rush.

# # Grouping Status and Pickup point and check the no of trips based on all the time slots - i.e Night , Morning , Late Night , Evening , Early Morning , Afternoon.

# In[58]:


df.groupby(by=['Status','Pickup point']).session.value_counts().unstack(0).plot.barh(figsize=(15, 10))


# In[228]:


df.groupby(by=['Status','Pickup point']).session.value_counts()


# # Visual representation in seaborn to have better clarity of the dataset based on pickup point , status 

# In[253]:


data=df.groupby(by=['Status','Pickup point']).session.value_counts().reset_index(name='Count')

plt.figure(figsize=(15,8))
p = sns.barplot(x='Pickup point', y='Count', data=data, hue='Status')


# In[252]:


plt.figure(figsize=(15,8))
p = sns.barplot(x='session', y='Count', data=data, hue='Status')


# ## Visual represenation of status of the trips completed (w.r.t to pickup point City and Airport) along with Time Slots.

# In[299]:


sns.catplot(x='Pickup point',col="Status", hue = 'hour',data=df ,kind="count")
plt.show()


# - More cars are cancelled from city - airport, for timeslots between 4:00 AM and 11:59 AM
# - More cars are unavailable from airport - city, for timeslots between 4:00 PM and 11:59 PM

# In[300]:


sns.catplot(x='Pickup point',col="Status", hue = 'session',data=df ,kind="count")
plt.show()


# ### Answer: 

# >>> ### Pressing problems are No cars are Available from Airport in Evening and Night
# >>> ### Cancelled requests in City is very high in Early Morning and Morning

# In[182]:


df[(df.Status == 'No Cars Available') | (df.Status == 'Cancelled')]


# In[177]:


df[(df.Status == 'No Cars Available') | (df.Status == 'Cancelled')]["Pickup point"].value_counts().plot.bar()


# ### Above analysis shows that withing 2 pickup points i.e Airport And City unavailaibility of cars (Cancelled and No Cars available ) are almost same,however city have slightly more requests than airport.

# # Question 2

# ### Find out the gap between supply and demand and show the same using plots.
# ### Find the time slots when the highest gap exists
# ### Find the types of requests (city-airport or airport-city) for which the gap is the most severe in the identified time slots

# In[292]:


# Create a new coloumn to AvailabilityStatus and merge the categories of "No Cars Available" and "Cancelled" to "Unavailable", and Trips Completed to Available.

df["AvailabilityStatus"]=df["Status"].replace({"No Cars Available":"Unavailable","Cancelled":"Unavailable","Trip Completed":"Available"})


# In[293]:


df.groupby(by=['AvailabilityStatus','Pickup point']).session.value_counts()


# In[294]:


sns.catplot(x="Pickup point", hue="AvailabilityStatus", kind="count", data=df);


# In[212]:


sns.catplot(x='AvailabilityStatus',col="Pickup point", hue = 'session',data=df ,kind="count")
plt.show()


# ### From the above plots it is clear that :
# 
# ### - For airport pickups, demand is more during the evening and night session slots
# ### - For city pickups, demand is more during the early morning and morning

# In[221]:


df.groupby(by=["session","AvailabilityStatus"])["Pickup point"].value_counts()


# In[297]:


# Checking the supply demand gap based on time slots 

most_severe_gap = df[((df['session'] == 'Evening') |
                           (df['session'] == 'Night') | 
                           (df['session'] == 'Early Morning') | 
                           (df['session'] == 'Morning') |
                           (df['session'] == 'Afternoon')) & 
                          (df['AvailabilityStatus'] == 'Unavailable')] 

plot = sns.catplot(x="session", hue="Pickup point", data=most_severe_gap, kind="count", 
            height=4, aspect = 3.2)

plot.fig.suptitle('Gap for cabs originating from airport and city based on time slots ', fontsize=12)
plot.set_xlabels('Time Slot', fontsize=12)
plot.set_ylabels('Supply Demand Gap', fontsize=12)
plt.show()


# In[298]:


gap = df[(df['AvailabilityStatus'] == 'Unavailable')] 


plot = sns.catplot(x="hour", hue="Pickup point", data=gap, kind="count", 
            height=4, aspect = 3.2)

plot.fig.suptitle('Gap for cabs originating from airport and city hourly basis', fontsize=12)
plot.set_xlabels('Hourly', fontsize=12)
plot.set_ylabels('Supply Demand Gap', fontsize=12)
plt.show()


# # Answer 
# >>> ### Observation so far:
# The problematic status are 'cancelled' and 'no cars available' as it leads to potential loss of revenue. We observed the hightest value of:
# 
# #### Status: "No car available"
# Where is it happening: Airport - i.e airport to city
# When is it happening: Evening 
# 
# #### Status: "Cancelled"
# Where is it happening: City - i.e city to airport
# When is it happening: Morning
# 
# 
# >>> ### To make our analayse our observation so far, we further looked into the 'gap' with hous . This again is in sync with above observations. The 'gap' which exists are the hightest:
# 
# #### Status: "No car available"
# Where is it happening: Airport - i.e airport to city
# When is it happening: Evening - (from 17:00 to 21:00)
# 
# #### Status: "Cancelled"
# Where is it happening: City - i.e city to airport
# When is it happening: Morning. (from 05:00 to 10:00)
# 

# In[317]:


# Demand Supply Pie chart
labels = ['Gap', 'Supply', 'Demand']
sizes = [df['AvailabilityStatus'].value_counts()[0],df['AvailabilityStatus'].value_counts()[1],
         df['AvailabilityStatus'].count()]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
plt.axis('equal')
plt.show()

