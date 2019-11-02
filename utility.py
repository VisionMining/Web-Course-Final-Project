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


def correlation_based(ui_matrix, users, items):
    pass


def adjust_cosine(ui_matrix, users, items):
    for i in range(items):
        user = ui_matrix[:, i]
        whl = (user != 0)
        useri = user[whl]
        ui_matrix[:, i][whl] = ui_matrix[:, i][whl] - np.average(useri)

    return cosine_based(ui_matrix, users, items)


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
        error += abs(entry[2] - entry[3]) ** 2
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