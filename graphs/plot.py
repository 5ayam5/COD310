import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["figure.figsize"] = (11.04,2.56)
df = pd.read_csv("data.csv")
ax = plt.subplot(111)
x = np.array([2 * i + 1.0 for i in range(len(df['Workload']))])
w = 0.3
handles = []
handles.append(ax.bar(x - w * 2.5, df['FastCool'], color='gray', width=w, align='center'))
handles.append(ax.bar(x - w * 1.5, df['RoundRobin'], color='blue', width=w, align='center'))
handles.append(ax.bar(x - w * 0.5, df['Alternation'], color='orange', width=w, align='center'))
handles.append(ax.bar(x, df['MFU'], color='green', width=w, align='center'))
handles.append(ax.bar(x + w * 0.5, df['TemPo'], color='brown', width=w, align='center'))
handles.append(ax.bar(x + w * 1.5, df['TemPoE'], color='cyan', width=w, align='center'))
handles.append(ax.bar(x + w * 2.5, df['NoDPBTM'], color='red', width=w, align='center'))
ax.axhline(y=1, color='black', alpha=0.2, linestyle='--')
plt.ylabel("Normalized Execution Time")
plt.xticks(x, df['Workload'])
plt.legend(handles, df.columns.values[1:], ncol=len(handles), prop={'size': 8})

plt.savefig("plot.svg")
