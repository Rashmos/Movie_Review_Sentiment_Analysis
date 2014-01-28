result_txt = []
import csv
import string
import math
test_list = []
prior = [None]*2
cond_Prob = {}
myValues = []
result = []


def pre_process_test():
    
    file = open("model_final.txt")
    pr = file.readline().split() 
    prior[0] = float(pr[1])
    prior[1] = (float(pr[3]))
    
    while 1:
        line = file.readline()
        if not line:
            break
        else:
            text = line.split(" ")
            term = text[0]
            cond_Prob[term] = list()
            cond_Prob[term].append(float(text[2]))
            cond_Prob[term].append(float(text[4].replace("\n","")))
        
    inp = raw_input("Enter the path to the test data file:\n ").lower()
    reader = csv.reader(open(inp,"rb")) 
    #stopwords=set([])
    stopwords = ["a","the","my","an","is","r","if"]
    for row in reader:
        result_txt.append(row[0])
        #row[0] = re.findall(r'\w+',row[0].strip(),flags = re.UNICODE | re.LOCALE)
        row[0]=row[0].replace('-','')
        row[0]=row[0].translate(string.maketrans("",""),string.punctuation)
        #row[0] = " ".join(row[0])
        myValues.append(row[0])
    myValues.pop(0)
    
    result_txt.pop(0)
    print 'text length',len(result_txt)
    for text in myValues:      
        new_string = ''
        string_list = text.split(" ")
        for item in string_list:
            item.strip()
            if not item in stopwords and not item == " " and not item == "":
                new_string += item+" "
        new_string = new_string.strip()
        test_list.append(new_string) 
    print len(test_list)

    
def ApplyBernoulliNB():
    i =1
    for d in test_list:
        document = d
        #document = document.replace("\"[", "")
        Vd = document.split(" ")
        C = [0,1]
    
        score = []
        for c in C:
            score.append(math.log(prior[c]))
            for t in cond_Prob:
                cond_prob1 = math.log(cond_Prob[t][c])
                cond_prob2 = math.log(1.0 - cond_Prob[t][c])
                if t in Vd:
                    score[c] += (cond_prob1)
                    #print "term ",t,cond_prob1
                    #print "term ",t,"score ", score[c],"label ", c
                else:
                    score[c] += (cond_prob2)
   
        maximum = max(score)
       
        if maximum == score[0]:
            result.append("0")
            label = 0
        else:
            result.append("1")
            label = 1
        print "score:",maximum,"label:",label, i
        i += 1
         
pre_process_test()
ApplyBernoulliNB()


     


fo = open('my_result_final.csv','w')
i = 0
while i < len(result):
    str = result[i] +','+ result_txt[i]+'\n'
    fo.write(str)
    i += 1

