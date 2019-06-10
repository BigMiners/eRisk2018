from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
from erisk2018data.handler import Task
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import Pipeline
import configparser
from random import shuffle
import pickle as pkl
from os.path import join

configs = configparser.ConfigParser()
configs.read('config.cfg')

# DATA
path_to_task = configs['Data']['task']
task = Task(path_to_task)
task_number = path_to_task[-1]
split = configs['Data']['split']
training = task.get_split(split, part='train', chunks=10)
_, labels, users = map(list, zip(*training))

posts = [post for user in users for post in user]
posts = list(filter(lambda p: len(p.split()) > 15, posts))

labels, users = zip(*filter(lambda p: len(p[1]) > 10, zip(labels, users)))
users = [' '.join(user) for user in users]


#### VECTORIZER #####

print('TF')
vectorizer_file = configs['Feature'].get('vectorizer', None)
if vectorizer_file:
    print('loading...')
    vectorizer = pkl.load(open(vectorizer_file, 'rb'))
else:
    print('building...')
    vectorizer = TfidfVectorizer(analyzer='word', strip_accents='ascii', ngram_range=(1, 3),
                                 stop_words='english', max_features=3000, use_idf=True)
    vectorizer.fit(posts)
    pkl.dump(vectorizer, open('tf{}_{}.p'.format(task_number, split), 'wb'))
print('done.')


#### LDA #####

print('LDA')
lda_file = configs['Feature'].get('lda')
if lda_file:
    print('loading...')
    lda = pkl.load(open(lda_file, 'rb'))
else:
    print('building...')
    lda = LatentDirichletAllocation(n_components=30, learning_method='online')
    lda.fit(vectorizer.transform(posts))
    pkl.dump(lda, open('lda_{}_{}.p'.format(task_number, split), 'wb'))
print('done.')


#### CLF #####

print('CLF')
mlp_file = configs['Model'].get('mlp')
if mlp_file:
    print('loading...')
    mlp = pkl.load(open(mlp_file, 'rb'))
else:
    if bool(configs['Training']['undersample']):
        print('undersampling')
        positives = list(filter(lambda s: s[0] == '1', zip(labels, users)))
        negatives = list(filter(lambda s: s[0] == '0', zip(labels, users)))
        shuffle(negatives)
        both = positives + negatives[:len(positives)]
        shuffle(both)
        labels, users = map(list, zip(*both))

    mlp = MLPClassifier(hidden_layer_sizes=(60, 30), max_iter=1500, activation='identity', solver='adam')

    print('training...')
    mlp.fit(lda.transform(vectorizer.transform(users)), labels)
    pkl.dump(mlp, open('clf_{}_{}.p'.format(task_number, split), 'wb'))
    print('done.')

print('saving...')
clf = Pipeline([('tf', vectorizer), ('lda', lda), ('mlp', mlp)])
pkl.dump(clf, open('pipeline_{}_{}.p'.format(task_number, split), 'wb'))
print('done')

print('VALIDATION')
training = task.get_split(configs['Data']['split'], part='test', chunks=10)
_, test_y, test_x = map(list, zip(*training))

test_x = [' '.join(user) for user in test_x]
pred_y = clf.predict(test_x)
print(clf.predict_proba(test_x))

print(classification_report(test_y, pred_y))

print(confusion_matrix(test_y, pred_y))