from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, __version__
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
import datetime
# Create a SQLAlchemy engine 
engine = create_engine('sqlite:///example.db') 
  
# Create a SQLAlchemy session 
Session = sessionmaker(bind=engine) 
sql_session = Session() 
  
# Define a SQLAlchemy model 
Base = declarative_base() 
  
  
class admin(Base):
    __tablename__ = 'admin'
    admin = Column(String)
    room_number = Column(Integer, primary_key = True)
    password = Column(String)
    def __init__(self, admin,room_number,password):
        self.room_number = room_number
        self.admin = admin
        self.password = password
class single_elim_room(Base):
    __tablename__ = 'single_elim_room'
    room_number = Column(Integer, primary_key = True) #room id
    empty = Column(Boolean) #is the room empty/displayable?
    room_admin = Column(String, ForeignKey(admin.admin)) #who manages the room?
    start = Column(Boolean) #have the first pairings been made?
    time = Column(String, nullable = False)
    def __init__(self, room_number,empty,start, time):
        self.room_number = room_number
        self.empty = empty
        self.start = start
        self.time = time
    def __repr__(self):
            return f"{self.room_number}"

class users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key = True)
    in_room = Column(Integer, ForeignKey(admin.room_number))
    ready = Column(Boolean)
    def __init__(self, username, in_room, ready):
        self.username = username
        self.in_room = in_room
        self.ready = ready
    def __repr__(self):
            return f"({self.username, self.in_room, self.ready})"
        
class matches(Base):
    __tablename__ = 'matches'
    player1 = Column(String, ForeignKey(users.username))
    player2 = Column(String, ForeignKey(users.username))
    p1_wins = Column(Integer)
    p1_losses = Column(Integer)
    draws = Column(Integer)
    identifier = Column(String, primary_key = True)
    def __init__(self, player1,player2, p1_wins, p1_losses, draws,identifier):
        self.player1 = player1
        self.player2 = player2
        self.p1_wins = p1_wins
        self.p1_losses = p1_losses
        self.draws = draws
        identifier = identifier
    def __repr__(self):
            return f"({self.username, self.in_room, self.ready})"

# Create the example table 
Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 

def find_user(username): #returns the object for the user with this username, username is unique so accidentally skipping someone shouldn't be an issue
    return sql_session.query(users).filter_by(username = username).first()

def find_all_in_room(room_number): #returns all users in room as objects in a list, attributes are acessible as follows, list[x].attribute
    return sql_session.query(users).filter_by(in_room = room_number).all()

def assign_admin(username,room_number, password = ""):
    sql_session.add(admin(room_number = room_number, admin = username, password = password)) 
    sql_session.commit()

def create_new_user(username):
    sql_session.add(users(username = username, in_room = 0, ready = False))
    sql_session.commit()
    
def find_room(room_num):
    for i in sql_session.query(single_elim_room).all():
        if i.room_number == room_num:
            return i
    return -1

for i in range(10):
    sql_session.add(single_elim_room(room_number = i, empty = True,start = False, time = "0")) 
sql_session.commit()

create_new_user("bob1")
create_new_user("bob2")
create_new_user("bob3")
room = find_room(1)
if room.start != True:
    print("hello")
    room.start = True
    room.time = datetime.datetime.now()
    sql_session.commit()