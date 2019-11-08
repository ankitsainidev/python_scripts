#!/usr/bin/env python
# coding: utf-8

# In[190]:


email = '' #email or mobile number
password = '' #password
headlessBrowser = True
addressOfGeckodriverFirefox = '/home/ankit/Downloads/geckodriver-v0.24.0-linux64/geckodriver' 
pagename = 'Anox'  # get id and pagename from the link of your page ex:'https://www.facebook.com/Anox-2477477185610065/posts/'
pageid = '2477477185610065' #enter the page id from your page link

numPosts = 20 #number of posts for invitation
sleepTime = 2 #a positive number denoting the time in seconds to wait before performing next operation. increase if your device lags and decrease if you feel the script is taking long and device is working fine.

pageLink = f'https://www.facebook.com/{pagename}-{pageid}/posts'# DON'T CHANGE this field link of the page when you open it something like 'https://www.facebook.com/Anox-2477477185610065/posts/'
# In[191]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from time import sleep


# In[192]:
_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
if headlessBrowser:
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options = options, firefox_profile=_browser_profile,executable_path=addressOfGeckodriverFirefox)
else:

    


    # In[193]:


    browser = webdriver.Firefox(firefox_profile=_browser_profile,executable_path=addressOfGeckodriverFirefox)


# In[194]:


browser.get("http://www.facebook.com")
sleep(sleepTime)
browser.find_element_by_id('email').send_keys(email)

browser.find_element_by_id('pass').send_keys(password)

browser.find_element_by_id('u_0_2').click()

browser.get(pageLink)
postdiv = browser.find_element_by_class_name('_1xnd')
postlikes = None


# In[195]:


sleep(sleepTime)
tried = 0
last_height=-1
while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(sleepTime)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    postlikes = postdiv.find_elements_by_class_name('_3dlh')
    postlikes = [post for post in postlikes if post.get_attribute('class')=='_3dlh _3dli']
    if len(postlikes) >= numPosts:
        postlikes=postlikes[:numPosts]
        break
    elif last_height==new_height:
        tried+=1
        if tried>=20:
            print(f'Inviting for {len(postlikes)} posts only. As no more posts available. Or internet connection is too slow to load')
            break
    last_height = new_height


# In[200]:

totalInvites=0
def sendinvite(post):
    post.click()
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_5i_q")))
    finally:
        J =3
    likelistElm = browser.find_elements_by_class_name('_5i_p')
    
    myelm =None
    sleep(0.7)
    for likelist in likelistElm:
        if likelist.get_attribute('class') =='_5i_p':
            myelm = likelist
    while True:
        all_children = myelm.find_elements_by_class_name("pam")
        showchild = None
        ismore = False
        
        
        for child in all_children:
            if child.is_displayed():
                showchild = child
                ismore = True
                
                break
            else:
                ismore = False
        
        if ismore:
            showchild.click()
            while True:
                if showchild.is_displayed() == False:
                    break
                sleep(0.2)
        else:
            break
        sleep(sleepTime)
        
    likelistElm = browser.find_elements_by_class_name('_5i_p')
        
        
            
    toinvite = browser.find_elements_by_class_name('_42ft')
    for i,invite in enumerate(toinvite):
        if invite.text =='Invite':
            invite.click()
            totalInvites +=1
            while True:
                if browser.find_elements_by_class_name('_42ft')[i].text == 'Invited':
                    break
                sleep(0.2)
    all_children = myelm.find_elements_by_class_name("pam")
    browser.find_element_by_class_name('_50z-').click()
    return all_children


# In[202]:


for post in postlikes:
    sendinvite(post)
    sleep(sleepTime)
print(f'total {totalInvites} peoples are invited by this script')
