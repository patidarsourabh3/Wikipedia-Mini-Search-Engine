import time
from collections import defaultdict
import re
import sys
from Stemmer import Stemmer
stemmer = Stemmer('porter')
stop_words = defaultdict()
path = "/home/patidar/"

def stopwords_dict():
    global stop_words
    with open ('stopwords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stop_words[i]=1


def pre_process_query(query):
    query = re.split(r'[^A-Za-z0-9]+', query)
    tokens = []
    for line in query:
        word = stemmer.stemWord(line)
        if len(word) > 1 and len(word) < 15 and word not in stop_words:
            tokens.append(word)
    return tokens


def extract(s):

    ans = {}
    d = 0
    c = -1
    for i in range(0,len(s)):
        if ord(s[i])>=97 and ord(s[i])<=122:
            if c!=-1:
                ans[c] = d 
                d = 0   
            c = s[i]
        else:
            d = d*10 + ord(s[i])-48
    ans[c] = d

    return ans


def get_doc_name(i):

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


def calcScore(data):
    score = 0
    tags = ['t','b','c','r','l','i']
    weights = {}
    weights['t']= 50
    weights['b']= 5
    weights['c']= 10
    weights['r']= 10
    weights['l']= 10
    weights['i']= 25
    
    for i in tags:
        if i in data:
            score += data[i] * weights[i]
    if 'd' in data:
        return data['d'], score

    return -1,-1


def calcScoreField(data, k):
    score = 0
    tags = ['t','b','c','r','l','i']
    weights = {}
    weights['t']= 50
    weights['b']= 5
    weights['c']= 10
    weights['r']= 10
    weights['l']= 10
    weights['i']= 25
    
    if k in data:
        score += data[k] * weights[k]
    if 'd' in data:
        return data['d'], score

    return -1,-1


def extractDetails(d,k='a',field=False):

    s = set()
    scores = {}
    d = d.split("|")
    for word in d:
        data = extract(word)
        if field:
            doc_num, score = calcScoreField(data, k)
        else:
            doc_num, score = calcScore(data)
        if doc_num !=1:
            scores[doc_num] = score
            s.add(doc_num)
    
    return s, scores


def find_file_num(word, secondary_query_list):

    i = 0
    j = len(secondary_query_list)-1
    while i<j:

        mid = (i+j)//2
        if secondary_query_list[mid] <= word:
            i = mid+1
        elif secondary_query_list[mid] > word:
            j = mid

    return i


def normal_query(query):
    query = pre_process_query(query)
    l = {}
    sets = []
    for i in range(len(query)):
        fno = find_file_num(query[i], secondary_query_list)
        f  = open(path+"/temp/f"+str(fno)+".txt", 'r')
        for line in f.readlines():
            a, b = line.split(" ")
            if a==query[i]:
                s, ans = extractDetails(b)
                sets.append(s)
                l[a] = ans 
                break
        f.close()

    if len(sets)>0:
        final_set = sets[0]
    for i in range(1, len(sets)):
        final_set = final_set.intersection(sets[i])

    score_dict = {}
    for i in range(len(query)):
        for j in final_set:
            if j!=-1:
                if j in score_dict:
                    score_dict[j] += l[query[i]][j]
                else:
                    score_dict[j] = l[query[i]][j]

    ans = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    
    return ans


def field_query(query):

    query_d = {}
    query = query.split(":")
    c = query[0]
    for i in range(1,len(query)):
        if i!= len(query)-1:
            query_d[c] = (query[i])[0:len(query[i])-2]
            c = (query[i])[len(query[i])-1]
        else:
            query_d[c] = query[i]
    
    # print(query_d)
    l = {}
    sets = []    
    final_set = []
    for k,v in query_d.items():    
        v = pre_process_query(v)
        # print(v)
        for i in range(len(v)):
            fno = find_file_num(v[i], secondary_query_list)
            f  = open(path+"/temp/f"+str(fno)+".txt", 'r')
            for line in f.readlines():
                a, b = line.split(" ")
                if a==v[i]:
                    # print(a)
                    s, ans = extractDetails(b,k,True)
                    sets.append(s)
                    l[a] = ans 
                    break
            f.close()
        # print(sets)

    if len(sets)>0:
        final_set = sets[0]
    for i in range(1, len(sets)):
        final_set = final_set.intersection(sets[i])

    score_dict = {}
    for i in range(len(v)):
        for j in final_set:
            if j!=-1:
                if j in score_dict:
                    score_dict[j] += l[v[i]][j]
                else:
                    score_dict[j] = l[v[i]][j]

    ans = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    return ans
    

if __name__ == '__main__':
    query_file = sys.argv[1] 
    stopwords_dict()
    sec = open(path+"/temp/secondary_index.txt",'r')
    secondary_query_list = []
    for i in sec.readlines():
        secondary_query_list.append(i.strip("\n"))
    sec.close()
    queries = open(path+query_file,'r')
    ans_file = open(path+"queries_op.txt",'w')
    for query in queries.readlines():
        start = time.time()
        query = query.lower()
        if 't:' in query or 'i:' in query or 'b:' in query or 'c:' in query or 'r:' in query or 'l:' in query:
            ans = field_query(query)
        else:
            ans = normal_query(query)
        c = 0
        for i in ans:
            ans_file.write(str(i[0])+", "+get_doc_name(i[0]).lower())
            c+=1
            if c==10:
                break
        
        ans_file.write(str(time.time()-start)+"\n\n")
        
    queries.close()
    ans_file.close()