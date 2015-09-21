from __future__ import print_function
from time import sleep
from threading import Semaphore, Thread
import random
import sys

class DrivingRange:

    def __init__(self, stash, num_per_bucket, num_threads):
        self.stash = stash
        self.num_per_bucket = num_per_bucket
        self.num_threads = num_threads
        self.balls_on_field = 0
        self.mutex = Semaphore(1)
        self.empty_stash = Semaphore(0)
        self.enough_stash = Semaphore(0)
        self.rng = random.Random()
        self.rng.seed(100)

    def golfer(self, id):
        num_balls = 0
        while True:
            if num_balls <= 0:
                self.mutex.acquire()
                if self.stash < self.num_per_bucket:
                    self.empty_stash.release()
                    self.enough_stash.acquire()
                    sleep(5)
                num_balls = self.num_per_bucket
                self.stash = self.stash - self.num_per_bucket
                print('Golfer {:2d} got {:2d} balls; Stash = {:5d}'.format(id, self.num_per_bucket, self.stash))
                self.mutex.release()
            self.mutex.acquire()
            self.balls_on_field += 1
            print('Golfer {:2d} hit ball {:2d}'.format(id, self.num_per_bucket-num_balls))
            num_balls -= 1
            self.mutex.release()
            self.sleep()

    def cart(self):
        while True:
            self.empty_stash.acquire()
            print('#######################################################')
            print('stash = {:5d}; Cart entering field'.format(self.stash))
            self.stash += self.balls_on_field
            temp = self.balls_on_field
            self.balls_on_field = 0
            print('Cart done, gathered {:5d} balls; stash = {:5d}'.format(temp, self.stash))
            print('#######################################################')
            self.enough_stash.release()

    def sleep(self):
        sleep(3 * self.rng.random())


if __name__ == '__main__':
    stash1 = 0
    num_per_bucket1 = 0
    num_threads1 = 0
    ts = list()
    if len(sys.argv) > 1:
        stash1 = int(sys.argv[1])
        num_per_bucket1 = int(sys.argv[2])
        num_threads1 = int(sys.argv[3])
        
    else:                                  # Default
        stash1 = 20
        num_per_bucket1 = 5
        num_threads1 = 3
    driving_range = DrivingRange(stash1, num_per_bucket1, num_threads1)
    for i in xrange(num_threads1):
        t = Thread(target=driving_range.golfer, args=[i])
        ts.append(t)

    t = Thread(target=driving_range.cart, args=[])
    ts.append(t)

    for t in ts:
        t.start()
    for t in ts:
        t.join()
         
                

