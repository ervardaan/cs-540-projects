import csv
import numpy as np
import math
from numpy import linalg as NA
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sc
def load_data(filepath):
    with open(filepath,newline='') as readfile:
        reader=csv.DictReader(readfile,delimiter=',',quotechar=' ')
        reader=list(reader)
        #if we have to remove the first key(empty) then add the below lines as well
        # i=0
        # for row in reader:
        #     k=list(row.keys())
        #     del row[k[0]]
        #     reader[i]=row
        #     i=i+1
    return reader
def calc_features(row):
    list1=[]
    elements=list(row.keys())
    for i in range(6):
       list1.append((float)(row[elements[i+2]]))#use this when we have not removed the first empty key 
       #list1.append((float)(row[elements[i+2]]))#use when we have removed first empty key
    convert=np.array(list1,dtype='f8')
    return convert
def hac(features):
    n=len(features)
    #given n feature vectors-create an adjacency matrix for initial distances for them so we can use them in the future(DP concept)
    #we get table of size n*n
    collect=createAdjacencymatrix(features)
    z=np.zeros((n-1,4))
    tracker=[]#not an nd array
    for i in range(n):
        tracker.append(i)
    clusters=[]#clusters is an array containing list of clusters(each list contains all the single nodes/points inside that cluster)
    for i in range(n-1):
        response=clustering_merging(clusters,tracker,collect,n)
        z[i][2]=response[2]
        z[i][1]=response[1]
        i1=(int)(z[i][1])
        z[i][0]=response[0]
        i0=(int)(z[i][0])
        #case 1-1 and 0 are both single points
        #case 2-1 and 0 are both clusters
        #case 3-1 and 0 are either
        listnew=[]
        if i1<n and i0<n:
            listnew.append(i0)
            listnew.append(i1)
            tracker[i1]=-1
            tracker[i0]=-1
            clusters.append(listnew)#Now clusters list contains this new cluster
        elif i1>=n and i0>=n:
            getcluster=clusters[i0-n]
            getcluster2=clusters[i1-n]
            for k in getcluster:
                listnew.append(k)
            for l in getcluster2:
                listnew.append(l)
            clusters.append(listnew)
        elif i0>=n:
            getcluster=clusters[i0-n]
            for k in getcluster:
                listnew.append(k)
            listnew.append(i1)
            clusters.append(listnew)
        else:
            getcluster=clusters[i1-n]
            for k in getcluster:
                listnew.append(k)
            listnew.append(i0)
            clusters.append(listnew)
        tracker.append(i+n)#Now tracker keeps a track of it
        tracker[i0]=-1
        tracker[i1]=-1
        z[i][3]=len(listnew)
    return np.array(z)
def clustering_merging(clusters,tracker,collect,n):
    min_dist=100000000000000
    index1=0
    index2=0
    for i in tracker:
        #tracker contains indexes
        if i!=-1:#checking if some cluster/point has already been merged or not
            for j in tracker:
                if j!=-1 and j!=i:#checking for distance between itself
                    #case 1:i and j clusters both are single points
                    #case 2:i and j are both clusters
                    #case 3:one of them is a single point
                    if i<n and j<n:
                        dist=collect[i][j]
                        if min_dist>dist:
                            min_dist=dist
                            index1=i if i<j else j
                            index2=j if i<j else i
                    elif i>=n and j>=n:
                        dist=distance_two_clusters(clusters[i-n],clusters[j-n],collect)
                        if min_dist>dist:
                            min_dist=dist
                            index1=i if i<j else j
                            index2=j if i<j else i
                    elif i>=n:
                        dist=distance_cluster_point(clusters[i-n],j,collect)
                        if min_dist>dist:
                            min_dist=dist
                            index1=j
                            index2=i
                    else:
                        dist=distance_cluster_point(clusters[j-n],i,collect)
                        if min_dist>dist:
                            min_dist=dist
                            index1=i
                            index2=j
    return index1,index2,min_dist
def distance_two_clusters(cluster1,cluster2,collect):
    #gives complete linkage distance between 2 clusters
    max=-1000000000000
    for index in cluster1:
        #Index is a point index in the cluster1
        for index2 in cluster2:
            #index2 is point index in cluster2
            #dist=eucleidian_method2(collect[index],collect[index2])
            dist=collect[index][index2]
            if(max<dist):
                max=dist
    return max#complete linkage distance
def distance_cluster_point(cluster1,point,collect):
    max=-1000000000000
    for index in cluster1:
        #point is an index
        #dist=eucleidian_method2(collect[index],point)
        dist=collect[index][point]
        if(max<dist):
                max=dist
    return max#complete linkage distance
def eucleidian_method1(vector1,vector2):
    return NA.norm(np.array(vector1)-np.array(vector2))
def createAdjacencymatrix(features):
    n=len(features)
    collect=np.zeros((n,n))#diagonal values(distance with itself) are always 0
    for i in range(n):
        element=features[i]
        for j in range(i+1,n):
            element2=features[j]
            #collect[i][j]=eucleidian_method1(element,element2)
            collect[i][j]=eucleidian_method2(element,element2)
        for k in range(0,i):
            collect[i][k]=collect[k][i]
    return collect
def eucleidian_method2(vector1,vector2):
    sum=0
    for i in range(len(vector1)):
        sum+=math.pow(vector1[i]-vector2[i],2)
    return math.sqrt(sum)
def fig_hac(Z,names):
    fig=plt.figure()
    sc.dendrogram(Z,labels=names,leaf_rotation=90)
    fig.tight_layout()
    return fig
def normalize_features(features):
    m=np.mean(features,axis=0)
    sd=np.std(features,axis=0)
    for i in features:
        for j in range(6):
            i[j]=(i[j]-m[j])/(sd[j])
    return features
if __name__=="__main__":
    data = load_data("countries.csv")
    country_names = [row["Country"] for row in data]
    features = [calc_features(row) for row in data]
    features_normalized = normalize_features(features)
    n = 170
    Z_raw = hac(features[:n])
    Z_normalized = hac(features_normalized[:n])
    fig = fig_hac(Z_raw, country_names[:n])
    plt.show()

