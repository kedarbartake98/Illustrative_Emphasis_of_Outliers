import json
from flask import Flask, render_template, request, redirect, Response, jsonify
import pandas as pd
from flask import Flask
from joblib import Parallel, delayed
from math import floor, ceil 

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
import sys, os
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import LocalOutlierFactor, KernelDensity, NearestNeighbors


################################# GLOBAL CODE ##################################

# create the Flask instance
app = Flask(__name__) 

housing_full=pd.read_csv('Housing_data.csv')
N_NEIGHBORS = 5
sub_factor = 0.0

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
df['Flag'] = df['LOF Score'].map(lambda x: 'Outlier' if x>=1.5 else 'Data Point')


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
df['color'] = df.apply(lambda x: 'yellow' if x['kde'] >= threshold \
                                          else x['color'], axis = 1)

df['Flag'] = df.apply(lambda x: 'Density Peak' if x['kde'] >= threshold \
                                               else x['Flag'], axis = 1)

peaks = peaks[cols].to_numpy()

# Train a nearest neighbors model to assign datapoints their nearest density peak 
peaks_nn = NearestNeighbors(n_neighbors=N_NEIGHBORS)
peaks_nn.fit(peaks)

################################################################################

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendwith/<sub_factor>")
def sendwith(sub_factor):
    
    # Mode where we move inliners in and outliers out
    rect = parallel_implementation(df, move_inliers=True)
    
    return json.dumps(rect,cls=NpEncoder)


@app.route("/sendwithout/<sub_factor>")
def sendwithout(sub_factor):

    # Mode where we move outliers out and not inliers
    rect = parallel_implementation(df, move_inliers=False)

    return json.dumps(rect,cls=NpEncoder)

def parallel_implementation(df, move_inliers=False):
    '''
    Parallelize implementation of function across entire daraframe
    '''

    # Calculate number of rows per CPU core 
    num_cores = os.cpu_count()
    rows_per_core = ceil(len(df)/num_cores)

    # Distribute the df across all the cpu cores
    slices_list = [df.iloc[rows_per_core*core:rows_per_core*(core+1)] 
                   for core in range(num_cores)]

    # Execute the processing function on each slice parallely
    result_list = Parallel(n_jobs=num_cores, verbose=100)(delayed(move_outliers)
                           (df_slice, sub_factor, peaks, peaks_nn, move_inliers) 
                           for df_slice in slices_list)

    # Concatenate the dataframes received from all processes
    result = pd.concat(result_list)

    print('Result')
    print(result.head())

    # Convert into output format for sending to frontend
    final = []

    for i in range(0,len(result)):
        final.append({'A':result['X_new'].iloc[i],\
                      'B':result['Y_new'].iloc[i],\
                      'C':result['color'].iloc[i],\
                      'D':result['Flag'].iloc[i]})

    print('#'*100)
    print(len(final))
    print('#'*100)
    print(final)

    rect = {'datapoints': final}

    return rect


def move_outliers(df, sub_factor, peaks, peaks_nn, move_inliers=False):
    '''
    Calculate new coordinates for points after moving them using our 
    displacement vectors. 
    '''
    sub_factor = float(sub_factor)

    for i in range(len(df)):
        
        # Assigning the nearest neighbor density peak to each point and 
        # calculating the distance 

        distance, index = peaks_nn.kneighbors(df[cols].iloc[i].to_numpy() \
                                                              .reshape(1,-1))
        
        distances = distance[0]
        indexes = index[0]
        
        dx,dy=0,0
        
        # Getting the X and Y directions towards the density peaks and adding 
        x = df[cols[0]].iloc[i]
        y = df[cols[1]].iloc[i]
        
        for peak_ind in indexes:
            curr_peak = peaks[peak_ind,:]
            
            dx += curr_peak[0] - x
            dy += curr_peak[1] - y

        '''
        Scaling the magnitude of the vector (can experiment with more 
                                             mathematical formulations)
        
        Here, the idea is :
        - The higher the density, the more the point gets pulled towards the 
          density peak
        - The higher the outlier score, the more the point gets pushed out 
          (hence, -ve sign)
        - Similarly, farther away the point from the density peak, the more 
          it gets pushed out  
        
        '''    

        if not move_inliers:

            if (df['LOF Score'].iloc[i]-1)>0:
                scale = ((df['LOF Score'].iloc[i]-\
                        sub_factor)*distance[0][0])/df['kde'].iloc[i]
            else:
                # Changed
                scale = 0
        else:
            outlier_score = df['LOF Score'].iloc[i]
            kde_val = df['kde'].iloc[i]
            scale = ((outlier_score-sub_factor)*distance[0][0])/kde_val

        dx *= scale
        dy *= scale
        
        df['X_new'].iloc[i] = (df[cols[0]].iloc[i]+dx).astype(float)
        df['Y_new'].iloc[i] = (df[cols[1]].iloc[i]+dy).astype(float)

    return df

if __name__ == "__main__":
    app.run(debug=True)

