import numpy as np
import math
from numpy import linalg as LA


def cosine_based(vector1, vector2):
    """
    Compute two vectors cosine based similarity.
    :param vector1: 1-D array
    :type vector1: list
    :param vector2: 1-D array
    :type vector2: ndarray
    :return: similarity score
    :rtype: float
    """
    similarity = np.dot(vector1, vector2) / (LA.norm(vector1, 2) * LA.norm(vector2, 2))
    return similarity


def MAE(predict_value, true_value):
    error = 0
    count = 0
    for i in range(len(predict_value)):
        error += abs(predict_value[i] - true_value[i])
        count += 1
    if count == 0:
        return error
    return float(error) / count


def RMSE(predict_value, true_value):
    error = 0
    count = 0
    for i in range(len(predict_value)):
        error += abs(predict_value[i] - true_value[i]) ** 2
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
    return (rating - minVal) / (maxVal - minVal) + 0.01


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


if __name__ == '__main__':
    a = [1, 2, 3]
    b = np.array(a)
    b[0] = 4
    print([{}] * 5)
    print(b)
