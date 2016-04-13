from flask import Flask, render_template, request
from difflib import SequenceMatcher
# TODO: add uploading file option bro. 
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('plag.html')

@app.route('/', methods = ['POST'])
def my_form_post():

    file1 = request.form['txt']
    file2 = request.form['text']
    similarity_ratio = SequenceMatcher(None,file1,file2).ratio()*100
    if similarity_ratio > 70:
        return '<h1>plagarism has BEEN detected with documents being ' + str(similarity_ratio) + '% similar'
    else:
        return '<h1>plagarism has NOT BEEN detected with documents being ' + str(similarity_ratio) + '% similar'

if __name__ == '__main__':
    app.run()
