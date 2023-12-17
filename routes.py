from flask import render_template, request, flash, redirect, session, send_file, url_for, abort
from app import app
from user_utils import *
from creation_utils import *
from group_utils import *
from project_utils import *
from csrf_protection import *

@app.route("/")
def index():
    generate_token()
    return render_template("index.html", csrf_token=session["csrf_token"]) 
    
@app.route("/registration")
def registration():
    generate_token()
    return render_template("registration.html", csrf_token=session["csrf_token"])

@app.route("/register", methods=["GET", "POST"])
def register():
    check_token()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return register_user(username, password)
    return render_template("registration.html")

@app.route("/login", methods=["POST"])
def login():
    check_token()
    return login_user(request)

@app.route("/logout")
def logout():
    return logout_user()

@app.route("/create_group")
def create_group():
    generate_token()
    return render_template("create_group.html", csrf_token=session["csrf_token"])

@app.route("/createg", methods=["GET", "POST"])
def createg():
    check_token
    if request.method == "POST":
        group_name = request.form["group_name"]
        collaborators = request.form.getlist("collaborators")
        creator_id = session.get("user_id")
        return create_g(group_name, creator_id, collaborators)
    return render_template("create_group.html")

@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    check_token()
    if request.method == "POST":
        project_name = request.form["project_name"]
        group_id = request.form["group_id"]
        creator_id = session.get("user_id")
        create_p(project_name, group_id)
        return redirect(url_for("group_projects", group_id=group_id))
    return render_template("group.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        user_groups = get_user_groups(user_id)
        return render_template("dashboard.html", user_groups=user_groups)
    else:
        flash("Please log in first", "error")
        return redirect("/")

@app.route("/group_projects/<int:group_id>")
def group_projects(group_id):
    generate_token()
    projects, group_name = get_group_projects(group_id)
    return render_template("group_projects.html", projects=projects, group_id=group_id, group_name=group_name,csrf_token=session["csrf_token"])


@app.route("/add_users_to_group/<int:group_id>", methods=["POST"])
def add_users_to_group(group_id):
    check_token()
    if request.method == "POST":
        user_ids = [int(user_id.strip()) for user_id in request.form["user_ids"].split(',')]
        return add_users(group_id, user_ids)

@app.route("/project_details/<int:project_id>")
def project_details(project_id):
    generate_token()
    project = get_project_details(project_id)
    return render_template("project_details.html", project=project,csrf_token=session["csrf_token"])

@app.route('/upload_file', methods=['POST'])
def upload_file():
    check_token()
    return uploader()

@app.route("/uploads/<int:project_id>", methods=["GET", "POST"])
def uploads(project_id):
    generate_token()
    if request.method == "GET":
        # Fetch project details
        project_sql = text("SELECT name, id FROM projects WHERE id = :project_id")
        project_result = db.session.execute(project_sql, {"project_id": project_id})
        project = project_result.fetchone()
        # Get latest files for each type
        latest_files = get_latest_files(project_id)
        # Render the template with the project details and latest_files
        return render_template("uploads.html", project=project, latest_files=latest_files,csrf_token=session["csrf_token"])
    elif request.method == "POST":
        # Handle POST request if needed
        return redirect(url_for('uploads', project_id=project_id,csrf_token=session["csrf_token"]))
    else:
        return abort(405) 

@app.route("/download_file/<int:file_id>")
def download_file(file_id):
    path=get_filepath(file_id)
    return send_file(path, as_attachment=True)
