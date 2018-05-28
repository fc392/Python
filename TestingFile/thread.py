from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from time import sleep
import threading
url = 'iproofread.cn'
def test_online(i):
    with open('train1.txt','r') as f:
        text = f.read()
    f.close()
    print(i)

    #设置chromedriver的路径
    driver = webdriver.Chrome()#打开驱动
    driver.maximize_window()#最大化窗口
    driver.implicitly_wait(20)#设置最大响应时间
    driver.get('http://'+url)

    #找到输入区
    element = driver.find_element_by_id('in_text')
    element.send_keys(text)
    element = driver.find_element_by_id('input-btn-submit')
    start = time.clock()
    element.click()
    WebDriverWait(driver,30,0.1).until(ec.presence_of_all_elements_located,(By.CLASS_NAME,'cl_edit_span'))
    end = time.clock()
    print('\nAverage Run time is:%s s'%(end-start))

def test_time(i):
    print(i)
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
    print('\n%sth Average Run time is:%ss'%(i,(end-start)))
    driver.close()
    return end-start

def test_offline():
    # 设置chromedriver的路径
    driver = webdriver.Chrome()  # 打开驱动
    driver.maximize_window()  # 最大化窗口
    driver.implicitly_wait(20)  # 设置最大响应时间
    driver.get('http://' + url)

    #登录
    element = driver.find_element_by_id('btn-login').click()
    element = driver.find_element_by_id('login-email').send_keys('694913652@qq.com')
    element = driver.find_element_by_id('password').send_keys('199505201')
    element = driver.find_element_by_id('login').click()

    #进入离线校对功能，找到文件上传区
    #element = driver.find_element_by_xpath("/html/body/div[2]/ul/a").get_attribute("href").click()
    url1 = driver.find_elements_by_tag_name("a")[4].get_attribute("href")
    driver.get(url1)
    element = driver.find_element_by_id('upfile').send_keys(r'D:\ProgramingFile\Python\TestingFile\1W\1.docx')
    element = driver.find_element_by_id('upload')
    start = time.clock()
    element.click()
    sleep(20)
    driver.refresh()
    try:
        while(WebDriverWait(driver, 1, 0.1).until(ec.text_to_be_present_in_element((By.CLASS_NAME, 'fill-state state-ing'), '正在'))):
            driver.refresh()
    except:
        end = time.clock()
    print('\nAverage Run time is:%s s'%(end-start-1))

if __name__ == '__main__':
    #for i in range(10):
    #    threading.Thread(target=test_time,args=(i,)).start()
    #sum = 0
    #for i in range(100):
    #    sum += test_time(i)
    #print('Total Average Time is: %ss'%(sum/100))
    test_offline()