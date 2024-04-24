"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team activity details in I-Learn

"""

from datetime import datetime, timedelta
import threading

# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def is_prime(n):
    global numbers_processed
    numbers_processed += 1

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


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads

    start = 10000000000
    range_count = 100000
    
    def check_for_primes(index):
        global prime_count
        for i in range(start, start + (range_count//10)):
            if is_prime(i*10-index-1):
                prime_count += 1
                print(i, end=', ', flush=True)
        print(flush=True)

    t0 = threading.Thread(target=check_for_primes, args=(0,))
    t1 = threading.Thread(target=check_for_primes, args=(1,))
    t2 = threading.Thread(target=check_for_primes, args=(2,))
    t3 = threading.Thread(target=check_for_primes, args=(3,))
    t4 = threading.Thread(target=check_for_primes, args=(4,))
    t5 = threading.Thread(target=check_for_primes, args=(5,))
    t6 = threading.Thread(target=check_for_primes, args=(6,))
    t7 = threading.Thread(target=check_for_primes, args=(7,))
    t8 = threading.Thread(target=check_for_primes, args=(8,))
    t9 = threading.Thread(target=check_for_primes, args=(9,))


    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()


    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()


    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


