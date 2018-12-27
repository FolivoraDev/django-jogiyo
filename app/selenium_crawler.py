from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
# Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
driver = webdriver.Chrome('/home/folivoradev/Downloads/chromedriver')
# PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
# driver = webdriver.PhantomJS('/home/folivoradev/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

driver.get('https://www.yogiyo.co.kr/mobile/#/')

# address_input
# button_search_address

driver.find_element_by_name('address_input').clear()
driver.find_element_by_name('address_input').send_keys('구로구')

driver.find_element_by_id('button_search_address').click()

a = driver.find_elements_by_class_name('ng-binding')

for i in a:
    print(i.text)

# driver.close()
