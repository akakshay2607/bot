import os
# import glob
# import pandas as pd
from time import sleep
# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from threading import Barrier,Thread
from selenium.webdriver.chrome.options import Options
import subprocess
from warnings import filterwarnings
filterwarnings('ignore')
import random
import undetected_chromedriver as uc
import sys
sys.setrecursionlimit(10**6)
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import requests as req
from multiprocessing import shared_memory

hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
phpInfo = ["indiatransform.com/hosting/go/", "license.php"] # phpInfo = ["serverIp", "fileName.php"]

def main():
    print("Print")
    licenseKey = input("License: ") #not working
    if(licenseKey != ""):
        phpResponse = req.get("https://" + phpInfo[0] + "/" + phpInfo[1] + "?key=" + licenseKey + "&type=CheckLicense&hwid=" + hwid)
        responseString = str(phpResponse.content)
        if(responseString.find(hwid) >= 1):
            print("successfully logged in")
            if __name__ == "__main__":
                proc = []
                for i in range(forms_):
                    p = multiprocessing.Process(target=forms,args=([form_names[i],]))
                    p.start()
                    proc.append(p)

                for p in proc:
                    p.join()
        else:
            print(responseString)
    else:
        main()

global creds
global slots
slots = []
slot = []
import zipfile
def proxies(username, password, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (endpoint, port, username, password)

    extension = 'proxies_extension.zip'

    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return extension


def start_new_booking(driver):
    close_pop_up(driver)
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/dashboard':
        print('On start new booking page')
    try:
        driver.find_element(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']").click()
        print('clicked on Start new booking')
        print('going to check the centres')
    except:
        sleep(1)
    try:
        driver.find_element(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']").click()
        print('clicked on Start new booking')
        print('going to check the centres')
    except:
        pass
    try:
        # start new booking
        driver.find_element(By.XPATH,'/html/body/app-root/div/app-dashboard/section[1]/div/div[1]/div[2]/button').click()
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    try:
        if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
            print('No internet')
            return 'page not found'
    except:
        pass
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            print('Sorry, you have been blocked')
            print('Quitting driver')
            return 'page not found'
    except:
        pass
    
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/dashboard':
        return start_new_booking(driver)


def wait_till_login_loads(driver,creds,cats,cities,i,formname,slot,j=0):
    while j<5:
        print('On login page')
        driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('This site can’t be reached')
                print('Quitting the driver')
                return page_not_found(driver,creds,cats,cities,formname,formname,slot,i)
        except:
            pass
        try:
            if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
                print('Sorry, you have been blocked page')
                print('Quitting the driver')
                driver.delete_all_cookies()    
                driver.refresh()   
        except:
            pass
        try:
            if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
                print('No internet')
                print('Quitting the driver')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        try:
            driver.find_element(By.XPATH,"/html/body/app-root/div/app-login/section/div/div/mat-card/form/button")
            print('found sign in')
            return
        except:
            j+=1
            return wait_till_login_loads(driver,creds,cats,cities,formname,slot,i,j)
        sleep(2)
    return page_not_found(driver,creds,cats,cities,formname,slot,i)

def go_to_login_page(driver,creds,cats,cities,formname,slot,i,j=0):
    actions = ActionChains(driver)
    with open(formname) as f:
        text = f.readlines()
    for idx,line in enumerate(text):
        if "Proxies" in line:
            proxy_ips = text[idx+1:]
    userid = proxy_ips[0].strip().split(':')[-2:][0]
    pass_ = proxy_ips[0].strip().split(':')[-2:][1]
    while j<3:
        try:
            print('Going to book-an-appointment page')
            driver.get(f'https://{userid}:{pass_}@visa.vfsglobal.com/ind/en/pol/book-an-appointment')  ## lets see if this works for alerts
        except Exception as e:
            print(e)
        sleep(7)
        driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                print('Quitting the driver')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        try:
            if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
                print('Sorry, you have been blocked page')
                print('Quitting the driver')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)   
        except:
            pass
        try:
            if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
                print('No internet')
                print('Quitting the driver')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        driver.delete_all_cookies()
        try:
            print('clicking on book now')
            print(driver.find_element(By.XPATH,'//*[@id="__layout"]/div/main/div/div/div[3]/div/p[19]/a').text)
#             butn = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/main/div/div/div[3]/div/p[19]/a')
#             actions.move_to_element_with_offset(butn,20,20).click().perform()
            driver.find_element(By.XPATH,'//*[@id="__layout"]/div/main/div/div/div[3]/div/p[19]/a').click()
            print('clicked on book now')
            return 
        except:
            j+=1
            return go_to_login_page(driver,creds,cats,cities,formname,slot,i,j)
    return page_not_found(driver,creds,cats,cities,formname,slot,i)

def chose_cred(creds):
    cred = random.choice(creds)
    print(cred)
    if cred[0].split('=')[1].strip():
        return cred
    else:
        return chose_cred(creds)

def login_withot_captcha(driver,creds,cats,cities,formname,slot,i):
    print(creds)
    print(cats)
    print(formname)
    go_to_login_page(driver,creds,cats,cities,formname,slot,i)
    sleep(2)
    driver.delete_all_cookies()

    sleep(20)
    try:
        driver.switch_to.window(driver.window_handles[1])
        wait_till_login_loads(driver,creds,cats,cities,formname,slot,i)
    except:
        pass
    vfs_account_email = creds[0].split('=')[1].strip()
    vfs_account_password = creds[1].split('=')[1].strip()
    try:
        close_pop_up(driver)
    except:
        pass
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        sleep(1)
    except:
        pass

    def check_captcha(driver,slot,j=0):
        print('checking captcha')
        while j<3:
            print(j)
            driver.switch_to.default_content()
            try:
                frames = driver.find_elements(By.TAG_NAME,"iframe")
                driver.switch_to.frame(frames[0])
                sleep(1)
                g_captcha = []
                try:
                    g_captcha = driver.find_element(By.XPATH,"//td[@id='branding']")
                except:
                    pass
                if not g_captcha:
                    print('Found Google captcha')
                    print('Quitting driver')
                    return page_not_found(driver,creds,cats,cities,formname,slot,i)
            except:
                pass
            try:
                driver.find_element(By.XPATH,'//*[@id="cf-stage"]').click()
            except:
                pass
            success = []
            try:
                success = driver.find_element(By.XPATH,"//div[@id='success']").text
            except:
                pass
            if not success:
                j+=1
                return check_captcha(driver,slot,j)
            else:
                return
        else:
            return
    try:  
        check_captcha(driver,slot)
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            print('Quitting driver')
            return page_not_found(driver,creds,cats,cities,formname,slot,i)
    except:
        pass
    
    try:
        if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
            print('No internet')
            print('Quitting driver')
            return page_not_found(driver,creds,cats,cities,formname,slot,i)
    except:
        pass
    
    try:
        driver.find_element(By.XPATH,'//*[@id="cf-stage"]').click()
    except:
        pass
    try:
        driver.switch_to.default_content()
    except:
        pass
    
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            print('Sorry, you have been blocked')
            print('Quitting driver')
            return page_not_found(driver,creds,cats,cities,formname,slot,i)
    except:
        pass
    
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-0"]'))).send_keys(vfs_account_email)
    except:
        pass

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-1"]'))).send_keys(vfs_account_password)
    except:
        pass
    print('Entered Email and Password')
    try:
        driver.switch_to.default_content()
    except:
        pass
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/div/app-login/section/div/div/mat-card/form/button'))).click()
        print('clicked on Login')
    except:
        sleep(2)
    try:
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-login/section/div/div/mat-card/form/button").click()
        print('clicked on Login')
    except:
        pass
    
    sleep(10)
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/login':
        print('Login timeout')
        print('Quitting driver')
        return page_not_found(driver,creds,cats,cities,formname,slot,i)


# In[9]:


def close_pop_up(driver):
    try:
        driver.find_element(By.XPATH,'//*[@id="onetrust-close-btn-container"]/button').click()
    except:
        pass


def get_nationality(curr_nationality,nationalities):
    for i,val in enumerate(nationalities):
        if curr_nationality.upper() in val:
            return i
 
def gender_select(gender):
    if gender.upper() == 'MALE':
        return 1
    elif gender.upper() == 'FEMALE':
        return 0
    else:
        return 2

def form_filler(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality):
    try:
        # first name
        print('Filling the form')
        try:
            driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']").send_keys(first_name)
            sleep(0.2)
        except:
            sleep(2)
            driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']").send_keys(first_name)
            sleep(0.2)

        # last name
        driver.find_element(By.XPATH,"//input[@placeholder='Please enter last name.']").send_keys(last_name)
        sleep(0.2)

        # Gender
        driver.find_element(By.XPATH,"//mat-select").click()
        sleep(0.2)
        driver.find_elements(By.XPATH,"//mat-option")[gender_select(gender)].click()
        
        # DOB
        driver.find_element(By.XPATH,"//input[@placeholder='Please select the date']").send_keys(dob)
        sleep(0.2)

        # passport number
        driver.find_element(By.XPATH,"//input[@placeholder='Enter passport number']").send_keys(pass_number)
        sleep(0.2)
        
        # Nationality
        driver.find_elements(By.XPATH,"//mat-select")[1].click()
        sleep(0.2)
        options = driver.find_elements(By.XPATH,"//mat-option")
        for option in options:
            try:
                if option.text == curr_nationality.upper():
                    option.click()
            except:
                pass
            
        # passport Expiry date
        driver.find_elements(By.XPATH,"//input[@placeholder='Please select the date']")[1].send_keys(pass_expiry)
        sleep(0.2)

        # Country code
        driver.find_element(By.XPATH,"//input[@placeholder='44']").send_keys(country_code)
        sleep(0.2)

        # ph number
        driver.find_element(By.XPATH,"//input[@placeholder='012345648382']").send_keys(contact_number)
        sleep(0.2)

        # email
        driver.find_element(By.XPATH,"//input[@placeholder='Enter Email Address']").send_keys(email)
        sleep(0.2)

    except:
        pass

def page_not_found(driver,cred,cats,cities,formname,slot,i):
    print('in page not found')
    driver.quit()
    i+=1
    driver,i = new_driver(i,formname)
    sleep(2)
    return child_func1(driver,cred,cats,cities,formname,slot,i)


def hover2(driver,sub_cat,k=0):
    a = sub_cat.split('=')[1].strip().split(',') 
    for j in range(len(a)):
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-5']"))).click()
        except:
            pass
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-5']"))).click()
        except:
            pass
        try:
            driver.find_element(By.XPATH,'//*[@id="mat-select-value-3"]').click()
        except:
            pass
            
        try:
            box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
        except:
            k+=1
            if k==3:
                return 'bar'
            return hover2(driver,sub_cat,k)
        for i in box.find_elements(By.XPATH,"//mat-option"):
            try:
                if a[j] in i.text:
                    i.click()
                    break
            except:
                pass
        sleep(5)
        cont_btn = []
        try:
            cont_btn = driver.find_elements(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']")
        except:
            pass
        if cont_btn:
            try:
                print(driver.find_element(By.XPATH,"//div[@class='border-info mb-0 ng-star-inserted']").text)
            except:
                pass
            return 'continue'
        bar = []
        try:
            bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
            return 'bar'
        except:
            pass
        sleep(2)


# In[14]:


def payment(driver,formname):
    try:
        print('Entering Payment details')
        # form_cat = formname.split('.')[0] + '_cat.txt'
        with open(formname) as f:       
            text = f.readlines()
        for i in text:
            # Debit card
            if 'DEBIT' in i:
                Debit = i.split('=')[1].strip()
            if 'DBCVV' in i:
                Dcvv = i.split('=')[1].strip()
            if 'DBEXPIRY' in i:
                Dexpiry = i.split('=')[1].strip()
            if 'FIRST NAME' in i:
                Dfirst_name = i.split('=')[1].strip()
            if 'LAST NAME' in i:
                Dlast_name = i.split('=')[1].strip()

            if 'CREDIT' in i:
                Credit = i.split('=')[1].strip()
            if 'CCCVV' in i:
                Ccvv = i.split('=')[1].strip()
            if 'CCEXPIRY' in i:
                Cexpiry = i.split('=')[1].strip()
            if 'FIRST' in i:
                Cfirst_name = i.split('=')[1].strip()
            if 'LAST' in i:
                Clast_name = i.split('=')[1].strip()
            if 'Pin_code' in i:
                Pin_code = i.split('=')[1].strip()
            if 'Mobile' in i:
                Mobile = i.split('=')[1].strip()
            if 'city' in i:
                city= i.split('=')[1].strip()
            if 'state' in i:
                state = i.split('=')[1].strip()

        dbt = [Debit,Dcvv,Dexpiry,Dfirst_name,Dlast_name]
        cdt = [Credit,Ccvv,Cexpiry,Cfirst_name,Clast_name]
        
        # if not Debit:
        #     pick = cdt
        #     driver.find_element(By.XPATH,"//span[contains(text(),'Credit Card')]").click()
        #     sleep(2)
        # else:
        #     pick = dbt
        #     driver.find_element(By.XPATH,"//span[contains(text(),'Debit Card')]").click()
        pick = cdt
            
        # postal code
        driver.find_element(By.XPATH,"//input[@id='pincode']").send_keys(Pin_code)
        sleep(1)
        #  
        # city
        driver.find_element(By.XPATH,"//input[@id='billing_city']").send_keys(city)
        sleep(1)
        # state
        driver.find_element(By.XPATH,"//input[@id='billing_state']").send_keys(state)
        sleep(1)
        # Address
        driver.find_element(By.XPATH,"//input[@id='billing_address1']").send_keys(city + " " + state)
        sleep(1)
        # next Button
        driver.find_element(By.XPATH,'//*[@id="nextbtn"]').click()
        sleep(2)
        
        # phone
        driver.find_element(By.XPATH,"//input[@id='phone']").send_keys(Mobile)
        sleep(1)
        # name on card
        driver.find_element(By.XPATH,"//input[@id='ccName']").send_keys(f"{pick[-2]} {pick[-1]}")
        sleep(1)
        # card number
        driver.find_element(By.XPATH,'//*[@id="ccardNo"]').send_keys(f"{pick[0]}")
        sleep(1)
        # expiry
        try:
            driver.find_element(By.XPATH,'//*[@id="creditcard_expiryMonth"]').send_keys(f"{pick[2].split('/')[0]}")
            sleep(1)
        except Exception as e:
            print(e)
            pass
        try:
            driver.find_element(By.XPATH,'//*[@id="creditcard_expiryYear"]').send_keys(f"{pick[2].split('/')[1]}")
        except Exception as e:
            print(e)
            pass
        # CVV
        driver.find_element(By.XPATH,'//*[@id="ccvv"]').send_keys(f"{pick[1]}")
        sleep(2)   
        driver.find_element(By.XPATH,"//label[@id='tc']").click()
        sleep(1) 
        
    except:
        sleep(3)
        print(j)
        if j<4:
            j+=1
            driver.refresh()
            sleep(3)
            return payment(driver,formname,j)
        else:
            pass


def month_matcher(driver,req_month):
    # print(req_month)
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for i,m in enumerate(months):
        if req_month in m:
            req_month_idx = i
    try:
        current_month = driver.find_element(By.XPATH,"//div[@class='fc-header-toolbar fc-toolbar ']").text.split()[0]
        for i,m in enumerate(months):
            if current_month in m:
                current_month_idx = i
    except:
        return month_matcher(driver,req_month)
    
    if req_month_idx < current_month_idx:
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[1]"))).click()
        except:
            pass
        sleep(2)
        # h6 = []
        try:
            text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
            return 'page not found'
        except:
            pass
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
        sleep(2)
        return month_matcher(driver,req_month)

    elif req_month_idx > current_month_idx:
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[2]"))).click()
        except:
            pass
        sleep(2)
        # h6 = []
        try:
            text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
            return 'page not found'
        except:
            pass
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
        sleep(2)
        return month_matcher(driver,req_month)
    
    # h6 = []
    try:
        text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
        return 'page not found'
    except:
        pass

    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    else:
        return 'matched'

def back_and_forward(driver,month_,slot_trigger):
    try:
        btns = driver.find_element(By.XPATH,"//div[@class='fc-button-group']").find_elements(By.XPATH,".//button")
    except:
        pass
    try:
        btns[0].click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    except:
        pass
    
    try:
        btns[1].click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    sleep(3)
    a = month_matcher(driver,month_)
    if a=='page not found':
        return 'page not found'
    select_date(driver,month_,slot_trigger)
    
def select_date(driver,month_,slot_trigger):
    # print(month_)
    if slot_trigger == 'A':
        r1,r2  = 1,10
    if slot_trigger == 'B':
        r1,r2  = 10,20
    if slot_trigger == 'C':
        r1,r2  = 20,32
    if slot_trigger == 'D':
        r1,r2  = 1,32
        
    slot_range = range(r1,r2)
    day = []
    month = []
    try:
        table = driver.find_element(By.XPATH,"//table[@class='fc-scrollgrid-sync-table']")
        rows = table.find_elements(By.XPATH,".//tr")    
    except:
        pass
    try:
        for row in rows:
            ele = []
            for i in row.find_elements(By.XPATH,'.//td'):

                if 'future date-availiable' in i.get_attribute('class'):
                    ele.append(i)
            try:
                day = int(ele[0].text.strip())
                if day in slot_range:
                    ele[0].click()
                    month = driver.find_element(By.XPATH,'//h2[@class="fc-toolbar-title"]').text
                    print([day,month])
                    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                        return 'page not found'
                    sleep(2)
                    return day,month
            except:
                pass
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            return 'page not found'   
    except:
        pass
    return back_and_forward(driver,month_,slot_trigger)

def select_date_from_mult_months(driver,month_,slot_trigger):
    # print(month_)
    if slot_trigger == 'A':
        r1,r2  = 1,10
    if slot_trigger == 'B':
        r1,r2  = 10,20
    if slot_trigger == 'C':
        r1,r2  = 20,32
    if slot_trigger == 'D':
        r1,r2  = 1,32
    slot_range = range(r1,r2)
    day = []
    month = []
    try:
        table = driver.find_element(By.XPATH,"//table[@class='fc-scrollgrid-sync-table']")
        rows = table.find_elements(By.XPATH,".//tr")    
    except:
        pass
    try:
        for row in rows:
            ele = []
            for i in row.find_elements(By.XPATH,'.//td'):

                if 'future date-availiable' in i.get_attribute('class'):
                    ele.append(i)
            try:
                day = int(ele[0].text.strip())
                if day in slot_range:
                    ele[0].click()
                    month = driver.find_element(By.XPATH,'//h2[@class="fc-toolbar-title"]').text
                    print([day,month])
                    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                        return 'page not found'
                    sleep(2)
                    return day,month
            except:
                pass
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found','page not found'
    except:
        pass
    return day,month

def check_multiple_months(driver,req_months,slot_trigger):
    if len(req_months)>1:
        for month_ in req_months:
            a = month_matcher(driver,month_)
            if a=='page not found':
                return 'page not found','page not found'
            day,month = select_date_from_mult_months(driver,month_,slot_trigger)
            if day == 'page not found':
                return 'page not found','page not found'
            if month:
                return day,month
        else:
            return check_multiple_months(driver,req_months,slot_trigger)
    else:
        a = month_matcher(driver,req_months[0])
        if a=='page not found':
            return 'page not found','page not found'
        day,month = select_date(driver,req_months[0],slot_trigger)
        return day,month

def get_form_info(filename):
    with open(filename) as f:
        text = f.readlines()
    for j,i in enumerate(text):
        if 'First name' in i:
            first_name = i.split('-')[1].strip()
        if 'Last name' in i:
            last_name = i.split('-')[1].strip()
        if 'Gender' in i:
            gender = i.split('-')[1].strip()
        if 'DOB' in i:
            dob = i.split('-')[1].strip()
            while '/' in dob:
                dob = dob.replace('/','')
        if 'Current Nationality' in i:
            curr_nationality = i.split('-')[1].strip()
        if 'Passport Number' in i:
            pass_number = i.split('-')[1].strip()
        if 'Passport Expiry Date' in i:
            pass_expiry = i.split('-')[1].strip()
            while '/' in pass_expiry:
                pass_expiry = pass_expiry.replace('/','')
        if 'country code' in i:
            country_code = i.split('-')[1].strip()
        if 'Contact number' in i:
            contact_number = i.split('-')[1].strip()
        if 'E_mail' in i:
            email_ = i.split('-')[1].strip()
        # if 'Nationalities' in i:
        #     nationalities = text[j+1:]
    return first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email_


def new_driver(i,formname):
    with open(formname) as f:
        text = f.readlines()
    for idx,line in enumerate(text):
        if "Proxies" in line:
            proxy_ips = text[idx+1:]

    if i < len(proxy_ips):
        pass
    else:
        print('This was the last ip')
        i = 0

    creds,sub_em,cties,sub_cats,receiver_emails,triggers,req_months,repeat_triggers,headless_triggers,ct,st = get_creds(formname)
    headless_trigger = headless_triggers[0]
    try:
        userid = proxy_ips[0].strip().split(':')[-2:][0]
        pass_ = proxy_ips[0].strip().split(':')[-2:][1]
        proxy = ":".join(proxy_ips[i].strip().split(':')[:-2])
        print(proxy)
        endpoint = proxy.split(':')[0]
        port = proxy.split(':')[1]
        options = uc.ChromeOptions()
        mobile_emulation = { "deviceName": "Samsung Galaxy S20 Ultra" } #c
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        mobile_emulation = {"deviceMetrics": { "width": 412, "height": 915, "pixelRatio": 3.0, "touch": True },      
                            "userAgent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 Edg/115.0.0.0" } #c
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument('--no-first-run')
        options.add_argument('--lang=en')
        options.add_argument('--no-service-autorun')
        options.add_argument('--password-store=basic')
        options.add_argument("--window-size=380,915")
        if headless_trigger:
            print('Headless')
            options.add_argument('--headless=new')
        else:
            pass
        options.add_argument('--disable-session-crashed-bubble')
        options.add_experimental_option("detach", True)
        proxies_extension = proxies(userid, pass_, endpoint, port)
        options.add_extension(proxies_extension)
        driver = uc.Chrome(options=options)
    except Exception as e:
        i+=1
        print(e)
        print('Error')
        return new_driver(i,formname)
    return driver,i


def main_2(driver,email_sub_creds,sub_cat,city,formname,slot,ip):
    print(city)
    cities_to_ignore = city.split('=')[1].strip().split(',')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-3']"))).click()
        sleep(2)
    except:
        sleep(2)
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-3']"))).click()
        sleep(2)
    except:
        pass
    try:
        print('clicking')
        driver.find_element(By.XPATH,'//*[@id="mat-select-value-1"]').click()
    except Exception as e:
        print(e)
        pass
        
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found','page not found','page not found'
        
    try:
        box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
    except:
        sleep(2)
        
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found','page not found','page not found'
    except:
        pass
    
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found','page not found','page not found'
    close_pop_up(driver)
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            return 'page not found','page not found','page not found'
    except:
        pass
    try:
        if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
            print('No internet')
            return 'page not found','page not found','page not found'
    except:
        pass

    cnt = []
    try:
        cnt = driver.find_element(By.XPATH,"//h6[@class='d-inline pull-right text-right ng-star-inserted']")
    except:
        pass
    if not cnt:
        return 'page not found','page not found','page not found'

    try:
        centres_ = box.find_elements(By.XPATH,"//mat-option")    
        main_centeres = []
        for l in centres_:
            main_centeres.append(l.text)
        print(f"cities to ignore {cities_to_ignore}")
        print(len(cities_to_ignore))
        remove_index = []
        if len(cities_to_ignore)==1:
            if not cities_to_ignore[0]:
                remove_index = []
        else:
            try:
                for l,val in enumerate(main_centeres):
                    for cty in cities_to_ignore:
                        if cty in val:
                            remove_index.append(l)
            except:
                pass
        # done
        print(f"remove index {remove_index}")
        idx = [m for m in range(9)]
        for m in remove_index:
            try:
                idx.remove(m)
            except:
                pass
        print(f"idx {idx}")
        print(len(centres_))
        for i in range(len(idx)):
            try:
                centres_[idx[i]].click()
                ctr = centres_[idx[i]].text
                sleep(2)
                try:
                    bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                    print('Found Blue bar')
                    return 'page not found','page not found','page not found'
                except:
                    pass
                a = hover2(driver,sub_cat)
                if a == 'bar':
                    print('Found Blue bar')
                    return 'page not found','page not found','page not found'
                sleep(2)
                cont_btn = []
                try:
                    cont_btn = driver.find_elements(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']")
                except:
                    pass
                if cont_btn:
                    sleep(1)
                    slt = driver.find_element(By.XPATH,"//div[@class='border-info mb-0 ng-star-inserted']").text
                    cent_sub_cat = "Appointment for centre " + ctr + "\nsub category "+ sub_cat
                    slt_info = cent_sub_cat + "\n" + slt
                    print(slt_info)
                    
                    if slt in slot:
                        pass
                    else:
                        slt = driver.find_element(By.XPATH,"//div[@class='border-info mb-0 ng-star-inserted']").text
                        print(len(slot))
                        len_slot = 0
                        for i in slot:
                            if 'aaaaaaaaaa' not in i:
                                len_slot +=1
                        if len_slot < len(email_sub_creds):
                            print('going for new slot')
                            slot[len_slot] = slt
                            print(f'Starting new sub-thread for {email_sub_creds[len_slot]}')
                            p = multiprocessing.Process(target=func1,args=([email_sub_creds[len_slot],sub_cat,city,formname,slot,ip+1]))
                            p.start()
                            print('continue')
                            return 'Continue',slt,cent_sub_cat
                        else:
                            print('Slots over')
                            return 'Continue',slt,cent_sub_cat
                try:
                    if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                        print('site cannnot be reached')
                        return 'page not found','page not found','page not found'
                except:
                    pass
                
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    sleep(2)
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    pass
                box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
                opts = box.find_elements(By.XPATH,".//mat-option")
                
                # h6 = []
                try:
                    h6 = driver.find_element(By.XPATH,"//div[@class='mt-15']").find_element(By.XPATH,".//h6").text
                    if 'Sorry' in h6:
                        return 'page not found','page not found','page not found'
                except:
                    pass
            except Exception as e:
                print(e)
                pass        
    except Exception as e:
        print(e)
        pass
    return main_2(driver,email_sub_creds,sub_cat,city,formname,slot,ip)

def get_form_page(driver,j=0):
    while j<10:
        a = ''
        try:
            a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
        except:
            pass
        if a:
            print('on form page')
            return 'found'
        j+=1
        sleep(2)
        return get_form_page(driver,j)
    return 'page not found'

def get_applicants_page(driver,j=0):
    while j<10:
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,"//p[contains(text(),'you must book appointment individually')]").text
        except:
            pass
        if ele:
            print('on applicant page')
            return 'found'
        j+=1
        sleep(1)
        return get_applicants_page(driver,j)
    return 'page not found'

def get_service_page(driver,j=0):
    while j<10:
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,"//h1[contains(text(),'Services')]").text
        except:
            pass
        if ele:
            print('on Services page')
            return 'found'
        j+=1
        sleep(1)
        return get_service_page(driver,j)
    return 'page not found'

def get_calender_page(driver,j=0):
    while j<10:
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,"//h1[contains(text(),'Book an Appointment')]").text
        except:
            pass
        if ele:
            print('on calender page')
            return 'found'
        j+=1
        sleep(1)
        return get_calender_page(driver,j)
    return 'page not found'

def get_review_page(driver,j=0):
    while j<10:
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,"//h1[contains(text(),'Review')]").text
        except:
            pass
        if ele:
            print('on Review page')
            return 'found'
        j+=1
        sleep(1)
        return get_review_page(driver,j)
    return 'page not found'

def get_payment_disc_page(driver,j=0):
    while j<10:
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,"//h1[contains(text(),'Payment Disclaimer')]").text
        except:
            pass
        if ele:
            print('On Payment Disclaimer page')
            return 'found'
        j+=1
        sleep(1)
        return get_payment_disc_page(driver,j)
    return 'page not found'

def child_func1(driver,cred,cats,cities,formname,slot,i):
    print(cred)
    global num
    if 'email' in cred[0]:
        nums = []
        for n in cred[0].split('=')[0].strip():
            if n.isnumeric():
                nums.append(n)
        num = int("".join(nums))
        # slot = slots[num-1]
    else:
        nums = []
        for n in cred[0].split('=')[0].strip():
            if n.isnumeric():
                nums.append(n)
        num = int("".join(nums))
    with open(formname) as f:
        text = f.readlines()

    number_of_applicants = 0
    for line in text:
        if f'E_id_{num}' in line:
            number_of_applicants +=1
    
    print(f'Found {number_of_applicants} applicants')
    
    applicants = []
    # num_ = 1
    for num_ in range(1,number_of_applicants+1):
        for idx,val in enumerate(text):
            if f'E_id_{num}_Applicant {num_}' in val:
                text1 = text[idx:]
        for idx,val in enumerate(text1):
            if 'E_mail' in val:
                applicants.append(text1[:idx+1])
                break
              
    creds,sub_em,cties,sub_cats,receiver_emails,triggers,req_months,repeat_triggers,headless_triggers,coapplicant_triggers,slot_trigger = get_creds(formname)
    
    email_sub_creds = sub_em[num-1]
    headless_trigger = headless_triggers[0]
    repeat_trigger = repeat_triggers[0]
    coapplicant_trigger = coapplicant_triggers[0]

    login_withot_captcha(driver,cred,cats,cities,formname,slot,i)    
    booking = start_new_booking(driver)
    if booking == 'page not found':
        print('Quitting the driver')
        page_not_found(driver,cred,cats,cities,formname,slot,i)
        
    if repeat_trigger:
        print('Checking the centres')
        to_do,slt = main_12(driver,email_sub_creds,cats,cities,formname,slot,i)
    else:
        print('Checking the centres')
        to_do,slt,cent_sub_cat = main_2(driver,email_sub_creds,cats,cities,formname,slot,i)
        
    if to_do == 'page not found':
        print('Quitting the driver')
        page_not_found(driver,cred,cats,cities,formname,slot,i)
    if to_do == 'Continue':
        # check_slot2(driver,formname,cred,cats)
        close_pop_up(driver)
        a = driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]")
        while a:
            try:
                driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
            except:
                pass
            sleep(3)
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
        #         return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass

            try:
                a = []
                a = driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]")
            except:
                pass
            # sleep(3)
            
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        a = get_form_page(driver)
        sleep(2)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_applicant_info(applicants[0][1:])
        try:
            form_filler(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality)
        except Exception as e:
            print(e)
        a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
        while a:
            try:
                driver.find_element(By.XPATH,"/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button").click()
            except:
                pass
            sleep(2)
            
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass

            try:
                a = []
                a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
            except:
                pass
            sleep(5)
        # sleep(2)
        if not coapplicant_trigger:
            ap = applicant_filler(driver,number_of_applicants,applicants[1:])
            if ap == 'page not found':
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        a = get_applicants_page(driver)
        if a == 'page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
        while b:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),' Continue ')]"))).click()
            except:
                pass
            try:
                b = []
                b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
            except:
                pass
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass
            sleep(2)
    
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        a = get_calender_page(driver)
        if a == 'page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
        try:
            day,month = check_multiple_months(driver,req_months,slot_trigger)
        except Exception as e:
            print(e)
            
        if day=='page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

        def select_button(driver):
            try:
                driver.find_element(By.XPATH,"//input[@name='SlotRadio']").click()
            except:
                pass
            if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            sleep(0.2)
            selected = []
            try:
                selected = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']")
            except:
                pass
            if selected:
                time = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,'..').text
                time = time.split('\n')[0]
                return time
            else:
                return select_button(driver)
        time = select_button(driver)

        driver.find_element(By.XPATH,"/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button").click()
        # sleep(5)
        a = get_service_page(driver)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Services")]').text
        except:
            pass
        while ele:
            
            try:
                driver.find_element(By.XPATH,'/html/body/app-root/div/app-manage-service/section/mat-card[2]/div/div[2]/button').click()
            except:
                pass
            sleep(2)
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass
            try:
                ele = ''
                ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Services")]').text
            except:
                pass            
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        
        a = get_review_page(driver)
        if a=='page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        close_pop_up(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.2)
        driver.find_element(By.XPATH,"//mat-checkbox").click()
        sleep(0.2)
        driver.find_elements(By.XPATH,"//mat-checkbox")[1].click()
        sleep(0.2)
        # pay online
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        a = get_payment_disc_page(driver)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        # continue
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Payment Disclaimer")]').text
        except:
            pass
        while ele:
            
            try:
                driver.find_element(By.XPATH,'/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button').click()
            except:
                pass
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)
            except:
                pass
            try:
                ele = ''
                ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Payment Disclaimer")]').text
            except:
                pass
            # sleep(5)
        # driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        sleep(5)
        payment(driver,formname)
        sleep(2)
        return
    return func1(cred,cats,cities,formname,slot,i)


# repeat trigger 0
def main_12(driver,email_sub_creds,sub_cat,city,formname,ip):
    print(city)
    
    cities_to_ignore = city.split('=')[1].strip().split(',')
    try:
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-3']"))).click()
        sleep(2)
    except:
        sleep(2)
    try:
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-3']"))).click()
        sleep(2)
    except:
        pass
        
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found','page not found'
        
    try:
        box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
    except:
        sleep(2)
        
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found','page not found'
    except:
        pass
    
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found','page not found'
    close_pop_up(driver)
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            return 'page not found','page not found'
    except:
        pass
    try:
        if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
            print('No internet')
            return 'page not found','page not found'
    except:
        pass

    cnt = []
    try:
        cnt = driver.find_element(By.XPATH,"//h6[@class='d-inline pull-right text-right ng-star-inserted']")
    except:
        pass
    if not cnt:
        return 'page not found','page not found'
    
    try:
        centres_ = box.find_elements(By.XPATH,"//mat-option")    
        main_centeres = []
        for l in centres_:
            main_centeres.append(l.text)

        remove_index = []
        for l,val in enumerate(main_centeres):
            for cty in cities_to_ignore:
                if cty in val:
                    remove_index.append(l)

        idx = [m for m in range(10)]
        for m in remove_index:
            try:
                idx.remove(m)
            except:
                pass
        for i in range(len(centres_)):
            try:
                centres_[idx[i]].click()
                sleep(2)
                try:
                    bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                    return 'page not found','page not found'
                except:
                    pass
                a = hover2(driver,sub_cat)
                if a == 'bar':
                    print('Found Blue bar')
                    return 'page not found','page not found'
                sleep(2)
                cont_btn = []
                try:
                    cont_btn = driver.find_elements(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']")
                except:
                    pass
                if cont_btn:
                    sleep(1)
                    slt = driver.find_element(By.XPATH,"//div[@class='border-info mb-0 ng-star-inserted']").text
                    slt_info = sub_cat + " : " + slt
                    print(slt_info)
                    len_slot = 0
                    for i in slot:
                        if 'aaaaaaaaaa' not in i:
                            len_slot +=1
                    if len_slot < len(email_sub_creds):
                        print('Going to the new slot')
                        print(len(slot))
                        print('Starting new sub-thread')
                        p = multiprocessing.Process(target=func1,args=([email_sub_creds[len_slot],sub_cat,city,formname,slot,ip+1]))
                        p.start()
                        print('continue')
                        return 'Continue',slt
                    else:
                        print('Slots over')
                        return 'Continue',slt
                try:
                    if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                        print('site cannnot be reached')
                        return 'page not found','page not found'
                except:
                    pass
                
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    sleep(2)
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    pass
                box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
                opts = box.find_elements(By.XPATH,".//mat-option")
                
                # h6 = []
                try:
                    h6 = driver.find_element(By.XPATH,"//div[@class='mt-15']").find_element(By.XPATH,".//h6").text
                    if 'Sorry' in h6:
                        return 'page not found','page not found'
                except:
                    pass
            except:
                pass
                
    except:
        pass
    return main_12(driver,email_sub_creds,sub_cat,city,formname,slot,ip)

def func1(cred,cats,cities,formname,slot,i=0):
    print(cred)
    print(formname)
    global formname_
    formname_ = formname
    global num
    global req_months
    global co_applicants
    if 'email' in cred[0]:
        nums = []
        for n in cred[0].split('=')[0].strip():
            if n.isnumeric():
                nums.append(n)
        num = int("".join(nums))
        # slot = slots[num-1]
    else:
        nums = []
        for n in cred[0].split('=')[0].strip():
            if n.isnumeric():
                nums.append(n)
        num = int("".join(nums))
        
    with open(formname) as f:
        text = f.readlines()

    number_of_applicants = 0
    for line in text:
        if f'E_id_{num}' in line:
            number_of_applicants +=1
    
    print(f'Found {number_of_applicants} applicants')
    
    applicants = []
    # num_ = 1
    for num_ in range(1,number_of_applicants+1):
        for idx,val in enumerate(text):
            if f'E_id_{num}_Applicant {num_}' in val:
                text1 = text[idx:]
        for idx,val in enumerate(text1):
            if 'E_mail' in val:
                applicants.append(text1[:idx+1])
                break 

    creds,sub_em,ctie,sub_cats,receiver_emails,triggers,req_months,repeat_triggers,headless_triggers,coapplicant_triggers,slot_trigger = get_creds(formname)
    print(f'Number is {num}')
    
    email_sub_creds = sub_em[num-1]
    coapplicant_trigger = coapplicant_triggers[0]
    repeat_trigger = repeat_triggers[0]

    driver,i = new_driver(i,formname)
    actions = ActionChains(driver)
    login_withot_captcha(driver,cred,cats,cities,formname,slot,i)
    booking = start_new_booking(driver)
    if booking == 'page not found':
        page_not_found(driver,cred,cats,cities,formname,slot,i)
        
    if repeat_trigger:
        print('Going to check the centres')
        to_do,slt = main_12(driver,email_sub_creds,cats,cities,formname,slot,i)
    else:
        print('Going to check the centres')
        to_do,slt,cent_sub_cat = main_2(driver,email_sub_creds,cats,cities,formname,slot,i)
        
    if to_do == 'page not found':
        page_not_found(driver,cred,cats,cities,formname,slot,i)

    if to_do == 'Continue':
        # check_slot2(driver,formname,cred,cats)
        close_pop_up(driver)
        a = driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]")
        while a:
            try:
                driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
            except:
                pass
            sleep(3)
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
        #         return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass

            try:
                a = []
                a = driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]")
            except:
                pass
            # sleep(3)
            
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        a = get_form_page(driver)
        sleep(2)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_applicant_info(applicants[0][1:])
        try:
            form_filler(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality)
        except Exception as e:
            print(e)
        a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
        while a:
            try:
                driver.find_element(By.XPATH,"/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button").click()
            except:
                pass
            sleep(2)
            
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass

            try:
                a = []
                a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
            except:
                pass
            sleep(5)
        # sleep(2)
        if not coapplicant_trigger:
            ap = applicant_filler(driver,number_of_applicants,applicants[1:])
            if ap == 'page not found':
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        a = get_applicants_page(driver)
        if a == 'page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
        while b:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),' Continue ')]"))).click()
            except:
                pass
            try:
                b = []
                b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
            except:
                pass
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass
            sleep(2)
    
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        a = get_calender_page(driver)
        if a == 'page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
        try:
            day,month = check_multiple_months(driver,req_months,slot_trigger)
        except Exception as e:
            print(e)
            
        if day=='page not found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

        def select_button(driver):
            try:
                driver.find_element(By.XPATH,"//input[@name='SlotRadio']").click()
            except:
                pass
            if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            sleep(0.2)
            selected = []
            try:
                selected = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']")
            except:
                pass
            if selected:
                time = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,'..').text
                time = time.split('\n')[0]
                return time
            else:
                return select_button(driver)
        time = select_button(driver)

        driver.find_element(By.XPATH,"/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button").click()
        # sleep(5)
        a = get_service_page(driver)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Services")]').text
        except:
            pass
        while ele:
            
            try:
                driver.find_element(By.XPATH,'/html/body/app-root/div/app-manage-service/section/mat-card[2]/div/div[2]/button').click()
            except:
                pass
            sleep(2)
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
            except:
                pass
            try:
                ele = ''
                ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Services")]').text
            except:
                pass            
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        
        a = get_review_page(driver)
        if a=='page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        close_pop_up(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.2)
        driver.find_element(By.XPATH,"//mat-checkbox").click()
        sleep(0.2)
        driver.find_elements(By.XPATH,"//mat-checkbox")[1].click()
        sleep(0.2)
        # pay online
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        a = get_payment_disc_page(driver)
        if a == 'page not found':
            page_not_found(driver,cred,cats,cities,formname,slot,i)
        close_pop_up(driver)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found(driver,cred,cats,cities,formname,slot,i)
        except:
            pass
        # continue
        ele = ''
        try:
            ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Payment Disclaimer")]').text
        except:
            pass
        while ele:
            
            try:
                driver.find_element(By.XPATH,'/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button').click()
            except:
                pass
            try:
                bar = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                print('Found Blue bar')
                return page_not_found(driver,creds,cats,cities,formname,slot,i)
            except:
                pass
            try:
                ele = ''
                ele = driver.find_element(By.XPATH,'//h1[contains(text(),"Payment Disclaimer")]').text
            except:
                pass
            # sleep(5)
        # driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found(driver,cred,cats,cities,formname,slot,i)
        sleep(5)
        payment(driver,formname)
        sleep(2)
        return
    return func1(cred,cats,cities,formname,slot,i)

def get_applicant_info(text):
    for j,i in enumerate(text):
        if 'First name' in i:
            first_name = i.split('-')[1].strip()
        if 'Last name' in i:
            last_name = i.split('-')[1].strip()
        if 'Gender' in i:
            gender = i.split('-')[1].strip()
        if 'DOB' in i:
            dob = i.split('-')[1].strip()
            while '/' in dob:
                dob = dob.replace('/','')
        if 'Current Nationality' in i:
            curr_nationality = i.split('-')[1].strip()
        if 'Passport Number' in i:
            pass_number = i.split('-')[1].strip()
        if 'Passport Expiry Date' in i:
            pass_expiry = i.split('-')[1].strip()
            while '/' in pass_expiry:
                pass_expiry = pass_expiry.replace('/','')
        if 'country code' in i:
            country_code = i.split('-')[1].strip()
        if 'Contact number' in i:
            contact_number = i.split('-')[1].strip()
        if 'E_mail' in i:
            email_ = i.split('-')[1].strip()
    return first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email_

def form_filler_for_applicant(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality):
    # first name
    print('Filling the form')
    driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']").send_keys(first_name)
    sleep(1)

    # last name
    driver.find_element(By.XPATH,"//input[@placeholder='Please enter last name.']").send_keys(last_name)
    sleep(1)

    # DOB
    driver.find_element(By.XPATH,"//input[@placeholder='Please select the date']").send_keys(dob)
    sleep(1)

    # passport number
    driver.find_element(By.XPATH,"//input[@placeholder='Enter passport number']").send_keys(pass_number)
    sleep(1)

    # passport Expiry date
    driver.find_elements(By.XPATH,"//input[@placeholder='Please select the date']")[1].send_keys(pass_expiry)
    sleep(1)

    # Country code
    driver.find_element(By.XPATH,"//input[@placeholder='44']").send_keys(country_code)
    sleep(1)

    # ph number
    driver.find_element(By.XPATH,"//input[@placeholder='012345648382']").send_keys(contact_number)
    sleep(1)

    # email
    driver.find_element(By.XPATH,"//input[@placeholder='Enter Email Address']").send_keys(email)
    sleep(1)
    try:
        # Gender
        driver.find_element(By.XPATH,"//mat-select").click()
        sleep(2)
        driver.find_elements(By.XPATH,"//mat-option")[gender_select(gender)].click()
    except:
        pass
    # Nationality
    driver.find_elements(By.XPATH,"//mat-select")[1].click()
    sleep(2)
    # driver.find_elements(By.XPATH,"//mat-option")[get_nationality(curr_nationality,nationalities)].click()
    options = driver.find_elements(By.XPATH,"//mat-option")
    for option in options:
        try:
            if option.text == curr_nationality.upper():
                option.click()
        except:
            pass
        
def applicant_filler(driver,number_of_applicants,applicants,k=0):
    while number_of_applicants > 0:
        # Add another applicant
        print(f'filling details of {k+1} applicant')
        try:
            driver.find_element(By.XPATH,"//span[contains(text(),'Add another applicant')]").find_element(By.XPATH,"..").click()
        except:
            pass
        sleep(2)
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return 'page not found'
        first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_applicant_info(applicants[k][1:])
        try:
            form_filler_for_applicant(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality)
        except:
            pass
        try:
            a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
            while a:
                try:
                    driver.find_element(By.XPATH,"/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button").click()
                except:
                    pass
                sleep(2)
                try:
                    h6 = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
                    return 'page not found'
                except:
                    pass
                try:
                    a = []
                    a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
                except:
                    pass
                sleep(2)
        except:
            pass
        sleep(2)
        try:
            if 'you must book appointment individually' in driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']").text:
                number_of_applicants -=1
                k+=1
        except:
            pass
    return 'done'

def appointment_found(available_date,formname,slot_info):
    with open(formname) as f:
        text = f.readlines()
        
    for i in text:
        if 'receiver' in i:
            emails = i.split('=')[1].split(',')
    for i in text:
        if 'outlook_email' in i:
            sender = i.split('=')[1].strip()
        if 'out_pass' in i:
            password = i.split('=')[1].strip()
            
    import smtplib, ssl
    SMTP_HOST = 'smtp-mail.outlook.com'
    SMTP_USER = sender
    SMTP_PASS = password
    from_email = sender
    to_emails = emails
    body = f"\n{slot_info}\n"
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n" 
    headers += f"Subject:Appointment found\r\n"
    email_message = headers + "\r\n" + body 

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_emails, email_message)

        
def calender_appointment(day,month,time,formname,cred,cats):
    with open(formname) as f:
        text = f.readlines()
        
    for i in text:
        if 'receiver' in i:
            emails = i.split('=')[1].split(',')
    for i in text:
        if 'outlook_email' in i:
            sender = i.split('=')[1].strip()
        if 'out_pass' in i:
            password = i.split('=')[1].strip()
    email_ = cred[0].split('=')[1].strip()
    cats = cats.split('=')[1].strip()
    import smtplib, ssl
    SMTP_HOST = 'smtp-mail.outlook.com'
    SMTP_USER = sender
    SMTP_PASS = password
    from_email = sender
    to_emails = emails
    body = f"Appointment date -{cats} : {email_} : {day},{month} at {time} \n\n\n"
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n" 
    headers += f"Subject:Appointment Schedule\r\n"
    email_message = headers + "\r\n" + body 

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_emails, email_message)
        
def check_slot2(driver,formname,cred,sub_cat):
    email_ = cred[0].split('=')[1].strip()
    sub_cat = sub_cat.split('=')[1].strip()
    try:
        slot = driver.find_element(By.XPATH,"//div[@class='border-info mb-0 ng-star-inserted']").text
        slot_info = sub_cat + " : " + email_ +" : " + slot
        print(slot_info)
        if 'Earliest Available Slot' in slot:
            available_date = slot.split(':')[1].strip()
            appointment_found(available_date,formname,slot_info)
            print('available')
    except Exception as e:
        print(e)

def start_new_booking2(driver):
    close_pop_up(driver)
    try:
        driver.find_element(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']").click()
    except:
        sleep(2)
    try:
        driver.find_element(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']").click()
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    try:
        if 'No internet' in driver.find_element(By.XPATH,"//span[@jsselect='heading']").text:
            print('No internet')
            return 'page not found'
    except:
        pass
    
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/dashboard':
        return start_new_booking2(driver)


def wait_till_login_loads2(driver,creds,cats,cities,formname,slot,i,j=0):
    while j<5:
        driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        try:
            if driver.find_element(By.XPATH,"//h1").text == 'Access denied':
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        try:
            if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
                driver.delete_all_cookies()    
                driver.refresh()   
        except:
            pass
        try:
            driver.find_element(By.XPATH,"/html/body/app-root/div/app-login/section/div/div/mat-card/form/button")
            print('found sign in')
            return
        except:
            j+=1
            return wait_till_login_loads2(driver,creds,cats,cities,formname,slot,i,j)
        sleep(2)
    return page_not_found2(driver,creds,cats,cities,formname,slot,i)
    
def go_to_login_page2(driver,creds,cats,cities,formname,slot,i,j=0):
    while j<5:
        
        try:
            driver.get('https://visa.vfsglobal.com/ind/en/pol/book-an-appointment')
        except Exception as e:
            print(e)
            
        sleep(7)
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        driver.delete_all_cookies()
        try:
            driver.find_element(By.XPATH,'//*[@id="__layout"]/div/main/div/div/div[3]/div/p[19]/a').click()
            return 
        except:
            j+=1
            return go_to_login_page2(driver,creds,cats,cities,formname,slot,i,j)
    return page_not_found2(driver,creds,cats,cities,formname,slot,i)


def login_withot_captcha2(driver,creds,cats,cities,formname,slot,i):
    print(creds)
    print(cats)
    print(formname)
    go_to_login_page2(driver,creds,cats,cities,formname,slot,i)
    sleep(2)
    driver.delete_all_cookies()

    sleep(20)
    driver.switch_to.window(driver.window_handles[1])
    wait_till_login_loads2(driver,creds,cats,cities,formname,slot,i)
    vfs_account_email = creds[0].split('=')[1].strip()
    vfs_account_password = creds[1].split('=')[1].strip()
    close_pop_up(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    sleep(2)

    def check_captcha(driver,j=0):
        while j<3:
            driver.switch_to.default_content()
            try:
                frames = driver.find_elements(By.TAG_NAME,"iframe")
                driver.switch_to.frame(frames[0])
                sleep(1)
                g_captcha = []
                try:
                    g_captcha = driver.find_element(By.XPATH,"//td[@id='branding']")
                except:
                    pass
                if not g_captcha:
                    return page_not_found2(driver,creds,cats,cities,formname,slot,i)
            except:
                pass
            try:
                driver.find_element(By.XPATH,'//*[@id="cf-stage"]').click()
            except:
                pass
            success = []
            try:
                success = driver.find_element(By.XPATH,"//div[@id='success']").text
            except:
                pass
            if not success:
                j+=1
                return check_captcha(driver,j)
            else:
                return
        else:
            return
        #let me test i will come back
    check_captcha(driver)
    try:
        driver.find_element(By.XPATH,'//*[@id="cf-stage"]').click()
    except:
        pass
    
    driver.switch_to.default_content()
    
    try:
        if driver.find_element(By.XPATH,"//h1").text == 'Access denied':
            return page_not_found2(driver,creds,cats,cities,formname,slot,i)
    
    except:
        pass
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-0"]'))).send_keys(vfs_account_email)
    except:
        pass

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-1"]'))).send_keys(vfs_account_password)
    except:
        pass
    print('Entered Email and Password')
    driver.switch_to.default_content()
    try:
        print('clicking')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/div/app-login/section/div/div/mat-card/form/button'))).click()
        print('clicked')
    except:
        sleep(2)
    try:
        print('clicking')
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-login/section/div/div/mat-card/form/button").click()
        print('clicked')
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return page_not_found2(driver,creds,cats,cities,formname,slot,i)
    except:
        pass
    
    sleep(10)
    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/login':
        return page_not_found2(driver,creds,cats,cities,formname,slot,i)
    
def page_not_found2(driver,cred,cats,cities,formname,slot,i):
    i+=1
    driver,i = new_driver(i,formname)
    sleep(7)
    return child_func2(driver,cred,cats,cities,formname,slot,i)

def month_matcher2(driver,req_month):
    print(req_month)
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for i,m in enumerate(months):
        if req_month in m:
            req_month_idx = i
    try:
        current_month = driver.find_element(By.XPATH,"//div[@class='fc-header-toolbar fc-toolbar ']").text.split()[0]
        for i,m in enumerate(months):
            if current_month in m:
                current_month_idx = i
    except:
        return month_matcher2(driver,req_month)
    
    if req_month_idx < current_month_idx:
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[1]"))).click()
        except:
            pass
        sleep(2)
        # h6 = []
        try:
            text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
            if 'Sorry' in text_:
                return 'page not found'
        except:
            pass
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
        sleep(2)
        return month_matcher2(driver,req_month)

    elif req_month_idx > current_month_idx:
        try:
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[2]"))).click()
        except:
            pass
        sleep(2)
        # h6 = []
        try:
            text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
            if 'Sorry' in text_:
                return 'page not found'
        except:
            pass
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
        sleep(2)
        return month_matcher2(driver,req_month)
    
    # h6 = []
    try:
        text_ = driver.find_element(By.XPATH,"//span[@class='c-brand-blue']")
        if 'Sorry' in text_:
            return 'page not found'
    except:
        pass

    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    else:
        return 'matched'

def back_and_forward2(driver,month_,slot_trigger):
    try:
        btns = driver.find_element(By.XPATH,"//div[@class='fc-button-group']").find_elements(By.XPATH,".//button")
    except:
        pass
    try:
        btns[0].click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    except:
        pass
    
    try:
        btns[1].click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return 'page not found'
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    sleep(3)
    a = month_matcher2(driver,month_)
    if a=='page not found':
        return 'page not found'
    select_date2(driver,month_,slot_trigger)
    
def select_date2(driver,month_,slot_trigger):
    print(month_)
    if slot_trigger == 'A':
        r1,r2  = 1,10
    if slot_trigger == 'B':
        r1,r2  = 10,20
    if slot_trigger == 'C':
        r1,r2  = 20,32
    if slot_trigger == 'D':
        r1,r2  = 1,32
        
    slot_range = range(r1,r2)
    day = []
    month = []
    try:
        table = driver.find_element(By.XPATH,"//table[@class='fc-scrollgrid-sync-table']")
        rows = table.find_elements(By.XPATH,".//tr")    
    except:
        pass
    try:
        for row in rows:
            ele = []
            for i in row.find_elements(By.XPATH,'.//td'):

                if 'future date-availiable' in i.get_attribute('class'):
                    ele.append(i)
            try:
                day = int(ele[0].text.strip())
                if day in slot_range:
                    ele[0].click()
                    month = driver.find_element(By.XPATH,'//h2[@class="fc-toolbar-title"]').text
                    print([day,month])
                    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                        return 'page not found'
                    sleep(2)
                    return day,month
            except:
                pass
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass
    try:
        if 'Sorry, you have been blocked' in driver.find_element(By.XPATH,"//h1").text:
            return 'page not found'   
    except:
        pass
    return back_and_forward2(driver,month_,slot_trigger)

def select_date_from_mult_months2(driver,month_,slot_trigger):
    print(month_)
    if slot_trigger == 'A':
        r1,r2  = 1,10
    if slot_trigger == 'B':
        r1,r2  = 10,20
    if slot_trigger == 'C':
        r1,r2  = 20,32
    if slot_trigger == 'D':
        r1,r2  = 1,32
    slot_range = range(r1,r2)
    day = []
    month = []
    try:
        table = driver.find_element(By.XPATH,"//table[@class='fc-scrollgrid-sync-table']")
        rows = table.find_elements(By.XPATH,".//tr")    
    except:
        pass
    try:
        for row in rows:
            ele = []
            for i in row.find_elements(By.XPATH,'.//td'):

                if 'future date-availiable' in i.get_attribute('class'):
                    ele.append(i)
            try:
                day = int(ele[0].text.strip())
                if day in slot_range:
                    ele[0].click()
                    month = driver.find_element(By.XPATH,'//h2[@class="fc-toolbar-title"]').text
                    print([day,month])
                    if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                        return 'page not found'
                    sleep(2)
                    return day,month
            except:
                pass
    except:
        pass
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found','page not found'
    except:
        pass
    return day,month

def check_multiple_months2(driver,req_months,slot_trigger):
    if len(req_months)>1:
        for month_ in req_months:
            a = month_matcher2(driver,month_)
            if a=='page not found':
                return 'page not found','page not found'
            day,month = select_date_from_mult_months2(driver,month_,slot_trigger)
            if day == 'page not found':
                return 'page not found','page not found'
            if month:
                return day,month
        else:
            return check_multiple_months2(driver,req_months,slot_trigger)
    else:
        a = month_matcher2(driver,req_months[0])
        if a=='page not found':
            return 'page not found','page not found'
        day,month = select_date2(driver,req_months[0],slot_trigger)
        return day,month
    
def main_3(driver,sub_cat,city):
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found'
    try:
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-form-field-wrapper ng-tns-c63-3']"))).click()
        sleep(2)
    except:
        pass
        
    try:
        box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
    except:
        sleep(2)
    
    if driver.current_url =='https://visa.vfsglobal.com/ind/en/pol/page-not-found':
        return 'page not found'
    close_pop_up(driver)
    
    try:
        if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
            print('site cannnot be reached')
            return 'page not found'
    except:
        pass

    h6 = []
    try:
        text_ = driver.find_element(By.XPATH,"//div[@class='mt-15']").find_element(By.XPATH,".//h6").text
        if 'Sorry' in text_:
            return 'page not found'
    except:
        pass

    cnt = []
    try:
        cnt = driver.find_element(By.XPATH,"//h6[@class='d-inline pull-right text-right ng-star-inserted']")
    except:
        pass
    if not cnt:
        return 'page not found','page not found'
    
    try:
        centres_ = box.find_elements(By.XPATH,"//mat-option")    
        main_centeres = []
        for l in centres_:
            main_centeres.append(l.text)

        to_go_index = []
        for l,val in enumerate(main_centeres):
            if city in val:
                to_go_index.append(l)

        for i in range(len(centres_)):
            try:
                centres_[to_go_index[0]].click()
                sleep(2)
                a = hover2(driver,sub_cat)
                if a == 'bar':
                    return 'page not found'
                sleep(2)
                
                cont_btn = []
                try:
                    cont_btn = driver.find_elements(By.XPATH,"//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']")
                except:
                    pass
                if cont_btn:
                    sleep(1)
                    return 'Continue'
                try:
                    if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                        print('site cannnot be reached')
                        return 'page not found'
                except:
                    pass
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    sleep(2)
                try:
                    driver.find_element(By.XPATH,"//div[@class='mat-form-field-wrapper ng-tns-c63-3']").click()
                except:
                    pass
                box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
                opts = box.find_elements(By.XPATH,".//mat-option")

            except:
                pass
    except:
        pass
    return main_3(driver,sub_cat,city)

def child_func2(driver,cred,cats,cities,formname,i):      
    with open(formname) as f:
        text = f.readlines()
        
    number_of_applicants = 0
    for line in text:
        if f'E_id_{num}' in line:
            number_of_applicants +=1
    
    print(f'Found {number_of_applicants} applicants')
    
    applicants = []
    for num_ in range(1,number_of_applicants+1):
        for idx,val in enumerate(text):
            if f'E_id_{num}_Applicant {num_}' in val:
                text1 = text[idx:]
        for idx,val in enumerate(text1):
            if 'E_mail' in val:
                applicants.append(text1[:idx+1])
                break
            
    login_withot_captcha2(driver,cred,cats,cities,formname,i)    
    booking = start_new_booking2(driver)
    if booking == 'page not found':
        page_not_found2(driver,cred,cats,cities,formname,slot,i)
    to_do = main_3(driver,cats,cities)
    if to_do == 'page not found':
        page_not_found2(driver,cred,cats,cities,formname,slot,i)
    if to_do == 'Continue':
        close_pop_up(driver)
        try:
            driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
        except:
            pass                       
        try:
            driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
        except:
            pass
        sleep(2)
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        # first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_form_info(formname)
        first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_applicant_info(applicants[0][1:])
        form_filler(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality)
        a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
        while a:
            try:
                driver.find_element(By.XPATH,"/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button").click()
            except:
                pass
            sleep(2)

            
            try:
                a = []
                a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
            except:
                pass
            sleep(5)
        sleep(2)
        
        ap = applicant_filler(driver,number_of_applicants,applicants[1:])
        if ap == 'page not found':
            return page_not_found(driver,creds,cats,cities,formname,slot,i)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
        while b:
            try:
                WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),' Continue ')]"))).click()
            except:
                pass
            try:
                b = []
                b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
            except:
                pass
            sleep(5)
        sleep(2)

        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        
        driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
        sleep(1)
        day,month = check_multiple_months2(driver,req_months)
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        def select_button(driver):
            try:
                driver.find_element(By.XPATH,"//input[@name='SlotRadio']").click()
            except:
                pass
            if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return page_not_found2(driver,cred,cats,cities,formname,slot,i)
            sleep(2)
            selected = []
            try:
                selected = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']")
            except:
                pass
            if selected:
                time = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,'..').text
                time = time.split('\n')[0]
                return time
            else:
                return select_button(driver)
        time = select_button(driver)
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button").click()

        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(2)
        close_pop_up(driver)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-manage-service/section/mat-card[2]/div/div[2]/button"))).click()
        
        sleep(2)
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        close_pop_up(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        driver.find_element(By.XPATH,"//mat-checkbox").click()
        sleep(2)
        driver.find_elements(By.XPATH,"//mat-checkbox")[1].click()
        sleep(2)
        # pay online
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(2)

        close_pop_up(driver)
        # continue
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(2)
        payment(driver,formname)
        sleep(2)

        return
    return func2(cred,cats,cities,formname,i)
    
def func2(cred,cats,cities,formname,i=0):
    global num
    if 'email' in cred[0]:
        num = []
        for n in cred[0].split('=')[0].strip():
            if n.isnumeric():
                num.append(n)
        num = int("".join(num))
        global slt
        slt = slots[num-1]
        print(num)
        global email_sub_creds
        email_sub_creds = sub_em[num-1]

    with open(formname) as f:
        text = f.readlines()
        
    number_of_applicants = 0
    for line in text:
        if f'E_id_{num}' in line:
            number_of_applicants +=1
    
    print(f'Found {number_of_applicants} applicants')
    
    applicants = []
    # num_ = 1
    for num_ in range(1,number_of_applicants+1):
        for idx,val in enumerate(text):
            if f'E_id_{num}_Applicant {num_}' in val:
                text1 = text[idx:]
        for idx,val in enumerate(text1):
            if 'E_mail' in val:
                applicants.append(text1[:idx+1])
                break   
            
    driver,i = new_driver(i,formname)
    actions = ActionChains(driver)
    login_withot_captcha2(driver,cred,cats,cities,formname,slot,i)
    booking = start_new_booking2(driver)
    if booking == 'page not found':
        page_not_found2(driver,cred,cats,cities,formname,slot,i)
    to_do = main_3(driver,cats,cities)
    if to_do == 'page not found':
        page_not_found2(driver,cred,cats,cities,formname,slot,i)

    if to_do == 'Continue':
        close_pop_up(driver)
        try:
            driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
        except:
            pass                       
        try:
            driver.find_element(By.XPATH,"//span[contains(text(),' Continue ')]").click()
        except:
            pass
        sleep(2)
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        # first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email,nationalities = get_form_info(formname)
        first_name,last_name,gender,dob,curr_nationality,pass_number,pass_expiry,country_code,contact_number,email = get_applicant_info(applicants[0][1:])
        form_filler(driver,first_name,last_name,dob,pass_number,pass_expiry,country_code,contact_number,email,gender,curr_nationality)
        a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
        while a:
            try:
                driver.find_element(By.XPATH,"/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button").click()
            except:
                pass
            sleep(2)
            try:
                a = []
                a = driver.find_element(By.XPATH,"//input[@placeholder='Enter your first name']")
            except:
                pass
            sleep(5)
        sleep(2)
        
        ap = applicant_filler(driver,number_of_applicants,applicants[1:])
        if ap == 'page not found':
            return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass
        
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
        while b:
            try:
                WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),' Continue ')]"))).click()
            except:
                pass
            try:
                b = []
                b = driver.find_element(By.XPATH,"//p[@class='c-brand-grey-para mb-10']")
            except:
                pass
            sleep(5)

        sleep(2)

        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)

        close_pop_up(driver)
        
        driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
        sleep(1)
        day,month = check_multiple_months2(driver,req_months)
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        def select_button(driver):
            try:
                driver.find_element(By.XPATH,"//input[@name='SlotRadio']").click()
            except:
                pass
            if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
                return page_not_found2(driver,cred,cats,cities,formname,slot,i)
            sleep(2)
            selected = []
            try:
                selected = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']")
            except:
                pass
            if selected:
                time = driver.find_element(By.XPATH,"//input[@class='ba-slot-radio active']").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,'..').text
                time = time.split('\n')[0]
                return time
            else:
                return select_button(driver)
        time = select_button(driver)
        
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button").click()

        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(2)
        close_pop_up(driver)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/app-manage-service/section/mat-card[2]/div/div[2]/button"))).click()
        
        sleep(2)
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        
        try:
            if 'This site can’t be reached' in driver.find_element(By.XPATH,"//h1").text:
                print('site cannnot be reached')
                return page_not_found2(driver,creds,cats,cities,formname,slot,i)
        except:
            pass

        close_pop_up(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        driver.find_element(By.XPATH,"//mat-checkbox").click()
        sleep(2)
        driver.find_elements(By.XPATH,"//mat-checkbox")[1].click()
        sleep(2)
        # pay online
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(10)

        close_pop_up(driver)
        # continue
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-review-and-payment/section/mat-card/div[2]/div[2]/button").click()
        if driver.current_url == 'https://visa.vfsglobal.com/ind/en/pol/page-not-found':
            return page_not_found2(driver,cred,cats,cities,formname,slot,i)
        sleep(2)
        payment(driver,formname)
        sleep(5)

        return
    return func2(cred,cats,cities,formname,i)

def get_creds(formname):
    with open(formname) as f:
        text = f.readlines()
    creds = []
    for i,val in enumerate(text):
        if 'email' in val:
            creds.append(text[i:i+2])
        if 'cities1' in val:
            break

    sub_em = []
    for i,val in enumerate(text):
        if f"sub_creds" in val:
            a = []
            for k in range(3):
                a.append(text[i+1:i+3])
                i+=2
            sub_em.append(a)   

    cities = []
    for i,val in enumerate(text):
        if 'cities' in val:
            cities.append(text[i])

    sub_cats = []
    for i,val in enumerate(text):
        if 'sub_cat' in val:
            sub_cats.append(text[i])

    for i in text:
        if 'receiver_email' in i:
            receiver_emails = (i.split('=')[1].strip().split(','))

    for i in text:
        if 'Month_year' in i:
            req_months = (i.split('=')[1].strip().split(','))

    triggers = []
    for i in text:
        if 'trigger' in i:
            triggers.append(int(i.split('=')[1].strip()))

    repeat_triggers = []
    for i in text:
        if 'repeat_' in i:
            repeat_triggers.append(int(i.split('=')[1].strip()))
            
    headless_triggers = []
    for i in text:
        if 'headless' in i:
            headless_triggers.append(int(i.split('=')[1].strip()))

    coapplicant_triggers = []
    for i in text:
        if 'co_applicant_trigger' in i:
            coapplicant_triggers.append(int(i.split('=')[1].strip()))
    for i in text:
        if 'slot_trigggers' in i:
            slot_trigger = i.split('=')[1].strip()
            
    return creds,sub_em,cities,sub_cats,receiver_emails,triggers,req_months,repeat_triggers,headless_triggers,coapplicant_triggers,slot_trigger

slots0,slots1,slots2,slots3,slots4,slots5,slots6,slots7,slots8,slots9,slots10,slots11,slots12,slots13,slots14,slots15,slots16,slots17,slots18,slots19,slots20,slots21,slots22,slots23,slots24= ([] for i in range(25))
slots = [slots0,slots1,slots2,slots3,slots4,slots5,slots6,slots7,slots8,slots9,slots10,slots11,slots12,slots13,slots14,slots15,slots16,slots17,slots18,slots19,slots20,slots21,slots22,slots23,slots24]

forms_ = 0
form_names = []
for i in os.listdir():
    if '_cat' in i:
        form_names.append(i)
        forms_+=1
        
print(f'found {forms_} forms, Starting for {forms_} forms')

creds,sub_em1,cities,sub_cats,receiver_emails,triggers,req_months,rt,ht,ct,st = get_creds('form0_cat.txt')

global sub_em
sub_em = []
with open(f'form0_cat.txt') as f:
    text = f.readlines()
for i,val in enumerate(text):
    if f"sub_creds" in val:
        a = []
        for k in range(len(creds)):
            a.append(text[i+1:i+3])
            i+=2
        sub_em.append(a)

def new1(cred,sub_cat,cities,trigger,formname,slot,k):
    if trigger:
        cities_to_ignore = cities.split('=')[1].strip().split(',')
        Cities = ['Ahmedabad','Bangalore','Chandigarh','Chennai','Hyderabad','Jaipur','Kolkata','Mumbai','New Delhi']
        for i in cities_to_ignore:
            try:
                Cities.remove(i)
            except:
                pass
        a = len(Cities)
        print(Cities)
        func2(cred,sub_cat,cities,formname,slot,k)

    else:
        func1(cred,sub_cat,cities,formname,slot,k)

def forms(formname):
    creds,sub_em1,cities,sub_cats,receiver_emails,triggers,req_months,rt,gt,ct,st = get_creds(formname)
    a = len(creds)
    a = 1
    for i in range(a):
        slot = shared_memory.ShareableList(['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']*len(sub_em1[0]))
        p = multiprocessing.Process(target=new1,args=([creds[i],sub_cats[i],cities[i],triggers[i],formname,slot,i]))
        p.start()
        slot.close()

# slot = shared_memory.ShareableList(['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']*len(sub_em1[0]))
# if __name__ == "__main__":
#     func1(creds[0],sub_cats[2],cities[0],form_names[0],slot,3)

if __name__ == "__main__":
    multiprocessing.freeze_support() 
    proc = []
    for i in range(forms_):
        p = multiprocessing.Process(target=forms,args=([form_names[i],]))
        p.start()
        proc.append(p)
        
    for p in proc:
         p.join()
    # main()
