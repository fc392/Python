from urllib import request,parse
import urllib
import time

url1='http://iproofread.cn'
url2='http://iproofread.cn/user/word_proofread'
url3='http://iproofread.cn/user/to_offline_proofread'
Max=100
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

#def test_url_offline():
#    Form_Data = {}
#    doc_path = r'D:\ProgramingFile\Python\TestingFile\1W\1.docx'
#    files = {'files':open(doc_path,'rb')}
#    #txt = urllib.parse.urlencode(t)
#    req = urllib.request.Request(url3,files,header)
#    response = request.urlopen(req)
#    html=response.read().docode('utf-8')


if __name__== '__main__':
    with open('train1.txt','r') as f:
        txt=f.read()
    start=time.clock()
    #测试页面响应时间
    #for i in range(Max):
    #    html=get_url(url1)
    #测试在线审校
    for i in range(1,Max+1):
        test_url_online(url2,txt)
    #测试离线审校
    #test_url_offline()
    end=time.clock()
    print('\nAverage Run time is:%s s'%((end-start)/Max))