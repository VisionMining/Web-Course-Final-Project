import numpy as np
import sys

sys.path.append('..')

from rating_reader import RatingReader


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

    def predict(self):
        res = []
        for user_id, item_id, rating in self.rating_reader.get_test_set():
            # print(user_id, item_id)
            predict = self.__predict_one(user_id, item_id)
            res.append((predict, rating))
            print(predict, rating)

    def __predict_one(self, user_id, item_id):
        similarity_for_one_user = self.__compute_similarity_score_for_one_user(user_id, item_id)
        weighted_sum, similarity_sum = 0.0, 0.0
        for top_k in range(self.k_neighbor):
            if top_k >= len(similarity_for_one_user):
                break
            similarity = similarity_for_one_user[top_k][0]
            user_id_similar = similarity_for_one_user[top_k][1]
            rating = self.rating_reader.get_rating(user_id_similar, item_id)
            weighted_sum += (rating-self.users_mean_rating[user_id_similar]) * similarity
            similarity_sum += similarity
        if weighted_sum == 0 or similarity_sum == 0:
            predict = self.users_mean_rating[user_id]
        else:
            predict = self.users_mean_rating[user_id] + weighted_sum/similarity_sum
        return predict

    def __compute_similarity_score_for_one_user(self, user_id, item_id):
        similarity = []
        u1 = self.rating_reader.get_user_rating_vector(user_id)
        for user_id_other in range(self.user_num):
            if self.rating_reader.contains_rating(user_id_other, item_id):
                u2 = self.rating_reader.get_user_rating_vector(user_id_other)
                common = (u1 != 0) & (u2 != 0)
                if sum(common) == 0:
                    continue
                new_u1 = u1[common] - self.users_mean_rating[user_id] + 0.000001
                new_u2 = u2[common] - self.users_mean_rating[user_id_other] + 0.000001
                sim = np.dot(new_u1, new_u2) / (np.linalg.norm(new_u1, 2)*np.linalg.norm(new_u2, 2))
                similarity.append((sim, user_id_other))
        similarity = sorted(similarity, key=lambda x: x[0], reverse=True)
        return similarity


if __name__ == '__main__':
    rating_file = '../Processed-Data/mapped-ratings.csv'
    rating_reader = RatingReader(rating_file, k_fold=5)
    user_cf = UserCf(rating_reader, k_neighbor=30)
    user_cf.predict()

