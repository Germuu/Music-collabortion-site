from flask import Flask
from flask import redirect, render_template, request, session, url_for
from flask import flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "34d4713633d06b18cd607d75ed67de9d"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
db = SQLAlchemy(app) 



@app.route("/")
def index():
    return render_template("index.html") 


@app.route("/registration")
def registration():
    return render_template("registration.html") 

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql).params(username=username, password=hash_value))
        db.session.commit()
        return redirect("/")
    else:
        return render_template("registration.html")




@app.route("/login", methods=["POST"])
def login():
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



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_group")
def create_group():
    return render_template("create_group.html")




@app.route("/createg", methods=["GET", "POST"])
def createg():
    if request.method == "POST":
        group_name = request.form["group_name"]
        collaborators = request.form.getlist("collaborators")  # Use getlist to get multiple values

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
        creator_id = session.get("user_id")  # Assuming you store user_id in the session
        sql_creator = "INSERT INTO group_members (group_id, user_id) VALUES (:group_id, :user_id)"
        db.session.execute(text(sql_creator).params(group_id=group_id, user_id=creator_id))

        # ADD COLLABORATORS TO GROUP_MEMBERS TABLE
        sql_collaborator = "INSERT INTO group_members (group_id, user_id) VALUES (:group_id, :user_id)"
        for collaborator in collaborators:
            db.session.execute(text(sql_collaborator).params(group_id=group_id, user_id=collaborator))

        db.session.commit()
        return redirect("/group")
    else:
        return render_template("create_group.html")


@app.route("/group", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        project_name = request.form["project_name"]
        group_id = session.get("group_id")

        # CREATE PROJECT
        sql = "INSERT INTO projects (name,group_id) VALUES (:project_name,:group_id) RETURNING id"
        result = db.session.execute(text(sql).params(project_name=project_name,group_id=group_id))
        project_id = result.fetchone()[0]

        db.session.commit()
        flash("Project created successfully!", "success")
        return redirect("/")
    else:
        return render_template("group.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]

        # Fetch user's groups with both id and name from the database
        sql = text("SELECT DISTINCT groups.id, groups.name FROM groups "
                   "JOIN group_members ON groups.id = group_members.group_id "
                   "WHERE group_members.user_id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        user_groups = result.fetchall()

        return render_template("dashboard.html", user_groups=user_groups)
    else:
        flash("Please log in first", "error")
        return redirect("/")



@app.route("/group_projects/<int:group_id>")
def group_projects(group_id):
    # Fetch projects for the specified group from the database
    sql = text("SELECT name,id FROM projects WHERE group_id = :group_id")
    result = db.session.execute(sql, {"group_id": group_id})
    projects = result.fetchall()

    return render_template("group_projects.html", projects=projects)




@app.route("/project_details/<int:project_id>")
def project_details(project_id):
    # Fetch project details and files from the database
    project_sql = text("SELECT name, id FROM projects WHERE id = :project_id")
    project_result = db.session.execute(project_sql, {"project_id": project_id})
    project = project_result.fetchone()
    return render_template("project_details.html", project=project)



@app.route('/upload_file', methods=['POST'])
def upload_file():
    # Process the form data, including extracting the project ID
    project_id = request.form.get('project_id')

    # Your file handling logic here...

    # Redirect to the 'uploads' route with the given project ID
    return redirect(url_for('uploads', project_id=project_id))









@app.route("/uploads/<int:project_id>", methods=["GET", "POST"])
def uploads(project_id):
    if request.method == "GET":
        # Fetch projects and latest uploaded files for the specified project from the database
        project_sql = text("SELECT name, id FROM projects WHERE id = :project_id")
        project_result = db.session.execute(project_sql, {"project_id": project_id})
        project = project_result.fetchone()

        latest_file_sql = text(
            "SELECT id, file_path FROM project_files WHERE project_id = :project_id ORDER BY id DESC LIMIT 1"
        )
        latest_file_result = db.session.execute(latest_file_sql, {"project_id": project_id})
        latest_uploads = latest_file_result.fetchone()

        # Render the template with the project details and latest_uploads
        return render_template("uploads.html", project=project, latest_uploads=latest_uploads)

    elif request.method == "POST":
        # Handle POST request logic (if any) for the /uploads/<project_id> route
        # This might include processing form data, handling file uploads, etc.
        # ...

        # Redirect or render a response after handling the POST request
        return redirect(url_for('uploads', project_id=project_id))

    # Handle other request methods if needed
    else:
        return abort(405)  # Method Not Allowed







@app.route("/download_file/<int:file_id>")
def download_file(file_id):
    # Fetch file path from the database
    file_sql = text("SELECT file_path FROM project_files WHERE id = :file_id")
    file_result = db.session.execute(file_sql, {"file_id": file_id})
    file_path = file_result.scalar()

    return send_file(file_path, as_attachment=True)



