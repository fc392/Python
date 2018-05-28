#作者：刘畅
#功能：HMM（隐马尔可夫模型）分词
#计算后接字标签最有可能出现的概率
from collections import Counter
from math import log

hmm_model = {i:Counter() for i in 'sbme'}

with open('dict.txt',encoding='utf-8') as f:
    for line in f:
        lines=line.split(' ')
        if len(lines[0]) == 1:
            hmm_model['s'][lines[0]] +=int(lines[1])
        else:
            hmm_model['b'][lines[0][0]] +=int(lines[1])
            hmm_model['e'][lines[0][-1]] += int(lines[1])
            for m in lines[0][1:-1]:
                hmm_model['m'][m] += int(lines[1])
print(hmm_model)
log_total = {i:log(sum(hmm_model[i].values())) for i in 'sbme'}
print(log_total)

trans={'ss': 0.3,'sb': 0.7,'bm': 0.3,'be': 0.7,
       'mm': 0.3,'me': 0.7,'es': 0.3,'eb': 0.7}

trans = {i:log(j) for i,j in trans.items()}


def viterbi(nodes):#nodes表示需要分词的句子中所有字的标签情况
    paths = nodes[0]#第一个字的sbme标签情况
    for l in range(1, len(nodes)):  # l表示句子中的每个字对应的偏移量
        paths_ = paths
        paths = {}
        for i in nodes[l]:
            nows = {}
            for j in paths_:
                if j[-1]+i in trans:#当前字标签和后接字标签的组合能够出现时计算出现概率。
                    nows[j+i] = paths_[j] + nodes[l][i] + trans[j[-1]+i]
            k = max(nows.values())
            paths[list(nows.keys())[list(nows.values()).index(k)]] = k#将概率最大（最有可能出现的词计算胡来）
    return list(paths.keys())[list(paths.values()).index(max(paths.values()))]# return paths.keys()[paths.values()]#.index(max(paths.values()))]

def hmm_cut(s):
    nodes = [{i:log(j[t]+1)-log_total[i] for i,j in hmm_model.items()}for t in s]
    tags = viterbi(nodes)
    print(tags)
    words = [s[0]]
    for i in range(1,len(s)):
        if tags[i] in ['b','s']:
            words.append(s[i])
        else:
            words[-1] +=s[i]
    return words

if __name__ == '__main__':
    print(hmm_cut('结婚的和尚未结婚的'))