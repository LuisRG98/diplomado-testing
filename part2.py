import time
import ast
  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains

s = Service("C:\\Users\\Luis\\Documents\\webdriver\\chromedriver.exe")
driver = webdriver.Chrome(service=s)

#credentials
user = 'lrivas1'
passw = 'rivas1998'

with open('Output.txt') as f:
    data = f.read()
d = ast.literal_eval(data)


composerUrl = 'http://vindemo7.composer.dealer.com/website/as/vindemo7/vindemo7-admin/composer/index?deeplink=%2Fdealership%2Fstaff.htm&contentLocale=en_US&format=&__ssuMode=true#website'

cms_site = 'http://vindemo7.cms.dealer.com/dealership/staff.htm'

driver.get(composerUrl)
userInput = driver.find_element(By.ID, 'username').send_keys(user)
sigInButton = driver.find_element(By.ID,'signIn').click()
time.sleep(2)

passwInput = driver.find_element(By.ID,'password').send_keys(passw)
sigInButton = driver.find_element(By.ID,'signIn').click()


time.sleep(2)


for info in d.values():
    
    driver.get(composerUrl)
    time.sleep(5)
    driver.switch_to.frame('site-iframe')
    add =  driver.find_element(By.XPATH, "//button[text()='Create Staff Member']").click()
    time.sleep(2)
    driver.switch_to.default_content()
    new_name = driver.find_element(By.NAME, 'staffName').send_keys(info['name'])
    new_title = driver.find_element(By.NAME, 'staffTitle').send_keys(info['jobTitle'])
    new_department = driver.find_element(By.NAME, 'staffDepartment').send_keys(info['department'])
    
    if(info['phone'] !='no telephone present'):
        new_phone = driver.find_element(By.NAME, 'staffPhone').send_keys(info['phone'])
    
    if(info['email'] !='no email present'):
        new_email = driver.find_element(By.NAME, 'staffEmail').send_keys(info['email'])
        new_email = driver.find_element(By.NAME, 'staffEmail').send_keys(Keys.TAB, Keys.TAB, info['description'])
    else:
        new_email = driver.find_element(By.NAME, 'staffEmail').send_keys(Keys.TAB, Keys.TAB, info['description'])
   
    photo = driver.find_element(By.CLASS_NAME,'staffPhoto').click()
    time.sleep(3)
    carpetA = driver.find_element(By.XPATH, "//span[text()='Added DO NOT DELETE']").click() 
    time.sleep(5)
    filter = driver.find_element(By.XPATH, "//input[@class='x-form-text x-form-field x-form-text-clearable x-form-empty-field']")
    filter.send_keys(info['imageURL'])
    time.sleep(2)
    laimagen =  driver.find_element(By.XPATH, "//span[text()='"+info['imageURL']+"']")
    actionChains = ActionChains(driver)
    actionChains.double_click(laimagen).perform()    
    #driver.switch_to.default_content()
    save_button = driver.find_element(By.XPATH, "//button[text()='Save']").click()    
    time.sleep(10)

#verify if the site has the correct information uploaded
driver.get(cms_site)
data2 = {}
e2=0
time.sleep(5)
employees = driver.find_elements(By.XPATH, "//div[@id='staffList']//dl")

for person in employees:
    name = person.find_element(By.XPATH, "./dt[@class='fn']/a").get_attribute('innerText')
    pos = person.find_element(By.XPATH, "./dd[@class='title']").get_attribute('innerText')
    email = person.find_element(By.XPATH, "./dd[@class='email']").get_attribute('innerText')
    email_addres = email.replace("\n", "")
    if email_addres == '\n' or '':
        email_addres = 'no email present'        
    phone = person.find_element(By.XPATH, "./dd[@class='phone']").get_attribute('innerText')
    if phone == '\n' or '':
        phone = 'no phone present'
    bio = person.find_element(By.XPATH, "./dd[@class='bio']/p").get_attribute('innerText')
    data2[e2] = {'name': name, 'jobTitle':pos, 'description': bio, 'email': email_addres, 'phone': phone}
    e2=e2+1

for x_values, y_values in zip(d.values(), data2.values()):

    if x_values['name'] == y_values['name'] and x_values['jobTitle'] == y_values['jobTitle'] and x_values['description'] == y_values['description'] and x_values['phone'] == y_values['phone'] and x_values['email'] == y_values['email']:
        print('Empleado:' + x_values['name'] + 'tiene toda la informacion correcta') 
    else:
        print('Empleado:' + x_values['name'] + 'tiene datos incocistentes, por favor verificar la informacion')    
    # print(y_values)


driver.quit()