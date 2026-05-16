import matplotlib.pyplot as plt

def analysis_process(analysis, client, market):
    # process an analysis data structure to produce analysis output

    # initialize
    analysis = initialize(analysis, client)  # *******

    # analysis: plot survival probabilities
    if analysis['plotSurvivalProbabilities'] == 'y':
        # create figure
        analysis = createFigure(analysis)
        # call external function analPlotSurvivalProbabilities
        analPlotSurvivalProbabilities(analysis, client, market)
        # process figure
        analysis = processFigure(analysis)

    # analysis: plot scenarios
    if analysis['plotScenarios'] == 'y':
        # find types
        types = analysis['plotScenariosTypes']
        # create figures
        for i in range(len(types)):
            # create figure
            analysis = createFigure(analysis)
            # call external function analPlotScenarios
            analPlotScenarios(analysis, client, market, types[i])
            # process figure
            analysis = processFigure(analysis)

    # analysis: plot income distributions
    if analysis['plotIncomeDistributions'] == 'y':
        # find states
        states = analysis['plotIncomeDistributionsStates']
        # find types
        types = analysis['plotIncomeDistributionsTypes']
        # create figures
        for i in range(len(types)):
            for j in range(len(states)):
                # create Figure
                analysis = createFigure(analysis)
                # call external function analPlotIncomeDistributions
                analPlotIncomeDistributions(analysis, client, market, types[i], states[j])
                # process figure
                analysis = processFigure(analysis)

    # analysis: plot income maps
    if analysis['plotIncomeMaps'] == 'y':
        # find states
        states = analysis['plotIncomeMapsStates']
        # find types
        types = analysis['plotIncomeMapsTypes']
        # create figures
        for i in range(len(types)):
            for j in range(len(states)):
                # create Figure
                analysis = createFigure(analysis)
                # call external function analPlotIncomeMaps
                analPlotIncomeMaps(analysis, client, market, types[i], states[j])
                # process figure
                analysis = processFigure(analysis)

    # analysis: plot year over year incomes
    if analysis['plotYOYIncomes'] == 'y':
        # find states
        states = analysis['plotYOYIncomesStates']
        # find types
        types = analysis['plotYOYIncomesTypes']
        # create figures
        for i in range(len(types)):
            for j in range(len(states)):
                # create Figure
                analysis = createFigure(analysis)
                # call external function analPlotYOYIncomes
                analPlotYOYIncomes(analysis, client, market, types[i], states[j])
                # process figure
                analysis = processFigure(analysis)

    # analysis: plot recipient present values
    if analysis['plotRecipientPVs'] == 'y':
        # create figure
        analysis = createFigure(analysis)
        # call external function analPlotRecipientPVs
        analPlotRecipientPVs(analysis, client, market)
        # process figure
        analysis = processFigure(analysis)


    # analysis: plot PPCs and incomes
    if analysis['plotPPCSandIncomes'] == 'y':
        # find states
        states = analysis['plotPPCSandIncomesStates']
        # create figures
        for i in range(len(states)):
            # create figure
            analysis = createFigure(analysis)
            # call external function analPlotPPCSandIncomes
            analPlotPPCSandIncomes(analysis, client, market, states[i])
            # process figure
            analysis = processFigure(analysis)

    # analysis: plot yearly present values
    if analysis['plotYearlyPVs'] == 'y':
        # find states
        states = analysis['plotYearlyPVsStates']
        # create figures
        for i in range(len(states)):
            # create figure
            analysis = createFigure(analysis)
            # call external function analPlotYearlyPVs
            analPlotYearlyPVs(analysis, client, market, states[i])
            # process figure
            analysis = processFigure(analysis)

    # analysis: plot efficient incomes
    if analysis['plotEfficientIncomes'] == 'y':
        # find states
        states = analysis['plotEfficientIncomesStates']
        # find types
        types = analysis['plotEfficientIncomesTypes']
        # create figures
        for i in range(len(types)):
            for j in range(len(states)):
                # create figure
                analysis = createFigure(analysis)
                # call external function analPlotEfficientIncomes
                analPlotEfficientIncomes(analysis, client, market, types[i], states[j])
                # process figure
                analysis = processFigure(analysis)

    # finish all analyses
    finish(analysis)

def initialize(analysis, client):
    # Initialize variables
    # Set figure position and number
    figsize = client['figureSize']
    if len(figsize) < 2:
        ss = plt.get_current_fig_manager().window.wm_geometry().split('+')[0].split('x')
        figsize = [0.9 * float(ss[0]), 0.9 * float(ss[1])]
    figw = figsize[0]
    figh = figsize[1]
    ss = plt.get_current_fig_manager().window.wm_geometry().split('+')[0].split('x')
    x1 = (float(ss[0]) - figw) / 2
    x2 = (float(ss[1]) - figh) / 2
    analysis['figPosition'] = [x1, x2, figw, figh]
    # Set figure number and initialize stack
    analysis['figNum'] = 1
    analysis['stack'] = []

def createFigure(analysis):
    # Create a new figure
    fignum = plt.figure()
    plt.get_current_fig_manager().window.setGeometry(int(analysis['figPosition'][0]), int(analysis['figPosition'][1]), int(analysis['figPosition'][2]), int(analysis['figPosition'][3]))
    analysis['stack'].append(fignum)
    # Set colormap to the default set of colors
    plt.set_cmap('viridis')
    # Set font sizes
    plt.xlabel(plt.gca().get_xlabel(), fontsize=30)
    plt.ylabel(plt.gca().get_ylabel(), fontsize=30)
    plt.title(plt.gca().get_title(), fontsize=40)
    plt.rcParams.update({'font.size': 30})
    h = [obj for obj in plt.gcf().get_children() if isinstance(obj, plt.Text)]
    for i in range(len(h)):
        h[i].set_fontsize(30)
    # Set background color
    plt.gcf().set_facecolor((1, 1, 1))
    # If figures not stacked, remove bottom figure
    if analysis['stackFigures'].lower() == 'n':
        if len(analysis['stack']) > 2:
            plt.close(analysis['stack'][0])
            analysis['stack'] = analysis['stack'][1:]


def processFigure(analysis):
    # change figure number
    analysis['figNum'] += 1

    # delay before next figure or end
    if analysis['figureDelay'] > 0:
        plt.pause(analysis['figureDelay'])
    else:
        plt.pause(1)

def finish(analysis):
    if analysis['stackFigures'].lower() == 'n':
        if len(analysis['stack']) > 1:
            plt.close(analysis['stack'][0])

    if analysis['figuresCloseWhenDone'].lower() == 'y':
        plt.close('all')

