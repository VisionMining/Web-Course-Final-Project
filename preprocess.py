import csv


def filter_rating_by_zero(input_file_name, output_file_name):
    filtered_ratings = []
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            if row[2] != '0':
                filtered_ratings.append([row[0], row[1], row[2]])
        print(header)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['user-id', 'item-id', 'rating'])
        for rating in filtered_ratings:
            writer.writerow(rating)
    print('filter rating data by zero')


def compute_save_user_map(input_file_name, output_file_name):
    user_set = set()
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            user_set.add(row[0])
        print(header)
    user_list = list(user_set)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['original-user-id', 'mapped-user-id'])
        for i in range(len(user_list)):
            writer.writerow([user_list[i], i])
    print('compute and save user map complete')


def compute_save_item_map(input_file_name, output_file_name):
    item_set = set()
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            item_set.add(row[1])
        print(header)
    item_list = list(item_set)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['original-item-id', 'mapped-item-id'])
        for i in range(len(item_list)):
            writer.writerow([item_list[i], i])
    print('compute and save item map complete')


def get_user_item_map(user_map_file_name, item_map_file_name):
    user_map_dict = {}
    with open(user_map_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            user_map_dict[row[0]] = row[1]
        print(header)
    item_map_dict = {}
    with open(item_map_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            item_map_dict[row[0]] = row[1]
        print(header)
    return user_map_dict, item_map_dict


def compute_save_mapped_rating(user_map_dict, item_map_dict, input_file_name, output_file_name):
    mapped_ratings = []
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            mapped_ratings.append([user_map_dict[row[0]], item_map_dict[row[1]], row[2]])
        print(header)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['mapped-user-id', 'mapped-item-id', 'rating'])
        for rating in mapped_ratings:
            writer.writerow(rating)
    print('computer and save mapped rating data complete')


if __name__ == "__main__":
    raw_rating_data_file = 'Raw-Data/BX-Book-Ratings.csv'
    user_map_file = 'Processed-Data/user-map.csv'
    item_map_file = 'Processed-Data/item-map.csv'
    mapped_rating_data_file = 'Processed-Data/mapped-ratings.csv'
    no_zero_rating_data_file = 'Processed-Data/no-zero-ratings.csv'

    filter_rating_by_zero(raw_rating_data_file, no_zero_rating_data_file)
    compute_save_user_map(no_zero_rating_data_file, user_map_file)
    compute_save_item_map(no_zero_rating_data_file, item_map_file)
    user_map, item_map = get_user_item_map(user_map_file, item_map_file)
    compute_save_mapped_rating(user_map, item_map, no_zero_rating_data_file, mapped_rating_data_file)
    print('complete')
