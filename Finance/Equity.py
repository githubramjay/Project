import numpy

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
    def genCall(self, expiry, strike, IR):
        pass
    def genPut(self, expiry, strike, IR):
        pass

if __name__ == '__main__':
    one = Equity()
    two = Equity('AAPL')
    three = Equity('GOOG', [10,20,30])
    print(one)
    print(two)
    print(three)
