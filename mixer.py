from __future__ import print_function
from time import sleep
from threading import Semaphore, Thread
from collections import deque
import random
import sys

class Mixer:

    def __init__(self, num_leader, num_follower):
        self.num_leader = num_leader
        self.num_follower = num_follower
        self.leader_q = deque()
        self.follower_q = deque()
        for i in xrange(num_leader):
            self.leader_q.appendleft(i)
        for i in xrange(num_follower):
            self.follower_q.appendleft(i)
        self.switch_music1 = 0
        self.switch_music2 = 0
        self.switch_need = Semaphore(0)
        self.switch_complete = Semaphore(0)
        self.leader_arrived = Semaphore(0)
        self.follower_arrived = Semaphore(0)
        self.mutex = Semaphore(1)
        self.mutex1 = Semaphore(1)
        self.mutex2 = Semaphore(1)
        self.mutex11 = Semaphore(1)
        self.mutex22 = Semaphore(1)
        self.waiting_follower = -1
        self.rng = random.Random()
        self.rng.seed(100)

    def band_leader(self):
        previous = None
        i = 0
        songs = ['waltz', 'tango', 'foxtrot']
        while(True):
            self.switch_need.acquire()
            music = songs[i%3]
            if previous == None:
                while(len(self.leader_q) != self.num_leader and len(self.follower_q) != self.num_follower):
                    sleep(0.1)
                print('** Band leader starts playing {:>5s} **'.format(music))
                previous = music
                self.switch_music1 = 5
                self.switch_music2 = 5
            else:
                while(len(self.leader_q) != self.num_leader and len(self.follower_q) != self.num_follower):
                    sleep(0.1)
                print('** Band leader stops playing {:>5s} **'.format(previous))
                print('** Band leader starts playing {:>5s} **'.format(music))
                previous = music
                self.switch_music1 = 5
                self.switch_music2 = 5
            i += 1   
            self.switch_complete.release()

    def leader(self):
        while(True):
            self.mutex1.acquire()
            
            if self.switch_music1 <= 0:
                self.mutex.acquire()
                if self.switch_music1 <= 0:
                    self.switch_need.release()
                    self.switch_complete.acquire()
                self.mutex.release()
            self.switch_music1 -= 1
            self.mutex1.release()
            

            while (len(self.leader_q) == 0):
                sleep(0.1)
            self.mutex11.acquire()
            
            id = self.leader_q.pop()
            print('Leader {:2d} entering floor.'.format(id))                       #............
            self.leader_arrived.release()
            self.follower_arrived.acquire()
            partner = -1
            while(self.waiting_follower == -1):
                sleep(0.1)
            partner = self.waiting_follower
            print('Leader {:2d} and follower {:2d} are dancing.'.format(id, partner))                      #.............
            self.waiting_follower = -1
            self.mutex11.release()
            
            self.sleep()
            self.mutex11.acquire()
            self.leader_q.appendleft(id)
            print('Leader {:2d} getting back in line.'.format(id))                      #................
            self.mutex11.release()

    def follower(self):
        while(True):
            self.mutex2.acquire()
            
            if self.switch_music2 <= 0:
                self.mutex.acquire()
                if self.switch_music2 <= 0:
                    self.switch_need.release()
                    self.switch_complete.acquire()
                self.mutex.release()
            self.switch_music2 -= 1
            self.mutex2.release()

            while (len(self.follower_q) == 0):
                sleep(0.1)
            self.mutex22.acquire()
            
            id = self.follower_q.pop()
            print('Follower {:2d} entering floor.'.format(id))                       #............
            self.follower_arrived.release()
            self.leader_arrived.acquire()
            self.waiting_follower = id
            while(self.waiting_follower != -1):
                sleep(0.1)
            self.mutex22.release()
            self.sleep()
            self.mutex22.acquire()
            self.follower_q.appendleft(id)
            print('Follower {:2d} getting back in line.'.format(id))                      #................
            self.mutex22.release()

    def sleep(self):
        sleep(15 * self.rng.random())

if __name__ == '__main__':
    num_leader = 0
    num_follower = 0
    ts = list()
    if len(sys.argv) > 1:
        num_leader = int(sys.argv[1])
        num_follower = int(sys.argv[2])        
    else:                                  # Default
        num_leader = 2
        num_follower = 5
    mixer = Mixer(num_leader, num_follower)
    for i in xrange(num_leader):
        t = Thread(target=mixer.leader, args=[])
        ts.append(t)
    for i in xrange(num_follower):
        t = Thread(target=mixer.follower, args=[])
        ts.append(t)
    t = Thread(target=mixer.band_leader, args=[])
    ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()

