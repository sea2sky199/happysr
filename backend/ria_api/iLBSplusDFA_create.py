class iLBSplusDFA:
    def __init__(self):
        # creates a data structure for a combination of lockbox spending
        # and a deferred fixed annuity

        # lockbox proportions (matrix with TIPS in top row, market in bottom row)
        self.lockboxProportions = []

        # number of years of lockbox income
        self.numberOfLockboxYears = 20

        # lockbox bequest utility ratio
        self.bequestUtilityRatio = 0.50

        # percentile of last lockbox year income distribution for fixed annuity
        # 100=lowest income; 50=median income, 0=highest income
        self.percentileOfLastLockboxYear = 50

        # fixed annuity ratio of value to initial cost
        self.annuityValueOverCost = 0.90

        # total amount invested
        self.amountInvested = 100000
