from sklearn.neighbors  import KNeighborsClassifier
import pandas as pd
import gensim
import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


model_gen = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

out_df = pd.read_csv("parsed_df.csv")
out_df = out_df.drop(out_df[out_df['Sense ID'].map(str) == "nan"].index)

sense_ids = list(set(out_df['Sense ID']))

d = {}
ind = 0
for senseID in sense_ids:
    d[senseID] = ind
    ind += 1

# print(sense_ids)
# print(out_df.shape)
# print(d)


def get_vinter(out_df, model= model_gen):
    Y = []
    for y in out_df['Sense ID']:
        Y.append(d[y])
    V_right = []
    for VR in out_df['context_right']:
        VR = VR[1:-1].split(',')
        if len(VR) == 0:
            VR = ['the', 'and']
        if len(VR) == 1:
            VR.append('the')
        for i in range(len(VR)):
            if VR[i] == 'and':
                VR[i] = 'And'
        V_right.append(VR)

    V_left = []
    for VL in out_df['context_left']:
        VL = VL[1:-1].split(',')
        if len(VL) == 0:
            VL = ['the', 'and']
        if len(VL) == 1:
            VL.append('the')
        for i in range(len(VL)):
            if VL[i] == 'and':
                VL[i] = 'And'      
        V_left.append(VL)

    V_inter = []
    combined = []
    for vr,vl in zip(VR,VL):
        data = np.array([model[vr[0]], model[vr[1]], model[vl[0]], model[vl[1]]])
        pca = PCA(n_components=1)
        principal_comp = pca.fit_transform(data.T)
        vinter = list(principal_comp)
        V_inter.append(vinter)
        combined.append(vinter+vr+vl)
    return combined, Y



    
       

    # #return X,Y
    # # X is concatenated vr,vl,vinter
    # pass

def MLP_classifier(X,Y):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, stratify=Y, random_state=1)
    model = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)
    return model

def knn_classifier(X,Y):
    model = KNeighborsClassifier(n_neighbors=34)
    model.fit(X,Y)
    return model

def kmeans_classifier(X):
    ##initialization is inherently kmeans++
    kmeans = KMeans(n_clusters=34, random_state=0).fit(X)
    return kmeans


def get_data(out_df):
    X,Y = get_vinter(out_df)
    return X,Y

def predict_data(Xtest, model):
    return model.predict(Xtest)

def write_output():
    pass

x,y = get_data(out_df)


