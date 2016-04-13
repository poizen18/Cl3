from multiprocessing import Process, Pipe
import xml.etree.ElementTree as ET
import random
import time
# pconn = parent connection, cconn = child connection
# when you start new process the child process inherits the pipes of parents
# but when child closes conn the parent still has child connection open
# bug: sometimes when pivot is selected as -1 ,
# the list drops some elements:
# TODO: add extra statement after selecting pivot, to check if its negative,
# TODO: if it is, take pivot again
# the code is easy to understand and if elements are very high, say N=100000
# code is very fast.

class Quick:
    def qck(self,arr):
        if len(arr) <= 1:
            return arr
        pivot = arr.pop(random.randint(0, len(arr)-1))
        return self.qck([x for x in arr if x < pivot]) + [pivot] + self.qck([x for x in arr if x >= pivot])


    def quicksort(self,arr, conn, procNum):
        if procNum <= 0 or len(arr) <= 1:
            conn.send(self.qck(arr))
            conn.close()
            return

        pivot = arr.pop(random.randint(0, len(arr)-1))
        leftSide = [x for x in arr if x < pivot]
        rightSide = [x for x in arr if x > pivot]

        pconnLeft, cconnLeft = Pipe()

        leftProc = Process(target= self.quicksort, args=(leftSide, cconnLeft,procNum -1))

        pconnRight, cconnRight = Pipe()

        rightProc = Process(target=self.quicksort, args=(rightSide, cconnRight, procNum - 1))

        leftProc.start()
        rightProc.start()

        conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
        conn.close()

        leftProc.join()
        rightProc.join()


    def isSorted(self,arr):
        for i in range (1, len(arr)):
            if arr[i]<arr[i-1]:
                return False
        return True


# try to add more elements to the xml doc. more the elements, faster the code will be from serial code
tree = ET.parse('array.xml')
root = tree.getroot()
array =[]
for i in root.itertext():
    i = i.strip()
    if i != '':
        array.append(int(i))
if len(array) == 0:
    print 'list empty. abort'
    exit(1)

foolist = list(array)
length = len(foolist)
print 'length of array is: ', length

foo = Quick()  # AIM said: A class :P here it is, a classy code.
#N = 500000
#foolist = [random.random() for x in range(N)]

n = 4
pconn, cconn = Pipe()
start = time.time()
p = Process(target=foo.quicksort, args=(foolist, cconn, n))
p.start()
foolist = pconn.recv()
p.join()
elapsed = time.time() - start

print 'time taken by parallel : ', elapsed

if foo.isSorted(foolist) is True:
    if len(foolist) == length:
        print 'sorted with ', len(foolist),'\n',foolist
    else:
        print 'SORTED but kuch toh giraya. ', len(foolist)


'''
start = time.time()
boo = qck(foolist2)
elapsedserial = time.time() - start
print 'serial took: ', elapsedserial

if(elapsedserial < elapsed):
    print 'serial code is faster bro by: ',elapsed-elapsedserial
else:
    print 'parallel is faster than serial by: ',elapsedserial - elapsed
'''
