from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, and_, or_
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
import datetime


app = Flask(__name__,template_folder = 'templates')
app.secret_key = "dhtuisdhfu9 her79ry489fjiojf0298348idksmfoisn2rif9djf023hr8fdjf"
app.permanent_session_lifetime = datetime.timedelta(days = 7)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///example.db') 
Session = sessionmaker(bind=engine) 
sql_session = Session() 
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


Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 


def find_user(username): #returns the object for the user with this username, username is unique so accidentally skipping someone shouldn't be an issue
    return sql_session.query(users).filter_by(username = username).first()

def find_players_in_room(room_number): #returns all users in room as objects in a list, attributes are acessible as follows, list[x].attribute
    return sql_session.query(users).filter_by(in_room = room_number, dropped = False).order_by(users.id).all()

def assign_admin(username,room_number, password = ""):
    sql_session.add(admin(room_number = room_number, admin = username, password = password)) 
    sql_session.commit()

def find_room_admin(room_number):
    return sql_session.query(admin).filter_by(room_number = room_number).first()
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
    
def display_pairings(room_number):
    room = find_room(room_number)
    matched = sql_session.query(matches).filter(
    and_(
        matches.round == room.round,
        matches.time == room.time,
        matches.room == room.room_number,
    )
    ).all()
    flash("Round " + str(room.round) + " pairings:", "pairings")
    for i in matched:
        flash(i.player1 + " VS. " + i.player2, "pairings")

def fields_full():
    if "user" in session and "room" in session:
        return True
    return False
    

for i in range(10):
    sql_session.add(single_elim_room(room_number = i, empty = True,start = False, time = "0", round = "0")) 
sql_session.commit()



@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/single_elim", methods = ["POST", "GET"])
def single_elim(): #display all available rooms
    results = sql_session.query(single_elim_room).filter(single_elim_room.empty == False).all()
    for result in results:
        flash(str(result.room_number),"room_display")
        #if buttons are pressed
    if request.method == "POST":
        new = request.form.get("new_room")
        join = request.form.get("room_num") # TODO: check how to isolate buttons, both buttons are probably submitting the same field
        #check if user is logged in
        if find_user(session["user"]) == None:
            flash("Please login before joining a room","no_login")
            return redirect(url_for("login"))
        if join == "" and new == "":
            flash("please enter a room number","joining_issues")
        if new is not None:
            #create room button was pressed, find the first empty room
            room = sql_session.query(single_elim_room).filter(single_elim_room.empty == True, single_elim_room.room_number!= 0).first()
            if room != None: #succesfully created new room
                room.empty = False
                use = find_user(session["user"])
                use.in_room = room.room_number
                room.time = datetime.datetime.now()
                sql_session.commit()
                assign_admin(username = use.username,room_number = use.in_room)
                session["room"] = room.room_number
                if "admin_of" not in session:
                    session["admin_of"] = []
                session["admin_of"].append(room.room_number)
                flash("Welcome to room "+ str(room.room_number) + " " + use.username,"welcome")
                return redirect(url_for("waiting_room"))
            else:
            #too many rooms added
                flash("All rooms in use","joining_issues")
                return render_template("single_elim.html")
        if join.isdigit() and join != "0":
            #add user to room
            rooms = sql_session.query(single_elim_room).filter(single_elim_room.empty == False and single_elim_room.room_number > 0).all()
            for room in rooms:
                if int(join) == int(room.room_number): #sucessfully joined room
                    session["room"] = join
                    use = find_user(session["user"])
                    use.in_room = join
                    sql_session.commit()
                    flash("welcome to room " + join + " " + use.username,"welcome")
                    return redirect(url_for("waiting_room"))
            else:            
                flash("This is not an existing room","joining_issues")
                return render_template("single_elim.html")
        else:
            flash("This is not an existing room","joining_issues")
            return render_template("single_elim.html") 
    return render_template("single_elim.html")

@app.route("/login",methods = ["POST", "GET"])
def login():
   
    if request.method == "POST":
        session.permanent = True
        username = request.form.get("username")
        if username == "":
            flash("please enter a username", "no_login")
            return redirect(url_for("login"))
        results = find_user(username)
        session["user"] = username
        if results != None:
            flash("User found, Welcome Back","logged_in")
            flash (username)
            user = find_user(username)
            session["room"] = user.in_room
            session["ready"] = user.ready
            return redirect(url_for("post_log"))
            
        else:
            flash("User not found, new user created","logged_in")
            create_new_user(username = username)
            session["readied"] = False
            session["room"] = 0
            return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
    
@app.route("/single_elim/waiting_room",methods = ["POST", "GET"])
def waiting_room():
    room = find_room(session["room"])
    if not fields_full(): #check if user is in a room
        return redirect(url_for("single_elim"))
    
    if request.method == "POST":
        ready = request.form.get("ready")
        start = request.form.get("start_tourney")
        if ready != None:
            find_user(session["user"]).ready = True
            session["ready"] = True
            sql_session.commit()
        if start != None:
            if room.start != True:
                room.start = True
                room.round += 1
                pair_up(session["room"])

    for i in find_players_in_room(session["room"]):#display all players in room
        flash(i.username + "\n","player_list")
    if room.round != 0:
        display_pairings(session["room"])
    return render_template('waiting_room.html')

#may be scrapped later
@app.route("/login/post_log/")
def post_log():
    if "user" in session:
        if session["room"] != 0:
            return redirect(url_for("waiting_room"))
        else:
            return redirect(url_for("single_elim"))
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)
'''
if room.start != True:
                room.start = True'''