from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import threading
url = 'iproofread.cn'
def test_online():
    with open('train1.txt','r') as f:
        text = f.read()
    f.close()

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

if __name__ == '__main__':
    test_online()