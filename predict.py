import os
from erisk2018data.handler import Task
import configparser
import pickle as pkl
import numpy as np
from os.path import join
import sys

configs = configparser.ConfigParser()
configs.read('config.cfg')

models_dir = 'models'
pred_directory = sys.argv[1]

# DATA
task = Task(configs['Data']['task'])
pipeline_file = configs['Model'].get('clf')
model = pkl.load(open(pipeline_file, 'rb'))

print('TEST')
threshold = float(configs['Model']['threshold'])
shrink = float(configs['Model']['shrinking_ratio'])
decide = configs['Testing'].get('decide', None)

print('threshold: ', threshold)
print('shrinking ratio: ', shrink)
print('decide ', decide)
for chunk in range(1, int(sys.argv[2])+1):
    training = task.get_split(configs['Data']['split'], part='test', chunks=chunk)
    ids, test_y, test_x = map(list, zip(*training))
    posts = list(map(len, test_x))
    test_x = [' '.join(user) for user in test_x]
    # test_x = vectorizer.transform(test_x)
    # test_x = lda.transform(test_x)
    # pred_proba = clf.predict_proba(test_x)
    pred_proba = model.predict_proba(test_x)
    with open(os.path.join(pred_directory, 'UQAMA_{}.txt').format(chunk), 'w') as f:
        for uid, prob, num_of_posts in zip(ids, pred_proba, posts):
            decision = np.argmax(prob)
            if not decide:
                f.write('{}\t\t{}\t\t{}\n'.format(uid, 2 - decision, max(*prob)))
            elif max(*prob) > threshold or chunk >= 10:
                f.write('{}\t\t{}\n'.format(uid, 2 - decision))
            else:
                f.write('{}\t\t{}\n'.format(uid, 0))
        f.close()
    threshold *= shrink


