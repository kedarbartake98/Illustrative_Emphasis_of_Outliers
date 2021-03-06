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
import sys
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import KernelDensity, NearestNeighbors


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


def generic(df,cols):
	for column in cols:
	    df[column] = StandardScaler().fit_transform(df[[column]])
	N_NEIGHBORS = 5
	sub_factor = 0.0

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
	df['color'] = df.apply(lambda x: 'yellow' if x['kde'] >= threshold else x['color'], axis = 1)
	df['Flag'] = df.apply(lambda x: 'Density Peak' if x['kde'] >= threshold else x['Flag'], axis = 1)

	peaks = peaks[cols].to_numpy()

	#df.plot.scatter(x=cols[0], y=cols[1], c=df['color'],figsize=(10,10),
	                #title="Scatterplot with density peaks highlighted in yellow")

	# Train a nearest neighbors model to assign datapoints their nearest density peak 
	peaks_nn = NearestNeighbors(n_neighbors=N_NEIGHBORS)
	peaks_nn.fit(peaks)
	return df,peaks_nn,cols,peaks

@app.route("/sendwith",methods=['GET'])
def sendwith():

	dataset_name  = request.args.get('dataset_name', None)
	sub_factor  = request.args.get('sub_factor', None)
	if(dataset_name == "Housing"):
		housing_full=pd.read_csv('Housing_data.csv')
		df = housing_full[['SalePrice', 'LotFrontage']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks = generic(df,cols)
		rect = transform_with(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Air"):
		housing_full=pd.read_csv('AirQualityUCI.csv')
		df = housing_full[['T', 'C6H6_GT']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_with(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Estate"):
		housing_full=pd.read_csv('data 3.csv')
		df = housing_full[['INDUS', 'DIS']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_with(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Cereal"):
		housing_full=pd.read_csv('cereal.csv')
		df = housing_full[['calories', 'sodium']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks=generic(df,cols)
		rect = transform_with(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	else:
		housing_full=pd.read_csv('forestfires.csv')
		df = housing_full[['RH', 'DC']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_with(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)

@app.route("/sendwithout",methods=['GET'])
def sendwithout():

	dataset_name  = request.args.get('dataset_name', None)
	sub_factor  = request.args.get('sub_factor', None)
	if(dataset_name == "Housing"):
		housing_full=pd.read_csv('Housing_data.csv')
		df = housing_full[['SalePrice', 'LotFrontage']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_without(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Air"):
		housing_full=pd.read_csv('AirQualityUCI.csv')
		df = housing_full[['T', 'C6H6_GT']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_without(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Estate"):
		housing_full=pd.read_csv('data 3.csv')
		df = housing_full[['INDUS', 'DIS']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_without(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	elif(dataset_name == "Cereal"):
		housing_full=pd.read_csv('cereal.csv')
		df = housing_full[['calories', 'sodium']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_without(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	else:
		housing_full=pd.read_csv('forestfires.csv')
		df = housing_full[['RH', 'DC']]
		df = df.dropna()
		cols = list(df.columns)
		df,peaks_nn,cols,peaks =generic(df,cols)
		rect = transform_without(df,peaks_nn,sub_factor,cols,peaks)
		return json.dumps(rect,cls=NpEncoder)
	

def transform_with(df,peaks_nn,sub_factor,cols,peaks):
	for i in tqdm(range(len(df))):
    
    # Assigning the nearest neighbor density peak to each point and calculating the distance 
  		#print("HELLO")

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
		#print(type(sub_factor))
		sub_factor = float(sub_factor)
		scale = ((df['LOF Score'].iloc[i] - sub_factor) * distance[0][0])/df['kde'].iloc[i]
		dx *= scale
		dy *= scale
	    
		df['X_new'].iloc[i] = (df[cols[0]].iloc[i]+dx).astype(float)
		df['Y_new'].iloc[i] = (df[cols[1]].iloc[i]+dy).astype(float)

	
	final = []

	for i in range(0,len(df)):
		final.append({'A':df['X_new'].iloc[i],'B':df['Y_new'].iloc[i],'C':df['color'].iloc[i],'D':df['Flag'].iloc[i]})

	rect={
		'datapoints':final
	}
	print(final)
	return rect



def transform_without(df,peaks_nn,sub_factor,cols,peaks):
	for i in tqdm(range(len(df))):
    
    # Assigning the nearest neighbor density peak to each point and calculating the distance 
  		#print("HELLO")

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
		#print(type(sub_factor))
		sub_factor = float(sub_factor)
		if (df['Flag'].iloc[i]=='Outlier'):
			scale = ((df['LOF Score'].iloc[i]-sub_factor)*distance[0][0])/df['kde'].iloc[i]
			dx *= scale
			dy *= scale
			df['X_new'].iloc[i] = (df[cols[0]].iloc[i]+dx)
			df['Y_new'].iloc[i] = (df[cols[1]].iloc[i]+dy)
		else:
			df['X_new'].iloc[i] = df[cols[0]].iloc[i]
			df['Y_new'].iloc[i] = df[cols[1]].iloc[i]
		
	
	final = []

	for i in range(0,len(df)):
		final.append({'A':df['X_new'].iloc[i],'B':df['Y_new'].iloc[i],'C':df['color'].iloc[i],'D':df['Flag'].iloc[i]})

	rect={
		'datapoints':final
	}
	print(final)
	return rect


if __name__ == "__main__":
	app.run(debug=True)

