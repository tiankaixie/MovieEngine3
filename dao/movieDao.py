import re
import numpy as np
from scipy.io import loadmat

import plotly.plotly as py
import plotly.graph_objs as go

data_movies = loadmat('data/ex8_movies.mat')
data_movies_params = loadmat('data/ex8_movieParams.mat')

def loadMovie():
    bucket = []
    file = open('data/movie_ids.txt', 'r')
    for line in file:
        info = line.split(' ',1)
        bucket.append(info[1][:-1])
    # print bucket
    return bucket

def searchMovie(movieName):
    print 'enter search:'
    movieList = loadMovie()
    res_idx = [i for i, movie in enumerate(movieList) if re.search(movieName, movie, re.I)]
    print res_idx
    movieList = np.asarray(movieList)
    print 'going to return'
    Y = np.matrix(data_movies['Y'])
    R = np.matrix(data_movies['R'])
    rateList = []
    for x in res_idx:
        rateList.append("{0:.2f}".format(Y[x, R[x,].ravel().nonzero()][1,].mean()))
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print rateList
    res = zip(res_idx, movieList[res_idx],rateList)
    return res

def loadData():
    print 'Loading data:\n'
    Y = np.matrix(data_movies['Y'])
    R = np.matrix(data_movies['R'])
    X = np.matrix(data_movies_params['X'])
    Theta = np.matrix(data_movies_params['Theta'])
    num_users = int(data_movies_params['num_users'])
    num_movies = int(data_movies_params['num_movies'])
    num_features = int(data_movies_params['num_features'])

    # test rating
    my_ratings = np.matlib.zeros((1682,1))
    my_ratings[0] = 4
    my_ratings[97] = 2
    my_ratings[6] = 3
    my_ratings[11] = 5
    my_ratings[53] = 4
    my_ratings[63] = 5
    my_ratings[65] = 3
    my_ratings[68] = 5
    my_ratings[182] = 4
    my_ratings[225] = 5
    my_ratings[354] = 5
    Y = np.concatenate((my_ratings,Y),1)#print Y.shape
    idx = my_ratings.ravel().nonzero()
    idx = idx[1]
    my_mask = np.matlib.zeros((1682,1))
    my_mask[idx] = 1
    #print R.shape
    R = np.concatenate((my_mask,R),1)
    return Y, R, X, Theta, num_users, num_movies, num_features

def createMyRatings():
    my_ratings = [0] * 1682
    return my_ratings

def getRatedMovies(my_ratings):
    # my_ratings = np.squeeze(np.asarray(my_ratings))
    # print my_ratings
    # print '$$$$$$$$$$$$$$$$$$$$$$$$$4'
    idx = [i for i, e in enumerate(my_ratings) if e != 0]
    # print idx
    movieList = loadMovie()
    movieList = np.asarray(movieList)
    # print movieList[idx]

    return zip(movieList[idx],np.asarray(my_ratings)[idx])