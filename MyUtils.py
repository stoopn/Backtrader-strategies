from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import numpy as np

def ResampleDayToMonth(dates, datas):
    prevmonth = -1
    i = 0
    mondates = np.array([])
    mondatas = np.array([])
    monidx = np.array([])
    startdate = datetime.datetime.fromordinal(int(dates[0]))
    if startdate.day==1:
        mondates = np.append(mondates, dates[0])
        mondatas = np.append(mondatas, datas[0])
        prevmonth = startdate.month
        monidx = np.append(monidx, 0)
    for nowdate, nowdata in zip(dates,datas):
        currdate = datetime.datetime.fromordinal(int(nowdate))
        if currdate.month > prevmonth % 12:
            prevmonth=currdate.month
            mondates = np.append(mondates, nowdate)
            mondatas = np.append(mondatas, nowdata)
            monidx = np.append(monidx, i)
        i += 1
    return (monidx, mondates, mondatas)

def GetAnnualReturns(dates,datas):
    oldyear = datetime.datetime.fromordinal(int(dates[0])).year
    yearbeginsval = datas[0]
    currval = yearbeginsval
    annret_dates=np.array([])
    annret_returns=np.array([])
    i=0
    for nowdate, data in zip(dates,datas):
        prevval = currval
        curryear = datetime.datetime.fromordinal(int(nowdate)).year
        currval = data
        if curryear > oldyear:
            #print("B %.2f, E %.2f" % (yearbeginsval,prevval) )
            annret_returns = np.append(annret_returns, (prevval - yearbeginsval)/yearbeginsval)
            annret_dates = np.append(annret_dates, oldyear)
            oldyear = curryear
            yearbeginsval = prevval
        i += 1
    return (annret_dates, annret_returns)

