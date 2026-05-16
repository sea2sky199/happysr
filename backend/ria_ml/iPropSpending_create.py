def iPropSpending_create():
    iPropSpending = {}
    iPropSpending['investedAmount'] = 100000
    iPropSpending['useRMDlifeExpectancies'] = 'y'
    iPropSpending['nonRMDlifeExpectancies'] = []
    iPropSpending['nonRMDfirstLEAge'] = 70
    iPropSpending['portfolioOwnerCurrentAge'] = 65
    iPropSpending['showProportionsSpent'] = 'n'
    iPropSpending['showLockboxEquivalentValues'] = 'n'
    iPropSpending['glidePath'] = [[1.0], [1]]
    iPropSpending['showGlidePath'] = 'n'
    iPropSpending['retentionRatio'] = 0.999
    return iPropSpending
