import time
import sys
import os
import re

def num_file(dir_path):    
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def search(query, path):
    l = ""
    num = num_file(path+"/temp/")
    for i in range(1,num+1):
        f  = open(path+"/temp/d"+str(i)+".txt", 'r')
        for line in f.readlines():
            a, b = line.split(' ')
            if a==query :
                l+=b
                break
        f.close()
    return l

def extract(s):

    d = 0
    for i in range(1,len(s)):
        if ord(s[i])>=97 and ord(s[i])<=122:
            break          
        else:
            d = d*10 + ord(s[i])-48
        
    return d

def get_doc(i):

    if i%10000:
        fn = (i//10000)+1
    else:
        fn = i//10000 + 1
    
    f = open(path+"/title/title"+str(fn)+".txt", 'r')
    c = 0
    for j in f.readlines():
        c = c+1
        if c==i%10000:
            return j
        
    return -1

if __name__ == "__main__" :
    query = sys.argv[2]
    path = sys.argv[1]
    start = time.time()
    l = search(query, path)
    l = re.sub('\n', '', l)
    l = l.split('|')
    # print(l)
    x = []
    for i in l:
        x.append(get_doc(extract(i)))
    
    print("Total number of results found : ", len(x))
    if len(x)>10:
        x = x[:10]
    for i in x:
        if i!=-1:
            print(i, end='')
    print("Searching time : ", time.time()-start)