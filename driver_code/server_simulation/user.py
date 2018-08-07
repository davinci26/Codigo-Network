#!/usr/bin/env python3
import requests
import threading
import time
import threading
import argparse
import datetime
import numpy as np
lock = threading.Lock()
import json
results = []
user_id = []

# Define a function for the thread
def make_request(id):
    start = time.time()
    r = requests.post("http://127.0.0.1:8020/test/")
    end = time.time()
    results.append(end-start)
    user_id.append(id)

def make_simulation(size):
    # Create two threads as follows
    thread_list = []
    for i in range(0,size):
        thread_list.append(threading.Thread(target=make_request, args=(i,)))

    for i, thread in enumerate(thread_list):
        try:
            thread.start()
        except:
            print ("Error: unable to start thread - reached thread {}".format(i))
            size = i
            
    for i in range(0,i):
        thread_list[i].join()


def parse_results(results,thread_no):
    result_json = {'Date-time': now.strftime("%Y-%m-%d %H%M"),
                'Users': thread_no,
                'Avg_Time': np.mean(results),
                'Std_Time': np.std(results),
                'Results': results }
    with open(filepath, 'a+') as dataf:
        json.dump(result_json, dataf)
        dataf.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('--Threads', type=int, nargs='?',
                        help='Max number of users to spawn')
    parser.add_argument('--Increment', type=int, nargs='?',
                        help='User increment')

    args = parser.parse_args()
    filepath = './evaluation_scripts/datasets/server_results_new.json'  
    for thread_no in range(1,args.Threads+1, args.Increment):
        make_simulation(thread_no)
        now = datetime.datetime.now()
        print("Completed run {}/{}".format(thread_no,args.Threads))
        parse_results(results,thread_no)
        print("-> ".join(map(str, user_id)))
        results = []
        user_id = []
