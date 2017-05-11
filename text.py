import os
import nltk
from collections import Counter
#nltk.download()
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import collections
import operator
import math
from math import sqrt


global tokens
global tf_dict
global idf_dict
global tf_list
global tf_idf_list
global file_list
global normalized_tf_idf
global normalized_query
global tfwt_list

corpusroot = './presidential_debates'

def tokenize():
    global tokens
    global tf_list
    global file_list
    global normalized_tf_idf
    corpusroot = './presidential_debates'
    st=list()
    tf_list=list()
    file_list=list()
    for filename in os.listdir(corpusroot):
        file_list.append(filename)
        file = open(os.path.join(corpusroot, filename), "r",encoding='UTF-8')   #opening the file
        doc = file.read()
        file.close()
        doc = doc.lower()
        d=doc.split()
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        tokens = tokenizer.tokenize(doc)                                        #tokenize
        for each in tokens[:]:
            if each in nltk.corpus.stopwords.words("english"):
                tokens.remove(each)                                             #stopwards removal
        stemmer=PorterStemmer()
        stem_out=[]
        global stem_out
        for t in tokens[:]:
            stem_out.append(stemmer.stem(t))
        st.append(stem_out)
        l=dict(collections.Counter(stem_out))#http://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item-in-python
        tf_list.append(l)
    #print(tf_list)

    global l_file
    l_file= len(file_list)
    tfwt_list=list()
    global tfwt_list
    for one in tf_list:
        tf_dict=dict()
        for o in one:
            tf=((1+math.log10(one[o]))) #calculating term-frequency
            tf_dict[o]=tf
        tfwt_list.append(tf_dict)
    #print(tfwt_list)


    unique_dict=dict()
    complete_list=list()
    complete_list.append('')
    for i in range(0,len(st)):
        complete_list += st[i]
        global unique_dict
    complete_list.pop(0)
    unique_word_list = list(set(complete_list))
    for unique_word in unique_word_list:
        for doc_list in st:
            if unique_word in doc_list:
                if unique_word in unique_dict.keys():
                    unique_dict[unique_word] = unique_dict[unique_word] + 1
                else:
                    unique_dict[unique_word] = 1
    #print(unique_dict)

#def getidf(tokens):                                    #function getidf(token)
    idf_list = list()
    idf_dict = dict()
    global idf_dict
    for token in unique_dict:
        if token in unique_dict:
            idf = math.log10(l_file / unique_dict[token]) #calculating inverse document frequency
            idf_dict[token] = idf
            idf_list.append(idf_dict)
    #print(idf_list)
 #           return idf_dict[tokens]
  #      else:
   #         return -1

    #global tf_idf_dict
    #getidf(each)


#def getweight(filename,token):                        #function getweight(filename,token)
    tf_idf_list=list()
    global tf_idf_list
    for each in tfwt_list:
        #print(tfwt_list)
        #print(each)
        tf_idf_dict = dict()
        global tf_idf_dict
        for e in each:
            global idf_dict
            if e in idf_dict:
                tf_idf=each[e]*idf_dict[e]            #calculating weight of each term in a document

            tf_idf_dict[e]=tf_idf
            #print(tf_idf_dict)
        tf_idf_list.append(tf_idf_dict)
        #return tf_idf_dict[e]
    #else:
     #   return 0

    #print(tf_idf_list)
#getweight("a","gunjan")
tokenize()
def normalize():
    global normalized_tf_idf
    normalized_tf_idf = []
    for each in tf_idf_list:
        sums=0

        for item in each:
            sums=sums+((each[item])**2)                #length normalizing the tf-idf weights
        sums=sqrt(sums)
        norm_temp={}
        for tok in each:
            global normalized_tf_idf
            norm=each[tok]/sums
            norm_temp[tok]=norm
        normalized_tf_idf.append(norm_temp)
    #print (normalized_tf_idf)
normalize()

def getweight(filename,token):
    token_index = file_list.index(filename) #http://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
    doc_dic = normalized_tf_idf[token_index]
    print(doc_dic[token])
getweight("1976-10-22.txt","agenda")



tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
q_st=list()
q_list=list()
global qtf_dict
global normalized_query

def query(qstring):                                     #function query(string)
    global qtf_dict
    global normalized_query
    qstring=''.join(qstring)
    q=qstring.lower()
    q_tokens=tokenizer.tokenize(q)
    for s in q_tokens[:]:
        if s in nltk.corpus.stopwords.words("english"):
            q_tokens.remove(s)
    stemmer = PorterStemmer()
    q_stem_out =list()
    global q_stem_out
    for t in q_tokens[:]:
        q_stem_out.append(stemmer.stem(t))
    l = dict(collections.Counter(q_stem_out))
    q_list.append(l)
    for one in q_list:
        qtf_dict = dict()
        for o in one:

            q_tf = ((1 + math.log10(one[o])))
            qtf_dict[o] = q_tf
    #print(qtf_dict)

    sums_q=0
    for item in qtf_dict:
        sums_q=sums_q+((qtf_dict[item])**2)
    sums_q=sqrt(sums_q)
    normalized_query={}
    for tok in qtf_dict:
        norm=qtf_dict[tok]/sums_q
        normalized_query[tok]=norm
    #print (normalized_query)
qstring=input("terror attack")
query(qstring)

#creating PostingsList for each token
post_list = dict()
postingsList=dict()
all_file_stem={}
for e in file_list:
    # print(e)
    f = open(os.path.join(corpusroot, e), "r", encoding='UTF-8')
    d = f.read().split()
    stemmer = PorterStemmer()
    stem = []
    for t in d[:]:
        stem.append(stemmer.stem(t))
    all_file_stem[e]=stem
# print (all_file_stem)

for each in normalized_tf_idf:
    token_list = list()
    for o in each:
        token_dict = dict()
        for item in all_file_stem:
            if o in all_file_stem[item]:
                file=item
                token_dict[file]=each[o]
                   #print(token_dict)
            postingsList[o]=token_dict
        #print(postingsList)

sorted_postingsList={}

for item in postingsList:                       #creating a sorted postingsList for each token in the corpus
    temp_dict=postingsList[item]
    sorted_temp_dict = sorted(temp_dict.items(), key=operator.itemgetter(1))#http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    sorted_postingsList[item]=sorted_temp_dict
#print (sorted_postingsList)

k=10
top_k={}
for item in qtf_dict:
    if item in sorted_postingsList:
        sorted_posting=sorted_postingsList[item]
        top=sorted_posting[:k]
        top_k[item]=top
#print(top_k)

similarity_file={}
for file in file_list:
    flag = [0] * len(normalized_query) #http://stackoverflow.com/questions/8528178/list-of-zeros-in-python
    i=0

    sim = 0
    for each in normalized_query:
        value=top_k[each]
        len_value=len(value)
        k_i = 0
        for e in value:
            if e[0]==file:
                flag[i]=1
                tfidf=e[1]
                i+=1
                sim=sim+(tfidf*normalized_query[each])
                break
            elif e[0] != file:
                if k_i < len_value-1:
                    k_i+=1
                    continue
                else:
                    tfidf=e[1]
                    sim=sim+(tfidf*normalized_query[each])
    similarity_file[file]=sim
#print(similarity_file)

def similarity(topk_dic, file_list, normalized_query):
    #print(topk_dic)
    '''
    list_of_files = list()
    for token_key, list_of_tuples in topk_dic.items():
        temp_list = list()
        for tup in list_of_tuples:
            temp_list.append(tup[0])
        list_of_files.append(temp_list)
    common_file_result = set(list_of_files[0])
    for s in list_of_files[1:]:
        common_file_result.intersection_update(s)
    #print(common_file_result)
    '''
    final_score_dict = dict()
    for f in file_list:
        score = 0
        for token_key, list_of_tuples in topk_dic.items():
            for tup in list_of_tuples:
                if f == tup[0]:
                    score = score + normalized_query[token_key]*tup[1]
                else:
                    score = score + normalized_query[token_key]* list_of_tuples[-1][1]
        final_score_dict[f] = score
    return final_score_dict
similarity(top_k, file_list, normalized_query)

def query(qstring):
    #similarity(top_k, file_list, normalized_query)
    final_d=similarity(top_k, file_list, normalized_query)
    score_dict=sorted(final_d.items(), key=operator.itemgetter(1))
    #print(score_dict)
    for token_tup  in score_dict:
        print(token_tup[0],token_tup[1])
        break
query(qstring)







