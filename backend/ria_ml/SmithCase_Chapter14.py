import numpy as np
from client_create import client_create
from client_process import client_process
from market_create import market_create
from market_process import market_process
from iSocialSecurity_create import iSocialSecurity_create
from iSocialSecurity_process import iSocialSecurity_process
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

analysis = analysis_create()
analysis['plotRecipientPVs'] = 'y'
analysis_process(analysis, client, market)
