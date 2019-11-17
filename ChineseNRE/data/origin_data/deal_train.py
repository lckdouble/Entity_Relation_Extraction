#coding:utf8
import codecs
import sys
import pandas as pd
import numpy as np
from collections import deque  
import pdb

relation2id = {}
with codecs.open('relation2id.txt','r','utf-8') as input_data:
    for line in input_data.readlines():
        relation2id[line.split()[0]] = int(line.split()[1])
    input_data.close()
    #print relation2id



# 处理数据，将实体1、实体2与每个词的相对位置找出来，并把标签和句子本身存起来
datas = deque()
labels = deque()
positionE1 = deque()
positionE2 = deque()
count = [0,0,0,0,0]   # 存储每个关系出现次数
total_data=0
with codecs.open('train.txt','r','utf-8') as tfc:
    for lines in tfc:
        line = lines.split()
        # 要求每个关系的训练实例不超过80%
        num=[0,0,0,0,0]
        num[0] = 48
        num[1] = 32
        num[2] = 78
        num[3] = 43
        num[4] = 76

        if count[relation2id[line[2]]] <num[relation2id[line[2]]]*0.9:
            sentence = []
            index1 = line[3].index(line[0])   # 找出第一个实体在句子的位置
            position1 = []
            index2 = line[3].index(line[1])   # 找出第二个实体在句子的位置
            position2 = []

            for i,word in enumerate(line[3]):
                sentence.append(word)
                position1.append(i-index1)    # 找出每个词与第一个实体与第二个实体的相对距离
                position2.append(i-index2)
                i+=1
            datas.append(sentence)    # 训练数据加进去
            labels.append(relation2id[line[2]])    # 加标签
            positionE1.append(position1)   # 加实体1的相对位置
            positionE2.append(position2)   # 加实体2的相对位置
        count[relation2id[line[2]]]+=1
        total_data+=1
        
print(total_data,len(datas))
#################

# from compiler.ast import flatten
import collections
def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

# 这里是把所有的word转化为id存起来

print(flatten(["junk",["nested stuff"],[],[[]]]))
all_words = flatten(datas)
sr_allwords = pd.Series(all_words)
sr_allwords = sr_allwords.value_counts()

set_words = sr_allwords.index
set_ids = range(1, len(set_words)+1)
word2id = pd.Series(set_ids, index=set_words)
id2word = pd.Series(set_words, index=set_ids)

word2id["BLANK"]=len(word2id)+1
word2id["UNKNOW"]=len(word2id)+1
id2word[len(id2word)+1]="BLANK"
id2word[len(id2word)+1]="UNKNOW"
#print "word2id",id2word

max_len = 50
def X_padding(words):
    """把 words 转为 id 形式，并自动补全位 max_len 长度。"""
    ids = []
    for i in words:
        if i in word2id:
            ids.append(word2id[i])
        else:
            ids.append(word2id["UNKNOW"])
    if len(ids) >= max_len: 
        return ids[:max_len]
    ids.extend([word2id["BLANK"]]*(max_len-len(ids))) 

    return ids

def pos(num):
    if num<-40:
        return 0
    if num>=-40 and num<=40:
        return num+40
    if num>40:
        return 80

def position_padding(words):
    words = [pos(i) for i in words]
    if len(words) >= max_len:  
        return words[:max_len]
    words.extend([81]*(max_len-len(words))) 
    return words


# 处理数据，把words转化为id形式并补全最大长度
df_data = pd.DataFrame({'words': datas, 'tags': labels,'positionE1':positionE1,'positionE2':positionE2}, index=range(len(datas)))
df_data['words'] = df_data['words'].apply(X_padding)
df_data['tags'] = df_data['tags']
df_data['positionE1'] = df_data['positionE1'].apply(position_padding)
df_data['positionE2'] = df_data['positionE2'].apply(position_padding)

datas = np.asarray(list(df_data['words'].values))
labels = np.asarray(list(df_data['tags'].values))
positionE1 = np.asarray(list(df_data['positionE1'].values))
positionE2 = np.asarray(list(df_data['positionE2'].values))

print(datas.shape)
print(labels.shape)
print(positionE1.shape)
print(positionE2.shape)


import pickle
with open('../processed_data/entity_gingko_train.pkl', 'wb') as outp:
	pickle.dump(word2id, outp)
	pickle.dump(id2word, outp)
	pickle.dump(relation2id, outp)
	pickle.dump(datas, outp)
	pickle.dump(labels, outp)
	pickle.dump(positionE1, outp)
	pickle.dump(positionE2, outp)
print('** Finished saving the data.')



datas = deque()
labels = deque()
positionE1 = deque()
positionE2 = deque()
count = [0,0,0,0,0]
with codecs.open('train.txt','r','utf-8') as tfc:
    for lines in tfc:
        line = lines.split()
        # 其实是在划分数据集
        num=[0,0,0,0,0]
        num[0] = 48
        num[1] = 32
        num[2] = 78
        num[3] = 43
        num[4] = 76
        if count[relation2id[line[2]]] >=0.9*num[relation2id[line[2]]]:
            sentence = []
            index1 = line[3].index(line[0])
            position1 = []
            index2 = line[3].index(line[1])
            position2 = []

            for i,word in enumerate(line[3]):
                sentence.append(word)
                position1.append(i-3-index1)
                position2.append(i-3-index2)
                i+=1
            datas.append(sentence)
            labels.append(relation2id[line[2]])
            positionE1.append(position1)
            positionE2.append(position2)
        count[relation2id[line[2]]]+=1
        
        
        
df_data = pd.DataFrame({'words': datas, 'tags': labels,'positionE1':positionE1,'positionE2':positionE2}, index=range(len(datas)))
df_data['words'] = df_data['words'].apply(X_padding)
df_data['tags'] = df_data['tags']
df_data['positionE1'] = df_data['positionE1'].apply(position_padding)
df_data['positionE2'] = df_data['positionE2'].apply(position_padding)

datas = np.asarray(list(df_data['words'].values))
labels = np.asarray(list(df_data['tags'].values))
positionE1 = np.asarray(list(df_data['positionE1'].values))
positionE2 = np.asarray(list(df_data['positionE2'].values))


import pickle

with open('../processed_data/entity_gingko_test.pkl', 'wb') as outp:
    pickle.dump(datas, outp)
    pickle.dump(labels, outp)
    pickle.dump(positionE1, outp)
    pickle.dump(positionE2, outp)
print('** Finished saving the data.')


