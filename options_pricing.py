from enum import Enum
import math

import numpy as np
from scipy.stats import norm

class payoff_type(Enum) :
    european = 1
    asian = 2

class pricing_method(Enum) :
    black_scholes = 1
    monte_carlo = 2

class contract_type(Enum):
    call = 1
    put = 2

class Option :
    def __init__(self, spot, exer, rate, vol, matur, type, payoff_type, asian_period = None):
        self.spot = spot
        self.exer = exer
        self.rate = rate
        self.vol = vol
        self.matur = matur
        self.type = type
        self.payoff_type = payoff_type
        self.asian_period = asian_period
        self.price = None

        if self.payoff_type == payoff_type.asian :
            assert self.asian_period != None , "you must give a value for asian_period"
            self.asian_period = asian_period
            assert self.asian_period <= self.matur/12*252 , " asian period should not be smaller than contract's maturity period"



    def black_scholes(self):

        assert self.payoff_type == payoff_type.european , " Black_Scholes can only be used for European options"

        d1 = (math.log(self.spot/self.exer) + (self.rate + (self.vol**2)/2)*self.matur/12)/self.vol/math.sqrt(self.matur/12)
        d2 = d1 - self.vol*math.sqrt(self.matur/12)

        if self.type == contract_type.call :
            self.price = self.spot*norm.cdf(d1) - self.exer*math.exp(-self.rate*self.matur/12)*norm.cdf(d2)
        else :
            self.price = self.exer*math.exp(-self.rate*self.matur/12)*norm.cdf(-d2) - self.spot*norm.cdf(-d1)

        return self.price

    def monte_carlo(self , num_sim = 10000 ):

        assert num_sim >= 10000 , "to get a reliable result num_sim must be greater than 10000 "
        dt = 1/252
        days = self.matur/12*252
        days = int(days)
        s = np.zeros([num_sim , days])
        for i in range(num_sim) :
            s[i,0] = self.spot
            for j in range(1,days) :
                s[i,j] = s[i,j-1]*math.exp((self.rate - (self.vol**2)/2)*dt + self.vol*math.sqrt(dt)*np.random.standard_normal(1))

        if self.payoff_type == payoff_type.european :
            if self.type == contract_type.call :
                disc_values = np.maximum((s[:,days -1] - self.exer)*math.exp(-self.rate*self.matur/12) , 0)
                self.price = disc_values.mean()
            else :
                disc_values = np.maximum((self.exer - s[:,days -1])*math.exp(-self.rate*self.matur/12) , 0)
                self.price = disc_values.mean()
        else :
            period = int(self.asian_period/12*252)
            if self.type == contract_type.call:
                disc_values = np.maximum(np.average(s[:,days - period:] , axis = 1) - self.exer, 0) * math.exp(-self.rate*self.matur/12)
                self.price = disc_values.mean()
            else :
                disc_values = np.maximum(np.average(self.exer - s[:, days - period:], axis=1), 0) * math.exp(-self.rate * self.matur / 12)
                self.price = disc_values.mean()

        return  self.price