from flask import render_template

from keep.ui import app

@app.route('/')
def index():
  return render_template('index.html')
