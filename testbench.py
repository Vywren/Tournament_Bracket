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

class single_elim_room(Base):
    __tablename__ = 'single_elim_room'
    room_number = Column(Integer, primary_key = True) #room id
    empty = Column(Boolean) #is the room empty/undisplayable?
    room_admin = Column(String, ForeignKey(admin.admin)) #who manages the room?
    start = Column(Boolean) #have the first pairings been made?
    time = Column(String, nullable = False)
    round = Column(Integer, nullable = False)


class users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key = True)
    in_room = Column(Integer, ForeignKey(admin.room_number))
    ready = Column(Boolean)

        
class matches(Base):
    __tablename__ = 'matches'
    player1 = Column(String, ForeignKey(users.username))
    player2 = Column(String, ForeignKey(users.username))
    p1_wins = Column(Integer)
    p1_losses = Column(Integer)
    draws = Column(Integer)
    id = Column(Integer,primary_key = True, autoincrement=True)
    tt_identifier = Column(String, nullable=False)


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

def initial_pair_up(room_num):
    room = find_room(room_num)
    players = find_all_in_room(room_num)
    if players == None or room == None:
        print("issue")
        return -1
    count = len(players)
    for player in range(0,count-1,2):
        tt_id = str(room.room_number)+"/"+ str(room.round) + "/" + room.time
        sql_session.add(matches(player1 = players[player].username, player2 = players[player+1].username, p1_wins = 0, p1_losses = 0, draws = 0, tt_identifier = tt_id))
    sql_session.commit()
    return 1

for i in range(10):
    sql_session.add(single_elim_room(room_number = i, empty = True,start = False, time = "0", round = "0")) 
sql_session.commit()

create_new_user("bob1")
create_new_user("bob2")
create_new_user("bob3")
create_new_user("bob4")
create_new_user("bob5")
create_new_user("bob6")
find_user("bob1").in_room = 1
find_user("bob2").in_room = 1
find_user("bob3").in_room = 1
find_user("bob4").in_room = 1
find_user("bob5").in_room = 1
find_user("bob6").in_room = 1
room = find_room(1)
if room.start != True:
    print("hello")
    room.start = True
    room.time = datetime.datetime.now()
    sql_session.commit()
initial_pair_up(1)