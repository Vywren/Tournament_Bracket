from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 


app = Flask(__name__,template_folder = 'templates')
app.secret_key = "dhtuisdhfu9 her79ry489fjiojf0298348idksmfoisn2rif9djf023hr8fdjf"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
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
            return f"({self.room_number})"

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


Base.metadata.create_all(engine) 
#sql_session.add(users(email = "dylan@gmail.com")) 
results = sql_session.query(single_elim_room).filter(single_elim_room.room_number == 0).first()
if results == None:
    sql_session.add(single_elim_room(room_number = 0)) 
sql_session.commit()



@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/single_elim")
def single_elim():
    results = sql_session.query(single_elim_room).filter(single_elim_room.room_number == 0).first()
    flash(results)
    return render_template("single_elim.html")
@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        session["email"] = email
        session["username"] = username
        results = sql_session.query(users).filter(users.email == email).first()  
        if results != None:
            flash("Email found, Welcome Back")
            return redirect(url_for("post_log"))
            
        else:
            flash("Email not found, new user created")
            sql_session.add(users(email = email, username = username, in_room = 0))
            sql_session.commit()
            return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
@app.route("/login/post_log/")
def post_log():
    if "email" in session:
        return render_template('post_log.html')
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)
