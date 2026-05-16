import numpy as np
import matplotlib.pyplot as plt

def analPlotIncomeMaps(analysis, client, market, plottype, states):
    # make plottype lower case
    plottype = plottype.lower()

    # set real or nominal text
    if 'n' in plottype:
        rntext2 = 'Nominal '
    else:
        rntext2 = 'Real '
    if 'c' in plottype:
        rntext1 = 'Conditional'
    else:
        rntext1 = ''

    # set states text
    statestext = f'States = {states}'

    # convert client incomes to nominal values if required
    if 'n' in plottype:
        client.incomesM = market.cumCsM * client.incomesM

    # create matrix with 1 for each personal state to be included
    nscenarios = client.pStatesM.shape[0]
    cells = np.zeros_like(client.pStatesM)
    for s in states:
        cells += (client.pStatesM == s)

    # make matrix with incomes for included personal states
    incomes = cells * client.incomesM

    # find cells with included personal states
    ii = np.where(cells > 0)[0]

    # find minimum and maximum incomes for included personal states
    mininc = np.min(incomes[ii])
    maxinc = np.max(incomes[ii])

    # find last year with sufficient included states
    nscen, nyrs = incomes.shape
    numstates = np.sum(cells > 0, axis=1)
    minprop = analysis.plotIncomeMapsMinPctScenarios
    minnum = (minprop / 100) * nscen
    lastyear = np.max(np.where(numstates > minnum)[0]) + 1

    # reduce matrices to cover only included years
    incomes = incomes[:, :lastyear]
    cells = cells[:, :lastyear]

    # create colormap
    colormap = plt.get_cmap('default')
    colormap.set_under('w')

    # put a lower value in each excluded personal state
    ii = np.where(cells < 1)[0]
    incomes[ii] = mininc - 1

    # make changes if map is to be conditional
    if 'c' in plottype:
        condincs = []
        for yr in range(lastyear):
            yrincs = incomes[:, yr]
            yrcells = cells[:, yr]
            ii = np.where(yrcells > 0)[0]
            vals = yrincs[ii]
            num = len(vals)
            m = np.tile(vals, int(np.ceil(nscen / num)))
            v = m[:nscen]
            condincs.append(v)
        incomes = np.array(condincs).T
        colormap = plt.get_cmap('default')

    # truncate incomes above percentage of maximum income
    prop = 0.01 * analysis.plotIncomeMapsPctMaxIncome
    maxinc = prop * np.max(incomes[:, :lastyear])
    incomes[:, :lastyear] = np.minimum(maxinc, incomes[:, :lastyear])

    # plot
    plt.figure(figsize=analysis.figPosition)
    plt.grid()
    plt.imshow(np.sort(incomes[:, :lastyear], axis=0), cmap=colormap)
    plt.colorbar(orientation='vertical', fontsize=30)
    plt.xticks(fontsize=30)
    plt.yticks([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0], fontsize=30)
    plt.xlabel('Year', fontsize=30)
    plt.ylabel(f'Probability of Exceeding {rntext2}Income', fontsize=30)
    plt.title(f'{rntext1} Probabilities of Exceeding {rntext2}Income in {statestext}', fontsize=40, color='b')