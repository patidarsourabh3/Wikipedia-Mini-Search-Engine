totfiles = 0
import os
# def fileSplit():
#     lines = []
#     filecount = 0
#     threshold=10000
#     f = open(file_to_split, 'r')
#     sec = open(secondary_index_file, 'w')
#     line = f.readline().strip("\n")
#     while line:
#         word = line.split(' ')[0]
#         if not (word[0:7].isdecimal() and len(word)>10 ):
#             lines.append(line)
#         if len(lines) % threshold == 0 and lines != [] :
#             sec.write(lines[0].split(" ")[0] + '\n')
#             writ = open('/home/patidar/Desktop/temp/fin'+str(filecount+1)+'.txt', 'w')
#             for l in lines:
#                 writ.write(l + '\n')
#             filecount += 1
#             lines = []
#         line = file.readline().strip("\n")
        
#     if len(lines) > 0:
#         sec.write(lines[0].split(" ")[0] + '\n')
#         writ = open('/home/patidar/Desktop/temp/fin'+str(filecount+1)+'.txt', 'w')
#         for l in lines:
#             writ.write(l + '\n')
#         filecount += 1
#         lines = []
#     #os.remove('./10inddir/full.txt')
#     file.close()
#     sec.close()
#     return filecount
    
    
def splitFile(file_to_split, secondary_index_file, path, threshold ):
    f = open(file_to_split, 'r')
    secondary_index = open(secondary_index_file, 'w')
    lines = []
    file_counter = 1
    line = f.readline()
        
    while line:
        lines.append(line)
        if len(lines) == threshold:
            word = lines[0].split(" ")
            secondary_index.write(word[0]+"\n")
            f_temp = open(path+"f"+str(file_counter)+".txt", 'w')
            for i in lines:
                f_temp.write(i)
            lines = []
            f_temp.close()
            print("File Completed : ", file_counter)
            file_counter += 1
        line = f.readline()
        
        
    
    if len(lines) > 0:
        word = lines[0].split(" ")
        secondary_index.write(word[0]+"\n")
        f_temp = open(path+"f"+str(file_counter)+".txt", 'w')
        for i in lines:
            f_temp.write(i)
        lines = []
        f_temp.close()
        file_counter += 1 

        
    secondary_index.close()
    f.close()
    print("Total files are : ",file_counter)
        
    		
	
file_to_split = "/home/patidar/temp/d1.txt"
secondary_index_file = "/home/patidar/temp/secondary_index.txt"
path = "/home/patidar/temp/"
threshold = 10000
splitFile(file_to_split, secondary_index_file, path, threshold)




