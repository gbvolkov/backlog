import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np

def remove_weekends(dates: np.ndarray)->np.array:
    return dates[dates['day'].dt.weekday < 5].day.values.astype('datetime64[D]')

def get_weekends(dates: pd.DataFrame)->np.array:
    return dates[dates['day'].dt.weekday >= 5].day.values.astype('datetime64[D]')

def read_dates(name: str)->np.array:
    df_days = pd.read_csv(name)
    #df_days['day'] = 
    return df_days['day'].apply(pd.to_datetime, '%m/%d/%Y').values.astype('datetime64[D]')

class BusCalendar:
    def __init__(self):
        start_dt = date(2020, 1, 1)
        end_dt = date(2024, 12, 31)
        bdays = pd.DataFrame(pd.date_range(start_dt, end_dt, freq='D', unit="s").date, columns=['day'], dtype='datetime64[ns]')

        hdays = read_dates('holidays20-24.csv')
        wedays = get_weekends(bdays)
        bdays_plus = read_dates('busdays20-24.csv')
        
        self.hdays = np.array(list((set(hdays) | set(wedays)) - set(bdays_plus)))
        self.wedays = np.array(list(set(wedays)))
        self.bdays_plus = np.array(list(set(bdays_plus)))

    def date_diff(self, date1, date2)->int:
        bdays = np.busday_count(date1.date(), (date2+timedelta(days=1)).date(), weekmask = '1111111', holidays = self.hdays)
        return int(bdays)
    

cal = BusCalendar()

cdays = cal.date_diff(datetime(2022,2,20), datetime(2022,3,10))
hdays = np.logical_and(cal.hdays[:] >= datetime(2022,2,20).date(), cal.hdays[:]<=datetime(2022,3,10).date())
bdays = np.logical_and(cal.bdays_plus[:] >= datetime(2022,2,20).date(), cal.bdays_plus[:]<=datetime(2022,3,10).date())
print(cal.hdays[hdays])
print(cal.bdays_plus[bdays])


print(cdays)

