from __future__ import print_function
from time import sleep
from threading import Semaphore, Thread
import random
from timeit import Timer
import datetime
import sys

class Dining_philosopher_footman(object):
    def __init__(self, num_philosophers, num_meals):
        self.num_philosophers = num_philosophers
        self.num_meals = num_meals
        self.forks = list()
        for i in xrange(self.num_philosophers):
            self.forks.append(Semaphore(1))
        self.footman = Semaphore(self.num_philosophers-1)
        self.rng = random.Random()
        self.mutex = Semaphore(1)
        self.rng.seed(100)

    def left(self, i):
        return i

    def right(self, i):
        return (i + 1) % self.num_philosophers

    def sleep(self):
        sleep(self.rng.random() / 1000)

    def get_forks(self, i):
        self.footman.acquire()
        self.forks[self.right(i)].acquire()
        self.forks[self.left(i)].acquire()
        
    def put_forks(self, i):       
        self.forks[self.right(i)].release()
        self.forks[self.left(i)].release()        
        self.footman.release()

    def philosopher(self, id):
        while (self.num_meals > 0):
            self.get_forks(id)
            self.mutex.acquire()
            self.num_meals -= 1
            self.mutex.release()
            self.put_forks(id)
            self.sleep()

class Dining_philosopher_lefthand(object):
    def __init__(self, num_philosophers, num_meals):
        self.num_philosophers = num_philosophers
        self.num_meals = num_meals
        self.forks = list()
        for i in xrange(self.num_philosophers):
            self.forks.append(Semaphore(1))
        self.rng = random.Random()
        self.mutex = Semaphore(1)
        self.rng.seed(100)

    def left(self, i):
        return i

    def right(self, i):
        return (i + 1) % self.num_philosophers

    def sleep(self):
        sleep(self.rng.random() / 1000)

    def get_forks(self, i):
        if i != 0:                             #Try to get right fork first
            self.forks[self.right(i)].acquire()
            self.forks[self.left(i)].acquire()
        else:                                  #One philosopher tries to get left fork first
            self.forks[self.left(i)].acquire()
            self.forks[self.right(i)].acquire()
        
    def put_forks(self, i):        
        self.forks[self.right(i)].release()
        self.forks[self.left(i)].release()
        
    def philosopher(self, id):
        while (self.num_meals > 0):
            self.get_forks(id)
            self.mutex.acquire()
            self.num_meals -= 1
            self.mutex.release()
            self.put_forks(id)
            self.sleep()

class Dining_philosopher_Tanenbaum(object):
    def __init__(self, num_philosophers, num_meals):
        self.num_philosophers = num_philosophers
        self.num_meals = num_meals
        self.state = ['thinking'] * self.num_philosophers
        self.sem = list()
        for i in xrange(self.num_philosophers):
            self.sem.append(Semaphore(0))
        self.rng = random.Random()
        self.mutex = Semaphore(1)
        self.mutex2 = Semaphore(1)
        self.rng.seed(100)

    def left(self, i):
        return (i + self.num_philosophers - 1) % self.num_philosophers

    def right(self, i):
        return (i + 1) % self.num_philosophers

    def sleep(self):
        sleep(self.rng.random() / 1000)

    def get_forks(self, i):
        self.mutex.acquire()
        self.state[i] = 'hungry'
        self.test(i)
        self.mutex.release()
        self.sem[i].acquire()
        
    def put_forks(self, i):     
        self.mutex.acquire()  
        self.state[i] = 'thinking'
        self.test(self.right(i))
        self.test(self.left(i))
        self.mutex.release()

    def test(self, i):
        if self.state[i] == 'hungry' and self.state[self.left(i)] != 'eating' and self.state[self.right(i)] != 'eating':
            self.state[i] = 'eating'
            self.sem[i].release()

    def philosopher(self, id):
        while (self.num_meals > 0):
            self.get_forks(id)
            self.mutex2.acquire()
            self.num_meals -= 1
            self.mutex2.release()
            self.put_forks(id)
            self.sleep()

def time_footman():
    dining_philosopher_footman = Dining_philosopher_footman(20, 1000)
    ts = list()
    for i in xrange(20):
        t = Thread(target=dining_philosopher_footman.philosopher, args=[i])
        ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()

if __name__ == '__main__':
    num_philosophers = 0
    num_meals = 0
    if len(sys.argv) > 1:
        num_philosophers = int(sys.argv[1])
        num_meals = int(sys.argv[2])        
    else:                                  # Default
        num_philosophers = 20
        num_meals = 1000
    start_time = datetime.datetime.now()
    dining_philosopher_footman = Dining_philosopher_footman(num_philosophers, num_meals)
    ts = list()
    for i in xrange(num_philosophers):
        t = Thread(target=dining_philosopher_footman.philosopher, args=[i])
        ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    
   # timer = Timer(time_footman)
    end_time = datetime.datetime.now()
    #print('1, Footman solution, time elapsed: {:0.3f}s'.format(timer.timeit()))
    print("The running time for the footman solution is:")
    print(end_time - start_time)
    print()

    start_time = datetime.datetime.now()
    dining_philosopher_lefthand = Dining_philosopher_lefthand(num_philosophers, num_meals)
    ts = list()
    for i in xrange(num_philosophers):
        t = Thread(target=dining_philosopher_lefthand.philosopher, args=[i])
        ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    
   
    end_time = datetime.datetime.now()
    
    print("The running time for the left-handed philosopher solution is:")
    print(end_time - start_time)
    print()

    start_time = datetime.datetime.now()
    dining_philosopher_Tanenbaum = Dining_philosopher_Tanenbaum(num_philosophers, num_meals)
    ts = list()
    for i in xrange(num_philosophers):
        t = Thread(target=dining_philosopher_Tanenbaum.philosopher, args=[i])
        ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    
   
    end_time = datetime.datetime.now()
    
    print("The running time for the Tanenbaum solution is:")
    print(end_time - start_time)
    print()
    
