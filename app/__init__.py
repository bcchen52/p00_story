'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for
import secrets, sqlite3
import datetime

app = Flask(__name__)

app.secret_key = secrets.token_bytes(12)

currentusers = {}
stories = set()
edited_currentuser = []
user_watchlist = set()

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) 
c = db.cursor()    

command = "drop table if exists user;"         
c.execute(command)

command = "drop table if exists story;"         
c.execute(command)

command = "drop table if exists editstory;"         
c.execute(command)

command = "create table user(id int primary key, username text, password text, edited text);"      
c.execute(command)   

command = "create table story(id int primary key, user_id int, title text, content text, recentuser_id int, recent_content text, user_date text, recent_date text);"      
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
    db.close()

update_stories()

def update_edited_currentusers(username):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()  
    command = f''' select edited from user where username = "{username}";'''
    c.execute(command)   
    grab_edited = c.fetchone()
    #print(grab_edited)
    edited = grab_edited[0]
    #print(edited)
    edited_currentuser = edited.split(',')
    edited_currentuser = edited_currentuser[:-1]
    #print(edited_currentuser)
    edited_currentuser = [int(i) for i in edited_currentuser]
    #print(edited_currentuser)
    db.close()
    return(edited_currentuser)

def grab_stories(story_ids):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor() 
    for x in story_ids:
        command = f'''select title from story where id = {x};'''
        c.execute(command)   
        grab_title = c.fetchone()
        title = grab_title[0]
        user_watchlist.add(title)
    
    db.close()

def get_time():
    date_time = datetime.datetime.now()
    return(str(date_time)[:-10])
    

#we use user ids, and we often need to get the associated username
def grab_username(id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor() 
    command = f"select username from user where id = {id};"
    c.execute(command)
    grab_user = c.fetchone()
    db.close()

    return(grab_user[0])


db = sqlite3.connect(DB_FILE) 
c = db.cursor()   

content = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Imperdiet dui accumsan sit amet. Aliquet nec ullamcorper sit amet risus nullam eget felis. Scelerisque fermentum dui faucibus in ornare quam viverra orci. Turpis egestas maecenas pharetra convallis. Feugiat nibh sed pulvinar proin. Malesuada fames ac turpis egestas sed tempus. Proin libero nunc consequat interdum varius sit amet. Convallis convallis tellus id interdum velit laoreet id donec ultrices. Vestibulum lorem sed risus ultricies tristique. Pharetra diam sit amet nisl suscipit adipiscing bibendum est.

Pellentesque habitant morbi tristique senectus et netus et. Amet luctus venenatis lectus magna fringilla. Amet venenatis urna cursus eget nunc scelerisque viverra mauris in. Vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras. Aenean sed adipiscing diam donec adipiscing tristique risus nec. Nunc sed id semper risus in hendrerit gravida rutrum. Ultrices dui sapien eget mi proin sed. Aliquam malesuada bibendum arcu vitae elementum curabitur vitae nunc. Adipiscing at in tellus integer feugiat scelerisque varius morbi. Molestie a iaculis at erat pellentesque adipiscing. Sem viverra aliquet eget sit amet tellus cras. Elementum facilisis leo vel fringilla est ullamcorper. Sit amet massa vitae tortor condimentum lacinia quis. Cursus vitae congue mauris rhoncus aenean vel elit. Mi in nulla posuere sollicitudin. Tempus urna et pharetra pharetra massa massa ultricies mi. Mauris augue neque gravida in fermentum et sollicitudin ac.

Duis at tellus at urna condimentum. Consectetur libero id faucibus nisl. Consequat interdum varius sit amet mattis vulputate enim nulla aliquet. Leo a diam sollicitudin tempor. Metus dictum at tempor commodo ullamcorper a. Egestas purus viverra accumsan in nisl nisi scelerisque eu. Massa vitae tortor condimentum lacinia quis vel eros. Purus sit amet volutpat consequat. Vitae et leo duis ut diam quam nulla. Quam vulputate dignissim suspendisse in est ante in nibh. Aliquam sem et tortor consequat id porta nibh. Amet dictum sit amet justo donec. Egestas egestas fringilla phasellus faucibus scelerisque. Sit amet facilisis magna etiam tempor orci eu lobortis elementum. Nunc sed augue lacus viverra vitae congue eu consequat ac. Fames ac turpis egestas sed tempus urna. Mauris augue neque gravida in fermentum et sollicitudin. Urna id volutpat lacus laoreet non curabitur.

Sollicitudin nibh sit amet commodo nulla facilisi. Quis eleifend quam adipiscing vitae proin sagittis nisl. Enim nunc faucibus a pellentesque sit amet porttitor eget. Id diam vel quam elementum pulvinar etiam non quam. Sed tempus urna et pharetra pharetra massa massa. Semper viverra nam libero justo. Tempus iaculis urna id volutpat lacus laoreet non curabitur. Facilisis mauris sit amet massa vitae tortor condimentum lacinia quis. Mattis rhoncus urna neque viverra justo. Habitant morbi tristique senectus et netus et malesuada fames. Eu scelerisque felis imperdiet proin fermentum leo vel orci porta. Morbi tempus iaculis urna id volutpat lacus laoreet non curabitur. Feugiat in ante metus dictum at tempor commodo ullamcorper. Habitant morbi tristique senectus et netus. Nulla at volutpat diam ut venenatis tellus in metus vulputate. At tellus at urna condimentum mattis pellentesque id nibh tortor. Tincidunt lobortis feugiat vivamus at. Mi eget mauris pharetra et.

Maecenas ultricies mi eget mauris pharetra et ultrices neque. Morbi leo urna molestie at elementum. In pellentesque massa placerat duis ultricies. Eget nunc scelerisque viverra mauris in aliquam sem fringilla ut. Habitant morbi tristique senectus et. Tempor commodo ullamcorper a lacus vestibulum. Lectus mauris ultrices eros in cursus turpis massa tincidunt. Diam donec adipiscing tristique risus nec. Hendrerit dolor magna eget est lorem ipsum dolor. Iaculis urna id volutpat lacus laoreet non curabitur gravida arcu. Sapien nec sagittis aliquam malesuada bibendum arcu vitae elementum. Commodo odio aenean sed adipiscing diam donec adipiscing.
'''
command = f'''insert into story values(0, 0,"LoL Jungle Guide","{content}",0,"{content}","1955-10-13 01:02","1955-10-13 01:02");''' 
c.execute(command)   

content = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed velit dignissim sodales ut eu sem integer vitae justo. Turpis in eu mi bibendum neque egestas. Est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus. Penatibus et magnis dis parturient montes nascetur. Lobortis elementum nibh tellus molestie nunc non. Cras adipiscing enim eu turpis egestas pretium aenean pharetra. Dignissim sodales ut eu sem. Scelerisque eu ultrices vitae auctor eu augue ut. Lorem sed risus ultricies tristique nulla aliquet enim tortor at. Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh. Tellus mauris a diam maecenas sed enim. Neque aliquam vestibulum morbi blandit cursus. Enim blandit volutpat maecenas volutpat blandit aliquam etiam erat. Placerat orci nulla pellentesque dignissim enim sit amet venenatis.

Nisi est sit amet facilisis magna etiam. Arcu ac tortor dignissim convallis aenean et tortor at risus. Feugiat nisl pretium fusce id velit ut. In tellus integer feugiat scelerisque varius morbi enim nunc. Malesuada fames ac turpis egestas sed. Vestibulum lectus mauris ultrices eros in cursus. In pellentesque massa placerat duis ultricies lacus sed. Duis at consectetur lorem donec massa sapien faucibus et. Faucibus purus in massa tempor nec feugiat nisl pretium. Mauris commodo quis imperdiet massa tincidunt nunc. Amet porttitor eget dolor morbi non arcu. Urna condimentum mattis pellentesque id.

Nisi porta lorem mollis aliquam ut porttitor. Ut enim blandit volutpat maecenas volutpat. Sapien pellentesque habitant morbi tristique. Euismod nisi porta lorem mollis aliquam ut porttitor leo a. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Venenatis urna cursus eget nunc scelerisque viverra mauris in aliquam. Massa massa ultricies mi quis hendrerit dolor magna eget. At in tellus integer feugiat scelerisque varius morbi enim. Eget magna fermentum iaculis eu non. Eu nisl nunc mi ipsum faucibus. Tristique magna sit amet purus gravida quis blandit turpis cursus. Magna eget est lorem ipsum dolor sit amet. Imperdiet proin fermentum leo vel orci porta non pulvinar. Enim diam vulputate ut pharetra. Morbi tincidunt ornare massa eget. Est ullamcorper eget nulla facilisi etiam. Eget nulla facilisi etiam dignissim diam quis enim lobortis scelerisque. Amet dictum sit amet justo. Pharetra convallis posuere morbi leo urna molestie at. Potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed.

Vulputate odio ut enim blandit volutpat maecenas volutpat. Habitant morbi tristique senectus et netus et malesuada fames. Cras sed felis eget velit aliquet. Nunc sed augue lacus viverra vitae congue eu. Netus et malesuada fames ac turpis egestas. Ac tortor vitae purus faucibus ornare suspendisse sed nisi. Quis viverra nibh cras pulvinar mattis. Integer vitae justo eget magna fermentum. Integer quis auctor elit sed vulputate mi sit amet mauris. Duis at consectetur lorem donec massa sapien faucibus et molestie. At quis risus sed vulputate odio ut enim blandit volutpat. Odio aenean sed adipiscing diam. Odio ut sem nulla pharetra diam. Sed faucibus turpis in eu mi. Senectus et netus et malesuada fames. In vitae turpis massa sed elementum tempus egestas sed. In egestas erat imperdiet sed euismod nisi porta lorem mollis.
'''
content2 = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
'''

command = f'''insert into story values(1, 1,"Apples and evolution","{content + content2}",2,"{content2}","1462-02-29 09:25","1762-07-12 06:11");''' 
c.execute(command)  

command = f'''insert into user values(0, "Brian", "123","0,");''' 
c.execute(command) 

command = f'''insert into user values(1, "Weichen", "123","1,");''' 
c.execute(command) 

command = f'''insert into user values(2, "Vansh", "123","1,");''' 
c.execute(command) 

db.commit() 
db.close()

update_users()
update_stories()

@app.route("/")
def index():
    return render_template('homepage.html',
    watchlist=user_watchlist,
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

        edited_currentuser = []
        user_watchlist.clear()

        edited_currentuser = update_edited_currentusers(session["username"])
        grab_stories(edited_currentuser)

        #print(user_watchlist)
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

        params = (len(currentusers.keys()), user, password, "")

        command = f"insert into user values(?, ?, ?, ?);"       
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

        story_id = story[0]
        user_id = story[1]
        title = story[2]
        content = story[3]
        recentuser_id = story[4]
        original_date = story[6]
        recent_date = story[7]

        db.close()
        

        if title in user_watchlist:
            edited = True
        else: 
            edited = False



        return render_template('story.html',
            title=title,
            content=content,
            user=grab_username(user_id),
            recentuser=grab_username(recentuser_id),
            edited=edited,
            original_date=original_date,
            recent_date=recent_date,
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

            user = grab_username(story[1])
            content = story[3]
            recent_user = grab_username(story[4])
            recent_content = story[5]

            db.close()

            return render_template('edit.html',
                new=False,
                title=title,
                user=user,
                recent_user=recent_user,
                content=recent_content,
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
        recent_content = content

        db = sqlite3.connect(DB_FILE) 
        c = db.cursor() 

        if new == "False":
            command = f'''select * from story where title = "{title}";'''
            c.execute(command)   
            story = c.fetchone()

            id = story[0]
            user_id = story[1]
            oldcontent = story[3] + "\n"
            original_date = story[6]
            recent_date = get_time()

            user = session['username']

            command = f'''select id from user where username = "{user}";'''
            c.execute(command)   
            grab_recentuser_id = c.fetchone()
            recentuser_id = grab_recentuser_id[0]
            oldcontent += content
            content = oldcontent + "\n"
            #can add spot for user id
        else: 
            command = f'''select * from story where title = "{title}";'''
            c.execute(command)   
            story = c.fetchone()

            original_date = get_time()
            recent_date = get_time()
            
            if story is None:
                command = f'''select * from user where username = "{session["username"]}";'''
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

        command = f'''select * from user where id = {recentuser_id};'''
        c.execute(command) 
        grab_user = c.fetchone()
        password = grab_user[2]
        edited = grab_user[3]
        edited += f"{id},"

        command = f'''replace into user values({recentuser_id},"{session["username"]}","{password}","{edited}");'''
        c.execute(command)  

        db.commit() 
        
        #print(edited_currentuser)
        params = (id, user_id, str(title), str(content), recentuser_id, recent_content, original_date, recent_date)

        command = f'''replace into story values(?,?,?,?,?,?,?,?);'''
        c.execute(command,params)   

        db.commit() 
        db.close()

        edited_currentuser = update_edited_currentusers(session["username"])

        update_stories()
        
        grab_stories(edited_currentuser)

        return redirect(url_for('story',title=title))





@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()