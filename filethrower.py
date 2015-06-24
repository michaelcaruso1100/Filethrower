#Routes file
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.script import Manager
from werkzeug import secure_filename
import MySQLdb
import os
import random
import string

UPLOAD_FOLDER = 'files/'


app = Flask(__name__)

app.config['SECRET_KEY']= os.urandom(24)
bootstrap = Bootstrap(app)
manager = Manager(app)
app.config['	UPLOAD_FOLDER']= UPLOAD_FOLDER

db = MySQLdb.connect("localhost", "root", "", "files")



@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if __name__ == '__main__':
		if request.method == 'POST':
			rand_url = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(8))
			file = request.files['file']
			if file:
				filename = secure_filename(file.filename)
				fullpath = '/home/mike/Code/filethrower/files/' + rand_url
				os.mkdir(fullpath)
				file.save(os.path.join(fullpath, filename))
				
				c = db.cursor()
				query='INSERT INTO files values(\'' + rand_url + '\',\'' + filename + '\')'
				c.execute(query)
				db.commit()
				
				return redirect('/receive/' + rand_url)
	return render_template('send.html')
			
@app.route('/uploads/<path:filename>',methods=['GET', 	'POST'])
def download_file(filename):
	rand = request.args.get('rand')
	uploads = '/home/mike/Code/filethrower/files/' + rand + '/'
	
	
	return send_from_directory(uploads,filename, as_attachment=True)


@app.route('/receive/<rand>')
def receive(rand):	
	c = db.cursor()
	query = 'SELECT name from files where id =\'' + rand + '\''
	c.execute(query)
	result = c.fetchall()
	filename = str(result).translate(None,'(),\'')	
	return render_template('receive.html',rand = rand, filename=filename)

if __name__ == '__main__':
	manager.run()
