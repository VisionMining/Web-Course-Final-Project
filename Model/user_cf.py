import numpy as np
import sys

sys.path.append('..')

from rating_reader import RatingReader
from utility import cosine_based


class UserCf:

    def __init__(self, rating_reader, k_neighbor=30):
        """

        :param rating_reader: rating reader object
        :type rating_reader: RatingReader
        :param k_neighbor: k most similar user to predict rating
        :type k_neighbor: int
        """
        self.rating_reader = rating_reader
        self.k_neighbor = k_neighbor
        self.user_num = rating_reader.get_user_num()
        self.items_mean_rating = rating_reader.get_items_mean_rating()
        self.users_mean_rating = rating_reader.get_users_mean_rating()

    def __predict_one(self, user_id, item_id):
        similarity_for_one_user = self.__compute_similarity_score_for_one_user(user_id, item_id)
        weighted_sum, similarity_sum = 0.0, 0.0
        for top_k in range(self.k_neighbor):
            if top_k >= len(similarity_for_one_user):
                break
            similarity = similarity_for_one_user[top_k][0]
            rating = similarity_for_one_user[top_k][1]
            weighted_sum += similarity * rating
            similarity_sum += similarity
        if sum == 0:
            predict = self.users_mean_rating[user_id]
        else:
            predict = weighted_sum / similarity_sum
        return predict

    def __compute_similarity_score_for_one_user(self, user_id, item_id):
        u1 = self.rating_reader.get_user_rating_vector(user_id)
        similarity = []
        for user_id_other in range(self.user_num):
            if self.rating_reader.contains_rating(user_id_other, item_id):
                u2 = self.rating_reader.get_user_rating_vector(user_id_other)
                common = (u1 != 0) & (u2 != 0)
                new_u1 = u1[common] - self.items_mean_rating[common]
                new_u2 = u2[common] - self.items_mean_rating[common]
                sim = cosine_based(new_u1, new_u2)
                rating = self.rating_reader.get_rating(user_id_other, item_id)
                similarity.append((sim, rating))
        sorted(similarity, key=lambda x: x[0], reverse=True)
        return similarity


    def predict(self):
        for user_id, item_id, rating in self.rating_reader.get_training_set():
            predict = self.__predict_one(user_id, item_id)


if __name__ == '__main__':
    rating_file = '../Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k_fold=5)
    user_cf = UserCf(rr, k_neighbor=30)
