from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iGLWB_create import iGLWB_create
from iGLWB_process import iGLWB_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

iGLWB = iGLWB_create()
client, iGLWB = iGLWB_process(client, market, iGLWB)

analysis = analysis_create()
analysis['animationDelays'] = [1, 0.5]
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [[3, 1, 2]]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotIncomeDistributionsPctMaxIncome'] = 50
analysis['plotYOYIncomes'] = 'n'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [[3, 1, 2]]
analysis['plotRecipientPVs'] = 'y'
analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['rc']
analysis['plotIncomeMapsStates'] = [[3, 1, 2]]
analysis['plotIncomeMapsMinPctScenarios'] = 0.5
analysis['plotIncomeMapsPctMaxIncome'] = 25
analysis['plotPPCSandIncomes'] = 'y'
analysis['plotPPCSandIncomesSemilog'] = 'y'
analysis['plotPPCSandIncomesStates'] = [[3, 1, 2]]
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[3, 1, 2]]
analysis['plotEfficientIncomes'] = 'n'
analysis['plotEfficientIncomesStates'] = [[3, 1, 2]]
analysis['plotEfficientIncomesTypes'] = ['pcl']
analysis_process(analysis, client, market)
