from fileinput import filename
import time
import requests
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

s = Service("C:\\Users\\Luis\\Documents\\webdriver\\chromedriver.exe")
driver = webdriver.Chrome(service=s)


liveSite ='https://www.johnthornton.com/MeetOurDepartments'
liveSite2 ='https://www.crumps.com/MeetOurDepartments'
liveSite3 ='https://www.jorgchev.com/MeetOurDepartments'
liveSite4 ='https://www.bunninchevroletoffillmore.com/MeetOurDepartments'

driver.get(liveSite2)

data = {}
emails=[]
phones=[]
desc=[]
e=0

time.sleep(5)

departments = driver.find_elements(By.XPATH, "//section[@itemprop='department']")

for department in departments:

    dep = department.find_element(By.CLASS_NAME, 'title')
    depName = dep.get_attribute('innerText')
    
    decks = department.find_elements(By.XPATH, "./div[@class='deck']")
    
    for deck in decks: 
        
        names = deck.find_elements(By.XPATH, "./section /div /div[@class='text'] /div[@template='employeeTitle']")
        images= department.find_elements(By.XPATH, ".//div[@class='content'] //img")
        tertiaries = deck.find_elements(By.XPATH, "./section /div /div[@class='text'] /div[@class='link'] /div[@class='tertiary']")
        descriptions = deck.find_elements(By.XPATH, ".//p[@itemprop='description']")
        
        for description in descriptions:
            try:
                descript = description.get_attribute('innerText')
                desc.append(descript)
            except:
                desc.append(' ')
             
               
        for tertiary in tertiaries:
            try:
                email_url = tertiary.find_element(By.XPATH, "./a[@itemprop='email']").get_attribute('href').split(':')
                emails.append(email_url[1])
            except:
                emails.append('no email present')
      
            try:
                telephone_url = tertiary.find_element(By.XPATH, "./a[@itemprop='telephone']").get_attribute('href').split(':')
                phones.append(telephone_url[1])
            except:
                phones.append('no telephone present')

                
        for employ,img in zip(names,images):
            fullName, pos = (employ.get_attribute('innerText')).split('\n\n')
            
            if img.get_attribute('src') == 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==':
                imgURL=img.get_attribute('data-src')
            else:
                imgURL=img.get_attribute('src')
                
            
        
            # filename = imgURL.split("/")[-1]
            if e < 10:
                filename= '00'+str(e)+'.png'
            elif e >= 10 and e < 100:
                filename= '0'+str(e)+'.png'
            else:
                filename= str(e)+'.png'
            
            r = requests.get(imgURL, stream = True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                
                # Open a local file with wb ( write binary ) permission.
                with open(filename,'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    
                print('Image sucessfully Downloaded: ', filename)
            else:
                print('Image Couldn\'t be retreived')
                
            
            data[e] = {'name': fullName, 'jobTitle':pos, 'imageURL': filename, 'department': depName, 'description': desc[e], 'email': emails[e], 'phone': phones[e]}
            e = e+1
                
print(data)

text_file = open("Output.txt", "w")
text_file.write(str(data))
text_file.close()
driver.quit()