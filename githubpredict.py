from flask import Flask, render_template, request, redirect, url_for

import uuid
import datetime
import ast

import database
import process

app = Flask(__name__)

LASTQUERYFILE = "lastQuery.txt"
LASTQUERY = ""

LANGUAGES = ['r', 'python']
PREDYEARS = 5

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getdata', methods=['POST'])
def getData():
    queryName = ""

    wantsNewData = request.form.get('newData', False)
    with open(LASTQUERYFILE, 'r') as f:
        LASTQUERY = f.read().strip()
    if wantsNewData or LASTQUERY == "":
        queryName = uuid.uuid4()
        database.loadFreshData(queryName, LANGUAGES)
        with open(LASTQUERYFILE, 'w') as f:
            f.write(str(queryName))
    else:
        queryName = LASTQUERY

    npArrays = process.getNumpyArrays(queryName)
    preds = {}
    for lang in npArrays.keys():
        preds[lang] = process.getLinRegPred(npArrays[lang], PREDYEARS).tolist()

    return redirect(url_for('show', preds=preds))

@app.route('/show')
def show():
    curYear = datetime.datetime.now().year
    lastPredYear = curYear + PREDYEARS
    years = list(range(curYear, lastPredYear))

    preds = request.args.get('preds')
    preds = ast.literal_eval(preds)

    #Round all estimates to integers
    for counts in preds.values():
        for i in range(len(counts)):
            counts[i] = int(round(counts[i]))

    return render_template('results.html', result=preds, years=years, yearrange=PREDYEARS)

if __name__ == '__main__':
    app.run()