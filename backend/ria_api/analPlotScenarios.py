import numpy as np
import matplotlib.pyplot as plt

def analPlotScenarios(analysis, client, market, plottype):
    # make plottype lower case
    plottype = plottype.lower()

    # add labels
    plt.figure(figsize=(12, 6))
    plt.suptitle(f'Scenarios: {plottype}', color=[0, 0, 1])
    plt.grid(True)
    plt.xlabel('Year')
    if 'r' in plottype:
        plt.ylabel('Real Income, Estate or Fees')
    else:
        plt.ylabel('Nominal Income, Estate or Fees')
    plt.hold(True)

    # set colors for states 0,1,2,3,4 and fees (5)
    # orange; red; blue; green; orange; black
    cmap = np.array([[1, 0.5, 0], [1, 0, 0], [0, 0, 1], [0, 0.8, 0], [1, 0.5, 0], [0, 0, 0]])

    # convert client income and fees to nominal values if required
    if 'n' in plottype:
        client.incomesM = market.cumCsM * client.incomesM
        client.feesM = market.cumCsM * client.feesM

    # extract sample matrices for at least 100 scenarios
    n = max(100, analysis.plotScenariosNumber)
    nscen, nyrs = client.incomesM.shape
    firstScen = np.random.randint(nscen - n)
    lastScen = firstScen + n - 1
    scenPStates = client.pStatesM[firstScen:lastScen + 1, :]
    scenIncomes = client.incomesM[firstScen:lastScen + 1, :]
    scenFees = client.feesM[firstScen:lastScen + 1, :]

    # set personal states to be shown
    states = []
    if 'i' in plottype:
        states.extend([1, 2, 3])
    if 'e' in plottype:
        states.append(4)

    # find maximum value for y axis
    incomeCells = np.zeros_like(scenPStates)
    for i in range(len(states)):
        incomeCells += (scenPStates == states[i])
    maxIncome = 1.01 * np.max(incomeCells * scenIncomes)

    # if fee is to be included, find maximum fee for sample states
    if 'f' in plottype:
        maxFee = np.max(scenFees)
    else:
        maxFee = 0

    # set maximum for y axis
    maxY = 1.01 * max(maxIncome, maxFee)

    # set axes
    plt.axis([0, nyrs, 0, maxY])

    # set shade and delay parameter
    shade = analysis.animationShadowShade
    delays = analysis.animationDelays
    delayChange = (delays[1] - delays[0]) / (analysis.plotScenariosNumber - 1)

    # show scenarios
    delay = delays[0]
    for scenNum in range(analysis.plotScenariosNumber):
        # plot incomes
        incomes = scenIncomes[scenNum, :]
        pstates = scenPStates[scenNum, :]
        for pstate in states:
            x = np.where(pstates == pstate)[0]
            if len(x) > 0:
                y = incomes[x]
                plt.plot(x, y, '-*', color=cmap[pstate, :], linewidth=2.5)

        # plot fees
        if 'f' in plottype:
            fees = scenFees[scenNum, :]
            plt.plot(np.arange(1, nyrs + 1), fees, '*', color=cmap[5, :], linewidth=2.5)

        # pause
        plt.pause(delay)
        delay += delayChange

        # re-plot incomes using shading
        for pstate in states:
            x = np.where(pstates == pstate)[0]
            if len(x) > 0:
                y = incomes[x]
                clr = shade * cmap[pstate, :] + (1 - shade) * [1, 1, 1]
                plt.plot(x, y, '-*', color=clr, linewidth=2.5)

        # re-plot fees using shading
        if 'f' in plottype:
            clr = shade * cmap[5, :] + (1 - shade) * [1, 1, 1]
            plt.plot(np.arange(1, nyrs + 1), fees, '*', color=clr, linewidth=2.5)

    plt.show()