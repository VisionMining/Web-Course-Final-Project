import csv
import random


class RatingReader:
    """
    This class is used to read and manipulate rating triplet data.\n
    :Notice: rating data is a csv file separate by semicolon(;).\n
    :Format: user-id([0,user num-1]);item-id([0,item num-1]);rating([1,10])
    """

    def __init__(self, rating_file_name, k=5):
        """
        :param rating_file_name: rating file name
        :type rating_file_name: str
        """
        self.rand = random.Random(0)
        self.k_fold = k
        self.rating_file_name = rating_file_name
        self.user_num = 0
        self.item_num = 0
        self.rating_triplet = []
        self.read_rating()  # initial user num, item num and rating triplet
        self.user_id_based_adj_lists = [None] * self.user_num
        self.construct_user_id_based_adj_lists()
        self.train_set = [None] * self.user_num
        self.test_set = [None] * self.user_num
        # self.construct_item_id_based_adj_lists()
        self.user_max_rating_num = 0
        self.user_min_rating_num = 1000000

    def read_rating(self):
        with open(self.rating_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            header = next(csv_reader, None)
            for row in csv_reader:
                user_id = int(row[0])
                item_id = int(row[1])
                rating = int(row[2])
                self.user_num = max(self.user_num, user_id + 1)
                self.item_num = max(self.item_num, item_id + 1)
                self.rating_triplet.append([user_id, item_id, rating])
            print(header)

    def construct_user_id_based_adj_lists(self):
        for row in self.rating_triplet:
            user_id = row[0]
            item_id = row[1]
            rating = row[2]
            if self.user_id_based_adj_lists[user_id] is None:
                self.user_id_based_adj_lists[user_id] = ([item_id], [rating])
            else:
                self.user_id_based_adj_lists[user_id][0].append(item_id)
                self.user_id_based_adj_lists[user_id][1].append(rating)

    def generate_train_test_set(self):
        for user_id in len(self.user_id_based_adj_lists):
            self.rand.shuffle(self.user_id_based_adj_lists[user_id])
            total_size = len(self.user_id_based_adj_lists[user_id])
            split_size = len(self.user_id_based_adj_lists[user_id]) // self.k_fold
            self.train_set[user_id] = self.user_id_based_adj_lists[user_id][split_size:total_size]
            self.test_set[user_id] = self.user_id_based_adj_lists[user_id][0:split_size]
            self.user_max_rating_num = max(self.user_max_rating_num, total_size)
            self.user_min_rating_num = min(self.user_min_rating_num, total_size)

    def __str__(self):
        return f'user num: {self.user_num}, itme num: {self.item_num}, rating triplet: {self.rating_triplet[0:3]}\n' \
               f'user id based adj lists: {self.user_id_based_adj_lists[1002:1005]}\n'


if __name__ == "__main__":
    rating_file = 'Processed-Data/mapped-ratings.csv'
    rr = RatingReader(rating_file, k=5)
    print(rr)
    print('complete')
