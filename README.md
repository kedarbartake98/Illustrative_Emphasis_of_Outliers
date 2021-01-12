# Illustrative Emphasis of Outliers

### Problem Statement  
  
  Given a scatterplot, move the points in such a way that the outliers are highlighted and easy to point out. Essentialy, A scheme to produce distortions in scatterplots so that   outliers are higlighted. 
  
### Approach  
- **Outlier Selection** : Use *Local Outlier Score (LOF)* to decide which points are outliers based on certain thresholds 
  
  
- **Scatterplot Transformation**:  
To transform the scatterplot, we first cluster the data, and then calculate the density field using *Kernel Density Estimation (KDE)* and isolate *density peaks* in each cluster. Then, using following methods, we move the outliers away and (optionally) move the inliers inwards with respect to their nearest neighbor density peak.  

  - *Using LOF and KDE*:
  1. We calculate a vector for each point using factors like LOF score, KDE density, distance from nearest density peaks, etc.  
  2. We then move the point along the vector to produce a transformation.  
    
    
  - *Using Local Gradients* (TODO):  
  1. We compute a grid of points over the entire scatterplot and sample the KDE density over that grid. 
  2. For each point, sample the gradient of the density around that point and move the point in that direction to produce a transformation.  
    
    For details of implementation, refer to our [paper](Illustrative_Emphasis_of_Outliers.pdf)

Youtube Link: https://youtu.be/3YBtZIsyWsg
