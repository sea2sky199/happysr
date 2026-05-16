import numpy as np
import matplotlib.pyplot as plt

def analPlotScenarios(analysis, client, market, plottype):
    plottype = plottype.lower()
    ax = plt.gca()
    ax.grid(True)
    ax.set_title('Scenarios', color=[0, 0, 1])
    ax.set_xlabel('Year')
    if 'r' in plottype:
        ax.set_ylabel('Real Income, Estate or Fees')
    else:
        ax.set_ylabel('Nominal Income, Estate or Fees')

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0], [0, 0, 0]])

    incomesM = client['incomesM'].copy()
    feesM = client['feesM'].copy()
    if 'n' in plottype:
        incomesM = market['cumCsM'] * incomesM
        feesM = market['cumCsM'] * feesM

    n = max(100, analysis['plotScenariosNumber'])
    nscen, nyrs = incomesM.shape
    firstScen = np.random.randint(0, nscen - n)
    lastScen = firstScen + n
    scenPStates = client['pStatesM'][firstScen:lastScen, :]
    scenIncomes = incomesM[firstScen:lastScen, :]
    scenFees = feesM[firstScen:lastScen, :]

    states = []
    if 'i' in plottype:
        states.extend([1, 2, 3])
    if 'e' in plottype:
        states.append(4)

    incomeCells = np.zeros(scenPStates.shape)
    for s in states:
        incomeCells += (scenPStates == s)
    maxIncome = 1.01 * np.max((incomeCells > 0) * scenIncomes)
    maxFee = np.max(scenFees) if 'f' in plottype else 0
    maxY = 1.01 * max(maxIncome, maxFee)
    ax.set_xlim([0, nyrs])
    ax.set_ylim([0, maxY])

    shade = analysis['animationShadowShade']
    delays = analysis['animationDelays']
    nplot = analysis['plotScenariosNumber']
    delayChange = (delays[1] - delays[0]) / max(nplot - 1, 1)
    delay = delays[0]

    for scenNum in range(nplot):
        incomes = scenIncomes[scenNum, :]
        pstates = scenPStates[scenNum, :]
        for pstate in states:
            x = np.where(pstates == pstate)[0]
            if len(x) > 0:
                y = incomes[x]
                ax.plot(x, y, '-*', color=cmap[pstate], linewidth=2.5)
        if 'f' in plottype:
            fees = scenFees[scenNum, :]
            ax.plot(np.arange(nyrs), fees, '*', color=cmap[5], linewidth=2.5)
        plt.pause(delay)
        delay += delayChange
        for pstate in states:
            x = np.where(pstates == pstate)[0]
            if len(x) > 0:
                y = incomes[x]
                clr = shade * cmap[pstate] + (1 - shade) * np.array([1, 1, 1])
                ax.plot(x, y, '-*', color=clr, linewidth=2.5)
        if 'f' in plottype:
            clr = shade * cmap[5] + (1 - shade) * np.array([1, 1, 1])
            ax.plot(np.arange(nyrs), fees, '*', color=clr, linewidth=2.5)
