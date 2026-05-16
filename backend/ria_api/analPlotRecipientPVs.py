import numpy as np
import matplotlib.pyplot as plt

def analPlotRecipientPVs(analysis, client, market):
    # plot recipient present values as pie or bar chart
    # called by analysis_process function
    # compute values for state incomes
    pvs = []
    for state in range(5):
        ii = np.where(client.pStatesM == state)[0]
        pv = np.sum(market.pvsM[ii] * client.incomesM[ii])
        pvs.append(pv)
    # add states 0 to state 4 for estate total
    pvs = [pvs[1:4], pvs[0] + pvs[4]]
    # compute fees
    fees = np.sum(market.pvsM * client.feesM)
    # add fees to present values
    pvs.append(fees)
    # compute total value and create string in $thousands
    totalVal = np.sum(pvs)
    totalValStg = f'${round(totalVal / 1000):.0f} thousand'
    # if any value is zero change to small positive value
    pvs = [x if x != 0 else 0.00001 for x in pvs]
    # compute proportions
    props = 100 * (np.array(pvs) / np.sum(pvs))

    # create chart
    plt.figure(figsize=analysis.figPosition)
    plt.figure(1).canvas.set_window_title('RecipientPresent Values')
    # create legends
    legends = [
        f"{client.p1Name}: {props[0]:.1f}%",
        f"{client.p2Name}: {props[1]:.1f}%",
        f"Both: {props[2]:.1f}%",
        f"Estate: {props[3]:.1f}%",
        f"Fees: {props[4]:.1f}%"
    ]
    # create chart
    if min(props) >= 0:
        # create a pie chart
        if min(props) > 0.05:
            labels = [client.p1Name, client.p2Name, 'Both', 'Estate', 'Fees']
        else:
            labels = ['', '', '', '', '']
        plt.pie(props, labels=labels)
        plt.setp(plt.gca().get_legend_handles_labels()[1], fontsize=20)
        # create legend
        plt.legend(legends, loc='lower left')
        plt.colormap = plt.cm.get_cmap('viridis', len(legends))
    else:
        # create a bar chart
        plt.bar(range(len(props)), props)
        plt.grid()
        plt.ylabel('Percent of Total Value')
        plt.xticks(range(len(props)), [client.p1Name, client.p2Name, 'Both', 'Estate', 'Fees'])

    # add title
    plt.title(['Recipient Present Values', f'Total Value = {totalValStg}'], color=[0, 0, 1])
    plt.show()
