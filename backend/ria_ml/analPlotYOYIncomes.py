import numpy as np
import matplotlib.pyplot as plt

def analPlotYOYIncomes(analysis, client, market, plottype, states):
    plottype = plottype.lower()
    rntext = 'Nominal ' if 'n' in plottype else 'Real '
    statestext = 'States: ' + str(states)

    incomesM = client['incomesM'].copy()
    if 'n' in plottype:
        incomesM = market['cumCsM'] * incomesM

    cells = np.zeros(client['pStatesM'].shape)
    for s in states:
        cells += (client['pStatesM'] == s)

    col_sums = np.sum(cells, axis=0)
    nyrs = int(np.max(np.where(col_sums > 0)[0])) + 1 if np.any(col_sums > 0) else 1
    incs = incomesM[:, :nyrs]
    cells = cells[:, :nyrs]

    ii = np.where(cells > 0)
    maxval = np.max(incs[ii])
    minval = np.min(incs[ii])
    if analysis['plotYOYIncomesWithZero'].lower() == 'y':
        minval = 0

    ax = plt.gca()
    ax.set_xlim([minval, maxval])
    ax.set_ylim([minval, maxval])
    ax.grid(True)
    ax.set_xlabel(f'Year t {rntext}Income')
    ax.set_ylabel(f'Year t+1 {rntext}Income')
    ttl = f'Year over Year {rntext}Incomes: {statestext}, Year t: '

    cmap = np.array([[1, .5, 0], [1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0]])
    clrmat = np.array([cmap[s] for s in states])
    clrFull = np.mean(clrmat, axis=0)
    shade = analysis['animationShadowShade']
    clrShade = shade * clrFull + (1 - shade) * np.array([1, 1, 1])

    delays = analysis['animationDelays']
    delayChange = (delays[1] - delays[0]) / max(nyrs - 1, 1)
    delay = delays[0]

    ax.plot([minval, maxval], [minval, maxval], linewidth=1, color='k')

    for col in range(1, nyrs):
        ax.set_title(f'{ttl}{col}', color='b')
        cellmat = cells[:, col - 1:col + 1]
        ii2 = np.where(np.sum(cellmat, axis=1) >= 2)[0]
        ax.plot(incs[ii2, col - 1], incs[ii2, col], '.', color=clrFull, linewidth=2)
        ax.plot([minval, maxval], [minval, maxval], linewidth=2, color='k')
        plt.pause(delay)
        delay += delayChange
        ax.plot(incs[ii2, col - 1], incs[ii2, col], '.', color=clrShade, linewidth=2)
