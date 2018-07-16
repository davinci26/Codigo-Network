import json
import matplotlib.pyplot as plt
from scipy import stats

def plot(filepath):
    user_no = []
    delay_avg = []
    delay_std = []
    results = []

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
    plt.ylabel('Average delay[sec]')


def statistics(filepath):
    user_no = []
    results = []
    def pasrse(line):
        d = json.loads(line)
        user_no.append(d['Users'])
        results.append(d['Results'])
    
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            pasrse(line)
            line = fp.readline()

    for result in results:
        print(stats.describe(result))
        print("========================")

ipfs_path = './evaluation_scripts/ipfs_test/result.txt'
server_path = './evaluation_scripts/server_test/results.txt'


#statistics(ipfs_path)


plot(ipfs_path)
plt.show()
#plot(server_path)
#plt.show()
