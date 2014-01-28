import csv 
prior = []
condProb = {}
Vocab = [] 
myKeys = []
myValues = []
test_list = []
i = 0
import re
import string
import math
from collections import OrderedDict
cond_prob = {}
class0 = {}
class1 = {}
mt = {}
mutual = {}

def pre_process():

    inp = raw_input("Enter the path to the test data file:\n ").lower()
    reader = csv.reader(open(inp, "rb")) 
    for row in reader:
        #row[1] = re.findall(r'\w+',row[1].strip(),flags = re.UNICODE | re.LOCALE)
        row[1] = row[1].strip()
        row[1]=row[1].replace('-',' ')
        row[1]=row[1].translate(string.maketrans("",""),string.punctuation)
        row[0] = row[0].strip()
        texty = row[1].split(" ")
        for text in texty:
            if row[0] == '0' and not text == '':
                if not text in class0:
                    class0[text] = 1
                else:
                    class0[text] += 1
            if row[0] == "1" and not text == '':
                if not text in class1:
                    class1[text] = 1
                else:
                    class1[text] += 1
                 
                
        '''
        mutual_info = row[1].split(" ")
        Mutual_Info(mutual_info, row[0])
        '''
        stopwords=set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
        
        #row[1] = " ".join(row[1])
        myKeys.append(row[0])
        myValues.append(row[1])
    
    myKeys.pop(0)
    myValues.pop(0)
    x = 1

    vocab = []
    for text in myValues:      
        string_list = text.split(" ")
        for item in string_list:
            item.strip()
            if not item in stopwords and not item == " " and not item == "":
                vocab.append(item)
    Vocab = list(set(vocab))
    return Vocab
def Mutual_Info():
    print len(Vocab)
    for terms in Vocab:
        if terms in class0:
            N10 = float(class0[terms])
            N00 = float(len(class0))-N10
        else:
            N00 = float(len(class0))
            N10 = 0.0
        if terms in class1:
            N11 = float(class1[terms])
            N01 = float(len(class1))-N11
        else:
            N01 = float(len(class1))
            N11 = 0.0
        N = len(Vocab)
        
        x1 = N11/N
        x2 = (N*N11)/( (N11+N01)*(N11+N10) )
        if not x2 == 0:
            t1 = x1*math.log(x2,2)
        else:
            t1 = 0
        y1 = N01/N
        y2 = (N*N01)/( (N00+N01)*(N01+N11) )
        if not y2 == 0:
            t2 = y1*math.log(y2,2)
        else:
            t2 = 0
        z1 = N10/N
        z2 = (N*N10)/( (N10+N11)*(N10+N00) )
        if not z2 == 0:
            t3 = z1*math.log(z2,2)
        else:
            t3 = 0
        w1 = N00/N
        w2 = (N*N00)/( (N00+N01)*(N00+N10) )
        if not w2 == 0:
            t4 = w1*math.log(w2,2)
        else:
            t4 = 0
        value  = t1+t2+t3+t4
        mt[terms] = value
    mutual = OrderedDict(sorted(mt.items(), key=lambda x: x[1])) 
   # print mutual
    print len(mutual)
        
        
            
        
 
            

def countDocsInClassContainingTerm(t,label):
    p = 0
    count = 0
    while p < len(myKeys):
        temp = myValues[p].strip().split(" ")
        if myKeys[p] == str(label)  and t in temp:
            count = count+1
        p += 1         
    return count

def CountDocsInClass(c):
    i = str(c)
    count = myKeys.count(i)
    return count 

def trainBernoulli(Voc):
    V = Voc
    print len(V)
    i = 0
    C = [0,1]
    N_ct = 0.0
    N = float(len(myKeys))
    Nc= [None]*2
    prior = [None]*2
    for c in C:
        Nc[c] = CountDocsInClass(c)
        prior[c] = float(Nc[c])/float(N)
        for term in V:
            N_ct = float(countDocsInClassContainingTerm(term, c))
            num = N_ct+1.0
            den = Nc[c]+2.0
            if not term in cond_prob:
                cond_prob[term] = list()
            value = num/den
            cond_prob[term].append(value)
            i+=1
            print i
    fo = open('model_final.txt','w')
    zero = str(prior[0])
    one = str(prior[1])
    first = "Prior[0] "+zero+" Prior[1] "+one+"\n"
    fo.write(first)

    for terms in cond_prob:
        term = str(terms)
        label0 = str(cond_prob[terms][0])
        label1 = str(cond_prob[terms][1])
        string = term+" 0 "+label0+" 1 "+label1+"\n"
        fo.write(string)
        i += 1
        
Vocab = pre_process()
Mutual_Info()
trainBernoulli(Vocab)
    

