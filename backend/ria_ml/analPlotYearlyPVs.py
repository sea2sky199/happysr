import numpy as np
import matplotlib.pyplot as plt

def analPlotYearlyPVs(analysis, client, market, states):
    ax = plt.gca()
    ax.grid(True)
    ax.set_xlabel('Year')
    ax.set_ylabel('Present Value')

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0]])
    clrmat = np.array([cmap[s] for s in states])
    clrPV = np.mean(clrmat, axis=0)
    clrIneff = np.array([0, 0, 0])

    nscen, nyrs = client['pStatesM'].shape
    cells = np.zeros((nscen, nyrs))
    for s in states:
        cells += (client['pStatesM'] == s)

    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis['plotYearlyPVsMinPctScenarios']
    minnum = (minprop / 100) * nscen
    cond = (numstates > minnum) * np.arange(1, nyrs + 1)
    lastyear = int(np.max(cond)) if np.any(cond > 0) else 0
    if lastyear == 0:
        ax.set_title('Insufficient scenarios')
        return

    cellsM = cells[:, :lastyear]
    incsM = client['incomesM'][:, :lastyear]
    ppcsM = market['ppcsM'][:, :lastyear]

    totalpvs = []
    effpvs = []
    for yr in range(lastyear):
        rows = np.where(cells[:, yr] > 0)[0]
        pvs = market['pvsM'][rows, yr]
        incs = client['incomesM'][rows, yr]
        totalpv = np.dot(pvs, incs)
        effpv = np.dot(np.sort(pvs), np.sort(incs)[::-1])
        totalpvs.append(totalpv)
        effpvs.append(effpv)
    totalpvs = np.array(totalpvs)
    effpvs = np.array(effpvs)

    totaleff = 100 * (np.sum(effpvs) / np.sum(totalpvs)) if np.sum(totalpvs) > 0 else 0
    ttl1 = f'Yearly Present Values, States = {states}'
    ttl2 = f'Overall Efficiency = {round(0.1 * round(10 * totaleff), 1)}%'
    ax.set_title(f'{ttl1}\n{ttl2}', color='b')
    ax.set_xlim([0, lastyear + 1])
    ax.set_ylim([0, np.max(totalpvs)])

    x = np.arange(1, lastyear + 1)
    diffs = totalpvs - effpvs
    ax.bar(x, effpvs, color=clrPV, label='Efficient PV')
    ax.bar(x, diffs, bottom=effpvs, color=clrIneff, label='Inefficient PV')
    ax.legend()
    ax.grid(True)
