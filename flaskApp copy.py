from flask import Flask, render_template, request, redirect, url_for, session, flash
from admin_commands import *

#bracket access is designed as a store front tool and isn't website compatible
#will likely branch off into a separate project later

app = Flask(__name__,template_folder = 'templates')
app.secret_key = "dhtuisdhfu9 her79ry489fjiojf0298348idksmfoisn2rif9djf023hr8fdjf"

#check if room 0 exists,if not then create
'''results = sql_session.query(single_elim_room).filter(single_elim_room.room_number == 0).first()
if results == None:
    sql_session.add(single_elim_room(room_number = 0)) 
sql_session.commit()'''



@app.route("/")
def do_stuff():
    return render_template('index.html')

@app.route("/round_robin",methods = ["POST", "GET"])
def round_robin():
    return render_template('round_robin.html')
@app.route("/single_elim", methods = ["POST", "GET"])
def single_elim():
    #display available room numbers
    '''results = sql_session.query(single_elim_room).filter(single_elim_room.room_number > 0).all()
    for result in results:
        flash(str(result))'''
    if request.method == "POST":
        
        new = request.form.get("new_room")
        join = request.form.get("room_num")
        if session["user"] == None or session["email"] == None:
            flash("Please login before joining a room")
            return redirect(url_for("login"))
        if new is not None:
            #new room button was pressed
            '''greatest = sql_session.query(single_elim_room).count()
            if greatest <= 10:
                 sql_session.add(single_elim_room(room_number = greatest)) 
                 sql_session.commit()
                 flash("welcome to room "+ str(greatest))
                 return redirect(url_for("waiting_room"))
            else:
            #too many rooms added
                return render_template("single_elim.html")'''
        if join.isnumeric():
            #add user to room
            '''rooms = sql_session.query(single_elim_room).all()
            for room in rooms:
                if int(join) == int(room.room_number):
                    session["room"] = join
                    flash("welcome to room " + join)
                    return redirect(url_for("waiting_room"))
            else:            
                flash("This is not an existing room")
                return redirect(url_for("single_elim"))'''
    return render_template("single_elim.html")
@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        email = request.form["email"]
        phone_number = request.form["phone"]
        if first == "":
            flash("please enter a first name")
            return redirect(url_for("login"))
        if last == "":
            flash("please enter a last name")
        if email == "" or phone_number == "":
            flash("please enter an email or a phone number")
            return redirect(url_for("login"))
        session["first"] = first
        session["last"] = last
        players_with_name = search_player_full(first,last)
        in_db = False
        if players_with_name != []:
            in_db = True
        #check if user in database if yes welcome and redirect, if no create new account
        #results = sql_session.query(users).filter(users.email == email).first()  
        if in_db != True:
            flash("Welcome Back" + first + " " + last)
            return redirect(url_for("post_log"))
            
        else:
            flash("user, new user created")
            sql_session.add(users(email = email, username = username, in_room = 0))
            sql_session.commit()
            return redirect(url_for("post_log")'''
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
