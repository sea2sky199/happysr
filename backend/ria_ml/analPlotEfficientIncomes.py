import numpy as np
import matplotlib.pyplot as plt

def analPlotEfficientIncomes(analysis, client, market, plottype, states):
    ax = plt.gca()
    ax.grid(True)
    ax.set_xlabel('Cumulative Market Real Return')
    ax.set_ylabel('Real Income')

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0]])
    clrmat = np.array([cmap[s] for s in states])
    clrPoints = np.mean(clrmat, axis=0)
    shade = analysis['animationShadowShade']
    clrPointsShade = shade * clrPoints + (1 - shade) * np.array([1, 1, 1])
    clrCurve = np.array([0, 0, 0])
    clrCurveShade = shade * clrCurve + (1 - shade) * np.array([1, 1, 1])
    clrLine = np.array([1, 0.5, 0])
    clrLineShade = shade * clrLine + (1 - shade) * np.array([1, 1, 1])

    nscen, nyrs = client['pStatesM'].shape
    cells = np.zeros((nscen, nyrs))
    for s in states:
        cells += (client['pStatesM'] == s)

    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis['plotEfficientIncomesMinPctScenarios']
    minnum = (minprop / 100) * nscen
    cond = (numstates > minnum) * np.arange(1, nyrs + 1)
    lastyear = int(np.max(cond)) if np.any(cond > 0) else 0
    if lastyear == 0:
        ax.set_title('Insufficient scenarios')
        return

    delays = analysis['animationDelays']
    delayChange = (delays[1] - delays[0]) / max(lastyear - 1, 1)
    delay = delays[0]

    cellsM = cells[:, :lastyear]
    incsM = client['incomesM'][:, :lastyear]
    cumretsM = market['cumRmsM'][:, :lastyear]
    pvsM = market['pvsM'][:, :lastyear]

    maxincs = np.max(incsM * cellsM)
    cumretm = cumretsM * cellsM
    cumretv = np.sort(cumretm.ravel())
    maxcumrets = cumretv[int(round(0.999 * len(cumretv))) - 1]
    ax.set_xlim([0, maxcumrets])
    ax.set_ylim([0, maxincs])

    for yr in range(lastyear):
        rows = np.where(cells[:, yr] > 0)[0]
        pvs = pvsM[rows, yr]
        incs = incsM[rows, yr]
        cumrets = cumretsM[rows, yr]

        cumretsS = np.sort(cumrets)
        incsS = np.sort(incs)
        pvsS = np.sort(pvs)[::-1]

        if 'p' in plottype:
            ax.plot(cumrets, incs, '*', color=clrPoints)

        xvals = np.column_stack([np.ones(len(cumretsS)), cumretsS])
        b, _, _, _ = np.linalg.lstsq(xvals, incsS, rcond=None)
        incsFitted = b[0] + b[1] * cumretsS
        pvIncs = np.dot(pvs, incs)
        pvLine = np.dot(pvsS, np.sort(incsFitted))
        delta = (pvIncs - pvLine) / np.sum(pvs)
        incsFitted += delta

        if 'c' in plottype:
            ax.plot(cumretsS, incsS, '*', color=clrCurve)

        if 'l' in plottype and yr > 0:
            ax.plot(np.concatenate([[0], cumretsS]),
                    np.concatenate([[b[0] + delta], incsFitted]),
                    color=clrLine, linewidth=4)

        ax.set_title(f'Efficient Real Incomes Year, {yr + 1}  States: {states}', color='b')
        plt.pause(delay)

        if 'p' in plottype:
            ax.plot(cumrets, incs, '*', color=clrPointsShade)
        if 'c' in plottype:
            ax.plot(cumretsS, incsS, '*', color=clrCurveShade)
        if 'l' in plottype and yr > 0:
            ax.plot(np.concatenate([[0], cumretsS]),
                    np.concatenate([[b[0] + delta], incsFitted]),
                    color=clrLineShade, linewidth=4)

        plt.pause(delay)
        delay -= delayChange
