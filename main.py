import json
from flask import Flask, render_template, request, redirect, Response, jsonify
import pandas as pd
from flask import Flask
app = Flask(__name__) # creates the Flask instance

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns


import sklearn as skt
from sklearn import preprocessing 
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
import scipy.stats as sci
import random
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import manifold
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cdist, pdist
import sys
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import LocalOutlierFactor, KernelDensity, NearestNeighbors




housing_full=pd.read_csv('Housing_data.csv')
N_NEIGHBORS = 5

@app.route("/")
def index():
    return render_template("index.html")

df = housing_full[['SalePrice', 'LotFrontage']]
df = df.dropna()

cols = list(df.columns)

for column in cols:
    df[column] = StandardScaler().fit_transform(df[[column]])


loc = LocalOutlierFactor(n_neighbors=10)
loc.fit(df)

df['LOF Score'] = loc.negative_outlier_factor_*(-1)
df['Outlier'] = loc.fit_predict(df)

df['color'] = df['LOF Score'].map(lambda x: 'orange' if x>=1.5 else 'blue')


kde = KernelDensity()
kde.fit(df[cols])
df['kde'] = kde.score_samples(df[cols])
df['dens_X'] = [0]*len(df)
df['dens_Y'] = [0]*len(df)
df['dens_dist'] = [0]*len(df)
df['X_new'] = [0]*len(df)
df['Y_new'] = [0]*len(df)

# Transform metric values (LOF, Density)

# Calculate density peaks
# Currently set them to top 10% highest kde density points

threshold = np.percentile(df['kde'], 90)

# Calculate all points with density field greater than this value

peaks = df[df['kde'] >= threshold]
df['color'] = df.apply(lambda x: 'yellow' if x['kde'] >= threshold else x['color'], axis = 1)
peaks = peaks[cols].to_numpy()

#df.plot.scatter(x=cols[0], y=cols[1], c=df['color'],figsize=(10,10),
                #title="Scatterplot with density peaks highlighted in yellow")

# Train a nearest neighbors model to assign datapoints their nearest density peak 
peaks_nn = NearestNeighbors(n_neighbors=N_NEIGHBORS)
peaks_nn.fit(peaks)



@app.route("/sendData/<sub_factor>")
def sendData(sub_factor):
	for i in tqdm(range(len(df))):
    
    # Assigning the nearest neighbor density peak to each point and calculating the distance 
    
	    distance, index = peaks_nn.kneighbors(df[cols].iloc[i].to_numpy().reshape(1,-1))
	#     print('Distance : {}\n index: {}\n'.format(distance, index))
	    
	    distances = distance[0]
	    indexes = index[0]
	    
	    dx,dy=0,0
	    
	    # Getting the X and Y directions towards the density peaks and adding them
	    
	    x = df[cols[0]].iloc[i]
	    y = df[cols[1]].iloc[i]
	    
	    for peak_ind in indexes:
	        
	        curr_peak = peaks[peak_ind,:]
	        
	        dx += curr_peak[0] - x
	        dy += curr_peak[1] - y
	    
	    # Scaling the magnitude of the vector (can experiment with more mathematical formulations)
	    
	    # Here, the idea is :
	    # - The higher the density, the more the point gets pulled towards the density peak
	    # - The higher the outlier score, the more the point gets pushed out (hence, -ve sign)
	    # - Similarly, farther away the point from the density peak, the more it gets pushed out
	    
	    scale = ((df['LOF Score'].iloc[i]-sub_factor)*distance[0][0])/df['kde'].iloc[i]
	    
	    dx *= scale
	    dy *= scale
	    
	    df['X_new'].iloc[i] = df[cols[0]].iloc[i]+dx
	    df['Y_new'].iloc[i] = df[cols[1]].iloc[i]+dy

	df['X_new'] = StandardScaler().fit_transform(df[['X_new']])
	df['Y_new'] = StandardScaler().fit_transform(df[['Y_new']])

	new_cols = ['X_new', 'Y_new']
	return new_cols.to_json()


if __name__ == "__main__":
	app.run(debug=True)

