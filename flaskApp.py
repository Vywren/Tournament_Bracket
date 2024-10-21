from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, Column, Integer, String
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

class users(Base):
    __tablename__ = 'users'
    username = Column(Integer)
    email = Column(Integer, primary_key = True)


Base.metadata.create_all(engine) 
#sql_session.add(users(username = "bob", email = "dylan@gmail.com")) 
#sql_session.commit()




@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/single_elim")
def single_elim():
    return render_template("single_elim.html")

@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["usr"]
        email = request.form["email"]
        session["user"] = user
        session["email"] = email
        results = sql_session.query(users).filter(users.email == email).first()  
        if results != None:
            flash("Email found, Welcome Back")
            return redirect(url_for("post_log"))
            
        else:
            flash("Email not found, new user created")
            sql_session.add(users(username=user,email=email))
            sql_session.commit()
            return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
@app.route("/login/post_log/")
def post_log():
    if "user" in session:
        return render_template('post_log.html')
    else:
        return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug = True)
