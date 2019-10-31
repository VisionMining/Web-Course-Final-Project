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
        self.rating_file_name = rating_file_name
        self.user_num = 0
        self.item_num = 0
        self.user_adj_lists = {}
        self.construct_user_adj_lists_by_rating_file()
        self.train_set_user_adj = [None] * self.user_num
        self.train_set_item_adj = [None] * self.item_num
        self.test_set = [None] * self.user_num
        self.user_max_rating_num = 0
        self.user_min_rating_num = 1000000
        self.split_train_test_set_by_user()
        self.construct_item_adj_lists_by_train_set_user_adj()

    def construct_user_adj_lists_by_rating_file(self):
        with open(self.rating_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            header = next(csv_reader, None)
            for row in csv_reader:
                user_id = int(row[0])
                item_id = int(row[1])
                rating = float(row[2])
                self.user_num = max(self.user_num, user_id + 1)
                self.item_num = max(self.item_num, item_id + 1)
                if self.user_adj_lists.get(user_id, None) is None:
                    self.user_adj_lists[user_id] = [(item_id, rating)]
                else:
                    self.user_adj_lists[user_id].append((item_id, rating))
            print(header)

    def split_train_test_set_by_user(self):
        for user_id, item_rating_list in self.user_adj_lists.items():
            self.rand.shuffle(item_rating_list)
            total_size = len(item_rating_list)
            split_size = total_size // self.k_fold
            self.train_set_user_adj[user_id] = item_rating_list[split_size:total_size]
            self.test_set[user_id] = item_rating_list[0:split_size]
            self.user_max_rating_num = max(self.user_max_rating_num, total_size)
            self.user_min_rating_num = min(self.user_min_rating_num, total_size)

    def construct_item_adj_lists_by_train_set_user_adj(self):
        for user_id in range(self.user_num):
            item_rating_list = self.train_set_user_adj[user_id]
            for item_id, rating in item_rating_list:
                if self.train_set_item_adj[item_id] is None:
                    self.train_set_item_adj[item_id] = [(user_id, rating)]
                else:
                    self.train_set_item_adj[item_id].append((user_id, rating))

    def get_user_rating_vector(self, user_id):
        user_vector = np.zeros(self.item_num, dtype = float)
        for item_id, rating in self.train_set_user_adj[user_id]:
            user_vector[item_id] = rating
        return user_vector

    def get_item_rating_vector(self, item_id):
        item_vector = np.zeros(self.user_num, dtype = float)
        for user_id, rating in self.train_set_item_adj[item_id]:
            item_vector[user_id] = rating
        return item_vector

    def __str__(self):
        return f'user num: {self.user_num}, itme num: {self.item_num}\n' \
               f'user max, min rating num: {self.user_max_rating_num, self.user_min_rating_num}\n' \
               f'user adj lists: {self.user_adj_lists[1002]}\n' \
               f'train set user: {self.train_set_user_adj[1002]}\n' \
               f'train set item: {self.train_set_item_adj[48229]}\n' \
               f'test set: {self.test_set[1002]}\n'


if __name__ == "__main__":
    rating_file = 'Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k_fold=5)
    print(rr)
    print('complete')
