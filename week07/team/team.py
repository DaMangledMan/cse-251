"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""


from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

NAMES = {
        "ch" : [],
        "pl" : [],
        "st" : [],
        "ve" : [],
        "sp" : []
    }


# TODO Add your threaded class definition here
# class Request_thread(threading.Thread):
# 
#     def __init__(self, url):
#         # Call the Thread class's init function
#         threading.Thread.__init__(self)
#         self.url = url
#         self.response = {}
# 
#     def run(self):
#         response = requests.get(self.url)
#         # Check the status code to see if the request succeeded.
#         if response.status_code == 200:
#             self.response = response.json()
#         else:
#             print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here
def main_func(url, ex):
    response = requests.get(url)
    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        response = response.json()
    else:
        print('RESPONSE = ', response.status_code)
    
    return [response, ex]


def do_nothing(value):
    pass

def callback_func(_list:list):
    NAMES[_list[1]].append(_list[0])




def main():
    global call_count

    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    throwaway_names = []

    pool_top = mp.Pool(1)
    top_result = pool_top.apply_async(main_func, args=(TOP_API_URL, throwaway_names))

    call_count += 1


    # TODO Retireve Details on film 6

    # collecting film 6 data
    film6_url = top_result.get()[0]["films"] + "6"

    pool_f6 = mp.Pool(1)
    film6_result = pool_f6.apply_async(main_func, args=(film6_url, throwaway_names))

    call_count += 1

    # collecting information for each category of information
    
    # Start
    

    # Characters  
    pool_ch = mp.Pool(3)
    results = [pool_ch.apply_async(main_func, args=(x, "ch"), callback=callback_func) for x in film6_result.get()[0]["characters"]]

    # planets
    pool_pl = mp.Pool(3)
    results = [pool_pl.apply_async(main_func, args=(x, "pl"), callback=callback_func) for x in film6_result.get()[0]["planets"]]

    
    # starships
    pool_st = mp.Pool(3)
    results = [pool_st.apply_async(main_func, args=(x, "st"), callback=callback_func) for x in film6_result.get()[0]["starships"]]

    
    # vehicles
    pool_ve = mp.Pool(3)
    results = [pool_ve.apply_async(main_func, args=(x, "ve"), callback=callback_func) for x in film6_result.get()[0]["vehicles"]]

    
    # species
    pool_sp = mp.Pool(3)
    results = [pool_sp.apply_async(main_func, args=(x, "sp"), callback=callback_func) for x in film6_result.get()[0]["species"]]

    
    
    # Close/Join
    pool_ch.close()
    pool_ch.join()
    NAMES["ch"].sort()

    pool_pl.close()
    pool_pl.join()
    NAMES["pl"].sort()

    pool_st.close()
    pool_st.join()
    NAMES["st"].sort()

    pool_ve.close()
    pool_ve.join()
    NAMES["ve"].sort()

    pool_sp.close()
    pool_sp.join()
    NAMES["sp"].sort()

    
    # TODO Display results

    log.write("-------------------------------------------------------")
    title = film6_result.get()[0]["title"]
    log.write(f"Title   : {title}")
    director = film6_result.get()[0]["director"]
    log.write(f"Director: {director}")
    producer = film6_result.get()[0]["producer"]
    log.write(f"Producer: {producer}")
    release_date = film6_result.get()[0]["release_date"]
    log.write(f"Released: {release_date}")
    log.write_blank_line()
    log.write(f"Characters: {len(NAMES['ch'])}")
    log.write(", ".join(str(x) for x in NAMES["ch"]))
    log.write_blank_line()
    log.write(f"Planets: {len(NAMES['pl'])}")
    log.write(", ".join(str(x) for x in NAMES["pl"]))
    log.write_blank_line()
    log.write(f"Starships: {len(NAMES['st'])}")
    log.write(", ".join(str(x) for x in NAMES["st"]))
    log.write_blank_line()
    log.write(f"Vehicles: {len(NAMES['ve'])}")
    log.write(", ".join(str(x) for x in NAMES["ve"]))
    log.write_blank_line()
    log.write(f"Species: {len(NAMES['sp'])}")
    log.write(", ".join(str(x) for x in NAMES["sp"]))
    log.write_blank_line()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
