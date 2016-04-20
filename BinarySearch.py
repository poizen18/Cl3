import math
f = open ('array.txt','r')
f = f.readlines()
array = []
for i in range (len(f)):
    if not f[i] =='':
        try:
            number = int(f[i].strip())
            array.append(number)
        except ValueError:
            pass

array.sort()
print array
key = input("\n\nenter the value you want to search :")
try:
    key = int(key)
except ValueError:
    print 'enter an integer, Exiting.'
    exit(1)
print 'key entered is: ', key


def binarysearch(arr,low,high):
    global key
    mid = int(math.ceil(low+high/2))
    if (arr[mid]==key):
        print '\n', key, ' found at index ', mid+1

    else:
        if key<arr[mid]: binarysearch(arr,0,mid-1)
        if key>arr[mid]: binarysearch(arr,mid+1,high)




binarysearch(array,0,len(array)-1)
