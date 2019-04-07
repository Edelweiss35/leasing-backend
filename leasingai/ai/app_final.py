from flask import Flask, jsonify, send_from_directory
from werkzeug import secure_filename
from flask import request
from clause_analyze import main
from clause_analyze import clean
from clause_analyze import create_table
from classify_clause import matching_rate
from flask_cors import CORS
from flask_pymongo import PyMongo
from os.path import splitext

from flask import Flask, render_template, request, redirect, Response
import random, json
import pdb
from nltk.tokenize import sent_tokenize

filename = ""

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

# app.config['MONGO_DBNAME'] = 'connect_mongo'
# app.config['MONGO_URI'] = 'mongodb://clause_admin:goodboy777@ds115244.mlab.com:15244/connect_mongo'
app.config['MONGO_DBNAME'] = 'classify_lease'
app.config['MONGO_URI'] = 'mongodb://classifyuser:classify123$@ds135800.mlab.com:35800/classify_lease'

mongo = PyMongo(app)
@app.route('/')
def hello():
    return "Hello"

@app.route('/out/<path:path>')
def send_js(path):
    return send_from_directory('out', path)


def download_file(url):
    local_filename = url.split('/')[-1]
    local_filename = local_filename.replace("%20", "_")
    r = requests.get(url, stream=True)
    print(r)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return local_filename

#---------------  signup -----------
@app.route("/api/signup", methods=['POST','GET'])
def signup():
    loginuser = mongo.db.login_user
    
    userinfo = request.get_json()
    phone = userinfo['phone']
    password = userinfo['password']
    name = userinfo['name']
    email = userinfo['email']
    loginuser.insert({'phone':phone, 'password':password, 'name':name, 'email':email})
    token = email + "2354252"
    return token
#---------------  login -----------
@app.route("/api/login", methods=['POST','GET'])
def login():
    loginuser = mongo.db.login_user
    userinfo = request.get_json()
    email = userinfo['email']
    password = userinfo['password']
    finduser = loginuser.find_one({'email': email,'password':password})
    if finduser:
        email = finduser.get('email')
        token = email + "2354252"
        return email    
@app.route("/export", methods=['POST','GET'])
def download_file():
    filename = request.form['filename']
    name = splitext(filename)[0]
    url = 'http://localhost:8081/out/'+name+'.docx'
    print("_____________________ _______________")
    print(url)
    return url

@app.route('/submit', methods=['POST'])
def clause_upload():
    user = mongo.db.users
    check=""
    clause = {}
    pass_clause = []
    clausesall = request.get_json()
    user_email = clausesall['email']
    for item in clausesall['clauses']:
        reason=clean(item['reason'])
        clausename=clean(item['clausename'])
        action=clean(item['action'])
        if action == '':
            action = "Found"
        text=clean(item['text'])
        
        clause_exist = user.find_one({'email':user_email,'reason': reason,'clausename':clausename,'action':action,'text':text})
        if clause_exist:continue
        user.insert({'clausename':clausename,'email':user_email,'text':text,'reason':reason,'action':action})
    
    #for item in clausesall['clauses']:
    #    reason = item['reason']
    #    check = "no"
    #    for jtem in pass_clause:
    #        reason_exist = jtem['reason']
    #        if reason == reason_exist:check="yes"
    #    if check == "yes":continue  
    #    pass_clause.append(item)
    pass_clause = clausesall['legal_clauses']                               
    filename = clausesall['filename']
    content_clauses = main(filename,pass_clause) 
    l = []
    if content_clauses != None:
        for clause in content_clauses:
            clausename = clause['clausename']
            reason = clause['reason']
            content_text = clause['text']
            action = clause['action']
            if content_text == "":continue
            db_reason_clauses = user.find({'clausename':clausename,"reason":reason,'action':action})
            check_matching = 0
            for db_reason_clause in db_reason_clauses:
                key_text = db_reason_clause.get('text')  
                clause['key_text'] = key_text
                if(matching_rate(content_text, key_text) == 1):
                    check_matching = 1
            if ((check_matching == 1) and (action == 'Found')):
                l.append(clause)
            if ((check_matching == 0) and (action == 'Not Found') and (db_reason_clauses.count()>0)):
                l.append(clause)   
    else:
        l.append({'clausename': '',"reason": '','action': '', 'text': ''})

    print 'checking l content'
    print l
    export_result = create_table(filename, l)

    #name = main(f.filename, clause)
    #url = 'http://localhost:8081/out/'+name+'.docx'
    #print(filename)
    return jsonify(export_result)

@app.route('/get_legal', methods=['POST'])
def get_legal():
    user = mongo.db.users
    clauseall = request.get_json()
    reason_number = 0
    l=[]
    user_email = clauseall.get('email')
    print("---------------------------------------------------")
    print(user_email)
    for item in clauseall['clauses']:
        t={}
        reason = clean(item['reason'])
        clausename = clean(item['clausename'])
        action = clean(item['action'])
        if(action == ""): action = "Found"
        print(clausename)
        print(action)
        if(clausename == ""):
            db_clauses = user.find({'reason':reason})
        else:
            db_clauses = user.find({'reason':reason, 'clausename':clausename,'action':action,'email':user_email})
        reason_number =  db_clauses.count()
        t['reason']=reason
        t['text']=reason_number
        t['clausename']=clausename
        t['action']=action
        if reason_number > 0:
            if(clausename == ""):
                db_clause = user.find_one({'reason':reason})
                #t['clausename']=db_clause.get('clausename')
                #t['action']=db_clause.get('action')
        
            else:
                db_clause = user.find_one({'reason':reason, 'clausename':clausename})
                #t['action']=db_clause.get('action')
            #t['action']=db_clause.get('action')  
        else:
            user.insert({'clausename':clausename,'email':user_email,'reason':reason,'action':action})
            reason_number =  db_clauses.count()
            t['text']=reason_number
        l.append(t)
    return jsonify(l) 

@app.route('/fileupload', methods=['POST'])
def file_upload():
    f=request.files['selectedFile']	
    
    f.save(secure_filename(f.filename))
    filename = f.filename
    print("uploaded")
    return "hello"   

@app.route('/reason', methods=['POST','GET'])
def findall_reasons():
    user = mongo.db.users
    reasons = user.find()
    print("----------------", reasons);
    l=[]
    clause = request.get_json()
    print(clause['clauses'])
    print("ok")
    for reason in reasons:
       t={}
       #reason_temp = reason.reason
       t['reason'] = reason.get('reason')
       t['action'] = reason.get('action')
       t['clausename'] = reason.get('clausename')
       for l_temp in l:
           if t['action'] == l_temp['action']:t['action']=""
           if t['clausename'] == l_temp['clausename']:t['clausename']="" 
           if t['reason'] == l_temp['reason']:t['reason']="" 
       l.append(t)
    return jsonify(l)

@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name' : 'goodboy'})
    return 'Added User' 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081,debug=True)
