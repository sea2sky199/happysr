import numpy as np
import matplotlib.pyplot as plt

def analPlotIncomeDistributions(analysis, client, market, plottype, states):
    # initialize graph
    plt.figure(figsize=analysis.figPosition)
    plt.grid(True)
    plt.title(f"Income Distributions {plottype.lower()}")

    # set colors for states 0,1,2,3 and 4
    cmap = [(1, 0.5, 0), (1, 0, 0), (0, 0, 1), (0, 0.8, 0), (1, 0.5, 0)]

    # set condition labels
    if 'c' in plottype.lower():
        condition = 'if '
    else:
        condition = 'and '

    # set real or nominal text
    if 'n' in plottype.lower():
        rntext = 'Nominal '
    else:
        rntext = 'Real '

    # set states text
    statestext = f"{condition}States = {states}"

    # set labels
    plt.xlabel(f"{rntext}Income (x)")
    plt.ylabel(f"Probability {rntext}Income Exceeds x")
    ttlstart = f"{rntext}Incomes {statestext}: Year "

    # create matrix with 1 for each personal state to be included
    cells = np.zeros_like(client.pStatesM)
    for s in states:
        cells += (client.pStatesM == s)

    # convert client incomes to nominal values if required
    if 'n' in plottype.lower():
        client.incomesM = market.cumCsM * client.incomesM

    # create vector with number of scenarios for each year
    nscens = np.sum(cells, axis=0)
    # find number of years to plot
    nyrs = np.sum(nscens > 0)
    # find maximum income
    incomes = client.incomesM * cells
    maxIncome = np.max(incomes)

    # set axes for figure
    prop = 0.01 * analysis.plotIncomeDistributionsPctMaxIncome
    maxIncome = prop * maxIncome
    propShown = analysis.plotIncomeDistributionsProportionShown
    if propShown < 1.0:
        ii = np.where(cells == 1)[0]
        v = np.sort(incomes[ii])
        i = int(propShown * len(v))
        i = max(1, i)
        maxIncome = v[i]
    ax = [0, maxIncome, 0, 1]
    plt.axis(ax)
    plt.hold(True)

    # set delay change parameter
    delays = analysis.animationDelays
    delayChange = (delays[1] - delays[0]) / (nyrs - 1)

    # set initial delay
    delay = delays[0]

    # set parameters
    # set full color based on states
    clrmat = np.array([cmap[s] for s in states])
    clrFull = np.mean(clrmat, axis=0)
    # set shade color
    shade = analysis.animationShadowShade
    clrShade = shade * clrFull + (1 - shade) * [1, 1, 1]

    # plot each year's distribution
    for yr in range(nyrs):
        # find values for y axis
        rows = np.where(cells[:, yr] == 1)[0]
        incomes = client.incomesM[rows, yr]
        yx = np.arange(1, len(incomes) + 1)
        if 'c' in plottype.lower():
            yx = yx / len(yx)
        else:
            yx = yx / client.incomesM.shape[0]

        # compute probability of states and round to one decimal place
        if 'c' in plottype.lower():
            probPstates = len(incomes) / client.incomesM.shape[0]
        else:
            probPstates = len(incomes) / client.incomesM.shape[0]
        probPstates = round(1000 * probPstates) / 10

        plt.plot(incomes, yx, color=clrFull, label=f"{ttlstart}{yr+1} (Prob. {probPstates}%)")
        plt.hold(True)
		
    # plot if probability large enough
    if probPstates >= analysis.plotIncomeDistributionsMinPctScenarios:
        plt.plot(np.sort(incomes), np.sort(yx, reverse=True), color=clrFull, linewidth=3)
        ttl1 = f"{yr}"
        ttl2 = f"{probPstates:.0%} of Scenarios"
        plt.title([ttl1, ttl2], color='b')
        plt.pause(delay)
        plt.plot(np.sort(incomes), np.sort(yx, reverse=True), color=clrShade, linewidth=3)
        delay += delayChange 

    plt.legend()
    plt.show()