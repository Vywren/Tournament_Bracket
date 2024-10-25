from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 


app = Flask(__name__,template_folder = 'templates')
app.secret_key = "dhtuisdhfu9 her79ry489fjiojf0298348idksmfoisn2rif9djf023hr8fdjf"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///example.db') 
Session = sessionmaker(bind=engine) 
sql_session = Session() 
Base = declarative_base()

class single_elim_room(Base):
    __tablename__ = 'single_elim_room'
    room_number = Column(Integer, primary_key = True)
    empty = Column(Boolean)
    def __init__(self, room_number,empty):
        self.room_number = room_number
        self.empty = empty
    def __repr__(self):
            return f"{self.room_number}"

class users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key = True)
    in_room = Column(Integer, ForeignKey(single_elim_room.room_number))
    def __init__(self, username, in_room):
        self.username = username
        self.in_room = in_room
    def __repr__(self):
            return f"({self.username, self.in_room})"
        


Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 

def find_user(username):
    return sql_session.query(users).filter_by(username = username).first()

for i in range(10):
    sql_session.add(single_elim_room(room_number = i, empty = True)) 
sql_session.commit()



@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/single_elim", methods = ["POST", "GET"])
def single_elim(): #check for nonempty rooms to join
    results = sql_session.query(single_elim_room).filter(single_elim_room.empty == False).all()
    for result in results:
        flash(str(result))
        #if buttons are pressed
    if request.method == "POST":
        new = request.form.get("new_room")
        join = request.form.get("room_num")
        #check if user is logged in
        if find_user(session["user"]) == None:
            flash("Please login before joining a room")
            return redirect(url_for("login"))
        if join == "":
            flash("please enter a room number")
        if new is not None:
            #new room button was pressed
            greatest = sql_session.query(single_elim_room).filter(single_elim_room.empty == True).first()
            if greatest != None: #succesfully created new room
                greatest.empty = False
                use = find_user(session["user"])
                use.in_room = join
                sql_session.commit()
                flash("Welcome to room "+ str(greatest.room_number))
                return redirect(url_for("waiting_room"))
            else:
            #too many rooms added
                flash("All rooms in use")
                return render_template("single_elim.html")
        if int(join) > 0 and int(join) <= 10:
            #add user to room
            rooms = sql_session.query(single_elim_room).filter(single_elim_room.empty == False and single_elim_room.room_number > 0).all()
            for room in rooms:
                if int(join) == int(room.room_number): #sucessfully joined room
                    session["room"] = join
                    use = find_user(session["user"])
                    use.in_room = join
                    sql_session.commit()
                    flash("welcome to room " + join + " " + use.username)
                    return redirect(url_for("waiting_room"))
            else:            
                flash("This is not an existing room")
                return redirect(url_for("single_elim"))
    return render_template("single_elim.html")
@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        if username == "":
            flash("please enter a username")
            return redirect(url_for("login"))
        results = find_user(username)
        session["user"] = username
        if results != None:
            flash("User found, Welcome Back")
            flash (username)
            return redirect(url_for("post_log"))
            
        else:
            flash("User not found, new user created")
            sql_session.add(users(username = username, in_room = 0))
            sql_session.commit()
            return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
    
@app.route("/single_elim/waiting_room")
def waiting_room():
    return render_template('waiting_room.html')

@app.route("/login/post_log/")
def post_log():
    if "user" in session:
        return render_template('post_log.html')
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)
