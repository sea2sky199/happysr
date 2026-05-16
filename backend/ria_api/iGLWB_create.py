import numpy as np

def iGLWB_create():
    # Create a guaranteed lifetime withdrawal benefit data structure

    # Initial amount invested
    iGLWB = {'initialValue': 100000}

    # Single (s) or joint (j) life
    iGLWB['singleOrJoint'] = 'j'

    # Single life withdrawal proportions of TWB (from-age to-age proportion)
    iGLWB['singleLifeWithdrawalRates'] = np.array([[59, 64, 0.040], [65, 79, 0.050], [80, 120, 0.060]])

    # Joint life withdrawal proportions of TWB (from-age to-age proportion)
    # Based on age of younger spouse
    iGLWB['jointLifeWithdrawalRates'] = np.array([[59, 64, 0.035], [65, 79, 0.045], [80, 120, 0.055]])

    # Expense ratio for insurance rider as proportion of TWB
    iGLWB['expenseRatioOfTWB'] = 0.0120

    # Expense ratio for fund management and other fees
    # As proportion of account value
    iGLWB['expenseRatioOfFund'] = 0.0054

    # Save fee matrices with iGLWB data structure (y or n)
    iGLWB['saveFeeMatrices'] = 'n'

    return iGLWB

def iLBSplusDFA_create():
    # Creates a data structure for a combination of lockbox spending
    # and a deferred fixed annuity

    # Lockbox proportions (matrix with TIPS in top row, market in bottom row)
    iLBSplusDFA = {'lockboxProportions': np.array([])}

    # Number of years of lockbox income
    iLBSplusDFA['numberOfLockboxYears'] = 20

    # Lockbox bequest utility ratio
    iLBSplusDFA['bequestUtilityRatio'] = 0.50

    # Percentile of last lockbox year income distribution for fixed annuity
    # 100=lowest income; 50=median income, 0=highest income
    iLBSplusDFA['percentileOfLastLockboxYear'] = 50

    # Fixed annuity ratio of value to initial cost
    iLBSplusDFA['annuityValueOverCost'] = 0.90

    # Total amount invested
    iLBSplusDFA['amountInvested'] = 100000

    return iLBSplusDFA


