import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np

def remove_weekends(dates: np.ndarray)->np.array:
    return dates[dates['day'].dt.weekday < 5].day.values.astype('datetime64[D]')

def get_weekends(dates: pd.DataFrame)->np.array:
    return dates[dates['day'].dt.weekday >= 5].day.values.astype('datetime64[D]')

def read_dates(name: str)->np.array:
    df_days = pd.read_csv(name)
    return df_days['day'].apply(pd.to_datetime, '%m/%d/%Y').values.astype('datetime64[D]')

def get_dates_range(dates: np.array, date1: datetime, date2: datetime)-> np.array:
    return dates[np.logical_and(dates[:] >= date1.date(), dates[:]<=date2.date())]

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
        self.bdays = np.array(list(set(bdays['day'].apply(pd.to_datetime, '%m/%d/%Y').values.astype('datetime64[D]')) - ((set(hdays) | set(wedays)) - set(bdays_plus))))

    def date_diff(self, date1, date2)->int:
        bdays = np.busday_count(date1.date(), (date2+timedelta(days=1)).date(), weekmask = '1111111', holidays = self.hdays)
        return int(bdays)
    def get_bdays(self, date1, date2)->np.array:
        return get_dates_range(self.bdays, date1, date2)
    def get_hdays(self, date1, date2)->np.array:
        return get_dates_range(self.hdays, date1, date2)
    def get_wedays(self, date1, date2)->np.array:
        return get_dates_range(self.wedays, date1, date2)
    def get_bdays_plus(self, date1, date2)->np.array:
        return get_dates_range(self.bdays_plus, date1, date2)
    

cal = BusCalendar()

cdays = cal.date_diff(datetime(2022,2,20), datetime(2022,3,10))
hdays = cal.get_hdays(datetime(2022,2,20), datetime(2022,3,10))
bdays_plus = cal.get_bdays_plus(datetime(2022,2,20), datetime(2022,3,10))
wedays = cal.get_wedays(datetime(2022,2,20), datetime(2022,3,10))
bdays = cal.get_bdays(datetime(2022,2,20), datetime(2022,3,10))
print(hdays)
print(bdays_plus)
print(wedays)
print(bdays)


print(cdays)

