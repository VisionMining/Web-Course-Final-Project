import csv


def filter_rating_by_zero(input_file_name, output_file_name):
    filtered_ratings = []
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            use_id = row[0]
            item_id = row[1]
            rating = row[2]
            if rating != '0':
                filtered_ratings.append([use_id, item_id, rating])
        print(header)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['user-id', 'item-id', 'rating'])
        for triplet in filtered_ratings:
            writer.writerow(triplet)
    print('filter rating data by zero')


def generate_save_user_map(input_file_name, output_file_name):
    user_set = set()
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            user_id = row[0]
            user_set.add(user_id)
        print(header)
    user_list = list(user_set)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['original-user-id', 'mapped-user-id'])
        for mapped_user_id in range(len(user_list)):
            original_user_id = user_list[mapped_user_id]
            writer.writerow([original_user_id, mapped_user_id])
    print('generate and save user map complete')


def generate_save_item_map(input_file_name, output_file_name):
    item_set = set()
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            item_id = row[1]
            item_set.add(item_id)
        print(header)
    item_list = list(item_set)
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['original-item-id', 'mapped-item-id'])
        for mapped_item_id in range(len(item_list)):
            original_item_id = item_list[mapped_item_id]
            writer.writerow([original_item_id, mapped_item_id])
    print('generate and save item map complete')


def get_user_item_map(user_map_file_name, item_map_file_name):
    """

    :param user_map_file_name:
    :type user_map_file_name: str
    :param item_map_file_name:
    :type item_map_file_name: str
    :return:
    :rtype: dict, dict
    """
    user_map_dict = {}
    with open(user_map_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            original_user_id = row[0]
            mapped_user_id = row[1]
            user_map_dict[original_user_id] = mapped_user_id
        print(header)
    item_map_dict = {}
    with open(item_map_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            original_item_id = row[0]
            mapped_item_id = row[1]
            item_map_dict[original_item_id] = mapped_item_id
        print(header)
    return user_map_dict, item_map_dict


def generate_save_mapped_rating(user_map_dict, item_map_dict, input_file_name, output_file_name):
    mapped_ratings = []
    with open(input_file_name, mode='r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = next(csv_reader, None)
        for row in csv_reader:
            mapped_user_id = int(user_map_dict[row[0]])
            mapped_item_id = int(item_map_dict[row[1]])
            rating = row[2]
            mapped_ratings.append([mapped_user_id, mapped_item_id, rating])
        print(header)
    mapped_ratings = sorted(mapped_ratings, key=lambda x: (x[0], x[1]))
    with open(output_file_name, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['mapped-user-id', 'mapped-item-id', 'rating'])
        for rating in mapped_ratings:
            writer.writerow(rating)
    print('generate and save mapped rating data complete')


if __name__ == "__main__":
    raw_rating_data_file = 'Raw-Data/BX-Book-Ratings.csv'
    user_map_file = 'Processed-Data/user-map.csv'
    item_map_file = 'Processed-Data/item-map.csv'
    mapped_rating_data_file = 'Processed-Data/mapped-ratings.csv'
    no_zero_rating_data_file = 'Processed-Data/no-zero-ratings.csv'

    filter_rating_by_zero(raw_rating_data_file, no_zero_rating_data_file)
    generate_save_user_map(no_zero_rating_data_file, user_map_file)
    generate_save_item_map(no_zero_rating_data_file, item_map_file)
    user_map, item_map = get_user_item_map(user_map_file, item_map_file)
    generate_save_mapped_rating(user_map, item_map, no_zero_rating_data_file, mapped_rating_data_file)
    print('complete')
