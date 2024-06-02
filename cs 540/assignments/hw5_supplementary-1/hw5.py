import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as ln



'''
this method is not used anywhere and is just used for creating a chnaged/modified csv file from a raw file without cleaned data'''
def data_curation(filename):
    collect={}
    with open(filename,'r',newline='') as csvfile:
        file=list(csv.reader(csvfile,delimiter=',',quotechar=' '))
        for i in range(len(file)):
            if i!=0:
                row=file[i]
                year=row[0]
                year=year[1:5]
                if year not in collect.keys() and year!="2022":
                    days=row[1]#if not in data collection,then only row[3] will have some value otherwise its above rows with same year will have row[3]
                    collect[year]=days
    with open("hw5.csv",'w',newline='',) as output:#creating a file named hw5.csv only as per specifications
        writer=csv.writer(output)
        writer.writerow(["year"]+["days"])#we separate each value with a list and so store each of thwem inside a list and then concatenate contents of
        #Lists using + sign---also quotes around strings are not printed into the csv file
        for key in collect.keys():#have to remove 2022-2023 year as per the specifications
            object1=collect[key]
            writer.writerow([key]+[object1])

def readfile(filename):
    with open(filename,'r',newline='') as file:
        file1=list(csv.reader(file,delimiter=',',quotechar=' '))
        list1=[]
        list2=[]
        i=0##remove if header line is not there
        for i in range(1,len(file1)):
            element=file1[i]
            #remove if header line is not there
            list1.append(float(element[0]))#if we don't change string values to float then we will get a increasing line where y axis is jumbledand we
            #get y values just plotted in the order they come in the array and so even if value is very high,if it is first in the array,it is plotted in the
            #lower corner and a smaller y value is plotted above it because it is next in the array
            list2.append(float(element[1]))
        # plt.plot(list(collect.keys()),list(collect.values()))
        # plt.show()
        fig, ax = plt.subplots()
        ax.plot(np.array(list1),np.array(list2))
        plt.savefig("plot.jpg")
        plt.show()
        return (list1,list2)
def preprocessing(list1,list2):

    finallist=[]
    finallisty=[]
    for i in range(len(list1)):
        array1=np.array([1,int(list1[i])])
        finallisty.append(list2[i])
        finallist.append(array1)
    finallist=np.array(finallist,dtype='int64')
    finallisty=np.array(finallisty,dtype='int64')
    print("Q3a:")
    print(finallist)
    print("Q3b:")
    print(finallisty)
    return finallist,finallisty
def calculateZ(X,Y):
    Xt=X.transpose()# x is m*n and xt is n*m so xt dot x is n*m by m*n=gives n*n matrix where n is  smaller dimension of the matrix X
    print("Q3c:")
    Z=np.dot(Xt,X)
    print(Z)
    I=ln.inv(Z)
    print("Q3d:")
    print(I)
    X_pseudo_inverse=np.dot(I,Xt)
    print("Q3e:")
    print(X_pseudo_inverse)
    beta_hat=np.dot(X_pseudo_inverse,Y)
    print("Q3f:")
    print(beta_hat)
    return beta_hat

def prediction(x_test,beta_hat):
#we have two components of beta or theta vector and we will use beta_0 and beta_1 with a particular feature vector(x_new)
    #x_new will be a vector with one component(one extra added so two components)
    #we will do equation beta_0*x_1 +beta_1*x_1 where x_0 and x_1 are two scalar components of column vector x

    y_test_hat=beta_hat[0]*x_test[0]+beta_hat[1]*x_test[1]
    print("Q4: ",y_test_hat)
    print("Q5a: <")
    print("Q5b: ","for >,we have slope>0 and for <,we have slope<0 and for =0,we have no slope(constant function)")
    return y_test_hat
def limitation(beta_hat):
    x_star=-beta_hat[0]/beta_hat[1]
    # we get x_required=[1 x_star] as the feature vector which can get us to y_required=0
    print("Q6a: ",x_star)
    print("Q6b: ","for me the answer and value of x_star makes proper sense as the intercept is very high in one direction and so "
                  "we need a lot of magnitude in other direction to neutralize it-we have slope fixed and so can only keep "
                  "increasing x vector to neutralize beta_0")








    




if __name__=="__main__":
    #data_curation("chart.csv")
    #use above line to create hw5.csv file only once and we should have access to chart.csv file for using this method-note that this
    #method only works for chart.csv file and how it is formatted and how we want to take its values and scrap it so this method is very
    #specific and cannot be part of whole program-that is why it is just run once by me to get hw5.csv file


    list1,list2= readfile(sys.argv[1])#note that argv[0] contains the size of the input array of strings which is next line for one string in the input we have argv[0]=0
    X,Y=preprocessing(list1,list2)
    beta_hat=calculateZ(X,Y)
    y_test_hat=prediction(np.array([1,2022]),beta_hat)
    limitation(beta_hat)
