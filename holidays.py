import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np


def read_dates(name: str) -> pd.Series:
    return pd.read_csv(name, parse_dates=['day'], dayfirst=False)['day']

def get_dates_range(dates: pd.Series, date1: datetime, date2: datetime) -> pd.Series:
    return dates[(dates >= date1) & (dates <= date2)]


class BusCalendar:
    def __init__(self):
        start_dt = date(2020, 1, 1)
        end_dt = date(2024, 12, 31)

        hdays = read_dates('holidays20-24.csv')
        bdays_plus = read_dates('busdays20-24.csv')
        wedays = pd.bdate_range(start_dt, end_dt, weekmask='0000011', freq='C', inclusive='both')

        nwdays = pd.Series(sorted((set(hdays) | set(wedays)) - set(bdays_plus)))
        self.bdays_calendar = np.busdaycalendar(weekmask='1111111', holidays=nwdays.to_numpy(dtype='datetime64[D]'))

        self.nwdays = nwdays
        self.wedays = pd.Series(wedays)
        self.bdays_plus = bdays_plus
        self.bdays = pd.Series(pd.bdate_range(start_dt, end_dt, weekmask='1111111', freq='C', holidays=nwdays.dt.date.values, inclusive='both'))

    def date_diff(self, date1, date2) -> int:
        return np.busday_count(date1.date(), (date2 + timedelta(days=1)).date(), busdaycal=self.bdays_calendar)

    def get_bdays(self, date1, date2) -> pd.Series:
        return self.bdays[self.bdays.between(date1, date2)]

    def get_nwdays(self, date1, date2) -> pd.Series:
        return self.nwdays[self.nwdays.between(date1, date2)]

    def get_wedays(self, date1, date2) -> pd.Series:
        return self.wedays[self.wedays.between(date1, date2)]

    def get_bdays_plus(self, date1, date2) -> pd.Series:
        return self.bdays_plus[self.bdays_plus.between(date1, date2)]


#cal = BusCalendar()

#cdays = cal.date_diff(datetime(2022,2,20), datetime(2022,3,10))
#nwdays = cal.get_nwdays(datetime(2022,2,20), datetime(2022,3,10))
#bdays_plus = cal.get_bdays_plus(datetime(2022,2,20), datetime(2022,3,10))
#wedays = cal.get_wedays(datetime(2022,2,20), datetime(2022,3,10))
#bdays = cal.get_bdays(datetime(2022,2,20), datetime(2022,3,10))
#print(nwdays)
#print(bdays_plus)
#print(wedays)
#print(bdays)
#print(cdays)
