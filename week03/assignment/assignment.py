"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: <Your Name>

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

------------------------------------------------------------------------------

Justification:

- It does everything in the requirements and I turned in all the files 

"""

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(elephant_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(elephant_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here

def unpack_list_and_create(list):
    elephant_file = list[0]
    green_file = list[1]
    process_file = list[2]

    create_new_frame(elephant_file, green_file, process_file)



if __name__ == '__main__':
    # single_file_processing(300)
    print('cpu_count() =', CPU_COUNT)

    

    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpus and yaxis_times


    # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10

    img_prep_list = []

    for img_num in range(FRAME_COUNT):

        elephant_file = rf'elephant/image{img_num+1:03d}.png'
        green_file = rf'green/image{img_num+1:03d}.png'
        process_file = rf'processed/image{img_num+1:03d}.png'

        individual_img_list = [elephant_file, green_file, process_file]

        img_prep_list.append(individual_img_list)




    

    start_time = timeit.default_timer()


    # create_new_frame(elephant_file, green_file, process_file)
    
    for i in range(CPU_COUNT):
        xaxis_cpus.append(i+1)

        sub_start_time = timeit.default_timer()
        pool = mp.Pool(processes=i+1)
        results = pool.map(unpack_list_and_create, img_prep_list)
        yaxis_times.append(timeit.default_timer() - sub_start_time)
        log.write(f'\nTime To Process all images = {timeit.default_timer() - sub_start_time} with {i+1} processors')

        
    
    
     
    
    
    
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    log.write(f'\nTotal Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
