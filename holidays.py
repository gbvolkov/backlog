import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np

class BusCalendar:
    def __init__(self):
        h_df = pd.read_csv('holidays20-24.csv')
        h_df['day'] = h_df['day'].apply(pd.to_datetime, '%m/%d/%Y')
        h_df = h_df[h_df['day'].dt.weekday < 5].day.values.astype('datetime64[D]')
        
        self.hdays = h_df
        b_df = pd.read_csv('busdays20-24.csv')
        b_df['day'] = b_df['day'].apply(pd.to_datetime, '%m/%d/%Y')
        b_df = b_df[b_df['day'].dt.weekday >= 5].day.values.astype('datetime64[D]')

        self.bdays = b_df
        
    
    def date_diff(self, date1, date2)->int:
        #print(type(date1))
        #print(type(date1.date()))
        bdays = np.busday_count(date1.date(), date2.date(), weekmask = '1111100', holidays = self.hdays)
        return bdays

