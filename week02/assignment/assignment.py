"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here


def main():
    global call_count

    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls

    req_top = Request_thread(TOP_API_URL)

    req_top.start()
    
    req_top.join()
    call_count += 1


    # TODO Retireve Details on film 6

    # collecting film 6 data
    film6_url = req_top.response["films"]
    film6_url += "6"

    req_film6 = Request_thread(film6_url)
    
    req_film6.start()
    
    req_film6.join()
    call_count += 1

    # collecting information for each category of information
    
    # Start

    # Characters
    num_of_characters = 0
    ch_threads = []
    ch_names_list = []

    for ch_url in req_film6.response["characters"]:
        num_of_characters += 1
        ch_t = Request_thread(ch_url)
        ch_threads.append(ch_t)
        ch_t.start()
    
    # planets
    num_of_planets = 0
    pl_threads = []
    pl_names_list = []

    for pl_url in req_film6.response["planets"]:
        num_of_planets += 1
        pl_t = Request_thread(pl_url)
        pl_threads.append(pl_t)
        pl_t.start()
    
    # starships
    num_of_starships = 0
    ss_threads = []
    ss_names_list = []

    for ss_url in req_film6.response["starships"]:
        num_of_starships += 1
        ss_t = Request_thread(ss_url)
        ss_threads.append(ss_t)
        ss_t.start()
    
    # vehicles
    num_of_vehicles = 0
    ve_threads = []
    ve_names_list = []

    for ve_url in req_film6.response["vehicles"]:
        num_of_vehicles += 1
        ve_t = Request_thread(ve_url)
        ve_threads.append(ve_t)
        ve_t.start()
    
    # species
    num_of_species = 0
    sp_threads = []
    sp_names_list = []

    for sp_url in req_film6.response["species"]:
        num_of_species += 1
        sp_t = Request_thread(sp_url)
        sp_threads.append(sp_t)
        sp_t.start()
    
    
    # Join

    # People
    for ch_t in ch_threads:
        ch_t.join()
        call_count += 1
        ch_names_list.append(ch_t.response["name"])

    ch_names_list.sort()

    # Planets
    for pl_t in pl_threads:
        pl_t.join()
        call_count += 1
        pl_names_list.append(pl_t.response["name"])

    pl_names_list.sort()

    # Starships
    for ss_t in ss_threads:
        ss_t.join()
        call_count += 1
        ss_names_list.append(ss_t.response["name"])

    ss_names_list.sort()

    # Vehicles
    for ve_t in ve_threads:
        ve_t.join()
        call_count += 1
        ve_names_list.append(ve_t.response["name"])

    ve_names_list.sort()

    # Species
    for sp_t in sp_threads:
        sp_t.join()
        call_count += 1
        sp_names_list.append(sp_t.response["name"])

    sp_names_list.sort()



    # TODO Display results

    log.write("-------------------------------------------------------")
    title = req_film6.response["title"]
    log.write(f"Title   : {title}")
    director = req_film6.response["director"]
    log.write(f"Director: {director}")
    producer = req_film6.response["producer"]
    log.write(f"Producer: {producer}")
    release_date = req_film6.response["release_date"]
    log.write(f"Released: {release_date}")
    log.write_blank_line()
    log.write(f"Characters: {num_of_characters}")
    log.write(", ".join(str(x) for x in ch_names_list))
    log.write_blank_line()
    log.write(f"Planets: {num_of_planets}")
    log.write(", ".join(str(x) for x in pl_names_list))
    log.write_blank_line()
    log.write(f"Starships: {num_of_starships}")
    log.write(", ".join(str(x) for x in ss_names_list))
    log.write_blank_line()
    log.write(f"Vehicles: {num_of_vehicles}")
    log.write(", ".join(str(x) for x in ve_names_list))
    log.write_blank_line()
    log.write(f"Species: {num_of_species}")
    log.write(", ".join(str(x) for x in sp_names_list))
    log.write_blank_line()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
