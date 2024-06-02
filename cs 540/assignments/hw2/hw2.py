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

    #with open("C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/CS-540-UW-MADISON/cs 540/assignments/hw2/practice1/s.txt",encoding='utf-8') as f:
    with open("s.txt",encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    
    with open (filename,encoding='utf-8') as f:#opening the file through its filename
        # TODO:#TASK1
        for line in f:#get each line from file
            
            for c in list(line.strip()):#remove spaces and blanks from both ends of one line
                
                
                if c!=" ":#if any inbetween character is not a space
                    index=ord(c)-ord('A')#used to convert a single Unicode character into its integer representation
                    
                    if (index>=0 and index<=ord('Z')-ord('A')):
                        
                        character=chr(index+ord('A'))
                        
                       
                        X[character]=1 if character not in X else X[character]+1
                    elif (index-(ord('a')-ord('A'))>=0 and index-(ord('a')-ord('A'))<=ord('Z')-ord('A')):
                        character=chr(index-(ord('a')-ord('A'))+ord('A'))
                        
                        X[character]=1 if character not in X else X[character]+1
                    else:
                        continue
    for i in range(0,26):
        if chr(i+ord('A')) not in X:
            X[chr(i+ord('A'))]=0
    
    Y=dict()
    for key,value in sorted(X.items()):
        Y[key]=value
  
    return Y
def findProb(filename):
    prob_e=0.6
    prob_s=0.4    
    e1,s1=get_parameter_vectors()
    
    # X=shred("C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/cs 540/assignments/hw2/hw2/samples/letter0.txt")
    X=shred(filename)
    
    part1 = math.log(prob_e)
    part2 = math.log(prob_s)

    
    count = 0
    english_sum = 0
    for key, value in X.items():
        english_sum += value * math.log(e1[count])
        count += 1
    
    count2 = 0
    spanish_sum = 0
    for key, value in X.items():
        spanish_sum += value * math.log(s1[count2])
        count2 += 1
    
    f_english = part1 + english_sum
    f_spanish = part2 + spanish_sum
    F_english = f_english
    F_spanish = f_spanish
  
    #prob_lang=math.exp(F_y)/(math.exp(F_spanish)*math.exp(F_english))#main formula 2-if we use this then we get float division by 0 error
    #specifically for english or spanish
    if(F_spanish-F_english>=100):
        prob_english_given_x=0
    elif F_spanish-F_english<=-100:
        prob_english_given_x=1
    else:
        prob_english_given_x=1/(1+math.exp(F_spanish-F_english))
#printing
    print('Q1')
    for key in X.items():
        print(key[0],key[1])
    print('Q2')
    print(round(X[chr(0+ord('A'))]*math.log(e1[0]),4))
    
    print(round(X[chr(0+ord('A'))]*math.log(s1[0]),4))
    print('Q3')
    print(round(F_english,4))
    print(round(F_spanish,4))
    print('Q4')
    print(round(prob_english_given_x,4))
    
#findProb('English',"C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/cs 540/assignments/hw2/hw2/samples/letter3.txt")
#findProb('English',"letter.txt")#-will not run on local computer but will run on gradescope for suubmission
#findProb("C:/Users/varda/OneDrive/Documents/COLLEGE COURSEWORK/CS-540-UW-MADISON/cs 540/assignments/hw2/practice1/samples/letter4.txt")
findProb("samples/letter4.txt")

        
        


    