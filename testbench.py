from sqlalchemy import create_engine, Column, Integer, String 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
  
# Create a SQLAlchemy engine 
engine = create_engine('sqlite:///example.db') 
  
# Create a SQLAlchemy session 
Session = sessionmaker(bind=engine) 
sql_session = Session() 
  
# Define a SQLAlchemy model 
Base = declarative_base() 
  
  
class users(Base):
    __tablename__ = 'users'
    username = Column(Integer)
    email = Column(Integer, primary_key = True)
  
  
# Create the example table 
Base.metadata.create_all(engine) 
  
results = sql_session.query(users).filter(users.email == "dylan@gmail.com").first() 
  
# Print the results 
if results!= None:
    print(results) 
else:
    print("hello")
# Insert some data into the example table 
#session.add(users(username = "bob", email = "dylan@gmail.com")) 

#session.commit() 
  
# Use a mathematical equation as a filter in a query 
#results = session.query(users).filter(email = "dylan@gmail.com").first() 
  
# Print the results 
#for result in results: 
#    print(result) 
    