import numpy as np
import matplotlib.pyplot as plt

def analPlotEfficientIncomes(analysis, client, market, type, states):
    # Add labels
    plt.figure('Efficient Real Incomes')
    plt.gcf().set_size_inches(analysis['figPosition'][0], analysis['figPosition'][1])

    plt.grid(True)
    plt.xlabel('Cumulative Market Real Return')
    plt.ylabel('Real Income')

    # Set colors for points for states 0,1,2,3,and 4
    # orange; red; blue; green; orange; black
    cmap = np.array([[1, 0.5, 0], [1, 0, 0], [0, 0, 1], [0, 0.8, 0], [1, 0.5, 0]])

    # Set point color based on states
    clrmat = cmap[states]
    clrPoints = np.mean(clrmat, axis=0)

    # Set point shadow shade color
    shade = analysis['animationShadowShade']
    clrPointsShade = shade * clrPoints + (1 - shade) * np.array([1, 1, 1])

    # Set curve color and shade color
    clrCurve = np.array([0, 0, 0])
    clrCurveShade = shade * clrCurve + (1 - shade) * np.array([1, 1, 1])

    # Set line color and shade color
    clrLine = np.array([1, 0.5, 0])
    clrLineShade = shade * clrLine + (1 - shade) * np.array([1, 1, 1])

    # Create matrix with 1 for each personal state to be included
    cells = np.zeros_like(client['pStatesM'])
    for s in states:
        cells += (client['pStatesM'] == s)

    # Find last year with sufficient included states
    nscen, nyrs = cells.shape
    numstates = np.sum(cells > 0, axis=0)
    minprop = analysis['plotEfficientIncomesMinPctScenarios']
    minnum = (minprop / 100) * nscen
    lastyear = np.max(np.where(numstates > minnum)[0])
    if lastyear == 0:
        plt.title('Insufficient scenarios')
        return

    # Set initial delay and change parameter
    delays = analysis['animationDelays']
    delay = delays[0]
    delayChange = (delays[1] - delays[0]) / (lastyear - 1)
    delay = delays[0]

    # Truncate matrices
    cellsM = cells[:, :lastyear]
    incsM = client['incomesM'][:, :lastyear]
    cumretsM = market['cumRmsM'][:, :lastyear]
    pvsM = market['pvsM'][:, :lastyear]

    # Find maximum incomes
    maxincs = np.max(incsM * cellsM)

    # Find maximum cumulative market return for x axis
    # Includes 99.9% of possible values
    cumretm = cumretsM * cellsM
    cumretv = np.sort(cumretm.flatten())
    maxcumrets = cumretv[int(0.999 * len(cumretv))]

    # Scale axes
    plt.axis([0, maxcumrets, 0, maxincs])
    plt.grid(True)

    # Plot results
    for yr in range(lastyear):
        # Get data for year
        rows = np.where(cells[:, yr] > 0)[0]
        pvs = pvsM[rows, yr]
        incs = incsM[rows, yr]
        cumrets = cumretsM[rows, yr]

        # Sort data
        cumretsS = np.sort(cumrets)
        incsS = np.sort(incs)
        pvsS = np.sort(pvs)[::-1]

        # Plot points if desired
        if 'p' in type:
            plt.plot(cumrets, incs, '*', color=clrPoints)

        # Fit line for regression of sorted incomes and cumrets
        # incomeS = b(1) + b(2)*cumretS
        xvals = np.vstack([np.ones(len(cumretsS)), cumretsS]).T
        b = np.linalg.lstsq(xvals, incsS, rcond=None)[0]

        # Compute fitted incomes using regression equation
        incsFitted = b[0] + b[1] * cumretsS
        # Compute present value of original set of incomes
        pvIncs = np.sum(pvs * incs)
        # Compute present value of fitted line
        pvLine = np.sum(pvsS * incsFitted)
        # Find additional income for each scenario
        delta = (pvIncs - pvLine) / np.sum(pvs)
        # Increase each fitted income by a constant so pv = original amount
        incsFitted = incsFitted + delta

        # Plot sorted cumrets and incomes if desired
        if 'c' in type:
            plt.plot(cumretsS, incsS, '*', color=clrCurve)

        # Plot fitted line
        if 'l' in type and yr > 0:
            plt.plot([0, cumretsS], [b[0] + delta, incsFitted], color=clrLine, linewidth=4)

        # add title
        ttl1 = f'Efficient Real Incomes Year, {yr}  States: {states}'
        plt.title(ttl1, color='b')

        # pause
        plt.pause(delay)

        # shade points if plotted
        if 'p' in type:
            plt.plot(cumrets, incs, '*', color=clrPointsShade)

        # shade sorted cumrets and incomes if plotted
        if 'c' in type:
            plt.plot(cumretsS, incsS, '*', color=clrCurveShade)

        # shade fitted line if plotted
        if 'l' in type and yr > 1:
            plt.plot([0, cumretsS], [b[0] + delta, incsFitted], color=clrLineShade, linewidth=4)

        # pause
        plt.pause(delay)

        # change delay time
        delay -= delayChange