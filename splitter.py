from sklearn.model_selection import train_test_split
import csv
import sys
import os
import string

data_root = sys.argv[1]
users = []
labels = []

with open(os.path.join(data_root, 'risk_golden_truth.txt')) as file:
    for row in csv.reader(file, delimiter='\t'):
        if len(row) == 2:
            users.append(row[0])
            labels.append(row[1])
split_names = string.ascii_letters[:int(sys.argv[2])]
splits_dir = os.path.join(data_root, 'splits')
for name in split_names:
    split_dir = os.path.join(splits_dir, name)
    os.makedirs(split_dir)
    train_path = os.path.join(splits_dir, name, 'train.csv')
    test_path = os.path.join(splits_dir, name, 'test.csv')
    train_users, test_users, train_labels, test_labels = train_test_split(users, labels, test_size=float(sys.argv[3]),
                                                                          stratify=labels)

    with open(train_path, 'w') as file:
        writer = csv.writer(file, delimiter='\t')
        for user, label in zip(train_users, train_labels):
            writer.writerow([user, label])
        file.close()

    with open(test_path, 'w') as file:
        writer = csv.writer(file, delimiter='\t')
        for user, label in zip(test_users, test_labels):
            writer.writerow([user, label])
        file.close()

