import numpy as np


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
