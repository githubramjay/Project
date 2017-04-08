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
        return str(self.NAME + ' - Return: ' + str(self.RETURN) + ' Risk: ' +
            str(self.VAR**.5))
    def genData(self):
        prices = list(map(float, self.PRICES))
        comp = list(zip(prices, prices[1:]))
        for x in comp:
            self.RETURNS.append((x[1]-x[0])/x[0])
        self.RETURN = numpy.average(self.RETURNS)
        self.VAR = numpy.var(self.RETURNS)
    def extrapolate(self, time):
        stochastic = [numpy.random.normal() for _ in range(1000000)]
        stock = fin.Share(self.NAME)
        S = stock.get_price()
        dol = fin.Currency('USD')
        r = float(dol.get_rate())/100
        values = []
        for x in stochastic:
            A = r - float(self.VAR/2)
            sig = self.VAR**.5
            out = float(S)*exp(A*time - sig*sqrt(time)*x)
            values.append(out)
        return float(sum(values)/len(values))
    def genCall(self, expiry, strike):
        stochastic = [numpy.random.normal() for _ in range(1000000)]
        stock = fin.Share(self.NAME)
        S = stock.get_price()
        dol = fin.Currency('USD')
        r = float(dol.get_rate())/100
        values = []
        for x in stochastic:
            A = r - float(self.VAR/2)
            sig = self.VAR**.5
            out = [float(S)*exp(A*expiry - sig*sqrt(expiry)*x) - strike, 0]
            values.append(max(out))
        return {'call':self.NAME, 'price':exp(-r*expiry)*numpy.mean(values)}
    def genPut(self, expiry, strike):
        stochastic = [numpy.random.normal() for _ in range(1000000)]
        stock = fin.Share(self.NAME)
        S = stock.get_price()
        dol = fin.Currency('USD')
        r = float(dol.get_rate())/100
        values = []
        for x in stochastic:
            A = r - float(self.VAR/2)
            sig = self.VAR**.5
            out = [strike - float(S)*exp(A*expiry - sig*sqrt(expiry)*x), 0]
            values.append(max(out))
        return {'put':self.NAME, 'price':exp(-r*expiry)*numpy.mean(values)}

if __name__ == '__main__':
    one = Equity()
    two = Equity('AAPL')
    stock = fin.Share('GOOG')
    hist = stock.get_historical('2017-01-07', '2017-04-07')
    gprices = [p['Close'] for p in hist]
    three = Equity('GOOG', gprices)
    print(one)
    print(two)
    print(three)
    print(three.genPut(.5,900))
