import json
import matplotlib.pyplot as plt

user_no = []
delay_avg = []
delay_std = []

def parse_line(line):
    d = json.loads(line)
    user_no.append(d['Users'])
    delay_avg.append(float(d['Time']))
    
filepath = './evaluation_scripts/ipfs_test/ipfs_node_1_result.txt'  
with open(filepath) as fp:  
   line = fp.readline()
   while line:
        parse_line(line)
        line = fp.readline()

plt.scatter(user_no, delay_avg)
plt.show()
