
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup
import time
import pandas as pd
from pandas import DataFrame as DF
from IPython.display import display

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import smtplib
from email.mime.text import MIMEText


# In[2]:


def get_page(browser,page=''):
    browser.get(page)
    time.sleep(1)
    
def click_button(browser,xpath=''):
    dummy=browser.find_element_by_xpath(xpath)
    dummy.click()
    time.sleep(1)
    
def send_keys(browser,xpath='',value=''):
    dummy=browser.find_element_by_xpath(xpath)
    dummy.send_keys(value)
    time.sleep(1)
    


# In[3]:


db_dir='/media/disk3/feynman52/See26/crawler-ryh'
db_name='urls.db'
db_url = 'sqlite:///'+db_dir+'/'+db_name
db_url


# In[4]:


engine = create_engine(db_url, echo = False)
Base = declarative_base()

class Urls(Base):
    __tablename__ = 'urls'
    url_id = Column(Integer, primary_key=True)
    url_title = Column(String)
    url_link = Column(String)
    url_user = Column(String)
    url_hot = Column(String)
    
Base.metadata.create_all(engine)

# Urls.__table__.drop(engine)



# In[26]:


def add_to_table(items):
    session.add_all(items)
    session.commit()
    
def get_session(engine):
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def get_old_urls(session):
    old_url_objects=session.query(Urls).order_by(Urls.url_id.desc()).limit(100).all()
    return old_url_objects


def sql_to_df(query=''):
    engine = create_engine(db_url)
    df = pd.read_sql_query(query, engine)
    return df


def get_browser():
    options = Options()
    options.headless = True
    _browser_profile = webdriver.FirefoxProfile()
    _browser_profile.set_preference("dom.webnotifications.enabled", False)
    executable_path='/media/disk3/feynman52/dummy/SQLAlchemy/591/geckodriver'
    browser = webdriver.Firefox(executable_path=executable_path,
                                options=options,
                                firefox_profile=_browser_profile)
    return browser




def get_url_object(row):
    try:
        url_user=row.find('div',{'class':'author'}).text.replace('\n','')
        url_title=row.find('div',{'class':'title'}).text.replace('\n','')
        url_hot=row.find('div',{'class':'nrec'}).text.replace('\n','')
        url_link='https://www.ptt.cc'+row.find('a')['href']
        url_object=Urls(
            url_user=url_user,
            url_title=url_title,
            url_hot=url_hot,
            url_link=url_link,)
        return url_object
    except:
        return


browser=get_browser()
get_page(browser,page='https://www.ptt.cc/bbs/Gossiping/index.html')
click_button(browser,xpath='/html/body/div[2]/form/div[1]/button')

session=get_session(engine)



current=38928
temp=[]
while True:
    get_page(browser,page='https://www.ptt.cc/bbs/Gossiping/index%s.html'%(current))
    pageSource = browser.page_source  
    current_page = BeautifulSoup(pageSource,features="lxml")  
    
    rows=current_page.find_all('div',{'class':'r-ent'})
    new_urls=[get_url_object(row) for row in rows if get_url_object(row)!=None]
    
    old_urls=get_old_urls(session)
    old_urls=[x.url_link for x in old_urls]
    
    new_urls_after_remove=[x for x in new_urls if x.url_link not in old_urls]
    
    print('---------')
    print('current',current)
    print('new_urls_after_remove',len(new_urls_after_remove))
    
    if len(new_urls_after_remove)!=0:
        new_urls_after_remove=[(x.url_link,x) for x in new_urls_after_remove]
        temp+=new_urls_after_remove
        
    else:
        print('new urls=',len(temp))
        temp.sort()
        temp=[x[1] for x in temp]
        add_to_table(temp)
        break
        
    current-=1
    



