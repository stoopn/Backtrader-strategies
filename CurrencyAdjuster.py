#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016, 2017 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

class CurrencyDataFilter(bt.with_metaclass(bt.metabase.MetaParams, object)):
    '''
        The filter remodels the open, high, low, close to make HeikinAshi
        candlesticks
        '''
    params = (('currencydata',None),)

    def __init__(self, data):
        pass
    
    def __call__(self, data):
        o, h, l, c = data.open[0], data.high[0], data.low[0], data.close[0]
        #print("BLABLA")
        if self.p.currencydata is None:  # use the 1st data in the system if none given
            print("Warning, no currency data given!")
        if len(self.p.currencydata):
            cc = self.p.currencydata.open[0]
        else:
            cc=1
            print(cc)
            print(data)
        #print("BLABLA2")

        data.close[0] = c/cc
        #print("CCHF %.2f, CUSD: %.2f, USDCHF: %.2f" %(c,c/cc,cc))
        data.open[0] = o/cc
        data.high[0] = h/cc
        data.low[0] = l/cc
        #print("BLABLA3")

        return False  # length of data stream is unaltered



class PortfolioCurrencyAdjuster(bt.Observer):
    '''This observer tracks the broker value in another currency

    '''
    _stclock = True

    lines = ('currencybroker',)
    plotlines = dict(currencybroker=dict(_name='Cur. adj. broker'))

    params = (
        ('data', None),
        ('_doprenext', False),
        # Set to false to ensure the asset is measured at 0% in the 1st tick
    )

    def _plotlabel(self):
        labels = super(PortfolioCurrencyAdjuster, self)._plotlabel()
        labels.append(self.p.data._name)
        return labels

    def __init__(self):
        if self.p.data is None:  # use the 1st data in the system if none given
            print("Warning, no currency data given!")
        super(PortfolioCurrencyAdjuster, self).__init__()
        

    def next(self):
        self.lines.currencybroker[0] = self._owner.broker.getvalue()*self.p.data[0]

