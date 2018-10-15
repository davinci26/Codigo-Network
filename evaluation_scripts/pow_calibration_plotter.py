import matplotlib.pyplot as plt
import numpy as np

save_dir = './evaluation_scripts/Plots/'

def prob(n):
    return (10.**77/(2.**256*50.**n))

def expectation(n):
    return 1/prob(n)

def variance(n):
    p = prob(n)
    return (1-p)/(p*p)

max_it = 3
mean = []
std = []
difficulty = []
x = np.arange(1,max_it+1)
for ii in range(0,max_it):
    print("For ii = {} expectation = {} and Std = {}".format(ii+1,expectation(ii),np.sqrt(variance(ii))))
    mean.append(expectation(ii))
    std.append(np.sqrt(variance(ii)))
    difficulty.append(10.**77/(50.**ii))

fig = plt.figure(1)
plt.subplot(211)
plt.errorbar(x,mean,std,fmt='o')
plt.xticks(np.arange(1, max_it+1, step=1))
plt.xlabel('Firmware Added')
plt.ylabel('Sha3 Computations')
plt.subplot(212)
plt.scatter(x,difficulty)
plt.xticks(np.arange(1, max_it + 1, step=1))
plt.xlabel('Firmware Added')
plt.ylabel('PoW Difficulty')

fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
fig.savefig(save_dir + 'pow_cost' +'.png',bbox_inches='tight')
plt.show()