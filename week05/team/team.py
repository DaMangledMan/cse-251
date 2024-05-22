"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists
import queue



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
class Request_thread(threading.Thread):

    def __init__(self, file_name, Q: mp.Queue, sem: mp.Semaphore):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.file_name = file_name
        self.Q = Q
        self.sem = sem

    def run(self):
        self.file = open(rf"{self.file_name}")
        print("thread start")
        while True:
            print("thread continue")
            number = self.file.readline()
            number = number[:-1]
            if number == "":
                self.Q.put(None)
                self.sem.release()
                break
            self.Q.put(int(number))
            self.sem.release()

            
# TODO create prime_process function
def prime_process(Q: mp.Queue, sem: mp.Semaphore, primes):
    print("process start")
    while True:
        print("process continue")
        sem.acquire()
        number = Q.get()
        if number == None:
            Q.put(None)
            sem.release()
            break
        if is_prime(number):
            primes.append(number)


def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    primes = mp.Manager().list()
    Q = mp.Queue()
    process_sem = mp.Semaphore(0)
    pr_list = []

    # TODO create reading thread
    th = Request_thread(filename, Q, process_sem)

    # TODO create prime processes
    for _ in range(PRIME_PROCESS_COUNT):
        pr = mp.Process(target=prime_process, args=(Q, process_sem, primes))
        pr_list.append(pr)

    # TODO Start them all
    th.start()
    for pr in pr_list:
        pr.start()

    # TODO wait for them to complete
    th.join()
    for pr in pr_list:
        pr.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

