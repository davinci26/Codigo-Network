import matplotlib.pyplot as plt
import json
import numpy as np

save_dir = './evaluation_scripts/Plots/'

def parse_line(line):
    d = json.loads(line)
    return int(d['Users']),float(d['DuplBlocks'])

def parse_file(file):
    users = []
    duplicate_blocks = []
    with open(file) as fp:  
        line = fp.readline()
        while line:
            output = parse_line(line)
            users.append(output[0])
            duplicate_blocks.append(output[1])
            line = fp.readline()
    return users, duplicate_blocks

def linear_reg(xx,yy):
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, Y)[0]
    y_fit = m*np.array(x).astype(float) + c
    return y_fit


x,Y = parse_file('./evaluation_scripts/datasets/ipfs_duplicates_sim.json')

xx,YY = parse_file('./evaluation_scripts/datasets/ipfs_duplicates_lat.json')

y_fit = linear_reg(x,Y)
#yy_fit = linear_reg(xx,YY)

fig = plt.figure()   
plt.plot(x,Y,'x', label='Zero latency Data Points')
plt.plot(x, y_fit, 'r', alpha=0.8, label='Zero Latency Linear Regression Fit')
plt.plot(xx,YY,'x', label='Latency Data Points')
#plt.plot(xx, yy_fit, 'r', alpha=0.8, label='Latency Linear Regression Fit')

plt.ylabel('Duplicate Blocks')
plt.xlabel('Number of users in the swarm')
plt.legend()
plt.show()
#fig.savefig(save_dir + 'ipfs_duplicates.png', dpi=fig.dpi,bbox_inches='tight')