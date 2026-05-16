import numpy as np
from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iSocialSecurity_create import iSocialSecurity_create
from iSocialSecurity_process import iSocialSecurity_process
from iConstSpending_create import iConstSpending_create
from iConstSpending_process import iConstSpending_process
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

iConstSpending = iConstSpending_create()
iConstSpending['glidePath'] = [[1], [1]]
iConstSpending['retentionRatio'] = 0.999
iConstSpending['initialProportionSpent'] = 0.040
iConstSpending['graduationRatio'] = 1.00
iConstSpending['pStateRelativeIncomes'] = [1, 1, 1]
iConstSpending['investedAmount'] = 1000000
iConstSpending['showGlidePath'] = 'y'
client = iConstSpending_process(iConstSpending, client, market)

analysis = analysis_create()
analysis['animationDelays'] = [0.5, 0.5]
analysis['animationShadowShade'] = 1
analysis['figuresCloseWhenDone'] = 'n'
analysis['stackFigures'] = 'y'
analysis['figureDelay'] = 0
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotRecipientPVs'] = 'y'
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[1, 2], [3]]
analysis_process(analysis, client, market)
