import numpy as np
import matplotlib.pyplot as plt

def analPlotYOYIncomes(analysis, client, market, plottype, states):
    # plots income images using personal states in vector states
    
    # initialize graph
    plt.figure(figsize=analysis.figPosition)
    plt.grid(True)
    plt.title(f'YOYIncomes {plottype.lower()}')
    
    # set real or nominal text
    if 'n' in plottype.lower():
        rntext = 'Nominal '
    else:
        rntext = 'Real '
    
    # set states text
    statestext = f'States: {states}'
    
    # convert client incomes to nominal values if required
    if 'n' in plottype.lower():
        client.incomesM = market.cumCsM * client.incomesM
    
    # set labels
    plt.xlabel(f'Year t {rntext}Income')
    plt.ylabel(f'Year t+1 {rntext}Income')
    plt.title(f'Year over Year {rntext}Incomes: {statestext}, Year t: ')
    
    # create matrix with 1 for each personal state to be included
    cells = np.zeros_like(client.pStatesM)
    for s in states:
        cells += (client.pStatesM == s)
    
    # find last year with income for personal states
    nyrs = np.max(np.where(np.sum(cells, axis=0) > 0)[0]) + 1
    
    # modify matrices
    incs = client.incomesM[:, :nyrs]
    cells = cells[:, :nyrs]
    
    # set axes
    ii = np.where(cells > 0)[0]
    maxval = np.max(incs[ii])
    minval = np.min(incs[ii])
    if analysis.plotYOYIncomesWithZero == 'y':
        minval = 0
    plt.axis([minval, maxval, minval, maxval])
    
    # initialize plot
    plt.grid(True)
    plt.hold(True)
    
    # set colors for states 0,1,2,3 and 4
    cmap = [[1, 0.5, 0], [1, 0, 0], [0, 0, 1], [0, 0.8, 0], [1, 0.5, 0]]
    
    # set full color based on states
    clrmat = [cmap[s + 1] for s in states]
    clrFull = np.mean(clrmat, axis=0)
    
    # set shade color
    shade = analysis.animationShadowShade
    clrShade = shade * clrFull + (1 - shade) * [1, 1, 1]
    
    # set delay change parameter
    delays = analysis.animationDelays
    delayChange = (delays[1] - delays[0]) / (nyrs - 1)
    delay = delays[0]
    
    # plot 45 degree line
    plt.plot([minval, maxval], [minval, maxval], 'k-', linewidth=1)
    
    # plot incomes
    for col in range(1, nyrs):
        plt.title(f'{statestext}, Year t: {col}')
        cellmat = cells[:, col - 1:col]
        ii = np.where(np.sum(cellmat, axis=1) >= 2)[0]
        plt.plot(incs[ii, col - 1], incs[ii, col], '.', color=clrFull, linewidth=2)
        plt.plot([minval, maxval], [minval, maxval], 'k-', linewidth=2)
        plt.pause(delay)
        delay += delayChange
        plt.plot(incs[ii, col - 1], incs[ii, col], '.', color=clrShade, linewidth=2)


