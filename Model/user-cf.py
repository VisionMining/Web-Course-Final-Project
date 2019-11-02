import numpy as np
import sys

sys.path.append('..')

from ratingReader import RatingReader
from utility import adjust_cosine, cosine_based, correlation_based


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

    def __compute_similarity(self, ):
        pass

    def __predict_one(self, user, item):
        u1 = self.rating_reader.get_user_rating_vector(user)
        for user_other in range(self.user_num):
            if self.rating_reader.contains_rating(user_other, item):
                u2 = self.rating_reader.get_user_rating_vector(user_other)

    def predict(self):
        for user, item, rating in self.rating_reader.get_training_set():
            pass

if __name__ == '__main__':
    rating_file = 'Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k_fold=5)
    user_cf = UserCf(rr, k_neighbor=30)