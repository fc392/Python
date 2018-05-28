import re
import numpy as np
from keras.models import load_model

maxlen = 32
chars = []
#chars从0开始计数，索引为int存放顺序是字出现次数的多少，是一个统计概率。又因为0表示填充值的序号，所以后面再使用标签时会有一个+1过程
with open('chars.txt') as fc:
    for line in fc.readlines():
        line = line.split('\n')
        line = line[0].split()
        chars.append(line[0])
fc.close()

zy={'ss': 0.3,'sb': 0.7,'bm': 0.1,'be': 0.9,
    'mm': 0.3,'me': 0.7,'es': 0.3,'eb': 0.7}
zy = {i:np.log(zy[i]) for i in zy.keys()}

model = load_model('model.h5')

def viterbi(nodes):
    #第一个字不是b就是s,
    paths = {'b':nodes[0]['b'],'s':nodes[0]['s']}
    for l in range(1,len(nodes)):
        paths_ = paths.copy()          #保存上一次操作的结果
        paths = {}                     #path用于保存结果
        nows = {}  # nows用于保存结果
        for i in nodes[l].keys():     #取第L个字的概率分布
            for j in paths_.keys():   #将上一个字的可能概率一次进行尝试
                if j[-1]+i in zy.keys():   #如果前一个字和后一个字的标签符合zy的要求，计算出现概率
                    nows[j+i] = paths_[j]+nodes[l][i]+zy[j[-1]+i]
        print(nows,l)
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
    return np.array(result).reshape((-1,maxlen))
#对单个句子进行分词
def simple_cut(s):
    if s:
        #ch要reshape一下才能够输入到predict函数中。
        ch = ch2list(s)
        r = model.predict(ch,verbose=False)[0][:len(s)]#后面这两个方括号取值，保证输出长度为源字符串长度。
        print(r)
        r = np.log(r)
        #nodes表示句子中每个字对应四个标签的概率
        #zip函数相当于把多有传递进来的参数的相同位置的内容放在一个元组内，返回是一个包含多个元祖的元祖
        #假设传进来三个参数，相当于三个列表传了进来，那么去三个列表的第一个元素形成一个元祖，去三个列表第二个元素形成另一个元祖
        #最终组合成的多个元组形成一个新的元组返回。子元组的个数有最短元组决定
        nodes = [dict(zip(['s','b','m','e','x'],i[:5]))for i in r]
        #经过zip压缩后，nodes为一个4维矩阵，代表sbme的向量标签
        t=viterbi(nodes)
        words = []
        for i in range(len(s)):
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
    print(cut_word("结婚的和尚未结婚的"))