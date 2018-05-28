from urllib import request,parse
import urllib
import time
import docx

url1='http://iproofread.cn'
url2='http://iproofread.cn/user/word_proofread'
url3='http://iproofread.cn/user/to_offline_proofread'
Max=1000
header = {
    #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding':'gzip, deflate',
    #'Accept-Language':'zh-CN,zh;q=0.8',
    #'Cache-Control':'max-age=0',
    #'Connection':'keep-alive',
    #'Cookie':'JSESSIONID=CE4E5010F48E12CB9C604F41E8CA2FF1; USERNAME="694913652@qq.com"; PASSWORD=199505201; REMEMBER=true',
    #'Host':'iproofread.cn',
    #'Referer:http':'//iproofread.cn/user/index',
    #'Upgrade-Insecure-Requests':1,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.2.1.17116'
}
def get_url(url):
    response=request.urlopen(url)
    html=response.read().decode('utf-8')
    return html

def test_url_online(url,txt):
    Form_Data={}
    Form_Data['in_text']=txt
    data=parse.urlencode(Form_Data).encode('utf-8')
    response=request.urlopen(url,data)
    html=response.read().decode('utf-8')
    return html

def test_url_offline():
    Form_Data = {}
    doc_path = r'D:\ProgramingFile\Python\TestingFile\1W\1.docx'
    files = {'files':open(doc_path,'rb')}
    #txt = urllib.parse.urlencode(t)
    req = urllib.request.Request(url3,files,header)
    response = request.urlopen(req)
    html=response.read().docode('utf-8')


if __name__== '__main__':
    with open('train1.txt','r') as f:
        txt=f.read()
    start=time.clock()
    #测试页面响应时间
    for i in range(Max):
        html=get_url(url1)
    #测试在线审校
    #for i in range(1,Max+1):
    #test_url_online(url2,txt)
    #测试离线审校
    #test_url_offline()
    end=time.clock()
    print('\nAverage Run time is:%s s'%((end-start)/Max))