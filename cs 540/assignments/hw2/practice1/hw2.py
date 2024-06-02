import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    #with open("C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/CS-540-UW-MADISON/cs 540/assignments/hw2/practice1/e.txt",encoding='utf-8') as f:
    with open("e.txt",encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

   # with open('C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/CS-540-UW-MADISON/cs 540/assignments/hw2/practice1/s.txt',encoding='utf-8') as f:
    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        
        for line in f:#get each line and remove spaces
            
            for char in list(line.strip()):
                
                if(char!=" "):
                    index=ord(char)-ord('A')
                    difference=ord('Z')-ord('A')
                    upperLower=ord('a')-ord('A')
                    #3 conditions
                    if(index>=0 and index<=difference):
                        X[char]=1 if char not in X else X[char]+1
                    elif((index-upperLower)>=0 and (index-upperLower)<=difference):
                        character=chr(index-upperLower+ord('A'))
                        X[character]=1 if character not in X else X[character]+1
                    else:
                        continue
    for i in range(26):
        if(chr(i+ord('A')) not in X):
            X[chr(i+ord('A'))]=0
    Y=dict()#sorting the dictionary X and storing final result into dictionary Y
    for item,value in sorted(X.items()):
        Y[item]=value
    return Y
def findProb(filename):
    #Part1
    X=shred(filename)
    print('Q1')
    for key in X.items():
        print(key[0],key[1])
    #part2
    x1=X['A']
    e,s=get_parameter_vectors()
    e1=e[0]
    s1=s[0]
    print('Q2')
    print(round(x1*math.log(e1),4))
    print(round(x1*math.log(s1),4))
    #part3
    prob_e=0.6
    prob_s=0.4
    engl_sum=0
    count=0
    for key,val in X.items():
        engl_sum+=val*math.log(e[count])
        count+=1
    spanish_sum=0
    count=0
    for key,val in X.items():
        spanish_sum+=val*math.log(s[count])
        count+=1
    F_english=math.log(prob_e)+engl_sum
    F_spanish=math.log(prob_s)+spanish_sum
    print('Q3')
    print(round(F_english,4))
    print(round(F_spanish,4))
    #part4
    print('Q4')
    diff=F_spanish-F_english
    if diff>=100:
        print(round(0,4))
    elif diff<=-100:
        print(round(1,4))
    else:
        result=1/(1+math.exp(F_spanish-F_english))
        print(round(result,4))
   
    
    



# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!

if __name__=="__main__": 
   # findProb("C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/CS-540-UW-MADISON/cs 540/assignments/hw2/practice1/samples/letter4.txt")
   findProb("samples/letter4.txt")
