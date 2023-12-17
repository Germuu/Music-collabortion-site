
import os
from flask import request, render_template, redirect, url_for
from sqlalchemy import text
from db import db


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_project_details(project_id):
    # Fetch project details from the database
    project_sql = text("SELECT name, id FROM projects WHERE id = :project_id")
    project_result = db.session.execute(project_sql, {"project_id": project_id})
    project = project_result.fetchone()

    return project


def uploader():
    # Process the form data, including extracting the project ID
    project_id = request.form.get('project_id')

    # Loop through the file types and handle each file
    for file_type in ['track_1', 'track_2', 'track_3', 'track_4', 'track_5', 'track_6','track_7','track_8']:
        uploaded_file = request.files[file_type]

        if uploaded_file:
            # Save the file to the designated directory
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Save information to the database, including the file type
            file_sql = text("INSERT INTO project_files (project_id, file_path, comment, file_type) VALUES (:project_id, :file_path, :comment, :file_type)")
            db.session.execute(file_sql, {"project_id": project_id, "file_path": file_path, "comment": request.form.get('comment'), "file_type": file_type})
            db.session.commit()

    # Redirect to the 'uploads' route with the given project ID
    return redirect(url_for('uploads', project_id=project_id))



def get_latest_files(project_id):
    # Fetch latest file for each type, including the upload_timestamp
    file_types = ['track_1', 'track_2', 'track_3', 'track_4', 'track_5', 'track_6','track_7','track_8']
    latest_files = {}

    for file_type in file_types:
        latest_file_sql = text(
            "SELECT id, file_path, comment, upload_timestamp FROM project_files WHERE project_id = :project_id AND file_type = :file_type ORDER BY id DESC LIMIT 1"
        )
        latest_file_result = db.session.execute(latest_file_sql, {"project_id": project_id, "file_type": file_type})
        latest_file = latest_file_result.fetchone()

        # Convert the timestamp to a datetime object (assuming it's not already)
        if latest_file and 'upload_timestamp' in latest_file:
            latest_file['upload_timestamp'] = datetime.strptime(latest_file['upload_timestamp'], "%Y-%m-%d %H:%M:%S")

        latest_files[file_type] = latest_file

    return latest_files

def get_filepath(file_id):
    # Fetch file path from the database
    file_sql = text("SELECT file_path FROM project_files WHERE id = :file_id")
    file_result = db.session.execute(file_sql, {"file_id": file_id})
    file_path = file_result.scalar()

    return file_path