# Clear all previous variables and close any figures
import matplotlib.pyplot as plt
import numpy as np

# Clear all previous variables and close any figures
clear_all()

# Create a new client data structure
client = {}

# Process the client data structure
client = client_process(client)

# Create a new market data structure
market = {}

# Process the client data structure
market = market_process(market, client)

# Create social security accounts
iSocialSecurity = {}
iSocialSecurity['state1Incomes'] = [np.inf, 30000]
iSocialSecurity['state2Incomes'] = [np.inf, 30000]
iSocialSecurity['state3Incomes'] = [44000]

# Process social security accounts
client = iSocialSecurity_process(iSocialSecurity, client, market)

# Create and process AMDnLockboxes
AMDnLockboxes = {}
AMDnLockboxes['cumRmDistributionYear'] = 2
AMDnLockboxes['showProportions'] = 'y'
AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client)

# Create iLBAnnuity
iLBAnnuity = {}

# Set iLBAnnuity cost
iLBAnnuity['cost'] = 1000000

# Set annuity lockbox proportions
iLBAnnuity['proportions'] = AMDnLockboxes['proportions']

# Process LBAnnuity
client = iLBAnnuity_process(iLBAnnuity, client, market)

# Create analysis
analysis = {}

# Reset analysis parameters
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

# Produce analysis
analysis_process(analysis, client, market)

