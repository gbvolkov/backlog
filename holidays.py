import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np


def read_dates(name: str) -> np.ndarray:
    return pd.read_csv(name, parse_dates=['day'], dayfirst=False)['day'].to_numpy(dtype='datetime64[D]')

def get_dates_range(dates: np.ndarray, date1: datetime, date2: datetime) -> np.ndarray:
    return dates[(dates >= np.datetime64(date1.date())) & (dates <= np.datetime64(date2.date()))]


class BusCalendar:
    def __init__(self):
        start_dt = date(2020, 1, 1)
        end_dt = date(2024, 12, 31)
        
        hdays = read_dates('holidays20-24.csv')
        bdays_plus = read_dates('busdays20-24.csv')
        wedays = pd.bdate_range(start_dt, end_dt, weekmask='0000011', freq='C', inclusive='both').to_numpy(dtype='datetime64[D]')

        self.hdays = np.array(list((set(hdays) | set(wedays)) - set(bdays_plus)))
        self.bdays_calendar = np.busdaycalendar(weekmask='1111111', holidays=self.hdays)

        self.wedays = wedays
        self.bdays_plus = bdays_plus
        self.bdays = pd.bdate_range(start_dt, end_dt, weekmask='1111111', freq='C', holidays=self.hdays, inclusive='both').to_numpy(dtype='datetime64[D]')

    def date_diff(self, date1, date2) -> int:
        return np.busday_count(date1.date(), (date2 + timedelta(days=1)).date(), busdaycal=self.bdays_calendar)

    def get_bdays(self, date1, date2) -> np.ndarray:
        return get_dates_range(self.bdays, date1, date2)

    def get_hdays(self, date1, date2) -> np.ndarray:
        return get_dates_range(self.hdays, date1, date2)

    def get_wedays(self, date1, date2) -> np.ndarray:
        return get_dates_range(self.wedays, date1, date2)

    def get_bdays_plus(self, date1, date2) -> np.ndarray:
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

