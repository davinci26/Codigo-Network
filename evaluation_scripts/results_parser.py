import json
import matplotlib.pyplot as plt

def plot(filepath):
    user_no = []
    delay_avg = []
    delay_std = []

    def parse_line(line):
        d = json.loads(line)
        user_no.append(d['Users'])
        delay_avg.append(d['Avg Time'])
        delay_std.append(d['Std Time'])
    
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            parse_line(line)
            line = fp.readline()

    plt.errorbar(user_no, delay_avg, yerr = delay_std, fmt='o' )
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average delay[m]')


ipfs_path = './evaluation_scripts/ipfs_test/result.txt'
server_path = './evaluation_scripts/server_test/results.txt'

plot(ipfs_path)
#plot(server_path)

plt.show()
