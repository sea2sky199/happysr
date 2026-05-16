import numpy as np
import matplotlib.pyplot as plt

def analPlotSurvivalProbabilities(analysis, client, market):
    probSurvive1only = np.mean(client['pStatesM'] == 1, axis=0)
    probSurvive2only = np.mean(client['pStatesM'] == 2, axis=0)
    probSurviveBoth = np.mean(client['pStatesM'] == 3, axis=0)
    probSurviveAll = np.column_stack([probSurviveBoth, probSurvive1only, probSurvive2only])

    ax = plt.gca()
    ax.set_facecolor('white')
    x = np.arange(probSurviveAll.shape[0])
    ax.bar(x, probSurviveAll[:, 0], label='Both', color=[0, 0.8, 0])
    ax.bar(x, probSurviveAll[:, 1], bottom=probSurviveAll[:, 0],
           label=client['p1Name'] + ' only', color=[1, 0, 0])
    ax.bar(x, probSurviveAll[:, 2],
           bottom=probSurviveAll[:, 0] + probSurviveAll[:, 1],
           label=client['p2Name'] + ' only', color=[0, 0, 1])
    ax.grid(True)
    ax.set_title('Recipient Survival Probabilities', color=[0, 0, 1])
    ax.set_xlabel('Year')
    ax.set_ylabel('Probability')
    ax.legend()
