from flask import request, jsonify

from GeometrA import app
from GeometrA.src import WORKSPACE as ws
from GeometrA.src import TESTSCRIPT as ts
import pprint

@app.route('/GeometrA/TestScript/run', methods=['POST'])
def run():
    caseList = request.form['cases'].split('/')
    pprint.pprint(caseList)
    path = ws.projects[caseList[0]].suites[caseList[1]].path + '/' +caseList[2]
    ts.load(path)
    return ts.runAll()