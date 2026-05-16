import numpy as np
import matplotlib.pyplot as plt

def analPlotPPCSandIncomes(analysis, client, market, states):
    ax = plt.gca()
    ax.grid(True)
    ax.set_ylabel('log ( Price per Chance )')

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0]])
    clrmat = np.array([cmap[s] for s in states])
    clrFull = np.mean(clrmat, axis=0)
    shade = analysis['animationShadowShade']
    clrShade = shade * clrFull + (1 - shade) * np.array([1, 1, 1])

    nscen, nyrs = client['pStatesM'].shape
    cells = np.zeros((nscen, nyrs))
    for s in states:
        cells += (client['pStatesM'] == s)

    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis['plotPPCSandIncomesMinPctScenarios']
    minnum = (minprop / 100) * nscen
    cond = (numstates > minnum) * np.arange(1, nyrs + 1)
    lastyear = int(np.max(cond)) if np.any(cond > 0) else 0
    if lastyear == 0:
        ax.set_title('Insufficient scenarios')
        return

    cellsM = cells[:, :lastyear]
    incsM = client['incomesM'][:, :lastyear]
    ppcsM = market['ppcsM'][:, :lastyear]

    ii = np.where(cellsM > 0)
    incsvec = incsM[ii]
    maxinc = np.max(incsvec)
    mininc = np.min(incsvec)
    ppcsvec = ppcsM[ii]
    maxppc = np.max(ppcsvec)
    minppc = np.min(ppcsvec)

    delays = analysis['animationDelays']
    delayChange = (delays[1] - delays[0]) / max(lastyear - 1, 1)
    delay = delays[0]

    semilog = analysis['plotPPCSandIncomesSemilog']
    if mininc == 0:
        semilog = 'y'

    if semilog.lower() == 'y':
        ax.set_xlim([0, maxinc])
        ax.set_ylim([np.log(minppc), np.log(maxppc)])
        ax.set_xlabel('Real Income')
        for yr in range(lastyear):
            cellsv = cellsM[:, yr]
            ii2 = np.where(cellsv > 0)[0]
            incs = incsM[ii2, yr]
            ppcs = ppcsM[ii2, yr]
            ttl = f'PPCs and Real Incomes, States = {states}\nYear: {yr + 1}'
            ax.set_title(ttl, color='b')
            ax.plot(incs, np.log(ppcs), '*', color=clrFull, linewidth=0.5)
            plt.pause(delay)
            delay += delayChange
            ax.plot(incs, np.log(ppcs), '*', color=clrShade, linewidth=0.5)
    else:
        ax.set_xlim([np.log(mininc), np.log(maxinc)])
        ax.set_ylim([np.log(minppc), np.log(maxppc)])
        ax.set_xlabel('log ( Real Income )')
        for yr in range(lastyear):
            cellsv = cellsM[:, yr]
            ii2 = np.where(cellsv > 0)[0]
            incs = incsM[ii2, yr]
            ppcs = ppcsM[ii2, yr]
            ttl = f'PPCs and Real Incomes, States = {states}\nYear: {yr + 1}'
            ax.set_title(ttl, color='b')
            ax.plot(np.log(incs), np.log(ppcs), '*', color=clrFull, linewidth=0.5)
            plt.pause(delay)
            delay += delayChange
            ax.plot(np.log(incs), np.log(ppcs), '*', color=clrShade, linewidth=0.5)
