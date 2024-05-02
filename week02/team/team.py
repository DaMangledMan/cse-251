"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    
    def __init__(self, URL):
        super().__init__()
        self.url = URL
        
    def run(self):
        self.response = requests.get(rf"{self.url}")
        if self.response.status_code == 200:
            self.data = self.response.json()
    
    def get_data(self):
        return self.data

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle

        request = Request_thread(f'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')

        request.start()
        request.join()


    def draw_card(self):
        # TODO add call to get a card
        
        request = Request_thread(f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1')

        request.start()
        request.join()

        # print_dict(request.get_data())

        return request.get_data()["cards"][0]["code"]



    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    
    # request = Request_thread('https://deckofcardsapi.com/api/deck/new/')

    # request.start()
    # request.join()

    deck_id = 'lx3bkbz847cj'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(52):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

