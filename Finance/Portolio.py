import numpy
from Equity import Equity
import yahoo_finance as fin

#Minimum Variance Portfolio Allocation
class Portfolio:
    def __init__(self, equities=()):
        self.equities = equities
        self.Return = 0.0
        self.Risk = 0.0
    #returns as a tuple, covariance as a numpy matrix, positions as dictionary
    def allocate(self):
        global covariance
        global returns
        global positions
        returns = []
        covariance = []
        positions = {}
        size = len(self.equities)
        for x in self.equities:
            returns.append(tuple(x.RETURNS))
        for _ in range(size):
            covariance.append([])
        for x in covariance:
            for y in range(size):
                x.append(0.0)
        for i in range(size):
            for j in range(size):
                covariance[i][j] = float(numpy.cov(returns[i],
                    returns[j])[0][1])
        covariance = numpy.asmatrix(covariance)
        u = [1 for _ in range(size)]
        u = numpy.asmatrix(u)
        uT = u.transpose();
        C = numpy.linalg.inv(covariance)
        top = u.dot(C)
        bottom = u.dot(C).dot(uT)[0,0]
        top = top.tolist()
        p = top/bottom
        p = p.tolist()[0]
        names = [x.NAME for x in self.equities]
        positions = dict(zip(names,p))
        self.genRet()
        self.genRisk()
    def genRet(self):
        weights = [w for w in positions.values()]
        weights = numpy.asmatrix(weights)
        weights = weights.transpose()
        m = [m.RETURN for m in self.equities]
        m = numpy.asmatrix(m)
        self.Return = m.dot(weights)[0,0]
    def genRisk(self):
        weights = [w for w in positions.values()]
        weights = numpy.asmatrix(weights)
        self.Risk = weights.dot(covariance).dot(weights.transpose())[0,0]**.5
    def __str__(self):
        return positions.__str__() + ' Return: ' + str(self.Return) + ' Risk: ' + str(self.Risk)
    def basket(self):
        pass

if __name__ == '__main__':
    gstock = fin.Share('GOOG')
    ghist = gstock.get_historical('2017-01-07', '2017-04-07')
    gprices = [p['Close'] for p in ghist]
    astock = fin.Share('AAPL')
    ahist = astock.get_historical('2017-01-07', '2017-04-07')
    aprices = [p['Close'] for p in ahist]
    mstock = fin.Share('MSFT')
    mhist = mstock.get_historical('2017-01-07', '2017-04-07')
    mprices = [p['Close'] for p in mhist]

    google = Equity('GOOG', gprices)
    apple = Equity('AAPL', aprices)
    microsoft = Equity('MSFT', mprices)
    p = Portfolio((google, apple, microsoft))
    p.allocate()
    for x in p.equities:
        print(x)
        print(x.PRICES)
    print(p)
