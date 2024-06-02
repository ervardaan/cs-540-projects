import math

from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt
def load_and_center_dataset(filename):
    # Your implementation goes here!
    x=np.load(filename)#assume that we are given relative path
    x=x-np.mean(x,0)
    return x
def get_covariance(dataset):
    dp=np.dot(np.transpose(dataset),dataset)
    return dp/(len(dataset)-1)
def get_eig(S, m):
    eigs=eigh(S)#using once to just get the length in order to get the subset
    length=len(eigs[0])
    eigs_refined=eigh(S,subset_by_index=[length-m,length-1])
    eigenValues=eigs_refined[0]
    eigenVectors=eigs_refined[1]
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]
    return np.diag(eigenValues),eigenVectors
def get_eig_prop(S, prop):
    eigs_refined = eigh(S)
    eigenValues = eigs_refined[0]
    length = len(eigenValues)
    eigenVectors = eigs_refined[1]
    sum=np.sum(eigenValues)
    i=0
    while i<length:
        if eigenValues[i]/sum<prop:
            eigenValues=np.delete(eigenValues,i)
            eigenVectors=np.delete(eigenVectors,i,1)
            i=i- 1
        i=i+1
        length=len(eigenValues)
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]
    return np.diag(eigenValues), eigenVectors
def project_image(image, U):
    #Note:in caller function we have x as defined an image in rows so 1st row gives an image so to get image we did x[0] directly
    #here we have given x as an image in column vector form and even u_j will be in column vector form(every principal component is in
    # column vector form
    #given x_i and given U eigenvectors of size d by m where there are m eigenvectors out of original d eigenvectors
    #we take the product of u_j_transpose and x_i where 0<=j<=m to get m values of alpha_ij
    #this is what we call the projection into pca space of image x_i
    #Now we reconstruct to x_i_pca by doing alpha_ij by u_j for all j b/w 0 and m-output this value(a row vector)
    # x_i came in as a d by 1 column vector image and u_j was d by 1 itself-so we did transpose u_j and then multiplied to x_i
    # we get alpha_ij of size d by d hopefully but by  formula we are getting it of 1 by 1 only
    #converting row image to column image form
    Z=np.dot(np.transpose(U),image)
    return np.dot(U,Z)
def starter():
    x = load_and_center_dataset("YaleB_32x32.npy")
    S = get_covariance(x)
    eigValues,eigVectors=get_eig(S,2)
    eigValues2,eigVectors2=get_eig_prop(S,0.07)
    x_pca=project_image(x[0],eigVectors2)
    x_pca2=project_image(x[0],eigVectors)
    figure,ax1,ax2=display_image(x[0],x_pca)
    plt.show()

def display_image(orig, proj):
    n=len(proj)
    n1=len(orig)
    resized_proj=np.resize(proj,(int(math.sqrt(n)),int(math.sqrt(n))))
    resized_orig=np.resize(orig,(int(math.sqrt(n1)),int(math.sqrt(n1))))
    fig,(ax1,ax2)=plt.subplots(1,2)
    ax1.set_title("original")
    ax2.set_title("projection")
    image=ax1.imshow(resized_orig)
    project=ax2.imshow(resized_proj)
    fig.colorbar(image,ax=ax1)
    fig.colorbar(project,ax=ax2,location='right')
    return fig,ax1,ax2

starter()

