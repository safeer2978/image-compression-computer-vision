import flask
from flask_cors import CORS
from flask import Flask,jsonify,request,make_response,url_for,redirect
import requests, json
app = flask.Flask(__name__)
app.config["DEBUG"] = True



import matplotlib
import scipy
import scipy.ndimage
import matplotlib.pyplot as plt 
import numpy as np 
from PIL import Image
import scipy.misc


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# The below two are visualization libraires
import matplotlib.pyplot as plt
import seaborn as sns 
# for calculating interval
from time import time
from sklearn.cluster import KMeans 
from skimage import io





@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/demo', methods=['POST'])
def demo():
    lol = request.json['lol']
    return lol
@app.route('/pca', methods=['POST'])
def pca():
    file_path = request.json['file_path']
    param = request.json['param']
    numpc = param
    file_path = file_path.replace(" ", "\\")
    # IMPORTING IMAGE USING SCIPY AND TAKING R,G,B COMPONENTS
    a = matplotlib.pyplot.imread(file_path)
    a_np = np.array(a)
    a_r = a_np[:,:,0]
    a_g = a_np[:,:,1]
    a_b = a_np[:,:,2]

    a_r_recon, a_g_recon, a_b_recon = comp_2d(a_r,numpc), comp_2d(a_g,numpc), comp_2d(a_b,numpc) # RECONSTRUCTING R,G,B COMPONENTS SEPARATELY
    recon_color_img = np.dstack((a_r_recon, a_g_recon, a_b_recon)) # COMBINING R.G,B COMPONENTS TO PRODUCE COLOR IMAGE
    recon_color_img = Image.fromarray(recon_color_img)
    #recon_color_img.show()
    newfilepath=file_path[:-4]
    recon_color_img.save(newfilepath+"-compressed.png")
    return "Guess its done?"

def comp_2d(image_2d, numpc): # FUNCTION FOR RECONSTRUCTING 2D MATRIX USING PCA
    cov_mat = image_2d - np.mean(image_2d , axis = 0).T
    eig_val, eig_vec = np.linalg.eigh(np.cov(cov_mat)) # USING "eigh", SO THAT PROPRTIES OF HERMITIAN MATRIX CAN BE USED
    p = np.size(eig_vec, axis =1)
    idx = np.argsort(eig_val)
    idx = idx[::-1]
    eig_vec = eig_vec[:,idx]
    eig_val = eig_val[idx]
    numpc = int(numpc)
    # THIS IS NUMBER OF PRINCIPAL COMPONENTS, YOU CAN CHANGE IT AND SEE RESULTS
    if numpc <p or numpc >0:
        eig_vec = eig_vec[:, range(numpc)]
    score = np.dot(eig_vec.T, cov_mat)
    recon = np.dot(eig_vec, score) + np.mean(image_2d, axis = 0).T # SOME NORMALIZATION CAN BE USED TO MAKE IMAGE QUALITY BETTER
    recon_img_mat = np.uint8(np.absolute(recon)) # TO CONTROL COMPLEX EIGENVALUES
    return recon_img_mat

def recreate_image(centroids, labels, w, h):
    # centroids variable are calculated from the flattened image
    # centroids: w*h, d 
    # so each row depicts the values per depth
    d = centroids.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            # filling values in new image with centroid values
            image[i][j] = centroids[labels[label_idx]]
            label_idx += 1
    return image


@app.route('/kMeans', methods=['POST'])
def kMeans():
    file_path = request.json['file_path']
    param = request.json['param']
    file_path = file_path.replace(" ", "\\")
    img_original = io.imread(file_path)
    img = np.array(img_original,dtype=float) / 255
    # Save the dimensions, we will be need them later
    w, h, d = original_shape = img.shape
    image_array = img.reshape(-1,d)
    t0 = time()
    kmeans64 = KMeans(n_clusters = int(param),random_state=42,verbose=2,n_jobs=-1).fit(image_array)
    labels64 = kmeans64.labels_
    #print('Within cluster sum of square error for'+str( {n_colours[0]})+' clusters = '+str({round(kmeans64.inertia_,2)}))
    newfilepath=file_path[:-4]
    plt.imsave(newfilepath+"-compressed-kmeans.png", recreate_image(kmeans64.cluster_centers_, labels64, w, h))

    return "idk when itll be done.."

CORS(app)
app.run()