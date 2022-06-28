'''
threaded approach
'''

import time
from queue import Queue
from threading import Thread
import db
import cv2
import numpy as np
import pandas as pd
import csv
import datetime
import time

# Time for Threaded: 114.82532739639282 secs
NUM_WORKERS = 20
QUEUE = Queue()
DATA = []


def worker():
    '''
    Thread function
    '''
    # Constantly check the queue for addresses
    while True:
        image = QUEUE.get()
        DATA.append(db.extrair(image))
        # Mark the processed task as done
        QUEUE.task_done()
        if QUEUE.empty():
            break


def main():
    '''
    Main function
    '''
    start_time = time.time()
    # Create the worker threads
    threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
    # Add the websites to the task queue
    dataframe = pd.read_csv('./photos.csv', delimiter=';')

    for index, row in dataframe.iterrows():
        QUEUE.put(row)

    # Start all the workers
    for thread in threads:
        thread.start()
    # Wait for all the tasks in the queue to be processed
    QUEUE.join()
    end_time = time.time()
    print('Time for Threaded:', end_time - start_time, 'secs')
    print(len(DATA))


if __name__ == "__main__":
    main()
