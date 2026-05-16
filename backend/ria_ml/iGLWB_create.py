import numpy as np

def iGLWB_create():
    iGLWB = {}
    iGLWB['initialValue'] = 100000
    iGLWB['singleOrJoint'] = 'j'
    iGLWB['singleLifeWithdrawalRates'] = np.array([[59, 64, 0.040],
                                                    [65, 79, 0.050],
                                                    [80, 120, 0.060]])
    iGLWB['jointLifeWithdrawalRates'] = np.array([[59, 64, 0.035],
                                                   [65, 79, 0.045],
                                                   [80, 120, 0.055]])
    iGLWB['expenseRatioOfTWB'] = 0.0120
    iGLWB['expenseRatioOfFund'] = 0.0054
    iGLWB['saveFeeMatrices'] = 'n'
    return iGLWB
