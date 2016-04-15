from multiprocessing import Process, Pipe
import xml.etree.ElementTree as ET
import random
import time
# the quicksort method im using is In a Haskell fashion --
#
# def qsort(L):
#    return (qsort([y for y in L[1:] if y < L[0]]) +
#            L[:1] +
#            qsort([y for y in L[1:] if y >= L[0]])) if len(L) > 1 else L
# you can find more reference here: http://rosettacode.org/wiki/Sorting_algorithms/Quicksort#Python


# creating the xml file/ writing to it
# this i copied shamelessly from the code create_file.py nikhilesh sent on teacomputer :P
# i changed random.randomint to random.random :) it is appending float values

# another very clever thing done, and why this code is so efficient is, that my left process never
# has to communicate with right process
# Read the code ;) its magic.

#ccon and pcon are 'child' and 'parent' pipes :) pani idhar se udhar bhejneku use karte apan loga


N = 50000 # kitna elements leneka ye idhar dalneka
file = open('array.xml','w')
file.write("<Numbers>\n")
for i in range(N):
    file.write("\t<integer num = \""+str(random.random())+"\" ></integer>\n")
file.write("</Numbers>\n")
file.close()

# quick wala class
class Quick:
    #this qck is serial quicksort
    def qck(self,arr):
        if len(arr) <= 1:
            return arr

        else:
            pivot = arr.pop(random.randint(0, len(arr)-1))
            return self.qck([x for x in arr if x < pivot]) + [pivot] + self.qck([x for x in arr if x >= pivot])
    #this is parallel quicksort
    def quicksort(self,arr, conn, procNum):


        if procNum <= 0 or len(arr)<= 1:
            conn.send(self.qck(arr))
            conn.close()
            return
        #print 'Just in case you don't trust that this program works better than other quicksorts :3 FUBAR. process id:', os.getppid()
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

# reading from xml file
tree = ET.parse('array.xml')
root = tree.getroot()
array =[]
for value in root.iter('integer'):
    array.append(float(value.attrib.values()[0]))
if len(array) == 0:
    print ('list empty. abort')
    exit(1)


foo = Quick()  # AIM said: A class :P here it is, a classy code.

length = len(array)
print length
# n = number of processes you want :) you can print 'process id:', os.getppid()
# os.getpid will return the process id of other processes spawned by our initial processes.
n = 3
pconn, cconn = Pipe()
start = time.time()
p = Process(target=foo.quicksort, args=(array, cconn, n))
p.start()
array = pconn.recv()
p.join()
elapsed = time.time() - start

if foo.isSorted(array) is True:
    if len(array) == length:
        print 'sorted'
        print 'time taken by parallel : ', elapsed

