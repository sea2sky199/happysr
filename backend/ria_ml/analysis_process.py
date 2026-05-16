import matplotlib.pyplot as plt
from analPlotSurvivalProbabilities import analPlotSurvivalProbabilities
from analPlotScenarios import analPlotScenarios
from analPlotIncomeDistributions import analPlotIncomeDistributions
from analPlotIncomeMaps import analPlotIncomeMaps
from analPlotYOYIncomes import analPlotYOYIncomes
from analPlotRecipientPVs import analPlotRecipientPVs
from analPlotPPCSandIncomes import analPlotPPCSandIncomes
from analPlotYearlyPVs import analPlotYearlyPVs
from analPlotEfficientIncomes import analPlotEfficientIncomes

def analysis_process(analysis, client, market):
    analysis = _initialize(analysis, client)

    if analysis['plotSurvivalProbabilities'].lower() == 'y':
        analysis = _createFigure(analysis)
        analPlotSurvivalProbabilities(analysis, client, market)
        analysis = _processFigure(analysis)

    if analysis['plotScenarios'].lower() == 'y':
        for t in analysis['plotScenariosTypes']:
            analysis = _createFigure(analysis)
            analPlotScenarios(analysis, client, market, t)
            analysis = _processFigure(analysis)

    if analysis['plotIncomeDistributions'].lower() == 'y':
        for t in analysis['plotIncomeDistributionsTypes']:
            for s in analysis['plotIncomeDistributionsStates']:
                analysis = _createFigure(analysis)
                analPlotIncomeDistributions(analysis, client, market, t, s)
                analysis = _processFigure(analysis)

    if analysis['plotIncomeMaps'].lower() == 'y':
        for t in analysis['plotIncomeMapsTypes']:
            for s in analysis['plotIncomeMapsStates']:
                analysis = _createFigure(analysis)
                analPlotIncomeMaps(analysis, client, market, t, s)
                analysis = _processFigure(analysis)

    if analysis['plotYOYIncomes'].lower() == 'y':
        for t in analysis['plotYOYIncomesTypes']:
            for s in analysis['plotYOYIncomesStates']:
                analysis = _createFigure(analysis)
                analPlotYOYIncomes(analysis, client, market, t, s)
                analysis = _processFigure(analysis)

    if analysis['plotRecipientPVs'].lower() == 'y':
        analysis = _createFigure(analysis)
        analPlotRecipientPVs(analysis, client, market)
        analysis = _processFigure(analysis)

    if analysis['plotPPCSandIncomes'].lower() == 'y':
        for s in analysis['plotPPCSandIncomesStates']:
            analysis = _createFigure(analysis)
            analPlotPPCSandIncomes(analysis, client, market, s)
            analysis = _processFigure(analysis)

    if analysis['plotYearlyPVs'].lower() == 'y':
        for s in analysis['plotYearlyPVsStates']:
            analysis = _createFigure(analysis)
            analPlotYearlyPVs(analysis, client, market, s)
            analysis = _processFigure(analysis)

    if analysis['plotEfficientIncomes'].lower() == 'y':
        for t in analysis['plotEfficientIncomesTypes']:
            for s in analysis['plotEfficientIncomesStates']:
                analysis = _createFigure(analysis)
                analPlotEfficientIncomes(analysis, client, market, t, s)
                analysis = _processFigure(analysis)

    _finish(analysis)


def _initialize(analysis, client):
    figsize = client.get('figureSize', [1500, 900])
    if len(figsize) < 2:
        figsize = [1350, 900]
    analysis['figPosition'] = figsize
    analysis['figNum'] = 1
    analysis['stack'] = []
    return analysis


def _createFigure(analysis):
    fig = plt.figure()
    analysis['stack'].append(fig)
    fig.set_facecolor('white')
    return analysis


def _processFigure(analysis):
    analysis['figNum'] += 1
    if analysis['figureDelay'] > 0:
        plt.pause(analysis['figureDelay'])
    else:
        plt.show(block=False)
        input('Press Enter to continue...')
    return analysis


def _finish(analysis):
    if analysis['stackFigures'].lower() == 'n':
        if len(analysis['stack']) > 1:
            plt.close(analysis['stack'][0])
    if analysis['figuresCloseWhenDone'].lower() == 'y':
        plt.close('all')
