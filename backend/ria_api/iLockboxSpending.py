import numpy as np

class iLockboxSpending:
    def __init__(self):
        # create a lockbox spending data structure

        # amount invested
        self.investedAmount = 100000

        # relative payments from lockboxes: size(2,client number of years)
        # row 1: tips
        # row 2: market portfolio
        # may be provided by AMDnLockboxes.proportions, CMULockboxes.proportions,
        # combinedLickboxes.proportions or otherwise
        # note: lockboxes are to be spent for personal states 1,2,3 or 4
        self.lockboxProportions = np.array([])

        # bequest utility ratio
        # ratio of utility per dollar for bequest versus spending
        # note: this applies equally for personal states 1,2 and 3
        self.bequestUtilityRatio = 0.50

        # show lockbox amounts (y or n)
        self.showLockboxAmounts = 'y'