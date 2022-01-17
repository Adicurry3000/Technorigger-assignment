
import sqlalchemy as db
from sqlalchemy import  MetaData,Integer,Column,Table,Computed,String, Date, Boolean,create_engine, ForeignKey
from selenium import webdriver
from sqlalchemy import event


engine = create_engine('sqlite:///main.db', echo = True)
metadata = MetaData()

# @event.listens_for(engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

Locations = Table(
    "Locations",metadata,
    Column('Location',String)
    )

Skill = Table(
    "Skill",metadata,
    Column('Skills',String)
)

Company = Table(
    "Company",metadata,
    Column('Name',String),
    Column('openings',String),
    Column('Url',String)
)

Jobs = Table(
    "Jobs", metadata ,
    Column('Title', String),
    Column('Category', String ),
    Column('Post', String),
    Column('Required skills', None,ForeignKey('Skill.Skills') ),
    Column('Required experience', String),
    Column('Job_id',String),
    Column('Location', None,ForeignKey('Locations.Location')),
    Column('Company', None,ForeignKey('Company.Name')),
    Column('Date', String),
    Column('Job url', String),
    Column('Available', Boolean),
)



metadata.create_all(engine)


PATH = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(PATH)
driver2 = webdriver.Chrome(PATH)

driver.get('https://atlan.com/careers/')

main = driver.find_element_by_id('open-positions')

aTags = main.find_elements_by_tag_name('a')

count = 0
for a in aTags:
    title = a.find_element_by_class_name('mb-0')
    link = a.get_attribute('href')
    location = ''
    texts = ''
    cate = ''
    # print('Title:'+title.text)
    e_title = title.text
    # print('link:'+link)
    e_link = link
    driver2.get(link)
    loc = driver2.find_elements_by_tag_name('h4')
    for lo in loc:
        if location == '':
            location += lo.text
            # print('loc:'+location)
            
        else :
            cate += lo.text
            # print('category:'+cate)
            
    post_t = driver2.find_elements_by_tag_name('ul')
    count+=1
    texts = ''
    texts2 = ''
    texts3 = ''
    for lists in post_t:

        objs = lists.find_elements_by_tag_name('li')
        if texts=='':
            for obj in objs:
                texts = texts + obj.text

        
        elif texts2=='':
            for obj in objs:
                texts2 = texts2 + obj.text
                
        elif texts3=='':
            for obj in objs:
                texts3 = texts3 + obj.text
                  
        if texts3 != '':
            post = texts + texts2
            skills = texts3
        else:
            post = texts
            print(post)
            skills = texts2
    print('post:'+ post)
    print('skills:'+skills)
    print(count)
    conn = engine.connect()
    date = '17/1/2022'
    available = True
    company = 'Atlan'
    company_url = 'https://atlan.com/careers/'
    

    conn.execute(Jobs.insert(), [
        {'Title':e_title,'Category':cate ,'Post':post,'Job_id':count,'Required experience':skills,
        'Date':date, 'Job_url':e_link,'Available':available},
   
    ])
    conn.execute(Locations.insert(),[{'Location':location}])
    conn.execute(Skill.insert(),[{'Skills':skills}])
    s = Jobs.select()
    print(conn.execute(s).fetchall())

    
conn.execute(Company.insert(),[{'Company':company,'openings':count,'Url':company_url}])




driver.quit()

