# group_utils.py
from flask import flash, redirect, url_for
from sqlalchemy import text
from db import db


def get_group_projects(group_id):
    # Fetch projects for the specified group from the database
    project_sql = text("SELECT name, id FROM projects WHERE group_id = :group_id")
    project_result = db.session.execute(project_sql, {"group_id": group_id})
    projects = project_result.fetchall()

    # Fetch the name of the specified group from the database
    group_sql = text("SELECT name FROM groups WHERE id=:group_id")
    group_result = db.session.execute(group_sql, {"group_id": group_id})
    group_name = group_result.fetchone()[0]  # Assuming there is only one result

    return projects, group_name



def add_users(group_id, user_ids):
    try:
        # Use parameterized query to prevent SQL injection
        sql = text("INSERT INTO group_members (group_id, user_id) VALUES (:group_id, :user_id)")

        # Insert new rows into the group_members table for each user_id
        for user_id in user_ids:
            db.session.execute(sql, {"group_id": group_id, "user_id": user_id})

        # Commit the changes to the database
        db.session.commit()

        flash("Users added successfully!", "success")
    except Exception as e:
        # Handle exceptions, e.g., if there's an issue with the database
        db.session.rollback()
        flash(f"Error adding users: {str(e)}", "error")

    return redirect(url_for("group_projects", group_id=group_id))
