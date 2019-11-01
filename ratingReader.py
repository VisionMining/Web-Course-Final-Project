import csv
import random
import numpy as np


class RatingReader:
    """
    This class is used to read and manipulate rating triplet data.\n
    :Notice: rating data is a csv file separate by semicolon(;).\n
    :Format: user-id([0,user num-1]);item-id([0,item num-1]);rating([1,10])
    """

    def __init__(self, rating_file_name, k_fold=5):
        """
        :param rating_file_name: rating file name
        :type rating_file_name: str
        """
        self.rand = random.Random(0)
        self.k_fold = k_fold
        self.__rating_file_name = rating_file_name

        self.user_num = 0
        self.item_num = 0
        self.__user_adj_lists = {}
        self.__construct_user_adj_lists_by_rating_file()

        self.__training_user_adj = [None] * self.user_num
        self.__training_item_adj = [None] * self.item_num
        self.__training_set = []
        self.__test_set = []
        self.__split_train_test_set_by_user()
        self.__construct_item_adj_lists_by_training_user_adj()

        self.user_max_rating_num = 0
        self.user_min_rating_num = 1000000

    def __construct_user_adj_lists_by_rating_file(self):
        with open(self.__rating_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            header = next(csv_reader, None)
            for row in csv_reader:
                user_id = int(row[0])
                item_id = int(row[1])
                rating = float(row[2])
                self.user_num = max(self.user_num, user_id + 1)
                self.item_num = max(self.item_num, item_id + 1)
                if user_id in self.__user_adj_lists:
                    self.__user_adj_lists[user_id].append((item_id, rating))
                else:
                    self.__user_adj_lists[user_id] = [(item_id, rating)]
            print(header)

    def __split_train_test_set_by_user(self):
        for user_id, item_rating_list in self.__user_adj_lists.items():
            self.rand.shuffle(item_rating_list)
            total_size = len(item_rating_list)
            split_size = total_size // self.k_fold
            self.__training_user_adj[user_id] = dict(item_rating_list[split_size:total_size])
            for item_id, rating in item_rating_list[0:split_size]:
                self.__test_set.append((user_id, item_id, rating))

    def __construct_item_adj_lists_by_training_user_adj(self):
        for user_id in range(self.user_num):
            for item_id, rating in self.__training_user_adj[user_id].items():
                if self.__training_item_adj[item_id] is None:
                    self.__training_item_adj[item_id] = {user_id: rating}
                else:
                    self.__training_item_adj[item_id][user_id] = rating

    def contain_rating(self, user_id, item_id):
        return item_id in self.__training_user_adj[user_id]

    def get_user_rating_vector(self, user_id):
        user_vector = np.zeros(self.item_num, dtype = float)
        for item_id, rating in self.__training_user_adj[user_id].items():
            user_vector[item_id] = rating
        return user_vector

    def get_item_rating_vector(self, item_id):
        item_vector = np.zeros(self.user_num, dtype = float)
        for user_id, rating in self.__training_item_adj[item_id].items():
            item_vector[user_id] = rating
        return item_vector

    def get_training_set(self):
        if len(self.__training_set) == 0:
            for user_id in range(self.user_num):
                for item_id, rating in self.__training_user_adj[user_id].items():
                    self.__training_set.append((user_id, item_id, rating))
        return self.__training_set

    def get_test_set(self):
        return self.__test_set

    def __str__(self):
        return f'user num: {self.user_num}, itme num: {self.item_num}\n' \
            f'user adj lists: {self.__user_adj_lists[6998]}\n' \
            f'train set user: {self.__training_user_adj[6998]}\n' \
            f'train set item: {self.__training_item_adj[73256]}\n' \
            f'train set: {self.get_training_set()[0:3]}\n' \
            f'test set: {self.get_test_set()[0:3]}\n' \


if __name__ == "__main__":
    rating_file = 'Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k_fold=5)
    print(rr)
    print('complete')
