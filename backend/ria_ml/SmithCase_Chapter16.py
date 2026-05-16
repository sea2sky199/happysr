import numpy as np
from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iSocialSecurity_create import iSocialSecurity_create
from iSocialSecurity_process import iSocialSecurity_process
from AMDnLockboxes_create import AMDnLockboxes_create
from AMDnLockboxes_process import AMDnLockboxes_process
from iLBAnnuity_create import iLBAnnuity_create
from iLBAnnuity_process import iLBAnnuity_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

iSocialSecurity = iSocialSecurity_create()
iSocialSecurity['state1Incomes'] = np.array([[np.inf, 30000]])
iSocialSecurity['state2Incomes'] = np.array([[np.inf, 30000]])
iSocialSecurity['state3Incomes'] = np.array([44000])
client = iSocialSecurity_process(iSocialSecurity, client, market)

AMDnLockboxes = AMDnLockboxes_create()
AMDnLockboxes['cumRmDistributionYear'] = 2
AMDnLockboxes['showProportions'] = 'y'
AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client)

iLBAnnuity = iLBAnnuity_create()
iLBAnnuity['cost'] = 1000000
iLBAnnuity['proportions'] = AMDnLockboxes['proportions']
client = iLBAnnuity_process(iLBAnnuity, client, market)

analysis = analysis_create()
analysis['animationDelays'] = [0.5, 0.5]
analysis['animationShadowShade'] = 0.2
analysis['figuresCloseWhenDone'] = 'n'
analysis['stackFigures'] = 'n'
analysis['figureDelay'] = 0
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [[3], [1, 2]]
analysis['plotIncomeDistributionsProportionShown'] = 0.999
analysis['plotYOYIncomes'] = 'y'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [[3], [1, 2]]
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotRecipientPVs'] = 'y'
analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['r']
analysis['plotIncomeMapsStates'] = [[3], [1, 2]]
analysis['plotPPCSandIncomes'] = 'y'
analysis['plotPPCSandIncomesSemilog'] = 'n'
analysis['plotPPCSandIncomesStates'] = [[3], [1, 2]]
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[3], [1, 2]]
analysis_process(analysis, client, market)
