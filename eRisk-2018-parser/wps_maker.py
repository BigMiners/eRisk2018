import sys

all_users = {}
with open(sys.argv[1], 'r') as wpa_all:
    for line in wpa_all.readlines():
        line = line.replace('\n', '').split('\t\t')
        all_users[line[0]] = line[1]
    wpa_all.close()

relevant_users = []
with open(sys.argv[2], 'r') as relevant:
    for line in relevant.readlines():
        line = line.replace('\n', '').split('\t')
        relevant_users.append(line[0])
    relevant.close()


for user in relevant_users:
    print('{}\t\t{}'.format(user, all_users[user]))

