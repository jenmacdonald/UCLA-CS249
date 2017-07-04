from sklearn.cross_validation import ShuffleSplit
from sklearn.metrics import r2_score
from collections import defaultdict
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import Birch
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
import timeit
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


#import data###########################################
np.random.seed(5000)

path = "/Users/nnguyen/Documents/_Dev/CS-249/hw2/"
wine_df = pd.read_csv(path + "wine.data", header=None)

wine_df.columns = ["Type"
                   ,"Alcohol"
                   ,"Malic Acid"
                   , "Ash"
                   ,"Alcalinity of Ash"
                   , "Magnesium"
                   , "Total phenols"
                   , "Flavanoids"
                   , "Nonflavanoid phenols"
                   , "Proanthocyanins"
                   , "Color Intensity"
                   , "Hue"
                   , "OD280/OD315 of diluted wines"
                   , "Proline"]

Y1= wine_df["Type"].as_matrix()
Y = np.float64(Y1)
X = wine_df[["Alcohol"
             ,"Malic Acid"
             ,"Ash"
             ,"Alcalinity of Ash"
             ,"Magnesium"
             ,"Total phenols"
             ,"Flavanoids"
             ,"Nonflavanoid phenols"
             ,"Proanthocyanins"
             ,"Color Intensity"
             , "Hue"
             , "OD280/OD315 of diluted wines"
             , "Proline"]].as_matrix()


names = {
        0: "Alcohol"
        ,1: "Malic Acid"
        ,2: "Ash" 
        ,3: "Alcalinity of Ash"
        ,4: "Magnesium"
        ,5: "Total phenols"
        ,6: "Flavanoids"
        ,7: "Nonflavanoid phenols"
        ,8: "Proanthocyanins"
        ,9: "Color Intensity"
        ,10: "Hue"
        ,11: "OD280/OD315 of diluted wines"
        ,12: "Proline"
        
        }
##End Import Data ############################################################


#using RandomForestClassifier#################################################
rf = RandomForestClassifier(n_estimators = 1000, criterion='entropy')
#RandomForestRegressor(n_estimators = 100)
rf.fit(X,Y)

print ("Features sorted by their score:")
importance_features = {}
for column_id,feat_importance in enumerate(rf.feature_importances_):
    importance_features[names.get(column_id)] = feat_importance    
print(sorted(((v,k) for k,v in importance_features.items()),reverse=True) )
##End Random Forest ############################################################

      
###############################################################################
#Kmeans

X = wine_df[["Proline","Flavanoids","Color Intensity"]].as_matrix()

estimators_Kmeans = {'k_means_3': KMeans(n_clusters=3),
              'k_means_1': KMeans(n_clusters=1),
              'k_means_5': KMeans(n_clusters=5),
              'k_means_11': KMeans(n_clusters=11)}
    
fignum = 1
for name, est in estimators_Kmeans.items():
    print('Running ' + name)
    fig = plt.figure(fignum, figsize=None)
    plt.clf()
    ax = Axes3D(fig)
    plt.cla()
    start = timeit.default_timer()
    est.fit(X)
    stop = timeit.default_timer()

    print (stop - start )

    labels = est.labels_

    ax.scatter(X[:, 1], X[:, 0], X[:, 2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Flavanoids')
    ax.set_ylabel('Proline')
    ax.set_zlabel('Color Intensity')
    fignum = fignum + 1
    plt.show()


################################################################################
#Birch

X = wine_df[["Proline","Flavanoids","Color Intensity"]].as_matrix()

estimators_Birch= {'birch_3': Birch(n_clusters=3),
              'birch_1': Birch(n_clusters=1),
              'birch_5': Birch(n_clusters=5),
              'birch_11': Birch(n_clusters=11)}

fignum = 1
for name, est in estimators_Birch.items():
    print('Running ' + name)
    fig = plt.figure(fignum, figsize=None)
    plt.clf()
    ax = Axes3D(fig)
    plt.cla()
    start = timeit.default_timer()
    est.fit(X)
    stop = timeit.default_timer()

    print (stop - start )
    
    labels = est.labels_

    ax.scatter(X[:, 1], X[:, 0], X[:, 2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Flavanoids')
    ax.set_ylabel('Proline')
    ax.set_zlabel('Color Intensity')
    fignum = fignum + 1
    plt.show()

    

################################################################################
#AgglomerativeClustering

X = wine_df[["Proline","Flavanoids","Color Intensity"]].as_matrix()

estimators_AgglomerativeClustering= {'AgglomerativeClustering_3': AgglomerativeClustering(n_clusters=1),
              'AgglomerativeClustering_1': AgglomerativeClustering(n_clusters=3),
              'AgglomerativeClustering_5': AgglomerativeClustering(n_clusters=5),
              'AgglomerativeClustering_11': AgglomerativeClustering(n_clusters=11)}

fignum = 1
for name, est in estimators_AgglomerativeClustering.items():
    print('Running ' + name)
    fig = plt.figure(fignum, figsize=None)
    plt.clf()
    ax = Axes3D(fig)
    plt.cla()
    start = timeit.default_timer()
    est.fit(X)
    stop = timeit.default_timer()

    print (stop - start )
     
    labels = est.labels_

    ax.scatter(X[:, 1], X[:, 0], X[:, 2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Flavanoids')
    ax.set_ylabel('Proline')
    ax.set_zlabel('Color Intensity')
    fignum = fignum + 1
    plt.show()
    

################################################################################
#DBSCAN

X = wine_df[["Proline","Flavanoids","Color Intensity"]].as_matrix()

estimators_DBSCAN= {'DBSCAN_5': DBSCAN(eps=20,metric='euclidean', min_samples=5)
                    #'DBSCAN_1': DBSCAN(eps=10,metric='euclidean', min_samples=5)


                    }

fignum = 1
for name, est in estimators_DBSCAN.items():
    print('Running ' + name)
    fig = plt.figure(fignum, figsize=None)
    plt.clf()
    ax = Axes3D(fig)
    plt.cla()  
    start = timeit.default_timer()
    est.fit(X)
    stop = timeit.default_timer()
    
    print (stop - start )
    
    
    labels = est.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print('Estimated number of clusters: %d' % n_clusters_)

    ax.scatter(X[:, 2], X[:, 0], X[:, 1], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Proline')
    ax.set_zlabel('Flavanoids')
    fignum = fignum + 1
    plt.show()
    
    
fignum = 1
for name, est in estimators_DBSCAN.items():
    print('Running ' + name)
    fig = plt.figure(fignum, figsize=None)
    plt.clf()
    ax = Axes3D(fig)
    plt.cla()  
    start = timeit.default_timer()
    est.fit(X)
    stop = timeit.default_timer()
    
    print (stop - start )
    
    
    labels = est.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print('Estimated number of clusters: %d' % n_clusters_)

    ax.scatter(X[:, 1], X[:, 0], X[:, 2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Proline')
    ax.set_zlabel('Flavanoids')
    fignum = fignum + 1
    plt.show()   
    
    
    
    

