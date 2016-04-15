import threading
import random
import time
from pymongo import MongoClient
# TODO : USE SIMULATOR TO GATHER DATA VIA WSN
# create connection

client = MongoClient()

client = MongoClient('localhost',27017)
db = client.test_database
db = client['philosopher']
collection = db.test_collection
posts = db.posts


myStack = []
class Philosopher(threading.Thread):

    running = True
    global myStack
    global posts
    def __init__(self,xname,forkOnLeft,forkOnRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight


    def run(self):
        while(self.running):
            if(len(myStack)!=0):
                time.sleep(random.uniform(3,13))
                print '\n%s is hungry.' %self.name
                self.dine()
            else:
                print '\n%s has Nothing to eat.' %self.name
                self.running = False

    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight

        while self.running:
            f=fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break # lolwut
            fork1.release()
            print '\n%s swaps forks' % self.name
            fork1, fork2 = fork2,fork1
        else:
            return

        self.dinning()
        fork2.release()
        fork1.release()

    def dinning(self):
        try:
            self.kya_khara = myStack.pop()
            print '\n%s starts eating ' % self.name, self.kya_khara, '\n'
            foo = {"Philosopher": self.name,
                   "Food Item" : self.kya_khara}
            time.sleep(random.uniform(1, 10))
            print '\n%s finishes eating and leaves to think' % self.name
            try:
                posts.insert_one(foo).inserted_id
                #print post_id
            except:
                print '##################################### DB ERROR '
                pass

        except IndexError:
            print '\n%s has nothing to Eat' %self.name
            self.running = False


def DiningPhilosophers():
    global myStack
    forks = [threading.Lock() for n in range(5)]
    philosopherNames =('Chutiya','Bulla','Pappu Pager','Lamboo Aata','Ibu Hatela')

    foodItems = ('vadapav','meduvada','dosa','idli sambar','pohe with peas','samosa','burger','pizza')

    for i in range (random.randint(10,20)):
        myStack.append(foodItems[random.randint(0,len(foodItems)-1)])
    print '\nFood items available: ',myStack

    philosophers = [Philosopher(philosopherNames[i],forks[i%5],forks[(i+1)%5]) for i in range(5)]

    random.seed(1200)
    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(60)
    Philosopher.running = False
    print '\nNow we are finishing.'

DiningPhilosophers()

