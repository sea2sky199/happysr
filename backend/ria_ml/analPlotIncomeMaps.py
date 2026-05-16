import numpy as np
import matplotlib.pyplot as plt

def analPlotIncomeMaps(analysis, client, market, plottype, states):
    plottype = plottype.lower()
    rntext2 = 'Nominal ' if 'n' in plottype else 'Real '
    rntext1 = 'Conditional' if 'c' in plottype else ''
    statestext = 'States = ' + str(states)

    incomesM = client['incomesM'].copy()
    if 'n' in plottype:
        incomesM = market['cumCsM'] * incomesM

    nscenarios = client['pStatesM'].shape[0]
    cells = np.zeros(client['pStatesM'].shape)
    for s in states:
        cells += (client['pStatesM'] == s)

    incomes = cells * incomesM
    ii = np.where(cells > 0)
    mininc = np.min(incomes[ii])
    maxinc = np.max(incomes[ii])

    nscen, nyrs = incomes.shape
    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis['plotIncomeMapsMinPctScenarios']
    minnum = (minprop / 100) * nscen
    cond = (numstates > minnum) * np.arange(1, nyrs + 1)
    lastyear = int(np.max(cond)) if np.any(cond > 0) else nyrs
    incomes = incomes[:, :lastyear]
    cells = cells[:, :lastyear]

    if 'c' in plottype:
        condincs = []
        for yr in range(incomes.shape[1]):
            yrincs = incomes[:, yr]
            yrcells = cells[:, yr]
            ii2 = np.where(yrcells > 0)[0]
            vals = yrincs[ii2]
            num = len(vals)
            reps = int(np.ceil(nscen / num))
            m = np.tile(vals, reps)
            v = m[:nscen]
            condincs.append(v)
        incomes = np.column_stack(condincs)

    prop = 0.01 * analysis['plotIncomeMapsPctMaxIncome']
    maxinc = prop * np.max(incomes[:, :lastyear])
    incomes[:, :lastyear] = np.minimum(maxinc, incomes[:, :lastyear])

    sorted_inc = np.sort(incomes[:, :lastyear], axis=0)[::-1, :]

    ax = plt.gca()
    im = ax.imshow(sorted_inc, aspect='auto', cmap='viridis')
    plt.colorbar(im, ax=ax)
    ax.grid(True)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Probability of Exceeding ' + rntext2 + 'Income', fontsize=12)
    ttl = f'{rntext1} Probabilities of Exceeding {rntext2}Income in {statestext}'
    ax.set_title(ttl, color='b')
