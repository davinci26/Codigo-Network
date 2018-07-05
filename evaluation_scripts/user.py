#!/usr/bin/env python3
import requests
import threading
import time
import threading
import argparse
lock = threading.Lock()

# Define a function for the thread
def make_request():
    start = time.time()
    r = requests.post("http://35.206.132.245:8020/test/")
    end = time.time()
    lock.acquire() # thread blocks at this line until it can obtain lock
    # in this section, only one thread can be present at a time.
    with open("./evaluation_scripts/results.txt", 'a+') as dataf:
        dataf.write("Request time: {} \n".format(end-start))
    lock.release()


def make_simulation(size):
    # Create two threads as follows
    thread_list = []
    for i in range(0,size):
        thread_list.append(threading.Thread(target=make_request))

    for thread in thread_list:
        try:
            thread.start()
        except:
            print ("Error: unable to start thread - reached thread {}".format(i))

    for ii in range(0,i):
        thread_list[ii].join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('--Threads', type=int, nargs='?',
                        help='Number of users to spawn')
    args = parser.parse_args()
    make_simulation(args.Threads)

