from selenium import webdriver
import time
import threading

url = 'iproofread.cn'
def test_time():
    with open('train1.txt','r') as f:
        text = f.read()
    f.close()

    #设置chromedriver的路径
    driver = webdriver.Chrome()#打开驱动
    driver.maximize_window()#最大化窗口
    driver.implicitly_wait(20)#设置最大响应时间
    start = time.clock()
    driver.get('http://'+url)
    end = time.clock()
    driver.close()
    print('\nAverage Run time is:%s s'%(end-start))
    return (end-start)

if __name__ == '__main__':
    for i in range(5):
        threading.Thread(target=test_time)
    #print(test_online())