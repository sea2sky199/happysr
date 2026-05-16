# Clear all previous variables and close any figures
import matplotlib.pyplot as plt
import numpy as np

def clear_all():
    globals().clear()
    plt.close('all')

clear_all()

# Create a new client data structure
client = {}

# Process the client data structure
client = client_process(client)

# Create a new market data structure
market = {}

# Process the client data structure
market = market_process(market, client)

# Create social security
iSocialSecurity = {}

# Incomes in state 1, last column repeated for subsequent years
iSocialSecurity['state1Incomes'] = [np.inf, 30000]

# Incomes in state 2, last column repeated for subsequent years
iSocialSecurity['state2Incomes'] = [np.inf, 30000]

# Incomes for state 3, last column repeated for subsequent years
iSocialSecurity['state3Incomes'] = [44000]

# Process social security
client = iSocialSecurity_process(iSocialSecurity, client, market)

# Create analysis
analysis = {}
analysis['plotRecipientPVs'] = 'y'

# Process analysis
analysis_process(analysis, client, market)