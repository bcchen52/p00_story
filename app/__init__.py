'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for
import os, sqlite3

app = Flask(__name__)

app.secret_key = os.urandom(12)

currentusers = {}
stories = set()

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) 
c = db.cursor()    

command = "drop table if exists user;"         
c.execute(command)

command = "drop table if exists story;"         
c.execute(command)

command = "create table user(id int, username text, password text);"      
c.execute(command)   

command = "create table story(id int primary key, user_id int, title text, content text, recentuser_id int);"      
c.execute(command)   

command = f'''insert into story values(0, 0,"hello","welcome back to my asmr",0);''' 
c.execute(command)   

command = f'''insert into user values(0, "b", "123");''' 
c.execute(command)  


db.commit() 
db.close()


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

update_users()

# our html has a dropdown for current stories, and to list them we need to fill our list
# all our html files extend layout.html, but we cannot give it a variable if we do not call it
# with render_template where we add a parameter, so we need to add stories as a parameter
# everytime we render an html file
def update_stories():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()   
    command = "select title from story;"
    c.execute(command)   
    titles = c.fetchall()
    for x in titles:
        stories.add(x[0])
    print(stories)
    db.close()

update_stories()

#we use user ids, and we often need to get the associated username
def grab_username(id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor() 
    command = f"select username from user where id = {id};"
    c.execute(command)
    grab_user = c.fetchone()
    db.close()

    return(grab_user[0])
    




@app.route("/")
def index():
    return render_template('homepage.html',
    stories=list(stories))
    


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',
        stories=list(stories))
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        print(f"User entered: {user}")
        print(f"Password entered: {password}")

        if user not in currentusers.keys(): #check if user exists
            error = "User DNE"
            return render_template('login.html',
            error=error,
            stories=list(stories))

        if password != currentusers[user]: #check if password matches user
            error = "Wrong Password"
            return render_template('login.html',
            error=error,
            stories=list(stories))

        session.permanent = True
        session["username"] = user
        session['logged_in'] = True

        return redirect(url_for('index'))  #redirects to home page



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('register.html',
        stories=list(stories))

    if request.method == 'POST':

        user =  str( request.form.get('username') )
        password = str( request.form.get('password') )
        password2 = str( request.form.get('password2') )
        
        if user in currentusers.keys():
            error = "User already exists"
            return render_template('register.html',
            error=error,
            stories=list(stories))

        if password != password2:
            error = "Passwords don't match"
            return render_template('register.html',
            error=error,
            stories=list(stories))

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
    if request.method == 'GET':
        db = sqlite3.connect(DB_FILE) 
        c = db.cursor() 

        command = f'''select * from story where title = "{title}";'''
        c.execute(command)   
        story = c.fetchone()

        user_id = story[1]
        title = story[2]
        content = story[3]
        recentuser_id = story[4]

        print(content)

        db.close()
        
        return render_template('story.html',
            title=title,
            content=content,
            user=grab_username(user_id),
            recentuser=grab_username(recentuser_id),
            stories=list(stories)
            )

    if request.method == 'POST':
        return redirect(url_for('edit'))

@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method == 'GET':
        title = request.args.get('title')
        #if edit is accessed from a story page, the form will have an input named "title"
        #if title is none, it means it is not accessed from the button on a story page
        
        if title != None: #edit story

            db = sqlite3.connect(DB_FILE) 
            c = db.cursor() 

            command = f'''select * from story where title = "{title}";'''
            c.execute(command)   
            story = c.fetchone()

            content = story[3]

            db.close()

            return render_template('edit.html',
                new=False,
                title=title,
                content=content,
                stories=list(stories)
                )

        else: #new story
            return render_template('edit.html',
                new=True,
                stories=list(stories)
                )

    if request.method == 'POST':
        new = request.form.get('new')
        title = request.form.get('title')
        content = request.form.get('content')

        db = sqlite3.connect(DB_FILE) 
        c = db.cursor() 

        if new == "False":
            command = f'''select * from story where title = "{title}";'''
            c.execute(command)   
            story = c.fetchone()

            id = story[0]
            user_id = story[1]
            oldcontent = story[3]
            user = session['username']

            command = f'''select id from user where username = "{user}";'''
            c.execute(command)   
            grab_recentuser_id = c.fetchone()
            recentuser_id = grab_recentuser_id[0]
            oldcontent += content
            content = oldcontent
            #can add spot for user id
        else: 
            command = f'''select * from story where title = "{title}";'''
            c.execute(command)   
            story = c.fetchone()
            
            if story is None:
                command = f'''select * from user where username = "{session['username']}";'''
                c.execute(command)   
                user = c.fetchone()
                user_id = user[0]
                recentuser_id = user_id
                id = len(stories)

            else:
                error = "Story with that title already exists"
                return render_template('edit.html',
                    new=True,
                    error=error,
                    stories=list(stories)
                )


        command = f'''replace into story values({id},{user_id},"{title}","{content}",{recentuser_id});'''
        c.execute(command)   

        db.commit() 
        db.close()

        update_stories()
            
        return redirect(url_for('index'))





@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()