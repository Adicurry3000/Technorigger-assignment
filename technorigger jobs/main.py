from turtle import title
from unicodedata import category
import sqlalchemy as db
from sqlalchemy import  MetaData,Integer,Column,Table,Computed,String, Date, Boolean,create_engine

engine = create_engine('sqlite:///main.db', echo = True)

metadata = MetaData()

Jobs = Table(
    "Jobs", metadata ,
    Column('Title', String),
    Column('Category', String ),
    Column('Post', String),
    Column('Required skills', String ),
    Column('Required experience', Integer),
    Column('Location', String),
    Column('Company', String),
    Column('Date', String),
    Column('Job url', String),
    Column('Available', Boolean),

)

metadata.create_all(engine)

print("these are columns in our table %s" %(Jobs.columns.keys()))

title = input('title:')
category = input('category:')
post = input('post:')
skill = input('skill:')
exp = int(input('experience:'))
location = input('location:')
company = input('company:')
date = input('date:')
url = input('url:')
available = bool(input('Availability:'))



# ins a= Jobs.insert().values(Title=title, Category= category,  )
conn = engine.connect()


conn.execute(Jobs.insert(), [
   {'Title':title,'Category': category,'Post':post,'Required skills':skill,'Required experience':exp,'Location':location,'Company':company,
   'Date':date, 'Job_url':url,'Available':available},
   
])

s = Jobs.select()
print(conn.execute(s).fetchall())
