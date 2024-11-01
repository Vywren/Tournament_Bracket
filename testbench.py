from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, __version__,and_, or_
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
    username = Column(String, unique = True)
    in_room = Column(Integer, ForeignKey(admin.room_number))
    ready = Column(Boolean)
    dropped = Column(Boolean)
    id = Column(Integer, primary_key = True)

        
class matches(Base):
    __tablename__ = 'matches'
    player1 = Column(String, ForeignKey(users.username))
    player2 = Column(String, ForeignKey(users.username))
    p1_wins = Column(Integer)
    p1_losses = Column(Integer)
    id = Column(Integer,primary_key = True, autoincrement=True)
    time = Column(String, nullable=False)
    round = Column(Integer, nullable = False) 
    room = Column(Integer, ForeignKey(single_elim_room.room_number))
    loser = Column(String, ForeignKey(users.username))


# Create the example table 
Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 

def find_user(username): #returns the object for the user with this username, username is unique so accidentally skipping someone shouldn't be an issue
    return sql_session.query(users).filter_by(username = username).first()

def find_players_in_room(room_number): #returns all users in room as objects in a list, attributes are acessible as follows, list[x].attribute
    return sql_session.query(users).filter_by(in_room = room_number, dropped = False).order_by(users.id).all()

def assign_admin(username,room_number, password = ""):
    sql_session.add(admin(room_number = room_number, admin = username, password = password)) 
    sql_session.commit()

def create_new_user(username):
    sql_session.add(users(username = username, in_room = 0, ready = False, dropped = False))
    sql_session.commit()
    
def find_room(room_num):
    return sql_session.query(single_elim_room).filter_by(room_number = room_num).first()


def pair_up(room_num):
    room = find_room(room_num)
    players = find_players_in_room(room_num)
    if players == None or room == None:
        print("issue")
        return -1
    count = len(players)
    if count <= 1:
        print(players[0].username + " is your champion")
    for player in range(0,count-1,2):
        sql_session.add(matches(player1 = players[player].username, player2 = players[player+1].username, p1_wins = 0, p1_losses = 0, time = room.time, round = room.round, room = room.room_number, loser = None))
    sql_session.commit()
    return 1

def report(player, room_num, wins, losses):
    room = find_room(room_num)
    match = sql_session.query(matches).filter(
    and_(
        matches.round == room.round,
        matches.time == room.time,
        matches.room == room.room_number,
        or_(
            matches.player1 == player,
            matches.player2 == player
        )
    )
    ).first()
    if match.player1 == player:
        match.p1_wins = wins
        match.p1_losses = losses
    elif match.player2 == player:
        match.p1_wins = losses
        match.p1_losses = wins
    else:
        print("should not be happening")
        return -1
    sql_session.commit()
    if match.p1_wins > match.p1_losses:
        match.loser = match.player2
    elif match.p1_wins < match.p1_losses:
        match.loser = match.player1
    else:
        print("match was a draw, tie break")
    return 1
    
def advance_round(room):
    room = find_room(room)
    matched = sql_session.query(matches).filter(
    and_(
        matches.round == room.round,
        matches.time == room.time,
        matches.room == room.room_number,
    )
    ).all()
    for i in matched:
        if i.loser != None:
            find_user(i.loser).dropped = True
    room.round += 1
    sql_session.commit()
    pair_up(room.room_number)
    

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
pair_up(1)
report("bob2", 1, wins = 2, losses = 1)
report("bob4", 1, wins = 1, losses = 2)
report("bob6", 1, wins = 1, losses = 2)

advance_round(1)
report("bob2",1,wins = 2, losses = 1)
advance_round(1)
report("bob2",1,wins = 2, losses = 1)
advance_round(1)

