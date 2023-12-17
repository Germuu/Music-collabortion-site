# user_utils.py
from flask import flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db




def register_user(username, password):
    existing_user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username").params(username=username)
    ).fetchone()
    
    if existing_user:
        flash("User with the same name already exists. Choose a different name.")
        return redirect("/registration") # Redirect to the createg page to try again 
             
    
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql).params(username=username, password=hash_value))
    db.session.commit()


def login_user(request):
    username = request.form["username"]
    password = request.form["password"]

    # Check if the username exists in the database
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        flash("Invalid username", "error")
        return redirect("/")

    hash_value = user.password

    # Check if the entered password is correct
    if check_password_hash(hash_value, password):
        # Successful login
        session["user_id"] = user.id
        session["username"] = username
        flash("Login successful", "success")
        return redirect("/")
    else:
        # Invalid password
        flash("Invalid password", "error")
        return redirect("/")

def logout_user():
    if "username" in session:
        del session["username"]
    return redirect("/")


def get_user_groups(user_id):
    # Fetch user's groups with both id and name from the database
    sql = text("SELECT DISTINCT groups.id, groups.name FROM groups "
               "JOIN group_members ON groups.id = group_members.group_id "
               "WHERE group_members.user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    user_groups = result.fetchall()
    return user_groups