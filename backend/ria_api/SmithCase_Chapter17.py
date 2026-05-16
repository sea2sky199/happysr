# SmithCase_Chapter17.m
import matplotlib.pyplot as plt
import time
# Clear all previous variables and close any figures
clear_all()
start_time = time.time()

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
iSocialSecurity['state1Incomes'] = [float('inf'), 30000]
iSocialSecurity['state2Incomes'] = [float('inf'), 30000]
iSocialSecurity['state3Incomes'] = [44000]

# Process social security accounts
client = iSocialSecurity_process(iSocialSecurity, client, market)

# Create constant spending data structure
iConstSpending = {}
iConstSpending['glidePath'] = [1, 1]
iConstSpending['retentionRatio'] = 0.999
iConstSpending['initialProportionSpent'] = 0.040
iConstSpending['graduationRatio'] = 1.00
iConstSpending['pStateRelativeIncomes'] = [1, 1, 1]
iConstSpending['investedAmount'] = 1000000
iConstSpending['showGlidePath'] = 'y'

# Process the constant spending data structure
client = iConstSpending_process(iConstSpending, client, market)

# Create analysis
analysis = {}

# Reset analysis parameters
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

# Produce analysis
analysis_process(analysis, client, market)

