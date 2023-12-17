# creation_utils.py
from flask import session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from db import db



def create_g(group_name, creator_id, collaborators):
    # Check if the group with the given name already exists
    existing_group = db.session.execute(
        text("SELECT * FROM groups WHERE name = :group_name").params(group_name=group_name)
    ).fetchone()

    if existing_group:
        flash("Group with the same name already exists. Choose a different name.")
        return redirect("/createg")  # Redirect to the createg page to try again

    # CREATE GROUP
    sql = "INSERT INTO groups (name) VALUES (:group_name) RETURNING id"
    result = db.session.execute(text(sql).params(group_name=group_name))
    group_id = result.fetchone()[0]
    session["group_id"] = group_id

    # ADD CREATOR TO GROUP_MEMBERS TABLE
    sql_creator = "INSERT INTO group_members (group_id, user_id) VALUES (:group_id, :user_id)"
    db.session.execute(text(sql_creator).params(group_id=group_id, user_id=creator_id))

    # ADD COLLABORATORS TO GROUP_MEMBERS TABLE
    sql_collaborator = "INSERT INTO group_members (group_id, user_id) VALUES (:group_id, :user_id)"
    for collaborator in collaborators:
        db.session.execute(text(sql_collaborator).params(group_id=group_id, user_id=collaborator))

    db.session.commit()
    return redirect("/dashboard")


def create_p(project_name, group_id):
    # CREATE PROJECT
    sql = "INSERT INTO projects (name, group_id) VALUES (:project_name, :group_id) RETURNING id"
    result = db.session.execute(text(sql).params(project_name=project_name, group_id=group_id))
    project_id = result.fetchone()[0]

    db.session.commit()
    flash("Project created successfully!", "success")
    return project_id  # You can return the project_id if needed