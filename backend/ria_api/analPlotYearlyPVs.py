import numpy as np
import matplotlib.pyplot as plt

def analPlotYearlyPVs(analysis, client, market, states):
    # plot Yearly PVs for states
    # called by analysis_process function

    # add labels
    plt.figure(figsize=analysis.figPosition)
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Present Value')
    plt.hold(True)

    # set colors for states 0,1,2,3,and 4
    # orange; red; blue; green; orange; black
    cmap = np.array([[1, 0.5, 0], [1, 0, 0], [0, 0, 1], [0, 0.8, 0], [1, 0.5, 0]])

    # set efficient PV color based on states
    clrmat = cmap[np.array(states) + 1]
    clrPV = np.mean(clrmat, axis=0)

    # set inefficiency color
    clrIneff = [0, 0, 0]
    plt.set_cmap(np.vstack((clrPV, clrIneff)))

    # get matrix size
    nscen, nyrs = client.pStatesM.shape

    # set delay change parameter
    delays = analysis.animationDelays
    delayChange = (delays[1] - delays[0]) / (nyrs - 1)

    # set initial delay
    delay = delays[0]

    # create matrix with 1 for each personal state to be included
    cells = np.zeros_like(client.pStatesM)
    for s in states:
        cells += (client.pStatesM == s)

    # find last year with sufficient included states
    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis.plotYearlyPVsMinPctScenarios
    minnum = (minprop / 100) * nscen
    lastyear = np.max(np.where(numstates > minnum)[0]) + 1
    if lastyear == 0:
        plt.title('Insufficient scenarios')
        return

    # truncate matrices
    cellsM = cells[:, :lastyear]
    incsM = client.incomesM[:, :lastyear]
    ppcsM = market.ppcsM[:, :lastyear]

    # set up valuation vectors
    totalpvs = []
    effpvs = []

    # get present values
    for yr in range(lastyear):
        rows = np.where(cells[:, yr] > 0)[0]
        pvs = market.pvsM[rows, yr]
        incs = client.incomesM[rows, yr]
        totalpv = np.dot(pvs, incs)
        effpv = np.dot(np.sort(pvs), np.sort(incs, reverse=True))
        totalpvs.append(totalpv)
        effpvs.append(effpv)

    # compute total efficiency
    totaleff = 100 * (sum(effpvs) / sum(totalpvs))

    # title
    ttl1 = f'Yearly Present Values, States = {states}'
    ttl2 = f'Overall Efficiency = {0.1 * round(10 * totaleff)}%'
    plt.title([ttl1, ttl2], color='b')

    # scale axes
    plt.axis([0, lastyear + 1, 0, max(totalpvs)])
    plt.grid(True)

    # plot pvs
    diffs = np.array(totalpvs) - np.array(effpvs)
    plt.bar([effpvs, diffs], width=0.8, color=['g', 'r'], edgecolor='k', linewidth=1)
    plt.legend(['Efficient PV', 'Inefficient PV'])

