import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity


addedContent = np.load('data/cleaned/timeline_analysis_added_content.npy')
consistency = np.load('data/cleaned/timeline_analysis_consistency.npy')
nr_of_participants = len(addedContent)
 
colors = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
"#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
"#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
"#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
"#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
"#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
"#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
"#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
"#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
"#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
"#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
"#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
"#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C"]
area=np.ones([1, 14])*150
area[0,6]=5
colors2 = ['r', 'b', 'c', 'm', 'k', 'y']

#added_content_norm = np.linalg.norm(addedContent)
#consistency_norm = np.linalg.norm(consistency)/2
#consistency_x_shift = 0.1
#consistency_x_shift + (np.max(consistency) - consistency[index])/consistency_norm
consistency = 1/consistency
consistency[consistency == inf] = 0
nr_of_clusters = 3
X = np.column_stack((consistency, addedContent))
X = np.delete(X, 6, 0)
X = np.delete(X, 3, 0)
y_pred = KMeans(n_clusters=nr_of_clusters).fit_predict(X)

y_pred = np.insert(y_pred, 3, 1)
y_pred = np.insert(y_pred, 6, nr_of_clusters)


for index in range(0,nr_of_participants):
    label = 'p' + str(index+1)
    scatter_plot = plt.scatter(consistency[index], addedContent[index], s=area[0,index], facecolors=colors[index], edgecolors=colors2[y_pred[index]], alpha=0.5, label=label)

plt.ylim([0,80])
plt.xlim([0, 1])
lgd = plt.legend(loc=0, scatterpoints = 1, bbox_to_anchor=(1.3, 1.08))
title = plt.title('Interaction Timeline Summary: Consistency vs. # Added Content', y=1.08)
x_label = plt.xlabel('Consistency')
y_label = plt.ylabel('# Added Content')

plt.grid()
plt.savefig('data/cleaned/summary_plots/interaction_profiles_summary.png', dpi=300, bbox_extra_artists=(lgd, title, x_label, y_label, ), bbox_inches='tight')
plt.close()

# Gaussian KDE
X = addedContent * consistency
X_calc = np.delete(X, 6, 0)[:, np.newaxis]
X_plot = np.linspace(0, 40, 1000)[:, np.newaxis]
kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X_calc)
log_dens = kde.score_samples(X_plot)
val = 0.004
for index in range(0,nr_of_participants):
    label = 'p' + str(index+1)
    plt.plot(X[index], val, 'o', color=colors[index], label=label) 
lgd = plt.legend(loc=0, scatterpoints = 1, bbox_to_anchor=(1.3, 1.08))

plt.axhline(y=0.01, linewidth=1, color='r')
plt.plot(X_plot[:, 0], np.exp(log_dens))
plt.savefig('data/cleaned/summary_plots/interaction_profiles_summary_summary.png', dpi=300, bbox_extra_artists=(lgd, ), bbox_inches='tight')
plt.close()
