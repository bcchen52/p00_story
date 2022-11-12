'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for
import os, sqlite3

app = Flask(__name__)


app.secret_key = os.urandom(12)

currentusers = {}

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) 
c = db.cursor()    

command = "drop table if exists user;"         
c.execute(command)

command = "create table user(id int, username text, password text);"      
c.execute(command)   

command = "insert into user values(1, 'Brian' , '123' );"      
c.execute(command)   

command = "select * from user;"
c.execute(command)   
users = c.fetchall()
for x in users:
    currentusers[x[1]] = x[2]

print(currentusers)
db.commit() 
db.close()



@app.route("/")
def index():
    return render_template('homepage.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        print(f"User entered: {user}")
        print(f"Password entered: {password}")
        if user not in currentusers.keys(): #check if user exists
            error = "User DNE"
            return render_template('login.html',
            error=error)
        if password != currentusers[user]: #check if password matches user
            error = "Wrong Password"
            return render_template('login.html',
            error=error)
        session.permanent = True
        session["username"] = user
        session['logged_in'] = True
        return redirect(url_for('index'))  #redirects to home page



'''
@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'GET': #if opening this route
        return render_template('signup.html') 
    if request.method == 'POST': #if submitting information
        usernames = users.keys()
        newuser = request.form.get('username') #when using "POST" request.args DNE
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if newuser in usernames: #check if user exists
            error = "Username already exists"
            return render_template('signup.html', 
                error=error) #redirects back to page with error
        if password != confirmation: 
            error = "PASSWORDS DO NOT MATCH!!!!!!"
            return render_template('signup.html', 
                error=error)

        with open('users.csv','a') as csvfile: #if newuser works, add to csv
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([newuser,password])
        get_users() #update local dict to match csv

        return render_template('login.html')
'''


@app.route("/signup")
def signup():
    return render_template('register.html')



@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()