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
client = iFixedAnnuity_process(iFixedAnnuity, client, market)

analysis = analysis_create()
analysis['plotSurvivalProbabilities'] = 'y'
analysis_process(analysis, client, market)
