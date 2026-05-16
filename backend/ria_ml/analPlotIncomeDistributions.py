import numpy as np
import matplotlib.pyplot as plt

def analPlotIncomeDistributions(analysis, client, market, plottype, states):
    plottype = plottype.lower()
    ax = plt.gca()
    ax.grid(True)

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0]])

    condition = 'if ' if 'c' in plottype else 'and '
    rntext = 'Nominal ' if 'n' in plottype else 'Real '
    statestext = condition + 'States = ' + str(states)

    ax.set_xlabel(rntext + 'Income (x)')
    ax.set_ylabel('Probability ' + rntext + 'Income Exceeds x')
    ttlstart = rntext + 'Incomes ' + statestext + ': Year '

    incomesM = client['incomesM'].copy()
    if 'n' in plottype:
        incomesM = market['cumCsM'] * incomesM

    cells = np.zeros(client['pStatesM'].shape)
    for s in states:
        cells += (client['pStatesM'] == s)

    nscens = np.sum(cells, axis=0)
    nyrs = int(np.sum(nscens > 0))
    incomes_all = incomesM * cells
    maxIncome = np.max(incomes_all)

    prop = 0.01 * analysis['plotIncomeDistributionsPctMaxIncome']
    maxIncome = prop * maxIncome
    propShown = analysis['plotIncomeDistributionsProportionShown']
    if propShown < 1.0:
        ii = np.where(cells == 1)
        v = np.sort(incomes_all[ii])
        i = max(1, int(propShown * len(v)))
        maxIncome = v[i - 1]
    ax.set_xlim([0, maxIncome])
    ax.set_ylim([0, 1])

    clrmat = np.array([cmap[s] for s in states])
    clrFull = np.mean(clrmat, axis=0)
    shade = analysis['animationShadowShade']
    clrShade = shade * clrFull + (1 - shade) * np.array([1, 1, 1])

    delays = analysis['animationDelays']
    delayChange = (delays[1] - delays[0]) / max(nyrs - 1, 1)
    delay = delays[0]

    for yr in range(nyrs):
        rows = np.where(cells[:, yr] == 1)[0]
        incs = incomesM[rows, yr]
        yx = np.arange(1, len(incs) + 1)
        if 'c' in plottype:
            yx = yx / len(yx)
        else:
            yx = yx / incomesM.shape[0]

        probPstates = len(incs) / incomesM.shape[0] * 100
        probPstates = round(probPstates * 10) / 10

        if probPstates >= analysis['plotIncomeDistributionsMinPctScenarios']:
            ax.plot(np.sort(incs), np.sort(yx)[::-1], color=clrFull, linewidth=3)
            ax.set_title(f'{ttlstart}{yr + 1}\n{probPstates} Percent of Scenarios', color='b')
            plt.pause(delay)
            ax.plot(np.sort(incs), np.sort(yx)[::-1], color=clrShade, linewidth=3)
            delay += delayChange
