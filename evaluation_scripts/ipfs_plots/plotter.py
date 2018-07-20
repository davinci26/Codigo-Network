import matplotlib.pyplot as plt
import json
import numpy as np

save_dir = './evaluation_scripts/Plots/'

with open('./evaluation_scripts/ipfs_plots/results.json') as f:
    data = json.load(f)


x = np.arange(1,data['Users']+1)
A = np.vstack([x, np.ones(len(x))]).T
Y = data['DuplBlocks']
m, c = np.linalg.lstsq(A, Y)[0]


fig = plt.figure()   
plt.scatter(x,Y, label='Data Points')
plt.plot(x, m*x + c, 'r', label='Linear Regression Fit')
plt.title('IPFS main performance issue')
plt.ylabel('Duplicate Blocks')
plt.xlabel('Number of users in the swarm')
plt.legend()
fig.savefig(save_dir + 'ipfs_duplicates.png', dpi=fig.dpi)