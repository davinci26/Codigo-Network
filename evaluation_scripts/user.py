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

# Define a function for the thread
def make_request():
    start = time.time()
    r = requests.post("http://35.206.132.245:8020/test/")
    end = time.time()
    lock.acquire()
    results.append(end-start)
    lock.release()


def make_simulation(size):
    # Create two threads as follows
    thread_list = []
    for i in range(0,size):
        thread_list.append(threading.Thread(target=make_request))

    for i, thread in enumerate(thread_list):
        try:
            thread.start()
        except:
            print ("Error: unable to start thread - reached thread {}".format(i))
            size = i

    for k in range(0,size):
        thread_list[k].join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('--Threads', type=int, nargs='?',
                        help='Max number of users to spawn')
    parser.add_argument('--Increment', type=int, nargs='?',
                        help='User increment')

    args = parser.parse_args()

    for thread_no in range(1,args.Threads+1, args.Increment):
        make_simulation(thread_no)
        now = datetime.datetime.now()
        print("Completed run {}/{}".format(thread_no,args.Threads))
        result_json = {'Date-time': now.strftime("%Y-%m-%d %H%M"),
                       'Users': thread_no,
                       'Avg Time': np.mean(results),
                       'Std Time': np.std(results),
                       'Results': results }

        with open("./evaluation_scripts/results.txt", 'a+') as dataf:
            json.dump(result_json, dataf)
            dataf.write('\n')

        results = []
