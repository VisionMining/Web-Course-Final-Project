import numpy as np
from scipy.sparse import coo_matrix
from utility import adjust_cosine,cosine_based,correlation_based

train_split = np.loadtxt('../data/ml_ratings_trainset.txt')
row=train_split[:,0]
col=train_split[:,1]
data=train_split[:,2]
# num_user=1509
# num_item=2072
num_user=944
num_item=1683

# 去用户中心化，实验结果这在ub的三种相似度计算中是效果最好的。
ui_matrix = coo_matrix((data, (row,col)), shape=(num_user,num_item)).toarray()
usercf=userCF(ui_matrix, num_user,num_item, correlation_based)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse,_mae,_=usercf.predict_model(test_split)
# print(rmse)
print("correlation_based:")
print(_mae)

# 余弦相似度
ui_matrix = coo_matrix((data, (row,col)), shape=(num_user,num_item)).toarray()
usercf=userCF(ui_matrix, num_user,num_item, cosine_based)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse,_mae,_=usercf.predict_model(test_split)
# print(rmse)
print("cosine_based:")
print(_mae)

# 去物品中心化
ui_matrix = coo_matrix((data, (row,col)), shape=(num_user,num_item)).toarray()
usercf=userCF(ui_matrix, num_user,num_item, adjust_cosine)
test_split = np.loadtxt('../data/ml_ratings_testset.txt')
rmse,_mae,_=usercf.predict_model(test_split)
# print(rmse)
print("adjust_cosine:")
print(_mae)