"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import timeit

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4       # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(log:Log, data_queue:queue.Queue, read:threading.Semaphore, retrieve:threading.Semaphore):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        retrieve.acquire()

        # TODO process the value retrieved from the queue
        url = data_queue.get()
        read.release()
        
        if url == NO_MORE_VALUES:
            break

        response = requests.get(url)       

        # TODO make Internet call to get characters name and log it
        
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            data = response.json()
        else:
            print('RESPONSE = ', response.status_code)
        
        log.write(data["name"])



def file_reader(log:Log, file_name, data_queue:queue.Queue, read:threading.Semaphore, retrieve:threading.Semaphore): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    url_list = []
    file = open(file_name, "r")
    
    while True:
        url = file.readline()
        url = url[:-1]
        if url == "":
            break
        url_list.append(url)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for url in url_list:
        read.acquire()
        data_queue.put(url)
        retrieve.release()

    for _ in range(RETRIEVE_THREADS):
        read.acquire()
        data_queue.put(NO_MORE_VALUES)
        retrieve.release()
    
    


    



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue

    data_queue = queue.Queue(RETRIEVE_THREADS)
    read = threading.Semaphore(RETRIEVE_THREADS)
    retrieve = threading.Semaphore(0)

    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    file_th = threading.Thread(target=file_reader, args=(log, "urls.txt", data_queue, read, retrieve))

    retrieve_list = []
    for i in range(RETRIEVE_THREADS):
        retrieve_th = threading.Thread(target=retrieve_thread, args=(log, data_queue, read, retrieve))
        retrieve_list.append(retrieve_th)


    start_time = timeit.default_timer

    # TODO Get them going - start the retrieve_threads first, then file_reader
    file_th.start()
    for th in retrieve_list:
        th.start()

    # TODO Wait for them to finish - The order doesn't matter
    file_th.join()
    for th in retrieve_list:
        th.join()

    log.stop_timer("time to process all names")


if __name__ == '__main__':
    main()




