from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iFixedAnnuity_create import iFixedAnnuity_create
from iFixedAnnuity_process import iFixedAnnuity_process
from analysis_create import analysis_create
from analysis_process import analysis_process

client = client_create()
client = client_process(client)

market = market_create()
market = market_process(market, client)

iFixedAnnuity = iFixedAnnuity_create()
iFixedAnnuity['realOrNominal'] = 'n'
client = iFixedAnnuity_process(iFixedAnnuity, client, market)

analysis = analysis_create()
analysis['plotScenarios'] = 'n'
analysis['plotScenariosTypes'] = ['rie']
analysis['plotScenariosNumber'] = 10
analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc', 'ru']
analysis['plotIncomeDistributionsStates'] = [[3]]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['ru', 'rc']
analysis['plotIncomeMapsStates'] = [[3]]
analysis['plotIncomeMapsMinPctScenarios'] = 0.5
analysis['plotYOYIncomes'] = 'n'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [[3]]
analysis_process(analysis, client, market)
