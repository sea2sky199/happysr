"""
Comprehensive test of all Python modules in ria_ml/.
Uses matplotlib Agg backend to avoid GUI errors on WSL.
Runs with a small nScenarios count for speed.
"""
import sys
import os
import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# suppress animation delays — plt.pause blocks even on Agg backend
plt.pause = lambda x: None

sys.path.insert(0, os.path.dirname(__file__))

PASS = []
FAIL = []

def ok(name):
    PASS.append(name)
    print(f'  PASS  {name}')

def fail(name, exc):
    FAIL.append(name)
    print(f'  FAIL  {name}')
    traceback.print_exc()

# ─────────────────────────────────────────────
# 1. Create functions
# ─────────────────────────────────────────────
print('\n=== Create functions ===')

try:
    from client_create import client_create
    c = client_create()
    assert isinstance(c, dict) and 'p1Age' in c
    ok('client_create')
except Exception:
    fail('client_create', sys.exc_info())

try:
    from market_create import market_create
    m = market_create()
    assert isinstance(m, dict) and 'eC' in m
    ok('market_create')
except Exception:
    fail('market_create', sys.exc_info())

try:
    from analysis_create import analysis_create
    a = analysis_create()
    assert 'plotScenarios' in a
    ok('analysis_create')
except Exception:
    fail('analysis_create', sys.exc_info())

try:
    from AMDnLockboxes_create import AMDnLockboxes_create
    x = AMDnLockboxes_create()
    assert 'proportions' in x
    ok('AMDnLockboxes_create')
except Exception:
    fail('AMDnLockboxes_create', sys.exc_info())

try:
    from CMULockboxes_create import CMULockboxes_create
    x = CMULockboxes_create()
    assert 'initialMarketProportion' in x
    ok('CMULockboxes_create')
except Exception:
    fail('CMULockboxes_create', sys.exc_info())

try:
    from combinedLockboxes_create import combinedLockboxes_create
    x = combinedLockboxes_create()
    assert isinstance(x, dict)
    ok('combinedLockboxes_create')
except Exception:
    fail('combinedLockboxes_create', sys.exc_info())

try:
    from iConstSpending_create import iConstSpending_create
    x = iConstSpending_create()
    assert 'investedAmount' in x
    ok('iConstSpending_create')
except Exception:
    fail('iConstSpending_create', sys.exc_info())

try:
    from iPropSpending_create import iPropSpending_create
    x = iPropSpending_create()
    assert 'investedAmount' in x
    ok('iPropSpending_create')
except Exception:
    fail('iPropSpending_create', sys.exc_info())

try:
    from iFixedAnnuity_create import iFixedAnnuity_create
    x = iFixedAnnuity_create()
    assert 'cost' in x
    ok('iFixedAnnuity_create')
except Exception:
    fail('iFixedAnnuity_create', sys.exc_info())

try:
    from iGLWB_create import iGLWB_create
    x = iGLWB_create()
    assert 'initialValue' in x
    ok('iGLWB_create')
except Exception:
    fail('iGLWB_create', sys.exc_info())

try:
    from iLBAnnuity_create import iLBAnnuity_create
    x = iLBAnnuity_create()
    assert 'proportions' in x
    ok('iLBAnnuity_create')
except Exception:
    fail('iLBAnnuity_create', sys.exc_info())

try:
    from iSocialSecurity_create import iSocialSecurity_create
    x = iSocialSecurity_create()
    assert 'state3Incomes' in x
    ok('iSocialSecurity_create')
except Exception:
    fail('iSocialSecurity_create', sys.exc_info())

try:
    from iFAPlockbox_create import iFAPlockbox_create
    x = iFAPlockbox_create()
    assert 'yearOfAnnuityPurchase' in x
    ok('iFAPlockbox_create')
except Exception:
    fail('iFAPlockbox_create', sys.exc_info())

try:
    from iLockboxSpending_create import iLockboxSpending_create
    x = iLockboxSpending_create()
    assert 'investedAmount' in x
    ok('iLockboxSpending_create')
except Exception:
    fail('iLockboxSpending_create', sys.exc_info())

try:
    from iLBSplusDFA_create import iLBSplusDFA_create
    x = iLBSplusDFA_create()
    assert 'amountInvested' in x
    ok('iLBSplusDFA_create')
except Exception:
    fail('iLBSplusDFA_create', sys.exc_info())

try:
    from iLBSplusFAP_create import iLBSplusFAP_create
    x = iLBSplusFAP_create()
    assert 'amountInvested' in x
    ok('iLBSplusFAP_create')
except Exception:
    fail('iLBSplusFAP_create', sys.exc_info())

# ─────────────────────────────────────────────
# 2. Core pipeline: client + market
# ─────────────────────────────────────────────
print('\n=== Core pipeline ===')

import numpy as np

try:
    from client_process import client_process
    client = client_create()
    client['nScenarios'] = 500   # small for speed
    client = client_process(client)
    assert 'pStatesM' in client
    assert client['pStatesM'].shape[0] == 500
    nscen, nyrs = client['pStatesM'].shape
    ok(f'client_process  ({nscen} scen x {nyrs} yrs)')
except Exception:
    fail('client_process', sys.exc_info())
    print('  [fatal] Cannot continue without client — aborting remaining tests')
    sys.exit(1)

try:
    from market_process import market_process
    market = market_create()
    market = market_process(market, client)
    assert 'cumRmsM' in market and 'ppcsM' in market
    ok('market_process')
except Exception:
    fail('market_process', sys.exc_info())
    sys.exit(1)

# ─────────────────────────────────────────────
# 3. Lockbox proportions
# ─────────────────────────────────────────────
print('\n=== Lockbox proportions ===')

amd_props = None
try:
    from AMDnLockboxes_process import AMDnLockboxes_process
    amd = AMDnLockboxes_create()
    amd = AMDnLockboxes_process(amd, market, client)
    amd_props = amd['proportions']
    assert amd_props is not None and len(amd_props) > 0
    ok('AMDnLockboxes_process')
except Exception:
    fail('AMDnLockboxes_process', sys.exc_info())

cmu_props = None
try:
    from CMULockboxes_process import CMULockboxes_process
    cmu = CMULockboxes_create()
    cmu = CMULockboxes_process(cmu, market, client)
    cmu_props = cmu['proportions']
    assert cmu_props is not None and len(cmu_props) > 0
    ok('CMULockboxes_process')
except Exception:
    fail('CMULockboxes_process', sys.exc_info())

try:
    from combinedLockboxes_process import combinedLockboxes_process
    comb = combinedLockboxes_create()
    if amd_props is not None and cmu_props is not None:
        amd_box = AMDnLockboxes_create()
        amd_box['proportions'] = amd_props
        cmu_box = CMULockboxes_create()
        cmu_box['proportions'] = cmu_props
        comb['componentLockboxes'] = [amd_box, cmu_box]
        comb['componentWeights'] = [0.5, 0.5]
        comb = combinedLockboxes_process(comb, client)
        assert 'proportions' in comb
    ok('combinedLockboxes_process')
except Exception:
    fail('combinedLockboxes_process', sys.exc_info())

# ─────────────────────────────────────────────
# 4. Income strategies
# ─────────────────────────────────────────────
print('\n=== Income strategies ===')

def fresh_client():
    """Return a client with clean incomesM/feesM but same pStatesM."""
    import copy
    c2 = copy.deepcopy(client)
    return c2

try:
    from iSocialSecurity_process import iSocialSecurity_process
    c2 = fresh_client()
    ss = iSocialSecurity_create()
    c2 = iSocialSecurity_process(ss, c2, market)
    assert 'incomesM' in c2
    ok('iSocialSecurity_process')
except Exception:
    fail('iSocialSecurity_process', sys.exc_info())

try:
    from iFixedAnnuity_process import iFixedAnnuity_process
    c2 = fresh_client()
    fa = iFixedAnnuity_create()
    fa['guaranteedIncomes'] = [40000]
    c2 = iFixedAnnuity_process(fa, c2, market)
    assert 'incomesM' in c2
    ok('iFixedAnnuity_process')
except Exception:
    fail('iFixedAnnuity_process', sys.exc_info())

try:
    from iConstSpending_process import iConstSpending_process
    c2 = fresh_client()
    cs = iConstSpending_create()
    cs['investedAmount'] = 1000000
    c2 = iConstSpending_process(cs, c2, market)
    assert 'incomesM' in c2
    ok('iConstSpending_process')
except Exception:
    fail('iConstSpending_process', sys.exc_info())

try:
    from iPropSpending_process import iPropSpending_process
    c2 = fresh_client()
    ps = iPropSpending_create()
    ps['investedAmount'] = 1000000
    c2 = iPropSpending_process(ps, c2, market)
    assert 'incomesM' in c2
    ok('iPropSpending_process')
except Exception:
    fail('iPropSpending_process', sys.exc_info())

try:
    from iGLWB_process import iGLWB_process
    c2 = fresh_client()
    glwb = iGLWB_create()
    c2, glwb2 = iGLWB_process(c2, market, glwb)
    assert 'incomesM' in c2
    ok('iGLWB_process')
except Exception:
    fail('iGLWB_process', sys.exc_info())

try:
    from iLBAnnuity_process import iLBAnnuity_process
    c2 = fresh_client()
    lb = iLBAnnuity_create()
    if amd_props is not None:
        lb['proportions'] = amd_props
    lb['cost'] = 1000000
    c2 = iLBAnnuity_process(lb, c2, market)
    assert 'incomesM' in c2
    ok('iLBAnnuity_process')
except Exception:
    fail('iLBAnnuity_process', sys.exc_info())

try:
    from iLockboxSpending_process import iLockboxSpending_process
    c2 = fresh_client()
    lbs = iLockboxSpending_create()
    lbs['investedAmount'] = 1000000
    if amd_props is not None:
        lbs['lockboxProportions'] = amd_props
    c2, lbs2 = iLockboxSpending_process(lbs, c2, market)
    assert 'incomesM' in c2
    ok('iLockboxSpending_process')
except Exception:
    fail('iLockboxSpending_process', sys.exc_info())

try:
    from iFAPlockbox_process import iFAPlockbox_process
    c2 = fresh_client()
    fap = iFAPlockbox_create()
    fap['investedAmount'] = 1000000
    c2 = iFAPlockbox_process(c2, fap, market)
    assert 'incomesM' in c2
    ok('iFAPlockbox_process')
except Exception:
    fail('iFAPlockbox_process', sys.exc_info())

try:
    from iLBSplusDFA_process import iLBSplusDFA_process
    c2 = fresh_client()
    dfa = iLBSplusDFA_create()
    dfa['amountInvested'] = 1000000
    if amd_props is not None:
        dfa['lockboxProportions'] = amd_props
    c2, dfa2 = iLBSplusDFA_process(c2, dfa, market)
    assert 'incomesM' in c2
    ok('iLBSplusDFA_process')
except Exception:
    fail('iLBSplusDFA_process', sys.exc_info())

try:
    from iLBSplusFAP_process import iLBSplusFAP_process
    c2 = fresh_client()
    fap2 = iLBSplusFAP_create()
    fap2['amountInvested'] = 1000000
    if amd_props is not None:
        fap2['lockboxProportions'] = amd_props
        yr = fap2['annuitizationYear']
        props_arr = np.array(amd_props)[:, yr - 2]
        fap2['FAPlockboxProportionInTIPS'] = props_arr[0] / (props_arr[0] + props_arr[1])
    c2, fap3 = iLBSplusFAP_process(c2, fap2, market)
    assert 'incomesM' in c2
    ok('iLBSplusFAP_process')
except Exception:
    fail('iLBSplusFAP_process', sys.exc_info())

# ─────────────────────────────────────────────
# 5. Build a "full" client for analysis tests
# ─────────────────────────────────────────────
print('\n=== Building client for analysis ===')
try:
    c_full = fresh_client()
    cs2 = iConstSpending_create()
    cs2['investedAmount'] = 1000000
    from iConstSpending_process import iConstSpending_process
    c_full = iConstSpending_process(cs2, c_full, market)
    ok('client ready for analysis')
except Exception:
    fail('client for analysis', sys.exc_info())
    c_full = client  # fallback

# ─────────────────────────────────────────────
# 6. Analysis plot functions (Agg backend — no display)
# ─────────────────────────────────────────────
print('\n=== analPlot* functions ===')

def make_analysis(**kwargs):
    a = analysis_create()
    a.update(kwargs)
    return a

try:
    from analPlotSurvivalProbabilities import analPlotSurvivalProbabilities
    a = make_analysis()
    analPlotSurvivalProbabilities(a, c_full, market)
    ok('analPlotSurvivalProbabilities')
except Exception:
    fail('analPlotSurvivalProbabilities', sys.exc_info())

try:
    from analPlotScenarios import analPlotScenarios
    a = make_analysis(plotScenariosNumber=5)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotScenarios(a, c_full, market, 'ri')
    plt.close('all')
    ok('analPlotScenarios')
except Exception:
    fail('analPlotScenarios', sys.exc_info())

try:
    from analPlotIncomeDistributions import analPlotIncomeDistributions
    a = make_analysis(plotIncomeDistributionsMinPctScenarios=0.5,
                      plotIncomeDistributionsPctMaxIncome=50,
                      plotIncomeDistributionsProportionShown=1.0)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotIncomeDistributions(a, c_full, market, 'rc', [3, 1, 2])
    plt.close('all')
    ok('analPlotIncomeDistributions')
except Exception:
    fail('analPlotIncomeDistributions', sys.exc_info())

try:
    from analPlotIncomeMaps import analPlotIncomeMaps
    a = make_analysis(plotIncomeMapsMinPctScenarios=0.5,
                      plotIncomeMapsPctMaxIncome=50)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotIncomeMaps(a, c_full, market, 'rc', [3, 1, 2])
    plt.close('all')
    ok('analPlotIncomeMaps')
except Exception:
    fail('analPlotIncomeMaps', sys.exc_info())

try:
    from analPlotYOYIncomes import analPlotYOYIncomes
    a = make_analysis()
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotYOYIncomes(a, c_full, market, 'r', [3, 1, 2])
    plt.close('all')
    ok('analPlotYOYIncomes')
except Exception:
    fail('analPlotYOYIncomes', sys.exc_info())

try:
    from analPlotRecipientPVs import analPlotRecipientPVs
    a = make_analysis()
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotRecipientPVs(a, c_full, market)
    plt.close('all')
    ok('analPlotRecipientPVs')
except Exception:
    fail('analPlotRecipientPVs', sys.exc_info())

try:
    from analPlotPPCSandIncomes import analPlotPPCSandIncomes
    a = make_analysis(plotPPCSandIncomesSemilog='y',
                      plotPPCSandIncomesMinPctScenarios=0.5)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotPPCSandIncomes(a, c_full, market, [3])
    plt.close('all')
    ok('analPlotPPCSandIncomes')
except Exception:
    fail('analPlotPPCSandIncomes', sys.exc_info())

try:
    from analPlotYearlyPVs import analPlotYearlyPVs
    a = make_analysis(plotYearlyPVsMinPctScenarios=0.5)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotYearlyPVs(a, c_full, market, [3, 1, 2])
    plt.close('all')
    ok('analPlotYearlyPVs')
except Exception:
    fail('analPlotYearlyPVs', sys.exc_info())

try:
    from analPlotEfficientIncomes import analPlotEfficientIncomes
    a = make_analysis(plotEfficientIncomesMinPctScenarios=0.5)
    import matplotlib.pyplot as plt
    plt.figure()
    analPlotEfficientIncomes(a, c_full, market, 'pcl', [3])
    plt.close('all')
    ok('analPlotEfficientIncomes')
except Exception:
    fail('analPlotEfficientIncomes', sys.exc_info())

try:
    from analPlotYOUIncomes import analPlotYOUIncomes
    analPlotYOUIncomes(make_analysis(), c_full, market)
    ok('analPlotYOUIncomes')
except Exception:
    fail('analPlotYOUIncomes', sys.exc_info())

# ─────────────────────────────────────────────
# 7. analysis_process (orchestrator)
# ─────────────────────────────────────────────
print('\n=== analysis_process orchestrator ===')

try:
    from analysis_process import analysis_process
    a = analysis_create()
    a['plotSurvivalProbabilities'] = 'y'
    a['plotScenarios'] = 'y'
    a['plotScenariosTypes'] = ['ri']
    a['plotScenariosNumber'] = 5
    a['plotIncomeDistributions'] = 'y'
    a['plotIncomeDistributionsTypes'] = ['rc']
    a['plotIncomeDistributionsStates'] = [[3, 1, 2]]
    a['plotRecipientPVs'] = 'y'
    a['plotYearlyPVs'] = 'y'
    a['plotYearlyPVsStates'] = [[3, 1, 2]]
    analysis_process(a, c_full, market)
    ok('analysis_process')
except Exception:
    fail('analysis_process', sys.exc_info())

# ─────────────────────────────────────────────
# 8. Stub / empty modules
# ─────────────────────────────────────────────
print('\n=== Stub modules (import only) ===')

for mod in ['AngelaCase', 'AngelaCast']:
    try:
        __import__(mod)
        ok(mod)
    except Exception:
        fail(mod, sys.exc_info())

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
total = len(PASS) + len(FAIL)
print(f'\n{"="*50}')
print(f'Results: {len(PASS)} passed, {len(FAIL)} failed out of {total} tests')
if FAIL:
    print('\nFailed tests:')
    for f in FAIL:
        print(f'  - {f}')
    sys.exit(1)
else:
    print('All tests passed!')
    sys.exit(0)
