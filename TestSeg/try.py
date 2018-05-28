import re
import numpy as np
import pandas as pd
from keras.utils import np_utils
#from keras.models import load_model
#训练模型时需要的包
from keras.layers import Dense,Embedding,LSTM,TimeDistributed,Input,Bidirectional
from keras.models import Model

# 用于存放数据和各种标签,chars统计所有字，还有每个字的编号
data = []
label = []
chars = []
#Series是一个包含行索引的数组
tag = pd.Series({'s': 0, 'b': 1 , 'm': 2 , 'e': 4 , 'x': 4 })
#建模参数
maxlen = 32
word_size = 128

def clean(s): #整理一下数据，有些不规范的地方，去掉了单独存在的引号
    if u'“/s' not in s:
        return s.replace(u'”/s', '')
    elif u'”/s' not in s:
        return s.replace(u'“/s', '')
    elif u'‘/s' not in s:
        return s.replace(u'’/s', '')
    elif u'’/s' not in s:
        return s.replace(u'‘/s', '')
    else:
        return s

def get_xy(s):
    s = re.findall('(.)/(.)' , s)
    if s:
        s = np.array(s)
        return list(s[:,0]),list(s[:,1])

#读取数据
s = open('msr_train.txt').read()
s = s.split("\r\n")
s = u''.join(map(clean,s))#map函数就是将s中的每个元素都使用一次clean函数
s = re.split(u'[，。！？、]/[bmes]',s)

#数据预处理
for i in s:
    x = get_xy(i)
    if x:
        data.append(x[0])
        label.append(x[1])
#one-hot，reshape((-1,1))就是将行向量转换为列向量
def trans_one(x):
    _ = map(lambda y: np_utils.to_categorical(y,5),tag[x].values.reshape((-1,1)))
    _ = list(_)
    _.extend([np.array([[0,0,0,0,1]])]*(maxlen-len(x)))
    return np.array(_)

#DataFrame也是一个数组，但是既包含行索引也包含列索引
d = pd.DataFrame(index=range(len(data)))
d['data'] = data
d['label'] = label
d = d[d['data'].apply(len) <= maxlen]#得到所有长度小于32的句子,去掉所有长度超过32的句子
d.index = range(len(d))

#统计字频，用chars存储,保存到文件，便于后续进行快速处理
for i in data:
    chars.extend(i)
chars =  pd.Series(chars).value_counts()#统计字频
chars[:] = range(1,len(chars)+1)#按词频由大到小对字进行排序

fc = open('chars.txt','w')
for i in range(len(chars)+1):
    fc.writelines(str(chars[i-1 :i]))
fc.close()

#对句子进行填充，不够maxlen长度的句子用x进行填充,x在chars中的编号记为0
d['x'] = d['data'].apply(lambda x: np.array(list(chars[x])+[0]*(maxlen-len(x))))
d['y'] = d['label'].apply(trans_one)#进行one-hot编码

#模型设计
#模型训练好，保存为model.h5文件，下次使用的时候直接导入就好。
#输入的是长度为32的一个向量，不够进行填充，
#输出也是32*5的向量，考虑填充的标签

sequence =  Input(shape=(maxlen,),dtype='int32')
embedded = Embedding(len(chars)+1,word_size,input_length=maxlen,mask_zero=True)(sequence)
blstm = Bidirectional(LSTM(64,return_sequences=True),merge_mode='sum')(embedded)
output = TimeDistributed(Dense(5,activation='softmax'))(blstm)
model = Model(inputs=sequence,outputs=output)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
batch_size = 1024
history = model.fit(np.array(list(d['x'])),np.array(list(d['y'])).reshape((-1,maxlen,5)),batch_size=batch_size,nb_epoch=20)
model.save('model.h5')
#转移概率，单纯使用等概率，可以考虑进行修改

#model = load_model('model.h5')
zy = {'be':0.5, 'bm':0.5, 'eb':0.5, 'es':0.5,
      'me': 0.5, 'mm':0.5, 'sb':0.5, 'ss':0.5}
zy = {i:np.log(zy[i]) for i in zy.keys()}
#自己测试模型,好像不需要input层，直接输入就可以，不过具体怎么样还要经过验证
#model_my = Sequential()
#model_my.add(Input(shape=(maxlen,),dtype='int32'))
#model_my.add(Embedding(len(chars)+1, word_size, input_length=maxlen, mask_zero=True))
#model_my.add(Bidirectional(LSTM(64,return_sequences=True),merge_mode='sum'))
#model_my.add(TimeDistributed(Dense(5,activation='softmax')))
'''
def viterbi(nodes):
    #第一个字不是b就是s,
    paths = {'b':nodes[0]['b'],'s':nodes[0]['s']}
    for l in range(1,len(nodes)):
        paths_ = paths.copy()          #保存上一次操作的结果
        paths = {}                     #path用于保存结果
        for i in nodes[l].keys():     #取第L个字的概率分布
            nows = {}  #nows用于保存结果
            for j in paths_.keys():   #将上一个字的可能概率一次进行尝试
                if j[-1]+i in zy.keys():   #如果前一个字和后一个字的标签符合zy的要求，计算出现概率
                    nows[j+i] = paths_[j]+nodes[l][i]+zy[j[-1]+i]
            k = max(nows,key=nows.get)   #argmax计算列表中最大值的索引
            paths[k] = nows[k]
    #return list(paths.keys())[list(paths.values()).index(np.argmax(paths.values()))]
    return list(max(paths,key=paths.get))

#用于将句子转化为向量，one-hot编码
def ch2list(s):
    result = []
    for i in s:
        result.append(chars.index(i)+1)
    for i in range(maxlen-len(s)):
        result.append(0)
    return result
#对单个句子进行分词
def simple_cut(s):
    if s:
        #ch要reshape一下才能够输入到predict函数中。
        ch = ch2list(s)
        ch = np.array(ch).reshape((-1,maxlen))
        r = model.predict(ch,verbose=False)[0][:len(s)]#后面这两个方括号取值，保证输出长度为源字符串长度。
        r = np.log(r)
        #nodes表示句子中每个字对应四个标签的概率
        #zip函数相当于把多有传递进来的参数的相同位置的内容放在一个元组内，返回是一个包含多个元祖的元祖
        #假设传进来三个参数，相当于三个列表传了进来，那么去三个列表的第一个元素形成一个元祖，去三个列表第二个元素形成另一个元祖
        #最终组合成的多个元组形成一个新的元组返回。子元组的个数有最短元组决定
        nodes = [dict(zip(['s','b','m','e'],i[:4]))for i in r]
        print(nodes)
        #经过zip压缩后，nodes为一个4维矩阵，代表sbme的向量标签
        t=viterbi(nodes)
        words = []
        for i in range(len(s)):
            print(i)
            if t[i] in ['s','b']:
                words.append(s[i])
            else:
                words[-1] += s[i]
        return words
    else:
        return []
#标点符号划分
not_cuts = re.compile('([\da-zA-Z]+)|[。，,、？！.?!]]')
#先按照标点符号将段落切分为句子，然后对每个句子进行分词。
def cut_word(s):
    result = []
    s = re.sub('[,.!?，。！？、]',' ',s)
    s = s.split()
    for i in s:
        result.extend(simple_cut(list(i)))
    return result

if __name__ == '__main__':
    print(cut_word("今天天气很好，我们玩的都很开心。"))'''