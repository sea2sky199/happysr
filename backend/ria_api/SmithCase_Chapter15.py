# Clear all previous variables and close any figures
import matplotlib.pyplot as plt
import time

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

# Create and process AMDnLockboxes
AMDnLockboxes = {}
AMDnLockboxes['showProportions'] = 'y'
AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client)

# Create and process CMULockboxes
CMULockboxes = {}
CMULockboxes['showProportions'] = 'y'
CMULockboxes = CMULockboxes_process(CMULockboxes, market, client)

# Create and process combined lockboxes
combinedLockboxes = {}
combinedLockboxes['componentLockboxes'] = [AMDnLockboxes, CMULockboxes]
combinedLockboxes['componentWeights'] = [0.5, 0.5]
combinedLockboxes['showCombinedProportions'] = 'y'
combinedLockboxes = combinedLockboxes_process(combinedLockboxes, client)

