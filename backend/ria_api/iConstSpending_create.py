def iConstSpending_create():
    iConstSpending = {}
    iConstSpending['investedAmount'] = 100000
    iConstSpending['initialProportionSpent'] = 0.040
    iConstSpending['pStateRelativeIncomes'] = [0.5, 0.5, 1.0]
    iConstSpending['graduationRatio'] = 1.00
    iConstSpending['glidePath'] = np.array([[1.0], [1]])
    iConstSpending['showGlidePath'] = 'n'
    iConstSpending['retentionRatio'] = 0.999
    return iConstSpending