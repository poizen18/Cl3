from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/',methods = ['POST'])
def checkpost():
    stopwords = ('a','is','and','this','the','has','for','it')
    text1 = request.form['txt1']
    text2 = request.form['txt2']
    text1 = text1.encode('utf8')
    text2 = text2.encode('utf8')

    text1 = text1.strip()
    text2 = text2.strip()

    text2 = text2.replace('.', ' ')
    text2 = text2.replace(',', ' ')
    text2 = text2.replace(';', ' ')
    text2 = text2.replace('-', ' ')
    text2 = text2.split(' ')
    text1 = text1.replace('.', ' ')
    text1 = text1.replace(',', ' ')
    text1 = text1.replace(';', ' ')
    text1 = text1.replace('-', ' ')
    text1 = text1.split(' ')
    text1 = set(text1) - set(stopwords)
    text2 = set(text2) - set(stopwords)
    common = (set(text1) & set(text2))
    commonlen =len(common)
    totallen = float((len(text1)+len(text2))/2)
    try:
        ratio = float(commonlen/totallen)*100
    except ZeroDivisionError:
        ratio = 0

    return 'plagiarism has been detected by: '+str(ratio)+"% "

if __name__=="__main__":
    app.debug = True
    app.run()
