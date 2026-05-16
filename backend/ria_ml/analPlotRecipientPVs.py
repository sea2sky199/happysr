import numpy as np
import matplotlib.pyplot as plt

def analPlotRecipientPVs(analysis, client, market):
    pvs = []
    for state in range(5):
        ii = np.where(client['pStatesM'] == state)
        pv = np.sum(market['pvsM'][ii] * client['incomesM'][ii])
        pvs.append(pv)

    pvs_arr = np.array([pvs[1], pvs[2], pvs[3], pvs[0] + pvs[4]])
    fees = np.sum(market['pvsM'] * client['feesM'])
    pvs_arr = np.append(pvs_arr, fees)

    totalVal = np.sum(pvs_arr)
    totalValStg = str(round(totalVal / 1000))

    pvs_arr[pvs_arr == 0] = 0.00001
    props = 100 * (pvs_arr / np.sum(pvs_arr))

    ax = plt.gca()
    labels = [client['p1Name'], client['p2Name'], 'Both', 'Estate', 'Fees']

    if np.min(props) >= 0:
        pie_labels = labels if np.min(props) > 0.05 else ['', '', '', '', '']
        wedges, texts = ax.pie(props, labels=pie_labels)
        legend_labels = [f'{labels[i]}: {props[i]:.1f} %' for i in range(5)]
        ax.legend(wedges, legend_labels, loc='lower right')
        cmap_colors = [[1, 0, 0], [0, 0, 1], [0, .8, 0], [1, .5, 0], [0, 0, 0]]
        for i, w in enumerate(wedges):
            w.set_facecolor(cmap_colors[i])
    else:
        ax.bar(range(5), props)
        ax.grid(True)
        ax.set_ylabel('Percent of Total Value')
        ax.set_xticks(range(5))
        ax.set_xticklabels(labels)

    ax.set_title(f'Recipient Present Values\nTotal Value = ${totalValStg} thousand', color=[0, 0, 1])
