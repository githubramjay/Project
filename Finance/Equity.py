import numpy
import sys
import time
from math import *
import yahoo_finance as fin

class Equity:
    def __init__(self, NAME='N/A', PRICES=[]):
        self.NAME = NAME
        self.PRICES = PRICES
        self.RETURNS = []
        self.RETURN = 0.0
        self.VAR = 0.0
        if len(self.PRICES) > 1:
            self.genData()
    def __str__(self):
        return str(self.NAME + ': Return - ' + str(self.RETURN) + ' Risk - ' +
            str(self.VAR**.5))
    def genData(self):
        prices = list(map(float, self.PRICES))
        comp = list(zip(prices, prices[1:]))
        for x in comp:
            self.RETURNS.append((x[1]-x[0])/x[0])
        self.RETURN = numpy.average(self.RETURNS)
        self.VAR = numpy.var(self.RETURNS)
    def extrapolate(self, expiry):
        stochastic = [numpy.random.normal() for _ in range(1000000)]
        stock = fin.Share(self.NAME)
        S = stock.get_price()
        dol = fin.Currency('USD')
        r = float(dol.get_rate())/100
        values = []
        for x in stochastic:
            A = r - float(self.VAR/2)
            sig = self.VAR**.5
            out = float(S)*exp(A*expiry - sig*sqrt(expiry)*x)
            values.append(out)
        return float(sum(values)/len(values))
    def genCall(self, expiry, strike):
        extrapolated_price = self.extrapolate(expiry)
        print(extrapolated_price)
        values = [extrapolated_price - strike, 0]
        return {'call':self.NAME, 'value':max(values)}
    def genPut(self, expiry, strike, IR):
        extrapolated_price = self.extrapolate(expiry)
        values = [strike - extrapolated_price, 0]
        return {'Put':self.NAME, 'value':max(values)}

if __name__ == '__main__':
    one = Equity()
    two = Equity('AAPL')
    stock = fin.Share('GOOG')
    gprices = []
    for _ in range(10):
        gprices.append(stock.get_price())
        time.sleep(10)
    three = Equity('GOOG', gprices)
    print(one)
    print(two)
    print(three.genCall(.5,700))
