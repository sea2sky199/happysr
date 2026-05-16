import numpy as np
import matplotlib.pyplot as plt

def analPlotPPCSandIncomes(analysis, client, market, states):
    # plot PPCS and incomes for states
    # called by analysis_process function

    # add labels
    plt.figure(figsize=(analysis.figPosition[2], analysis.figPosition[3]))
    plt.grid(True)
    plt.ylabel('log ( Price per Chance )')
    plt.hold(True)

    # set colors for states 0,1,2,3,and 4
    # orange; red; blue; green; orange; black
    cmap = np.array([[1, 0.5, 0], [1, 0, 0], [0, 0, 1], [0, 0.8, 0], [1, 0.5, 0]])
    # set full color based on states
    clrmat = cmap[np.array(states) + 1]
    clrFull = np.mean(clrmat, axis=0)
    # set shade color
    shade = analysis.animationShadowShade
    clrShade = shade * clrFull + (1 - shade) * [1, 1, 1]

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
    minprop = analysis.plotPPCSandIncomesMinPctScenarios
    minnum = (minprop / 100) * nscen
    lastyear = np.max(np.where(numstates > minnum)[0]) + 1
    if lastyear == 0:
        plt.title('Insufficient scenarios')
        return

    # truncate matrices
    cellsM = cells[:, :lastyear]
    incsM = client.incomesM[:, :lastyear]
    ppcsM = market.ppcsM[:, :lastyear]

    # find maximum and minimum incomes
    ii = np.where(cellsM > 0)[0]
    incsvec = incsM[ii]
    maxinc = np.max(incsvec)
    mininc = np.min(incsvec)
    # find maximum and minimum PPCs
    ppcsvec = ppcsM[ii]
    maxppc = np.max(ppcsvec)
    minppc = np.min(ppcsvec)

    # set delay change parameter
    delays = analysis.animationDelays
    delayChange = (delays[1] - delays[0]) / (nyrs - 1)

    # set initial delay
    delay = delays[0]

    # if minimum income is zero, require semilog
    if mininc == 0:
        analysis.plotPPCSandIncomesSemilog = 'y'

    if analysis.plotPPCSandIncomesSemilog == 'y':
        # set axes and label
        plt.axis([0, maxinc, np.log(minppc), np.log(maxppc)])
        plt.xlabel('Real Income')

        for yr in range(lastyear):
            # get data
            cellsv = cellsM[:, yr]
            ii = np.where(cellsv > 0)[0]
            incs = incsM[ii, yr]
            ppcs = ppcsM[ii, yr]

            # title
            ttl1 = f'PPCs and Real Incomes, States = {states}'
            ttl2 = f'Year: {yr + 1}'
            plt.title([ttl1, ttl2], color='b')

            # plot points
            plt.plot(incs, np.log(ppcs), '*', color=clrFull, linewidth=0.5)
            plt.pause(delay)
            # shade points
            delay += delayChange
            plt.plot(incs, np.log(ppcs), '*', color=clrShade, linewidth=0.5)

    else:
        # set axes and labels
        plt.xlabel('log ( Real Income )')
        plt.axis([np.log(mininc), np.log(maxinc), np.log(minppc), np.log(maxppc)])

        for yr in range(lastyear):
            # get data
            cellsv = cellsM[:, yr]
            ii = np.where(cellsv > 0)[0]
            incs = incsM[ii, yr]
            ppcs = ppcsM[ii, yr]

            # title
            ttl1 = f'PPCs and Real Incomes, States = {states}'
            ttl2 = f'Year: {yr + 1}'
            plt.title([ttl1, ttl2], color='b')

    # plot points
    plt.plot(np.log(incs), np.log(ppcs), '*', color=clrFull, linewidth=0.5)
    plt.pause(delay)
    # shade points
    delay += delayChange
    plt.plot(np.log(incs), np.log(ppcs), '*', color=clrShade, linewidth=0.5)