# coding=utf-8
import requests
from requests.exceptions import RequestException
import re
import json

url=[]
#获取url页面信息
def get_page(url):
    try:
        response = requests.get(url)
        response.encoding='gb2312'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#获取所需要爬取的信息
def get_detail(html):
    # its用于存放最终结果
    # it用于存放每个h2的结果
    its=[]
    res=[]
    #获取分类标签
    n=html.count('<li>')
    p1='<li class="this">(.*?)</li>.*?'
    p2='<li>(.*?)</li>.*?'
    for i in range(0,n-1):
        p1=p1+p2
    pattern=re.compile(p1,re.S)
    result1=re.findall(pattern,html)
    result1=result1[0]
    for num in result1:
        res.append(num)

    #根据标签获取内容
    items=html.split('</head>')[1]
    items=items.split('<div class="p_tab">')
   # print(items)
    items=items[1:11]
    ide=0
    #对每个大标签<li>进行处理
    for item in items:
        str=item.split('<h2>')
        it = []#用于存放中间结果
        #对每一个小标签<div>进行处理
        for st in str:
            if st:
                n=st.count('blank')
                p1='(.*?)</h2>.*?'
                p2='<p><a.*?blank">(.*?)</a></p>.*?'
                p3='.*?<td><p>(.*?)</p>'
                #对特殊情况进行判断
                r1=st.count('委员：')>0
                r2= st.count('常务委员会委员（按姓氏笔画为序）：')>0
                r3=st.count('text-align: center;')>0
                for i in range(0,n//2):
                    p1=p1+p2
                if r1:#委员一行添加特殊正则表达式即可
                    p1=p1+p3
                if r2:#常务委员一行格式较为复杂，创建一个新的函数进行处理
                    p1='(.*?)</h2>.*?'
                    j = st.split('</table>')[1].count('blank')
                    n=n-j*2
                    for i in range(0, n // 2):
                        p1 = p1 + p2
                    text=detail_process(st,1)
                if r3:#存在外接URL，提取并进行处理
                    p1='(.*?)</h2>.*?'
                    j = st.split('</table>')[2].count('blank')
                    n=n-j
                    for i in range(0, n // 2):
                        p1 = p1 + p2
                    text=detail_process(st,2)
                    pass
                pattern=re.compile(p1,re.S)
                result=re.findall(pattern,st)
                if r2:
                    result.append(text)
                if r3:
                    result.append(text)
                    pass
                it.append(result)
                #print(result)
        it.insert(0,res[ide])
        ide=ide+1
        its.append(it)
    for nums in its:
        write_to_file(nums)

#对需要爬取的部分信息进行处理
def detail_process(text,i):
    if i==1:
        p2='<p><a.*?blank">(.*?)</a></p>'
        pattern=re.compile(p2,re.S)
        result=re.findall(pattern,text.split('</table>')[1])
        if result:
            result.insert(0,"常务委员会委员（按姓氏笔画为序）：")
        return result
    else:
        #获取隐藏在代码中的url
        res=[]
        p1='<a href="(.*?)".*?<b>(.*?)</b>'
        pattern=re.compile(p1,re.S)
        result=re.findall(pattern,text.split('</table>')[2])
        if result:
            for r in result:
                url.append(r[0])
        #访问URL，获取内容
        for u in url:
            html=get_page(u)
            p1='<p>\\n\\t(.*?)</p>'
            pattern=re.compile(p1,re.S)
            result=re.findall(pattern,html)
            res.append(result)
        return res

        pass

#写文件
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n\n')
        f.close()

#对另外一个页面进行处理
def get_depart(html):
    html=html.split('<div class="ind_p1_con w1000_320_index clearfix">')[1]
    html=html.split('<div class="ind_p1_left">')[0]
    items=html.split('</div>')
    p1='<h2.*?htm">(.*?)</a>(.*?)</em>'
    p2='<dd><span.*?>(.*?)</span.*?><a href.*?>(.*?)</a></em>'
    li=[]
    for item in items:
        pattern1=re.compile(p1,re.S)
        res1=re.findall(pattern1,item)
        pattern2=re.compile(p2,re.S)
        res2=re.findall(pattern2,item)
        res1.append(res2)
        li.append(res1)
    for l in li:
        print(l)
        write_to_file(l)
    pass

#主函数
def main():
    url1 = 'http://cpc.people.com.cn/GB/64162/394696/index.html'
    url2 = 'http://ldzl.people.com.cn/dfzlk/front/firstPage.htm'
    html1=get_page(url1)
    if html1:
        pass
        #get_detail(html1)
    html2=get_page(url2)
    if html2:
        get_depart(html2)
        #print(html2)
        pass

if __name__ == '__main__':
    main()
