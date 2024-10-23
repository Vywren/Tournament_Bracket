from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
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
    def __init__(self, room_number):
        self.room_number = room_number
    def __repr__(self):
            return f"{self.room_number}"

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

Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 
#sql_session.add(users(email = "dylan@gmail.com")) 
results = sql_session.query(single_elim_room).filter(single_elim_room.room_number == 0).first()
if results == None:
    sql_session.add(single_elim_room(room_number = 0)) 
sql_session.commit()



@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/single_elim", methods = ["POST", "GET"])
def single_elim():
    results = sql_session.query(single_elim_room).filter(single_elim_room.room_number > 0).all()
    for result in results:
        flash(str(result))
    if request.method == "POST":
        new = request.form.get("new_room")
        join = request.form.get("room_num")
        if session["user"] == None or session["email"] == None:
            flash("Please login before joining a room")
            return redirect(url_for("login"))
        if new is not None:
            #new room button was pressed
            greatest = sql_session.query(single_elim_room).count()
            if greatest <= 10:
                 sql_session.add(single_elim_room(room_number = greatest)) 
                 sql_session.commit()
                 flash("welcome to room "+ str(greatest))
                 return redirect(url_for("waiting_room"))
            else:
            #too many rooms added
                return render_template("single_elim.html")
        if join.isnumeric():
            #add user to room
            rooms = sql_session.query(single_elim_room).all()
            for room in rooms:
                if int(join) == int(room.room_number):
                    session["room"] = join
                    flash("welcome to room " + join)
                    return redirect(url_for("waiting_room"))
            else:            
                flash("This is not an existing room")
                return redirect(url_for("single_elim"))
    return render_template("single_elim.html")
@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        if username == "":
            flash("please enter a username")
            return redirect(url_for("login"))
        if email == "":
            flash("please enter an email")
            return redirect(url_for("login"))
        results = sql_session.query(users).filter(users.email == email).first()  
        session["email"] = email
        session["username"] = username
        if results != None:
            flash("Email found, Welcome Back")
            flash (username)
            return redirect(url_for("post_log"))
            
        else:
            flash("Email not found, new user created")
            sql_session.add(users(email = email, username = username, in_room = 0))
            sql_session.commit()
            return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
    
@app.route("/single_elim/waiting_room")
def waiting_room():
    return render_template('waiting_room.html')

@app.route("/login/post_log/")
def post_log():
    if "email" in session:
        return render_template('post_log.html')
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)
