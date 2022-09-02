import re
from collections import defaultdict
from nltk.corpus import stopwords
from Stemmer import Stemmer

stop_words = set()
f = open("stopwords.txt", 'r')
for line in f.readlines():
    stop_words.update(line)
f.close()

word_dict = defaultdict(dict)
stemmer = Stemmer('porter')


def tokenize(text):
    text = re.split(r'[^A-Za-z0-9]+', text)
    tokens = []
    print(stop_words)
    for line in text:
        word = stemmer.stemWord(line)
        print(word)
        if len(word) > 1 and len(word) < 15 and word not in stop_words:
            tokens.append(word)
    return tokens
    

def extractInfobox(text):

    st_pattern = re.compile(r'\{infobox')
    end_pattern = re.compile(r'\}\}\n(\w|\'|\n)')
    infobox = st_pattern.split(text)
    infobox_l = []
    infobox_list = []
    if len(infobox):
        for ele in infobox[1:]:
            data = end_pattern.split(ele)[0]
            text = text.replace(data, '')
            infobox_list.append(data)
        for ele in infobox_list:
            for line in ele.split('\n'):
                if len(line) and line[0] == '|':
                    value = line.split("=")
                    if len(value) > 1:
                        value = tokenize(value[1])
                        infobox_l += value
    
    
    return text, infobox_l


def extractCategories(text):
    pattern = re.compile(r"\[\[category:(.*)\]\]")
    cat = pattern.findall(text)
    text = pattern.sub('', text)
    categories = []
    for line in cat:
    	categories += tokenize(line)
    
    return text, categories


def extractReferences(text):
    pattern = re.compile(r'==references==|== references ==|== references==|==references ==')
    ref = pattern.split(text)
    refer = []
    if len(ref)>1:
        ref = ref[1].split('\n')
        for sent in ref[2:]:
            if len(sent) and sent[0] !='*':
                break
            if len(sent):
                sent = re.sub(r'http\S+', '', sent)
                refer += tokenize(sent)
                text = text.replace(sent,'')
    
      
    return text, refer


def extractLinks(text):
    pattern = re.compile(r'==external links==|== external links ==|== external links==|==external links ==')
    link = pattern.split(text)
    links = []
    if len(link)>1:
        link = link[1].split('\n')
        for sent in link[2:]:
            if len(sent) and sent[0] !='*':
                break
            if len(sent):
                sent = re.sub(r'http\S+', '', sent)
                links += tokenize(sent)
                text = text.replace(sent,'')
            
    return text, links


def extractBody(text):
    text = re.sub(r'http\S+', '', text) 
    text = text[0:int(len(text)*0.45)]
    body = []
    for sent in text.split('\n'):
        body += tokenize(sent)
    return body


def processTitle(title):
    title = title.lower()
    title = tokenize(title)
    
    return title


def processText(title,text, doc):

    global unique_words, total_tokens
    title = processTitle(title)
    text = text.lower()
    text, infobox = extractInfobox(text)
    text, categories = extractCategories(text)
    text, references = extractReferences(text)
    text, links = extractLinks(text)
    body = extractBody(text)

    return title, body, references, categories, links, infobox