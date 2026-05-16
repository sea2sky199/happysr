import numpy as np
from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from AMDnLockboxes_create import AMDnLockboxes_create
from AMDnLockboxes_process import AMDnLockboxes_process
from iLBSplusFAP_create import iLBSplusFAP_create
from iLBSplusFAP_process import iLBSplusFAP_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

AMDnLockboxes = AMDnLockboxes_create()
AMDnLockboxes['showProportions'] = 'y'
AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client)

iLBSplusFAP = iLBSplusFAP_create()
iLBSplusFAP['lockboxProportions'] = AMDnLockboxes['proportions']

yr = iLBSplusFAP['annuitizationYear']
props = np.array(iLBSplusFAP['lockboxProportions'])[:, yr - 2]
iLBSplusFAP['FAPlockboxProportionInTIPS'] = props[0] / (props[0] + props[1])
client, iLBSplusFAP = iLBSplusFAP_process(client, iLBSplusFAP, market)

analysis = analysis_create()
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [[3, 1, 2]]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotIncomeDistributionsPctMaxIncome'] = 50
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[3, 1, 2]]
analysis['plotRecipientPVs'] = 'y'
analysis_process(analysis, client, market)
