'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for
import os, sqlite3

app = Flask(__name__)

app.secret_key = os.urandom(12)

currentusers = {}
stories = []

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) 
c = db.cursor()    

command = "drop table if exists user;"         
c.execute(command)

command = "drop table if exists story;"         
c.execute(command)

command = "create table user(id int, username text, password text);"      
c.execute(command)   

command = "create table story(id int, user_id int, title text, content text);"      
c.execute(command)   

command = f'''insert into story values(1, 1,"hello","welcome back to my asmr");''' 
c.execute(command)   


db.commit() 



def update_users():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()   
    command = "select * from user;"
    c.execute(command)   
    users = c.fetchall()
    for x in users:
        currentusers[x[1]] = x[2]
    #print(currentusers)
    db.close()

# our html has a dropdown for current stories, and to list them we need to fill our list
def update_stories():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()   
    command = "select title from story;"
    c.execute(command)   
    titles = c.fetchall()
    for x in titles:
        stories.append(x[0])
    #print(stories)
    db.close()

update_stories()
    




@app.route("/")
def index():
    return render_template('homepage.html',
    stories=stories)
    


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



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':

        user =  str( request.form.get('username') )
        password = str( request.form.get('password') )
        password2 = str( request.form.get('password2') )
        
        if user in currentusers.keys():
            error = "User already exists"
            return render_template('register.html',
            error=error)

        if password != password2:
            error = "Passwords don't match"
            return render_template('register.html',
            error=error)

        # Add to table
        db = sqlite3.connect(DB_FILE) 
        c = db.cursor()  

        params = (len(currentusers.keys()), user, password)

        print(params)
        command = f"insert into user values(?, ?, ?);"       
        c.execute(command, params)   

        db.commit() 
        db.close()

        update_users()

        return redirect(url_for('login'))  #redirects to home page
        
@app.route("/story/<title>", methods=['GET','POST'])
def story(title):
    
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor() 

    command = f'''select * from story where title = "{title}";'''
    c.execute(command)   
    story = c.fetchone()

    user_id = story[1]
    title = story[2]
    content = story[3]

    print(content)



    db.close()
    
    

    return render_template('story.html',
        title=title,
        content=content
        )



@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()