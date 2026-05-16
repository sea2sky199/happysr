# SmithCase_Chapter19.py

# Clear all previous variables and close any figures
import matplotlib.pyplot as plt
import numpy as np

# Assuming the functions are defined elsewhere and imported
# from your_module import client_create, client_process, market_create, market_process, iGLWB_create, iGLWB_process, analysis_create, analysis_process

# Create a new client data structure
client = client_create()

# Process the client data structure
client = client_process(client)

# Create a new market data structure
market = market_create()

# Process the client data structure
market = market_process(market, client)

# Create a new GLWB structure
iGLWB = iGLWB_create()
# Process the GLWB data structure
client, iGLWB = iGLWB_process(client, market, iGLWB)

# Create analysis
analysis = analysis_create()
analysis['animationDelays'] = [1, 0.5]

# Scenarios
analysis['plotScenarios'] = 'y'
analysis['plotScenariosTypes'] = ['ri']
analysis['plotScenariosNumber'] = 20

analysis['plotIncomeDistributions'] = 'y'
analysis['plotIncomeDistributionsTypes'] = ['rc']
analysis['plotIncomeDistributionsStates'] = [np.array([3, 1, 2])]
analysis['plotIncomeDistributionsMinPctScenarios'] = 0.5
analysis['plotIncomeDistributionsPctMaxIncome'] = 50

analysis['plotYOYIncomes'] = 'n'
analysis['plotYOYIncomesTypes'] = ['r']
analysis['plotYOYIncomesStates'] = [np.array([3, 1, 2])]

analysis['plotRecipientPVs'] = 'y'

analysis['plotIncomeMaps'] = 'y'
analysis['plotIncomeMapsTypes'] = ['rc']
analysis['plotIncomeMapsStates'] = [np.array([3, 1, 2])]
analysis['plotIncomeMapsMinPctScenarios'] = 0.5
analysis['plotIncomeMapsPctMaxIncome'] = 25

analysis['plotPPCSandIncomes'] = 'y'
analysis['plotPPCSandIncomesSemilog'] = 'y'
analysis['plotPPCSandIncomesStates'] = [np.array([3, 1, 2])]

analysis['plotYearlyPVs'] = 'y'
analysis['plotYearlyPVsStates'] = [np.array([3, 1, 2])]

analysis['plotEfficientIncomes'] = 'n'
analysis['plotEfficientIncomesStates'] = [np.array([3, 1, 2])]
analysis['plotEfficientIncomesTypes'] = ['pcl']

# Process analysis
analysis_process(analysis, client, market)
