# noinspection PyUnresolvedReferences
import time
from webbrowser import Chrome
import keyboard
import random
from selenium import webdriver
from bs4 import BeautifulSoup

phone = "18059183600"
uname_ok = "zy0001"
friend = "zy0002"
pwd = "zy111222"

# 1)登录页面
driver=webdriver.Chrome()
driver.maximize_window()
driver.get("https://login.feishu.cn/accounts/page/login?app_id=11&redirect_uri=https%3A%2F%2Fwww.feishu.cn%2F&template_id=7159153320657698818")
driver.find_element_by_xpath('//div[@class="switch-login-mode-box"]').click()
time.sleep(2)

#1）登录：输入手机号码
driver.find_element_by_name('mobile_input').send_keys(phone)
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/div[2]/label/span[1]/input').click()
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/button').click()

#1）登录：输入密码页面
time.sleep(2)
driver.find_element_by_xpath('//input[@name="password_input"][1]').send_keys(pwd)
time.sleep(2)
driver.find_element_by_xpath('//div[@class="step-box__footer"]/button[1]').click()

#登录成功 ，判断是否登录成功
time.sleep(15)
uname=driver.find_element_by_xpath('//div[@class="_pp-header-name"][1]').get_attribute('innerHTML')
if uname == uname_ok:
    print("case1:{0}用户登录成功。。。".format(uname))
else:
    print("case1:{0}用户登录不成功。。。".format(uname))
    #关闭浏览器
    driver.close()

#2）从右上⻆找到9个点（在头像的旁边）找到"消息"
time.sleep(3)
driver.find_element_by_xpath('//div[@class="_pp-product-container"]/span[@class="universe-icon _pp-product-icon"]').click()
time.sleep(3)
driver.find_element_by_xpath('//div[@class="_pp_grid_list"]/ul/li/div[@title="消息"]').click()

#3）从主界⾯中找到菜单栏->"通讯录/contacts"⻚⾯ ，4. 进⼊到tester2并进⼊聊天界⾯
#焦点在新打开的页面上，在进行操作
driver.switch_to.window(driver.window_handles[-1])
time.sleep(30)
driver.find_element_by_xpath('//p[text()="{}"]'.format(friend)).click()

#5. 分别发送⼀条少于10个字消息
time.sleep(5)
string1 = "世界如此美好。。。。"
string2 = format(random.randrange(1,100000001))
result = string1 + string2
driver.find_element_by_xpath('//div[@class="lark-editor-wrap"]/pre[@class="lark-editor lark-empty"]').send_keys(result)
keyboard.send('enter')
#判断:发送消息成功
time.sleep(5)
result2=driver.find_element_by_xpath('(//div[@class="richTextContainer"])[last()]').get_attribute('innerHTML')

if result in result2 :
    print( "case2:发送聊天消息成功。。。聊天发送内容为：{0}".format(result2))
else:
    print( "case2:发送聊天消息不成功。。。聊天发送内容为：{0}".format(result2))
    #关闭浏览器
    driver.close()

#退出登录
driver.find_element_by_xpath('//div[@class="appNavbar_avatarContainer-inside"]').click()
time.sleep(3)
driver.find_element_by_xpath('//div[@class="tenantUserCard_link"][2]').click()
driver.find_element_by_xpath('//button[@class="larkc-btn larkc-btn-normal larkc-btn-error larkc-btn-large"]').click()
driver.close()