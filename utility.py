import numpy as np
import random
import math
import time
from numpy.linalg import norm
from tqdm import tqdm
from scipy.sparse import coo_matrix


def cosine_based(data, num1, num2):
    """
    计算最基本的余弦相似度，
    如果是计算用户相似度，则data矩阵以用户为行，项目为列，
    如果是计算项目相似度则相反
    :param data:
    :type data:
    :param num1:
    :type num1:
    :param num2:
    :type num2:
    :return:
    :rtype:
    """
    print("beginsim")
    #data=data.toarray()
   
    dataT=data.T
    nn=np.matmul(data[0],dataT)
    for i in range(1,num1):
        nn=np.vstack((nn,np.matmul(data[i],dataT)))
    #print(nn)
    normal=np.empty(num1)
    for i in range(num1):
        normal[i]=norm(data[i])    
    normalT=normal[:, np.newaxis]
    normal=normal[np.newaxis,:]
    nor=np.matmul(normalT,normal)+0.0000001
    similarity=np.divide(nn,nor)
    return similarity-np.identity(num1)


    # 减去用户评分均值
    #如果是计算用户相似度，则data矩阵以用户为行，项目为列，
    #如果是计算项目相似度则相反
def correlation_based(ui_matrix,users,items):
    for i in range(users):
        user=ui_matrix[i,:]
        whl=(user!=0)
        useri=user[whl]
        ui_matrix[i,:][whl]=ui_matrix[i,:][whl]-np.average(useri)
    return cosine_based(ui_matrix,users,items)

    # 减去物品评分均值
    #如果是计算用户相似度，则data矩阵以用户为行，项目为列，
    #如果是计算项目相似度则相反
def adjust_cosine(ui_matrix,users,items): 
    for i in range(items):
        user=ui_matrix[:,i]
        whl=(user!=0)
        useri=user[whl]
        ui_matrix[:,i][whl]=ui_matrix[:,i][whl]-np.average(useri)
    
    return cosine_based(ui_matrix,users,items)


def MAE(res):
    error = 0
    count = 0
    for entry in res:
        error += abs(entry[2] - entry[3])
        count += 1
    if count == 0:
        return error
    return float(error) / count


def RMSE(res):
    error = 0
    count = 0
    for entry in res:
        error += abs(entry[2] - entry[3])**2
        count += 1
    if count == 0:
        return error
    return math.sqrt(float(error) / count)


def checkRatingBoundary(prediction, min_val, max_val):
    if prediction > max_val:
        return max_val
    elif prediction < min_val:
        return min_val
    else:
        return round(prediction, 3)


def denormalize(rating, minVal, maxVal):
    return minVal + (rating - 0.01) * (maxVal - minVal)

def normalize(rating, minVal, maxVal):
    return (rating-minVal)/(maxVal-minVal)+0.01

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))


