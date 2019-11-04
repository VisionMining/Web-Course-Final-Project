import csv
import random
import numpy as np
import copy


class RatingReader:
    """
    This class is used to read and manipulate rating triplet data.\n
    :Notice: rating data is a csv file separate by semicolon(;).\n
    :Format: user-id([0,user num-1]);item-id([0,item num-1]);rating([1,10])
    """

    def __init__(self, rating_file_name, k_fold=5):
        """
        :param k_fold: k fold cross validation
        :type k_fold: int
        :param rating_file_name: rating file name
        :type rating_file_name: str
        """
        self.__rating_file_name = rating_file_name
        self.k_fold = k_fold
        self.__rand = random.Random(0)

        self.__user_num = 0
        self.__item_num = 0
        self.__user_adj_lists = {}
        self.__construct_user_adj_lists_by_rating_file()

        self.__training_set = []
        self.__test_set = []
        self.__split_training_test_set_by_user()

        self.__training_user_adj = [None] * self.__user_num
        self.__training_item_adj = [None] * self.__item_num
        self.__construct_training_user_adj_lists_by_training_set()
        self.__construct_training_item_adj_lists_by_training_set()

        self.__users_mean_rating = [0.0] * self.__user_num
        self.__items_mean_rating = [0.0] * self.__item_num
        self.__compute_users_mean_rating()
        self.__compute_items_mean_rating()

    def __construct_user_adj_lists_by_rating_file(self):
        with open(self.__rating_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            header = next(csv_reader, None)
            for row in csv_reader:
                user_id = int(row[0])
                item_id = int(row[1])
                rating = float(row[2])
                self.__user_num = max(self.__user_num, user_id + 1)
                self.__item_num = max(self.__item_num, item_id + 1)
                if user_id in self.__user_adj_lists:
                    self.__user_adj_lists[user_id].append((item_id, rating))
                else:
                    self.__user_adj_lists[user_id] = [(item_id, rating)]
            print(header)

    def __split_training_test_set_by_user(self):
        for user_id in range(self.__user_num):
            item_rating_list = self.__user_adj_lists.get(user_id)
            self.__rand.shuffle(item_rating_list)
            total_size = len(item_rating_list)
            split_size = total_size // self.k_fold
            for idx in range(total_size):
                item_id, rating = item_rating_list[idx]
                if idx < split_size:
                    self.__test_set.append((user_id, item_id, rating))
                else:
                    self.__training_set.append((user_id, item_id, rating))

    def __construct_training_user_adj_lists_by_training_set(self):
        for user_id, item_id, rating in self.__training_set:
            if self.__training_user_adj[user_id] is None:
                self.__training_user_adj[user_id] = {item_id: rating}
            else:
                self.__training_user_adj[user_id][item_id] = rating

    def __construct_training_item_adj_lists_by_training_set(self):
        for user_id, item_id, rating in self.__training_set:
            if self.__training_item_adj[item_id] is None:
                self.__training_item_adj[item_id] = {user_id: rating}
            else:
                self.__training_item_adj[item_id][user_id] = rating

    def __compute_users_mean_rating(self):
        for user_id in range(self.__user_num):
            ratings = self.__training_user_adj[user_id].values()
            if len(ratings) > 0:
                self.__users_mean_rating[user_id] = sum(ratings) / len(ratings)

    def __compute_items_mean_rating(self):
        for item_id in range(self.__item_num):
            if self.__training_item_adj[item_id] is None:
                continue
            ratings = self.__training_item_adj[item_id].values()
            self.__items_mean_rating[item_id] = sum(ratings) / len(ratings)

    def get_user_num(self):
        return self.__user_num

    def get_item_num(self):
        return self.__item_num

    def contains_rating(self, user_id, item_id):
        return item_id in self.__training_user_adj[user_id]

    def get_rating(self, user_id, item_id):
        if self.contains_rating(user_id, item_id):
            return self.__training_user_adj[item_id][item_id]
        else:
            return 0.0

    def get_user_rating_vector(self, user_id):
        user_vector = np.zeros(self.__item_num, dtype=float)
        for item_id, rating in self.__training_user_adj[user_id].items():
            user_vector[item_id] = rating
        return user_vector

    def get_item_rating_vector(self, item_id):
        item_vector = np.zeros(self.__user_num, dtype=float)
        for user_id, rating in self.__training_item_adj[item_id].items():
            item_vector[user_id] = rating
        return item_vector

    def get_users_mean_rating(self):
        return np.array(self.__users_mean_rating, dtype=float)

    def get_items_mean_rating(self):
        return np.array(self.__items_mean_rating, dtype=float)

    def get_training_set(self):
        if len(self.__training_set) == 0:
            for user_id in range(self.__user_num):
                for item_id, rating in self.__training_user_adj[user_id].items():
                    self.__training_set.append((user_id, item_id, rating))
        return copy.deepcopy(self.__training_set)

    def get_test_set(self):
        return copy.deepcopy(self.__test_set)

    def __str__(self):
        return f'user num: {self.__user_num}, item num: {self.__item_num}\n' \
            f'user adj lists: {self.__user_adj_lists[1]}\n' \
            f'train set user: {self.__training_user_adj[1]}\n' \
            f'train set item: {self.__training_item_adj[93649]}\n' \
            f'data size: {len(self.get_training_set())+len(self.get_test_set())}'


if __name__ == "__main__":
    rating_file = 'Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k_fold=5)
    print(rr)
    print(rr.get_user_rating_vector(1)[93649])
    print(rr.get_item_rating_vector(93649)[1])
    print('complete')
