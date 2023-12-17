from flask import Flask

app = Flask(__name__)
app.secret_key = "34d4713633d06b18cd607d75ed67de9d"
app.config['STATIC_FOLDER'] = 'static'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import routes