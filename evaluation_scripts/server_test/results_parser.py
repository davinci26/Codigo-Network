import json
import matplotlib.pyplot as plt

user_no = []
delay_avg = []
delay_std = []

def parse_line(line):
    d = json.loads(line)
    user_no.append(d['Users'])
    delay_avg.append(d['Avg Time'])
    delay_std.append(d['Std Time'])

filepath = './evaluation_scripts/server_test/results.txt'  
with open(filepath) as fp:  
   line = fp.readline()
   while line:
        parse_line(line)
        line = fp.readline()

plt.errorbar(user_no, delay_avg, yerr=delay_std)
plt.show()
