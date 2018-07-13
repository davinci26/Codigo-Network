import argparse
import json
import numpy as np
import datetime

parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--nodes', type=int, nargs='?',
                    help='Number of Nodes')

# {"Used Id": "1", "Date-time": "2018-07-13 1255", "Users": 91, "Time": "6.5955727100372314"}
# {"Avg Time": , "Users": 1, "Results": [0.03027057647705078], "Date-time": "2018-07-05 1429", "Std Time": 0.0}
results = []
def parse_line(line):
    d = json.loads(line)
    results.append(float(d['Time']))

if __name__ == '__main__':
    args = parser.parse_args()
    for n in range(1,args.nodes+1):    
        filepath = "./evaluation_scripts/ipfs_test/ipfs_nodes_{}_result.txt".format(n) 
        with open(filepath) as fp:  
            line = fp.readline()
            while line:
                    parse_line(line)
                    line = fp.readline()
    print([results])
    now = datetime.datetime.now()
    result_json = {'Date-time': now.strftime("%Y-%m-%d %H%M"),
                   'Users': args.nodes,
                   'Avg Time': np.mean(results),
                   'Std Time': np.std(results),
                   'Results': results }
    
    out_file = "./evaluation_scripts/ipfs_test/result.txt".format(n)  
    with open(out_file, 'a+') as dataf:
        json.dump(result_json, dataf)
        dataf.write('\n')

    print("============== File Merge Completed ===================") 
