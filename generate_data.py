import datetime
from datetime import date,timedelta
import nsepy
import time
from nsepy import get_history
import pandas as pd
import numpy as np
from tqdm import tqdm
options_data=pd.DataFrame()

#Function generates possible expiry dates for the given date
def possible_expiry_date(date):
    dates=[]
    for i in expiry_dates:
        if i>date and (i-date).days<365:
            dates.append(i)
    return dates

#Reading the dates where the options will expire

file1 = open('dates.txt', 'r') 
dates=[]
for lines in file1:
    temp=lines.split()[2]
    if temp[0]=='"':
        dates.append(temp[1:-2])
expiry_dates=[date(int(i.split('-')[2]),int(i.split('-')[1]),int(i.split('-')[0])) for i in dates]
expiry_dates=list(set(expiry_dates))
expiry_dates.sort()
expiry_dates=expiry_dates[3:]   

#Generating date range
date_range=[]
sdate = date(2015, 10, 2)   # start date
edate = date(2020, 10, 5 )   # end date
delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    date_range.append(sdate + timedelta(days=i))   
#Getting data from NSE website
count=0
for a in tqdm(date_range):
    count+=1
    #Options trading does not happen on weekends
    temp=pd.DataFrame()
    if a.weekday()==5 or a.weekday()==6:
        continue
    possible_expiry_dates=possible_expiry_date(a)
    for p in possible_expiry_dates:
        nifty_opt = get_history(symbol="NIFTY",start=a,end=a,index=True,option_type='CE',expiry_date=p)
        nifty_opt["DateOfTrade"]=a
        temp=temp.append(nifty_opt)
    options_data=options_data.append(temp)
    if count%10==0:
        options_data.to_pickle("options.pkl")
        with open("options_data.csv", 'a') as f:
            options_data.to_csv(f, header=f.tell()==0)
        options_data=pd.DataFrame()
options_data.to_csv("options_data.csv",index=False)