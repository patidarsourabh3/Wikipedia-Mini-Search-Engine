import xml.sax
import sys
import os
import time
from pre_processing import processText
from collections import defaultdict, OrderedDict 

word_dict = defaultdict(dict)
title_list = ""
tf_list = ""
doc = 0
total_tokens = 0
title_doc_size = 10000
unique_words = set()
dict_size = 10000
total_tokens = 0
path = ""
s = 0

def write_title(title_list):
	global doc,title_doc_size, path
	if doc%title_doc_size==0:
		f = open(path+"/title/title"+str(doc//title_doc_size)+".txt", 'w')
	else:
		f = open(path+"/title/title"+str((doc//title_doc_size)+1)+".txt", 'w')
	f.write(title_list)
	f.close()

def write_tf(tf_list):
	global doc,title_doc_size, path
	if doc%title_doc_size==0:
		f = open(path+"/tf/tf"+str(doc//title_doc_size)+".txt", 'w')
	else:
		f = open(path+"/tf/tf"+str((doc//title_doc_size)+1)+".txt", 'w')
	f.write(tf_list)
	f.close()

def makeIndex(title, body, references, categories, links, infobox):
    
    global word_dict, doc
    for i in title:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [1,0,0,0,0,0]
        else:
        	word_dict[i][doc][0] += 1
            
    for i in body:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [0,1,0,0,0,0]
        else:
        	word_dict[i][doc][1] += 1

    for i in references:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [0,0,1,0,0,0]
        else:
        	word_dict[i][doc][2] += 1

    for i in categories:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [0,0,0,1,0,0]
        else:
        	word_dict[i][doc][3] += 1

    for i in links:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [0,0,0,0,1,0]
        else:
        	word_dict[i][doc][4] += 1
    
    for i in infobox:
        if not (i in word_dict and doc in word_dict[i]):
        	word_dict[i][doc] = [0,0,0,0,0,1]
        else:
        	word_dict[i][doc][5] += 1

    if doc%dict_size == 0:
        createIndex()
        word_dict = defaultdict(dict)


def createIndex():

    global total_tokens, doc, word_dict
    if doc%dict_size ==0:
        f = open(path+"/temp/d"+(str(doc//dict_size))+".txt", 'w')
    else:
        f = open(path+"/temp/d"+(str((doc//dict_size)+1))+".txt", 'w')
    tags = ['t','b','r','c','l','i']
    word_dict = OrderedDict(sorted(word_dict.items()))
    for k,v in word_dict.items():
        st = ""
        if len(v) > 10000:
            continue
        else:
            for k1, v1 in v.items():
                st += "d" + str(k1)
                for i in range(6):
                    if v1[i]:
                        st += tags[i] + str(v1[i])
                st += '|'
            f.write(str(k)+" "+st+"\n")
    
    f.close()


class WikiHandler(xml.sax.ContentHandler):
	
	global word_dict
	def __init__(self):
		self.title = ''
		self.title_flag = ''
		self.text = ''
		self.text_flag = ''
		
	def startElement(self, tag, attributes):
		if tag=="title":
			self.title_flag = 1 
			self.title = ""
		if tag=="text":
			self.text = ""
			self.text_flag = 1
		
	def characters(self, content):
		if self.title_flag == 1:
			self.title += content
		if self.text_flag == 1:
			self.text += content

	def endElement(self, tag):
		global title_list, tf_list, doc, total_tokens, unique_words, s
		if tag=="title":
			self.title_flag = 0
			title_list += self.title + "\n"
		if tag=="text":
			self.text_flag = 0
			doc += 1
			title, body, references, categories, links, infobox = processText(self.title, self.text, doc)
			makeIndex(title, body, references, categories, links, infobox)
			
			total_tokens += len(title)
			total_tokens += len(body)
			total_tokens += len(links)
			total_tokens += len(infobox)
			total_tokens += len(references)
			total_tokens += len(categories)
			doc_freq = len(title) + len(body) + len(links) + len(infobox) + len(references) + len(categories)
			tf_list += str(doc_freq) + "\n"

			# fi.write(str(doc_freq)+"\n")
			unique_words.update(title)
			unique_words.update(body)
			unique_words.update(links)
			unique_words.update(infobox)
			unique_words.update(references)      
			unique_words.update(categories)

			if doc%title_doc_size == 0:
				# print(time.time()-s)
				print(doc ," docs done : ", time.time()-s , " seconds")
				# s = time.time()
				write_title(title_list)
				write_tf(tf_list)
				title_list = ""
				tf_list = ""
			

if __name__ == "__main__" :
	
	path_dump = sys.argv[1]
	path_inverted_index = sys.argv[2]
	stat_file = sys.argv[3]
	if not os.path.exists(path_inverted_index):
		os.makedirs(path_inverted_index)
	
	path = path_inverted_index
	if not os.path.exists(path_inverted_index+"/temp"):
		os.makedirs(path_inverted_index+"/temp")
	if not os.path.exists(path_inverted_index+"/title"):
		os.makedirs(path_inverted_index+"/title")

	if not os.path.exists(path_inverted_index+"/tf"):
		os.makedirs(path_inverted_index+"/tf")



	start = time.time()
	s = start
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	
	Handler = WikiHandler()
	parser.setContentHandler( Handler )
	parser.parse(path_dump)
	write_title(title_list)
	write_tf(tf_list)
	createIndex()

	end = time.time()
	print("Time taken for indexing : ", end-start, " seconds")
	# fi.close()
	print("Total tokens : " , total_tokens)
	print("Total unique tokens : ", len(unique_words))
	f = open(stat_file, 'w')
	f.write(str(total_tokens)+"\n"+ str(len(unique_words)))
	f.close()
