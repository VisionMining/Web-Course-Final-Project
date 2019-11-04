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


def mae(predict_value, true_value):
    error = 0
    count = 0
    for i in range(len(predict_value)):
        error += abs(predict_value[i] - true_value[i])
        count += 1
    if count == 0:
        return error
    return float(error) / count


def rmse(predict_value, true_value):
    error = 0
    count = 0
    for i in range(len(predict_value)):
        error += abs(predict_value[i] - true_value[i]) ** 2
        count += 1
    if count == 0:
        return error
    return math.sqrt(float(error) / count)


if __name__ == '__main__':
    a = [1, 2, 3]
    b = np.array(a)
    b[0] = 4
    print([{}] * 5)
    print(b)
