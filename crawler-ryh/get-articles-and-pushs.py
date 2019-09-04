
# coding: utf-8

# In[18]:


# https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference


# In[19]:


from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup
import time
import pandas as pd
from pandas import DataFrame as DF
from IPython.display import display

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship,backref


import smtplib
from email.mime.text import MIMEText


from urllib.request import urlopen
import json 


# In[20]:


options = Options()
options.headless = True
# _browser_profile = webdriver.FirefoxProfile()
# _browser_profile.set_preference("dom.webnotifications.enabled", False)
executable_path='/media/disk3/feynman52/dummy/SQLAlchemy/591/geckodriver'
browser = webdriver.Firefox(executable_path=executable_path,
                            options=options)


# In[21]:


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
    
def get_session(engine):
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
    
def add_to_table(session,item):
    session.add(item)
    session.commit()
    
def delete_from_table(session,item):
    session.delete(item)
    session.commit()
    
def sql_to_df(engine,query=''):
    df = pd.read_sql_query(query, engine)
    return df

def get_engine(db_name=''):
    db_dir='/media/disk3/feynman52/See26/crawler-ryh'
    db_url = 'sqlite:///'+db_dir+'/'+db_name
    engine = create_engine(db_url, echo = False)
    return engine
    

    

def append_txt_to_file(txt=''):
    with open("error.txt", "a") as myfile:
        myfile.write("%s\n"%(txt))
        



# # get articles

# In[22]:


engine_article = get_engine(db_name='articles.db')

Base = declarative_base()
class Article(Base):
    __tablename__ = 'article'
    article_id = Column(Integer, primary_key=True)
    article_user = Column(String)
    article_group = Column(String)
    article_title = Column(String)
    article_time = Column(String)
    article_weekday = Column(Integer)
    article_ip = Column(String)   
    article_url = Column(String)    
    
    

class Push(Base):
    __tablename__ = 'push'
    push_id = Column(Integer, primary_key=True)
    push_user = Column(String)
    push_tag = Column(String)
    push_time = Column(String)
    push_content = Column(String)
    push_weekday = Column(Integer)
    push_ip = Column(String)
    
    article_id = Column(Integer, ForeignKey('article.article_id'))
    article = relationship("Article", back_populates = "push")
    
Article.push=relationship("Push", order_by = Push.push_id, back_populates = "article")
Base.metadata.create_all(engine_article)

# Push.__table__.drop(engine_article)
# Article.__table__.drop(engine_article)


# In[ ]:





# In[23]:


def get_current_page(browser,url):
    get_page(browser,page=url)
    pageSource = browser.page_source  
    current_page = BeautifulSoup(pageSource)  
    return current_page


# In[24]:


def get_article(current_page,article_url):
    article_meta_value=current_page.find_all('span',{'class':'article-meta-value'})
    article_meta_value=[x.string for x in article_meta_value]
    article_user=article_meta_value[0].split(' ')[0]    
    article_group=article_meta_value[1]
    article_title=article_meta_value[2]
    article_time=str(pd.to_datetime(article_meta_value[3]))
    article_weekday=pd.to_datetime(article_time).weekday()
    article_ip=current_page.find_all('span',{'class':'f2'})
    article_ip=[x.string for x in article_ip if x.string!=None and '來自' in x.string]
    
    try: 
        article_ip=article_ip[0]
        article_ip=article_ip[article_ip.find('來自: ')+len('來自: '):]
        article_ip=article_ip.split(' ')[0].replace('\n','')
    except:
        article_ip='no_article_ip'
    

    article=Article(
        article_user = article_user,
        article_group = article_group,
        article_title = article_title,
        article_time = article_time,
        article_weekday = article_weekday,
        article_ip = article_ip,
        article_url = article_url
    )
    
    return article


# # get pushs

# In[25]:


def get_pushs(current_page,article_time):
    pushs=current_page.find_all('div',{'class':'push'})
    push_objects=[]
    for push in pushs:
        push=push.find_all('span')
        
        if len(push)==0: continue
        
        push=[x.text.replace('\n','') for x in push]
        push_tag=push[0].replace(' ','')

        push_user=push[1]

        push_content=push[2].replace(': ','')

        push_ipdt=push[3]

        push_ip=push_ipdt[:-len('07/23 15:53')].replace(' ','')
        push_ip=push_ip if len(push_ip)>0 else 'no_push_ip'

        push_time=' '.join([article_time[:4],push_ipdt[-len('07/23 15:53'):]])
        push_time=str(pd.to_datetime(push_time))

        push_weekday=pd.to_datetime(push_time).weekday()

        push=Push(
            push_user = push_user,
            push_tag = push_tag,
            push_time = push_time,
            push_content = push_content,
            push_weekday = push_weekday,
            push_ip = push_ip
        )
        push_objects.append(push)
        
    return push_objects
    


# In[26]:


browser=get_browser()
get_page(browser,page='https://www.ptt.cc/bbs/Gossiping/index.html')
click_button(browser,xpath='/html/body/div[2]/form/div[1]/button')
session=get_session(engine_article)


# In[ ]:





# In[27]:



# xs = session.query(Push).filter(Push.article_id==None)
# for x in xs:
#     delete_from_table(session,x)


# In[ ]:





# In[37]:


def get_urls(engine_url,engine_article):
    new_urls=sql_to_df(engine_url,query='select * from urls').url.tolist()
    old_urls=sql_to_df(engine_article,query='select * from article').article_url.tolist()
    new_urls_after_remove=list(set(new_urls)-set(old_urls))
    new_urls_after_remove.sort()
    return new_urls_after_remove

engine_url=get_engine(db_name='urls.db')
urls=get_urls(engine_url,engine_article)
len(urls)


# In[38]:

old_urls=sql_to_df(engine_article,query='select * from article').article_url.tolist()
current=6000+len(old_urls)
total=len(urls)
for url in urls[current:]:
    
    print('---------------')
    print(url)
    print('%s/%s'%(current,total))
    current+=1
    
    
    try:
        current_page=get_current_page(browser,url=url)
        article=get_article(current_page,url)    
        pushs=get_pushs(current_page,article_time=article.article_time)
        article.push = pushs
        add_to_table(session,article)
        
    except Exception as e:
        print(e)
        append_txt_to_file(txt='---------------')
        append_txt_to_file(txt=url)
        append_txt_to_file(txt=e)
        
        
        
      
    




