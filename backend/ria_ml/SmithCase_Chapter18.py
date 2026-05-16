import numpy as np
from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iPropSpending_create import iPropSpending_create
from iPropSpending_process import iPropSpending_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

iPropSpending = iPropSpending_create()
iPropSpending['investedAmount'] = 1000000
iPropSpending['glidePath'] = [[1, 0], [0, 30]]
iPropSpending['showGlidePath'] = 'y'
iPropSpending['retentionRatio'] = 0.999
client = iPropSpending_process(iPropSpending, client, market)

analysis = analysis_create()
analysis['animationDelays'] = [0.2, 0.2]
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [[1, 2, 3]]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotYOYIncomes'] = 'y'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [[3, 1, 2]]
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20
analysis['plotRecipientPVs'] = 'y'
analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['ru', 'rc']
analysis['plotIncomeMapsStates'] = [[3, 1, 2]]
analysis['plotIncomeMapsMinPctScenarios'] = 0.5
analysis['plotPPCSandIncomes'] = 'y'
analysis['plotPPCSandIncomesSemilog'] = 'y'
analysis['plotPPCSandIncomesStates'] = [[3, 1, 2]]
analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [[3, 1, 2]]
analysis_process(analysis, client, market)
