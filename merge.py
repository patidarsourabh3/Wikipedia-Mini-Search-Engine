import os
import split
import time

path = "/home/patidar/temp/"

def mergeFiles(file1, file2, res):

    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    output_file = open("temp.txt", 'w')
    
    s1 = f1.readline()
    s2 = f2.readline()

    while s1 and s2:

        k1,v1 = s1.split(" ")
        k2,v2 = s2.split(" ")
        if k1 < k2:
            output_file.write(s1)
            s1 = f1.readline()
        elif k1 > k2:
            output_file.write(s2)
            s2 = f2.readline()
        else:
            v1 = v1.strip("\n")
            output_file.write(k1+" "+v1+v2)
            s1 = f1.readline()
            s2 = f2.readline()

    while s1:
        output_file.write(s1)
        s1 = f1.readline()
    
    while s2:
        output_file.write(s2)
        s2 = f2.readline()
    
    f1.close()
    f2.close()
    output_file.close()
    os.remove(file1)
    os.remove(file2)
    os.rename("temp.txt", res)

    print("Files "+ file1 + " and " + file2 + " merged into "+ res)
    print("Time taken : " ,time.time()-s , "seconds")
    print()

dir_list = os.listdir(path)
s = time.time()
# dir_list.sort()
total_files = len(dir_list)
while total_files !=1:
    if total_files % 2==0:
        for i in range(1,total_files,2):
            mergeFiles(path+"d"+str(i)+".txt", path+"d"+str(i+1)+".txt", path+"d"+str((i+1)//2)+".txt")
    else:
        for i in range(1,total_files-1,2):
            mergeFiles(path+"d"+str(i)+".txt", path+"d"+str(i+1)+".txt", path+"d"+str((i+1)//2)+".txt")
        os.rename(path+"d"+str(total_files)+".txt", path+"d"+str((total_files+1)//2)+".txt")
    dir_list = os.listdir(path)
    total_files = len(dir_list)
    print("Files remaining : " , total_files)


# fname = 1
# while len(dir_list) != 1:
#     if len(dir_list)%2 ==0 :
#         for i in range(0,len(dir_list),2):
#             mergeFiles(path+dir_list[i], path+dir_list[i+1], path+str(fname)+"_"+str(i//2)+".txt")
#     else:
#         for i in range(0,len(dir_list)-1,2):
#             mergeFiles(path+dir_list[i], path+dir_list[i+1], path+str(fname)+"_"+str(i//2)+".txt")
#         os.rename(path+dir_list[len(dir_list)-1],path+str(fname)+"_"+str(len(dir_list)//2)+".txt")
#     fname = fname + 1
#     dir_list = os.listdir(path)
#     dir_list.sort()

# print("Total time taken in merging : ", time.time()-start," seconds")
# # totfiles = split.fileSplit()

# # print("Total number of files are : ", totfiles)
# # print("Total time taken : ", time.time()-start," seconds")
