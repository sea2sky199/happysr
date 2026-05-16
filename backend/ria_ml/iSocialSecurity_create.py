import numpy as np

def iSocialSecurity_create():
    iSocialSecurity = {}
    iSocialSecurity['state1Incomes'] = np.array([[np.inf, 30000]])
    iSocialSecurity['state2Incomes'] = np.array([[np.inf, 30000]])
    iSocialSecurity['state3Incomes'] = np.array([44000])
    return iSocialSecurity
