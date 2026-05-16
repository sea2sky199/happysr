import numpy as np

class iLBSplusFAP:
    def __init__(self):
        # creates a data structure for a combination of lockbox spending
        # and future purchase of an annuity

        # lockbox proportions (matrix with TIPS in top row, market in bottom row
        self.lockboxProportions = np.array([])

        # lockbox spending bequest utility ratio for spending
        self.bequestUtilityRatio = 0.50

        # year in which annuity is to be purchased
        self.annuitizationYear = 20

        # set initial proportion in TIPS for lockbox to be used to purchase annuity
        self.FAPlockboxProportionInTIPS = 0.50

        # annuity ratio of value to initial cost
        self.annuityValueOverCost = 0.90

        # percentile of income distribution to match for FAP and last
        # spending lockbox (0 to 100)
        self.incomePercentileToMatch = 75

        # total amount invested
        self.amountInvested = 100000