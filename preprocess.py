import csv

raw_rating_data_file = 'Raw-Data/BX-Book-Ratings.csv'
user_map_file = 'Processed-Data/user-map.csv'
item_map_file = 'Processed-Data/item-map.csv'
mapped_rating_data_file = 'Processed-Data/mapped-ratings.csv'


def compute_save_user_map():
    user_set = set()
    with open(raw_rating_data_file, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            user_set.add(row[0])
        print(header)
    user_list = list(user_set)
    with open(user_map_file, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['original-user-id', 'mapped-user-id'])
        for i in range(len(user_list)):
            writer.writerow([user_list[i], i])
    print('compute and save user map complete')


def compute_save_item_map():
    item_set = set()
    with open(raw_rating_data_file, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            item_set.add(row[1])
        print(header)
    item_list = list(item_set)
    with open(item_map_file, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['original-item-id', 'mapped-item-id'])
        for i in range(len(item_list)):
            writer.writerow([item_list[i], i])
    print('compute and save item map complete')


def get_user_item_map():
    '''

    :return:
    :rtype:
    '''
    user_map = {}
    with open(user_map_file, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader, None)
        for row in csv_reader:
            user_map[row[0]] = row[1]
        print(header)
    item_map = {}
    with open(item_map_file, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader, None)
        for row in csv_reader:
            item_map[row[0]] = row[1]
        print(header)
    return user_map, item_map


def compute_save_mapped_rating():
    user_map, item_map = get_user_item_map()
    mapped_ratings = []
    with open(raw_rating_data_file, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            mapped_ratings.append([user_map[row[0]], item_map[row[1]], row[2]])
        print(header)
    with open(mapped_rating_data_file, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['mapped-user-id', 'mapped-item-id', 'rating'])
        for rating in mapped_ratings:
            writer.writerow(rating)
    print('computer and save mapped rating data complete')


if __name__ == "__main__":
    compute_save_user_map()
    compute_save_item_map()
    compute_save_mapped_rating()
