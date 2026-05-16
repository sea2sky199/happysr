# SmithCase_Chapter18.py

# Clear all previous variables and close any figures
import matplotlib.pyplot as plt
import numpy as np

# Assuming the functions are defined elsewhere and imported
# from your_module import client_create, client_process, market_create, market_process, iPropSpending_create, iPropSpending_process, analysis_create, analysis_process

# Create a new client data structure
client = client_create()
# Process the client data structure
client = client_process(client)

# Create a new market data structure
market = market_create()
# Process the client data structure
market = market_process(market, client)

# Create proportional spending account
iPropSpending = iPropSpending_create()
iPropSpending['investedAmount'] = 1000000
iPropSpending['glidePath'] = np.array([[1, 0], [0, 30]])
iPropSpending['showGlidePath'] = 'y'
iPropSpending['retentionRatio'] = 0.999
# Process proportional spending account
client = iPropSpending_process(iPropSpending, client, market)

# Create analysis
analysis = analysis_create()

# Change selected analysis settings
analysis['animationDelays'] = [0.2, 0.2]

analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [np.array([1, 2, 3])]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5

analysis['plotYOYIncomes'] = 'y'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [np.array([3, 1, 2])]

analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20

analysis['plotRecipientPVs'] = 'y'

analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['ru', 'rc']
analysis['plotIncomeMapsStates'] = [np.array([3, 1, 2])]
analysis['plotIncomeMapsMinPctScenarios'] = 0.5

analysis['plotPPCSandIncomes'] = 'y'
analysis['plotPPCSandIncomesSemilog'] = 'y'
analysis['plotPPCSandIncomesStates'] = [np.array([3, 1, 2])]

analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [np.array([3, 1, 2])]

# Process analysis
analysis_process(analysis, client, market)


