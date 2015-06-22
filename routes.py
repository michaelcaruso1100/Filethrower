from flask import Flask, render_template, request, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = '/home/mike/Code/CSC398/filethrower/files/'
ALLOWED_EXTENSIONS = set(['txt','mp3'])

app = Flask(__name__)

app.config['SECRET_KEY']= os.urandom(24)
bootstrap = Bootstrap(app)
manager = Manager(app)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return 'Successful Upload!'
		
	return render_template('send.html')
	
if __name__ == '__main__':
	manager.run()	
