import time
import numpy as np
import pandas  as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
from bs4 import BeautifulSoup
import math
from sklearn import datasets, svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from mpl_toolkits.mplot3d import Axes3D
import random
from sklearn.model_selection import train_test_split
import tensorflow as tf
import re


traindata = pd.read_csv('./originaldata.csv', encoding = 'shift_jis')
traindata['length'] = 0
traindata['vowel_rate'] = 0.0
traindata['site_num_log_bing'] = 0.0
traindata['site_num_log_yahoo'] = 0.0
traindata['learning_level'] = 0.0
traindata['word_class'] = ''
traindata['site_num_log_google'] = 0.0
print(traindata.head())


def scraping_bing(word):
    req = urllib.request.Request('https://www.bing.com/search?q=' + word, headers={'User-Agent': 'PracticalMachineLearning'})

    #print (req)

    f = urllib.request.urlopen(req)

    #print (f)

    bsObj = BeautifulSoup(f.read(), "html.parser")
    site_num_ori = bsObj.find('span', class_='sb_count').string
    site_num = int(site_num_ori.replace(',', '').replace(' 件の検索結果', ''))
    f.close()
    return math.log10(site_num)


def scraping_yahoo(word):
    num_str = str(random.randint(0, 500))
    req = urllib.request.Request('https://search.yahoo.co.jp/search?p=' + word,
                                 headers={'User-Agent': 'PracticalMachineLearning' + num_str })
    f = urllib.request.urlopen(req)
    bsObj = BeautifulSoup(f.read(), "html.parser")
    site_num_ori = str(bsObj.find('div', id = 'inf'))
    site_num_1 = re.sub(r'.*約', '', site_num_ori)
    site_num_2 = re.sub(r'件.*', '', site_num_1)
    site_num = int(site_num_2.replace(',', ''))
    f.close()
    return math.log10(site_num)
    

def scraping_weblio(word):
    req = urllib.request.Request('https://ejje.weblio.jp/content/'+ word,
                                 headers={'User-Agent': 'PracticalMachineLearning'})
#respose from server
    f = urllib.request.urlopen(req)

# bs object out of html respose
    bsObj = BeautifulSoup(f.read(), "html.parser")


    metatags = bsObj.findAll('meta')

    print(str(metatags[1]))

    word_class_1 = re.sub(r'】.*【*.*', '', str(metatags[1]))

    print(word_class_1)

    word_class = re.sub(r'.* 【', '', word_class_1)

    print(word_class)

    learning_level = bsObj.find('span', class_ = 'learning-level-content')
    f.close()
    return learning_level.string, word_class
    

def scraping_google(word):
    num_str = str(random.randint(0, 500))
    time.sleep(random.randint(1, 6))
    req = urllib.request.Request('https://www.google.com/search?q=' + word,
                                 headers={'User-Agent': 'PracticalMachineLearning' + num_str })
    f = urllib.request.urlopen(req)
    bsObj = BeautifulSoup(f.read(), "html.parser")
    site_num_ori = bsObj.find('div', id='resultStats').string
    site_num = int(site_num_ori.replace('約 ', '').replace(',', '').replace(' 件', ''))
    f.close()
    return math.log10(site_num)

#make traindata_original.csv.
for i in range(0, len(traindata.index)):
    print(str(i) + '回目')
    word = traindata.iat[i, 1]
    print(word)
    
    word_length = len(word)
    
    vowel_num = word.count('a')
    vowel_num += word.count('i')
    vowel_num += word.count('u')
    vowel_num += word.count('e')
    vowel_num += word.count('o')
            
    traindata.iat[i, 2] = word_length
    traindata.iat[i, 3] = (vowel_num / word_length)
    traindata.iat[i, 4] = scraping_bing(word)
    traindata.iat[i, 5] = scraping_yahoo(word)
    traindata.iat[i, 6], traindata.iat[i, 7] = scraping_weblio(word)
    traindata.iat[i, 8] = scraping_google(word)
    traindata.to_csv('traindata_original.csv', encoding = 'shift_jis')

#assign an integral number to each group from 0 to 4 in the ascending order of the average.
traindata = pd.read_csv('traindata_original.csv', encoding =  'shift_jis')
for i in range(0, len(traindata.index)):
    word_class = traindata.iat[i, 7]
    
    if word_class == '名詞':
        traindata.iat[i, 7] = 2
    elif word_class == '動詞':
        traindata.iat[i, 7] = 3      
    elif word_class == '形容詞':
        traindata.iat[i, 7] = 4
    elif word_class == '副詞':
        traindata.iat[i, 7] = 1
    else:
        traindata.iat[i, 7] = 0
    #save data every loop just in case.
    traindata.to_csv('traindata_original.csv', encoding =  'shift_jis')

#correlation coefficient
corr_mat = traindata.corr(method='pearson')
print(corr_mat)

#make traindata.csv by removing data whose correlation coefficient is lower than 0.5.
#I did by using Excel.
traindata = pd.read_csv('traindata.csv', encoding =  'shift_jis')
X = traindata.iloc[ : , 2:]
Y = traindata.iloc[ : , 0:1]
norm_X = (X - X.min()) / (X.max() - X.min())
Y_list = []
for i in range(0, len(Y.level)):
    Y_list.append(Y.iat[i, 0])

#PCA
pca = PCA(n_components=3)
X_proj = pca.fit_transform(norm_X)
print(X_proj)

fig = plt.figure(1, figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
axc = ax.scatter(X_proj[:,0], X_proj[:,1], X_proj[:,2], c=Y_list, s=1)
plt.colorbar(axc)
plt.show()

#CV
clf=svm.SVC(kernel='rbf')
gamma=np.logspace(-3,7,31)  
s_mean=[]
s_std=[]
for x in gamma:
    clf.gamma=x
    scores = cross_val_score(clf, X_proj, Y_list, cv=KFold(n_splits=5, shuffle=True))
    s_mean.append(scores.mean())
    s_std.append(scores.std())
    print(x)
print (s_mean)
print (s_std)


plt.figure(1, figsize=(12, 8))
plt.clf()
plt.semilogx(gamma, s_mean)
plt.semilogx(gamma, np.array(s_mean) + np.array(s_std), 'b--')
plt.semilogx(gamma, np.array(s_mean) - np.array(s_std), 'b--')
locs, labels = plt.yticks()
plt.yticks(locs, list(map(lambda x: "%g" % x, locs)))
plt.ylabel('CV score')
plt.xlabel('Parameter Gamma')
plt.ylim(0, 1)
plt.show()

#DNN
def DNN(X_proj_2, bit_Y):
    x_train, x_test, y_train, y_test = train_test_split(X_proj_2, bit_Y, test_size=0.2, random_state=None)
    data_size = len(X_proj_2.columns)
    sess = tf.InteractiveSession()
    x = tf.placeholder("float", [None, data_size])
    W = tf.Variable(tf.zeros([data_size,12]))
    b = tf.Variable(tf.zeros([12]))
    y = tf.nn.softmax(tf.matmul(x,W) + b)
    y_ = tf.placeholder("float", [None,12])
    cross_entropy = -tf.reduce_sum(y_*tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)
    
    x_y_train = pd.concat([x_train, y_train], axis=1)
    for i in range(1000):
        x_not, x_train_s, y_not, y_train_s = train_test_split(x_train, y_train, test_size=0.1, random_state=None)
        x_y_train_s = x_y_train.sample(n=1000)
        sess.run(train_step, feed_dict={x: x_y_train_s.iloc[:, :data_size], y_: x_y_train_s.iloc[:, data_size:]})

    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    return sess.run(accuracy, feed_dict={x: x_test, y_: y_test})

bit_Y = pd.DataFrame(np.zeros((len(Y.index), 12)), columns=range(1, 13))
for i in range(0, len(bit_Y.index)):
    ans = Y.iat[i, 0] 
    bit_Y.iat[i, int(ans)-1] = 1.0
X_proj_2 = pd.DataFrame(X_proj)
print(X_proj_2)


accuracy_sum = 0.0
for i in range(5):
    accuracy_sum += DNN(X_proj_2, bit_Y)
print('accuracy:' + accuracy_sum/5)

if __name__ == "__main__":
    main()