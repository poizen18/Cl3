import threading
import random
import time
from pymongo import MongoClient

# create connection
'''
client = MongoClient()

client = MongoClient('localhost',27017)
db = client.test_database
db = client['test-database']
collection = db.test_collection
posts = db.posts




'''
#queue is actually a stack, will change the variable name later. 
myQueue = []
class Philosopher(threading.Thread):

    running = True
    global myQueue
    global posts
    def __init__(self,xname,forkOnLeft,forkOnRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight


    def run(self):
        while(self.running):
            if(len(myQueue)!=0):
                time.sleep(random.uniform(3,13))
                print '%s is hungry.' %self.name
                self.dine()
            else:
                print '%s has Nothing to eat.' %self.name
                self.running = False

    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight

        while self.running:
            f=fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break # lolwut
            fork1.release()
            print '%s swaps forks' % self.name
            fork1, fork2 = fork2,fork1
        else:
            return

        self.dinning()
        fork2.release()
        fork1.release()

    def dinning(self):
        try:
            self.kya_khara = myQueue.pop()
            print '%s starts eating ' % self.name, self.kya_khara, '\n'
            foo = {"Philosopher": self.name,
                   "Food Item" : self.kya_khara}
            time.sleep(random.uniform(1, 10))
            print '%s finishes eating and leaves to think' % self.name
            #try:
            #    post_id= posts.insert_one(foo).inserted_id
            #except:
            #    pass

        except IndexError:
            print '\n %s has nothing to Eat' %self.name
            self.running = False


def DiningPhilosophers():
    global myQueue
    forks = [threading.Lock() for n in range(5)]
    philosopherNames =('Chutiya','Bulla','Pappu Pager','Lamboo Aata','Ibu Hatela')

    foodItems = ('vadapav','meduvada','dosa','idli sambar','pohe with peas','samosa','burger','pizza')

    for i in range (random.randint(10,20)):
        myQueue.append(foodItems[random.randint(0,len(foodItems)-1)])
    print 'Food items available: ',myQueue

    philosophers = [Philosopher(philosopherNames[i],forks[i%5],forks[(i+1)%5]) for i in range(5)]

    random.seed(1200)
    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(60)
    Philosopher.running = False
    print 'Now we are finishing.'

DiningPhilosophers()

