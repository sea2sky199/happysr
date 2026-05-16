from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from AMDnLockboxes_create import AMDnLockboxes_create
from AMDnLockboxes_process import AMDnLockboxes_process
from iLockboxSpending_create import iLockboxSpending_create
from iLockboxSpending_process import iLockboxSpending_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

AMDnLockboxes = AMDnLockboxes_create()
AMDnLockboxes['showProportions'] = 'n'
AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client)

iLockboxSpending = iLockboxSpending_create()
iLockboxSpending['lockboxProportions'] = AMDnLockboxes['proportions']
iLockboxSpending['bequestUtilityRatio'] = 0.5
iLockboxSpending['showLockboxAmounts'] = 'y'
client, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, client, market)

analysis = analysis_create()
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [[3, 1, 2]]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotIncomeDistributionsPctMaxIncome'] = 50
analysis['plotRecipientPVs'] = 'y'
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[3, 1, 2]]
analysis_process(analysis, client, market)
