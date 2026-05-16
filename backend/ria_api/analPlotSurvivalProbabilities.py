def analPlotSurvivalProbabilities(analysis, client, market):
    # plot survival probabilities
    # called by analysis_process function
    # get probabilities of survival
    probSurvive1only = np.mean(client.pStatesM == 1)
    probSurvive2only = np.mean(client.pStatesM == 2)
    probSurviveBoth = np.mean(client.pStatesM == 3)
    probSurviveAll = [probSurviveBoth, probSurvive1only, probSurvive2only]

    # create graph
    plt.figure(figsize=analysis.figPosition)
    plt.bar(np.arange(3), probSurviveAll, color=['g', 'r', 'b'])
    plt.grid(True)
    plt.title('Recipient Survival Probabilities', color=[0, 0, 1])
    plt.xlabel('Year')
    plt.ylabel('Probability')
    plt.legend([f'Both', f"{client.p1Name} only", f"{client.p2Name} only"])
    plt.set_cmap(np.array([[0, 0.8, 0], [1, 0, 0], [0, 0, 1]]))