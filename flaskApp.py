from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__,template_folder = 'templates')

@app.route("/")
def do_stuff():
    return render_template('index.html')
@app.route("/login",methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["usr"]
        email = request.form["email"]
        return redirect(url_for("post_log"))
    else:
        return render_template('login.html')
@app.route("/login/post_log/")
def post_log():
    return render_template('post_log.html')
if __name__ == "__main__":
    app.run(debug = True)