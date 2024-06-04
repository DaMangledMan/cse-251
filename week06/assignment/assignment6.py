"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """
    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, pipe1_conn_input, _MARBLE_COUNT, _CREATOR_DELAY):
        mp.Process.__init__(self)

        # TODO Add any arguments and variables here
        self.pipe1_conn_input = pipe1_conn_input
        self._MARBLE_COUNT = _MARBLE_COUNT
        self._CREATOR_DELAY = _CREATOR_DELAY

    def run(self):

        for _ in range(self._MARBLE_COUNT):
            marble_color = random.choice(self.colors)
            self.pipe1_conn_input.send(marble_color)
            time.sleep(self._CREATOR_DELAY)

        self.pipe1_conn_input.send(None)

        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, pipe1_conn_output, pipe2_conn_input, _NUMBER_OF_MARBLES_IN_A_BAG, _BAGGER_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe1_conn_output = pipe1_conn_output
        self.pipe2_conn_input = pipe2_conn_input
        self._NUMBER_OF_MARBLES_IN_A_BAG = _NUMBER_OF_MARBLES_IN_A_BAG
        self._BAGGER_DELAY = _BAGGER_DELAY

    def run(self):
        
        while True:
            bag = []
            for _ in range(self._NUMBER_OF_MARBLES_IN_A_BAG):
                marble = self.pipe1_conn_output.recv()
                if marble == None:
                    break
                bag.append(marble)
            if marble == None:
                self.pipe2_conn_input.send(None)
                break
            self.pipe2_conn_input.send(bag)
            time.sleep(self._BAGGER_DELAY)

        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, pipe2_conn_output, pipe3_conn_input, _ASSEMBLER_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe2_conn_output = pipe2_conn_output
        self.pipe3_conn_input = pipe3_conn_input
        self._ASSEMBLER_DELAY = _ASSEMBLER_DELAY

    def run(self):

        while True:
            gift = {}

            bag = self.pipe2_conn_output.recv()
            big_marble = random.choice(Marble_Creator.colors)

            gift["Large_Marble"] = big_marble
            gift["Bag_of_Marbles"] = bag

            if bag == None:
                self.pipe3_conn_input.send(None)
                break

            self.pipe3_conn_input.send(gift)
            time.sleep(self._ASSEMBLER_DELAY)

        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, pipe3_conn_output, _WRAPPER_DELAY, Q):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe3_conn_output = pipe3_conn_output
        self._WRAPPER_DELAY = _WRAPPER_DELAY
        self.Q = Q


    def run(self):
        num_of_gifts = 0
        while True:
            gift = self.pipe3_conn_output.recv()

            if gift == None:
                break

            num_of_gifts += 1
            with open(BOXES_FILENAME, "a") as file:
                file.write(f"{datetime.now()}: {gift}\n")

            time.sleep(self._WRAPPER_DELAY)
        
        self.Q.put(num_of_gifts)

        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    _MARBLE_COUNT = settings[MARBLE_COUNT]
    _CREATOR_DELAY = settings[CREATOR_DELAY]
    _NUMBER_OF_MARBLES_IN_A_BAG = settings[NUMBER_OF_MARBLES_IN_A_BAG]
    _BAGGER_DELAY = settings[BAGGER_DELAY]
    _ASSEMBLER_DELAY = settings[ASSEMBLER_DELAY]
    _WRAPPER_DELAY = settings[WRAPPER_DELAY]

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    pipe1_conn_input, pipe1_conn_output = mp.Pipe()
    pipe2_conn_input, pipe2_conn_output = mp.Pipe()
    pipe3_conn_input, pipe3_conn_output = mp.Pipe()

    Q = mp.Queue()

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creating = Marble_Creator(pipe1_conn_input, _MARBLE_COUNT, _CREATOR_DELAY)
    bagging = Bagger(pipe1_conn_output, pipe2_conn_input, _NUMBER_OF_MARBLES_IN_A_BAG, _BAGGER_DELAY)
    assembling = Assembler(pipe2_conn_output, pipe3_conn_input, _ASSEMBLER_DELAY)
    wrapping = Wrapper(pipe3_conn_output, _WRAPPER_DELAY, Q)

    log.write('Starting the processes')
    # TODO add code here
    creating.start()
    bagging.start()
    assembling.start()
    wrapping.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    creating.join()
    bagging.join()
    assembling.join()
    wrapping.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f"{Q.get()} gifts created")




if __name__ == '__main__':
    main()

