# Imports All Libiraries  👇👇👇
from flask import Flask, render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import math
from werkzeug.utils import secure_filename
# from flask_mail import Mail, Message
import json

with open("config.json", "r") as f:
    params = json.load(f)["params"]

local_server = True
app = Flask(__name__) # Making the flask app
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location'] # Set the Location to Upload a Files

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = params['gmail_user'],
# app.config['MAIL_PASSWORD'] = params['gmail_password']
# mail = Mail(app)

# Check the conditions about server 👇👇
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


db = SQLAlchemy(app) #Making the data base using SQLALchemy

# Making the table contact same as Data Base 👇👇👇  
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    Msg = db.Column(db.String(120), nullable=False)
    Email = db.Column(db.String(20), nullable=False)

# Making the table post same as Data Base 👇👇👇  
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)
    img_file = db.Column(db.String(120), nullable=True)


# home page 👇👇👇
@app.route("/")
def home():
    posts = Posts.query.filter_by().all() #Fetch the all post from Data base
    last = math.ceil(len(posts)/int(params['no_of_posts'])) #Calculate the number page

    page = request.args.get('page') #Get the numbers of page like 1 ,2 ,3 etc
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts']) + int(params['no_of_posts'])] # Show the 2 post on every page
    
    # Check the condition of page numbers 👇👇👇
    if page==1:
        prev = "#"
        move = "/?page="+ str(page+1) # Get Request the page from Data Base for post
    elif page==last:
        prev = "/?page="+ str(page-1)
        move = "#"
    else:
        prev = "/?page="+ str(page-1)
        move = "/?page="+ str(page+1)

        # return the structure of home page and make all function which perform some actions 👇👇    
    return render_template('index.html', params=params, posts=posts, prev=prev, move=move)

# DashBoard Start Here 👇👇
@app.route('/dashboard',methods = ['GET', 'POST'])
def DashBoard():
    
    # Check the user enter in admin panel or not 👇👇
    if 'user' in session and session['user'] == params['admin_user']:
            posts = Posts.query.all()
            return render_template('dashboard.html',params=params,posts=posts)
        # If user not in admin panel then enter the password and username  
    if request.method == 'POST':
        username = request.form.get('uname') #Name get from form of admin panel login html
        userpass = request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_password']:
            session['user'] = username 
            posts = Posts.query.filter_by().all()
            return render_template('dashboard.html',params=params,posts=posts)
    else:
        return render_template('login.html',params=params)

# About Page start here 👇👇
@app.route('/about')
def About():
    return render_template('about.html',params=params)

# Edit Page where we enter the new post
@app.route("/edit", methods=['GET', 'POST'])
def Edit():
    # Check the user enter in admin panel or not 👇👇
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.form.get('title') #All the get from Form of edit the post 
            tagline = request.form.get('tagline') #All the get from Form of edit the post 
            slug = request.form.get('slug') #All the get from Form of edit the post 
            content = request.form.get('content') #All the get from Form of edit the post 
            img = request.form.get('img_file') #All the get from Form of edit the post 
            date = datetime.now() #All the get from Form of edit the post 
            
            # All data assign the template varaible from forms vraible data
            post = Posts(title=title, slug=slug, content=content, tagline=tagline, img_file=img, date=date)
            db.session.add(post) # Add in the data base
            db.session.commit()  # Commit the changes to the database
    return render_template('edit.html',params=params)

@app.route("/editpost/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    box_title = ""  # Initialize box_title outside of the if block
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title=title, slug=slug, content=content, tagline=tagline, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.tagline = tagline
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/editpost/' + sno)

    post = Posts.query.filter_by(sno=sno).first()
    return render_template('editpost.html', params=params, post=post)

# Contact Page Start Here 
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    # used the post methods
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = Contacts(Name = name, Email = email,  Phone = phone,Msg = msg)
        db.session.add(entry)
        db.session.commit()

        # subject = f"New message from {name}"
        # sender = email
        # recipients = params['gmail_user'] # Change this to your recipient's email address
        # body = f"{msg}\nPhone: {phone}"
        # msgEmail = Message(subject=subject, sender=sender, recipients=recipients, body=body)
        # mail.send(msgEmail)
    return render_template('contact.html',params=params)

# Post Part Start here 👇👇
# This purpose is that when we show the post on the home page and click the post then they will move us on that post with their slugs

@app.route("/post/<string:post_slug>", methods=['GET'])
def Post_Route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,posts=post)

# Upload the a file and save the file in the folder 👇👇 
@app.route("/upload" ,methods = ['GET','POST'])
def Upload():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(file.filename)))
            return "Uploaded SuceesFuly"

# logout Page Start Here 👇👇
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

# Move to  DashBoard and delete the post from Data base 👇👇
@app.route("/delete/<string:sno>" , methods=['GET', 'POST'])
def delete(sno):
    if "user" in session and session['user']==params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")        

app.run(debug=True)
