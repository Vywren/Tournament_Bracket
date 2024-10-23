from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, __version__
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
  
# Create a SQLAlchemy engine 
engine = create_engine('sqlite:///example.db') 
  
# Create a SQLAlchemy session 
Session = sessionmaker(bind=engine) 
sql_session = Session() 
  
# Define a SQLAlchemy model 
Base = declarative_base() 
  
  
class single_elim_room(Base):
    __tablename__ = 'single_elim_room'
    room_number = Column(Integer, primary_key = True)
    empty = Column(Boolean)
    def __init__(self, room_number, empty):
        self.room_number = room_number
        self.empty = empty
    def __repr__(self):
            return f"{self.room_number}, {self.empty}"

class users(Base):
    __tablename__ = 'users'
    email = Column(String, primary_key = True)
    username = Column(String)
    in_room = Column(Integer, ForeignKey(single_elim_room.room_number))
    def __init__(self, email, username, in_room):
        self.email = email
        self.username = username
        self.in_room = in_room
    def __repr__(self):
            return f"({self.email, self.username, self.in_room})"

# Create the example table 
Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 
  
sql_session.add(single_elim_room(room_number = 0, empty = True)) 
sql_session.add(single_elim_room(room_number = 1, empty = True)) 
sql_session.add(single_elim_room(room_number = 2, empty = True)) 
sql_session.add(single_elim_room(room_number = 3, empty = True)) 

sql_session.add(users(email = "dylan@gmail.com",username = "bob",in_room = 0)) 
sql_session.commit() 



results = sql_session.query(users).filter(users.in_room == 0).first() 
results1 = sql_session.query(single_elim_room).all()
results2 = sql_session.query(single_elim_room).filter(single_elim_room.room_number == 1).first()

# Print the results 
if results!= None:
    print(results) 
else:
    print("hello")
if results1!= None:
    print(results1) 
else:
    print("hello")
if results2!= None:
    print(results2) 
else:
    print("hello")

for result in results1:
    hold = result.room_number
    if hold == 1:
        print(hold)
print(__version__ )
# Insert some data into the example table 

  
# Use a mathematical equation as a filter in a query 
#results = session.query(users).filter(email = "dylan@gmail.com").first() 
  
# Print the results 
#for result in results: 
#    print(result) 
    