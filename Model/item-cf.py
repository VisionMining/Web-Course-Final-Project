import sys
import numpy as np
from scipy.sparse import coo_matrix

sys.path.append('..')

from utility import adjust_cosine, cosine_based, correlation_based
from ratingReader import RatingReader

rating_file = 'Processed-Data/mapped-ratings.csv'
rr = RatingReader(rating_file, k_fold=5)

# 去物品中心化
ui_matrix = coo_matrix((data, (row, col)), shape=(num_item, num_user)).toarray()
itemcf = itemCF(ui_matrix, num_user, num_item, correlation_based)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse, _mae, _ = itemcf.predict_model(test_split)
# print(rmse)
print("correlation_based:")
print(_mae)

# 余弦相似度
ui_matrix = coo_matrix((data, (row, col)), shape=(num_item, num_user)).toarray()
itemcf = itemCF(ui_matrix, num_user, num_item, cosine_based)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse, _mae, _ = itemcf.predict_model(test_split)
# print(rmse)
print("cosine_based:")
print(_mae)

# 去用户中心化，实验结果这在ib的三种相似度计算中是效果最好的。
ui_matrix = coo_matrix((data, (row, col)), shape=(num_item, num_user)).toarray()
itemcf = itemCF(ui_matrix, num_user, num_item, adjust_cosine)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse, _mae, _ = itemcf.predict_model(test_split)
# print(rmse)
print("adjust_cosine:")
print(_mae)
