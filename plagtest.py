from flask import Flask, render_template, request
#from difflib import SequenceMatcher
#import re
# TODO: add uploading file option bro.
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('plag.html')

@app.route('/', methods = ['POST'])
def my_form_post():
    file1 = request.form['txt']
    file2 = request.form['text']
    count=0
    '''
    # lol, external pagal ho jayenga xD
    similarity_ratio = SequenceMatcher(None,file1,file2).ratio()*100
    if similarity_ratio > 70:
        return '<h1>plagarism has BEEN detected with documents being ' + str(similarity_ratio) + '% similar'
    else:
        return '<h1>plagarism has NOT BEEN detected with documents being ' + str(similarity_ratio) + '% similar'
    '''
    # accepted stuff is in unicode mein hai, so :
    filelist1=file1.encode('utf8')
    filelist2 = file2.encode('utf8')

    foo = filelist1.replace('.',' ')
    bar = filelist2.replace('.', ' ')
    foo= foo.replace(',',' ')
    foo = foo.replace(';', ' ')
    bar = bar.replace(',', ' ')
    bar = bar.replace(';', ' ')
    filelist1= foo
    filelist2 = bar
    filelist1=filelist1.split(' ')
    filelist2=filelist2.split(' ')

    #print filelist1, filelist2
    same_words= set(filelist1) & set(filelist2)
    count=len(same_words)


    similarity_ratio1= float(count)/len(filelist1)
    similarity_ratio2= float(count)/len(filelist2)
    mean_ratio=  (similarity_ratio1+similarity_ratio2)/2
    similarity_ratio=mean_ratio*100

    if similarity_ratio > 69:  # :P huehuehue
        return '<h1>plagarism has BEEN detected with documents being ' + str(similarity_ratio) + '% similar'
    else:
        return '<h1>plagarism has NOT BEEN detected with documents being ' + str(similarity_ratio) + '% similar'


if __name__ == '__main__':
    app.run()
