from flask import Blueprint, render_template, request, jsonify
from authentication.authenticateSalesforce import sf
import bcrypt
import jwt
import json

password = None
hashedPassword = None
name = None
email = None
obj = {name:'', email:''}

consumer = Blueprint('consumer', __name__, url_prefix='/consumer')

@consumer.route('/login', methods = ['GET', 'POST'])
def consumerLoginPage():
    if request.method == 'GET':
        return render_template('consumerlogin.html')
    if request.method == 'POST':
        req = request.data
        data = json.loads(req)
        email = data["Email"]
        password = data["Password"]
        consumers = sf.query("SELECT Id, Name, Email__c, Password__c FROM Consumer__c WHERE Email__c = \'" + email + "\' LIMIT 1")
        totalSize = 0
        records = []
        for key, value in consumers.items(): 
            if key == 'totalSize':
                totalSize = value
            if key == 'records':
                records = value
        if totalSize == 1:
            for record in records: 
                singleRecord = record
        if totalSize == 1:
            for key, value in singleRecord.items(): 
                if key == 'Password__c':
                    hashedPassword = value
                if key == 'Id':
                    Id = value
                if key == 'Name':
                    name = value
            if bcrypt.checkpw(password.encode('utf8'), hashedPassword.encode('utf-8')) == True:
                token = jwt.encode({'name':name, 'id':Id}, 'FLEKNNIRQSQ')
                data = {"token": token}
                return jsonify(data)
            else:
                data = {"Message": "Your Password is incorrect"}
                return jsonify(data), 401
        else:
            data = {"Message": "Your Username is incorrect"}
            return jsonify(data), 401

@consumer.route('/register', methods = ['GET', 'POST'])
def consumerRegisterPage():
    if request.method == 'POST':
        req = request.data
        data = json.loads(req)
        email = data["Email"]
        name = data["Name"]
        password = data["Password"]
        bytes_string = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))
        hashedPassword = str(bytes_string, 'utf-8')
        try:
            insert = sf.Consumer__c.create({'Name':name, 'Email__c':email, 'Password__c':hashedPassword})
            return insert
        except:
            return 'Sommething went wrong'
    if request.method == 'GET':
        return render_template('consumerregister.html')

@consumer.route('/dashboard', methods = ['GET', 'POST'])
def consumerAccountPage():
    Id = None
    if request.method == 'GET':
        return render_template('consumerdashboard.html')
    if request.method == 'POST':
        req = request.data
        data = json.loads(req)
        token = data["token"]
        try:
            data = jwt.decode(token, "FLEKNNIRQSQ")
            Id = data["id"]
            record = sf.query("SELECT Id, Name, Email__c, Photo__c FROM Consumer__c WHERE Id = \'" + Id + "\'")
            return record
        except:
            return "False"

@consumer.route('/product', methods = ['GET', 'POST'])
def getProduct():
    if request.method == 'GET':
        token = request.args.get('token')
        try:
            data = jwt.decode(token, "FLEKNNIRQSQ")
            Id = data["id"]
            record = sf.query("SELECT Id, Name, Amount__c, Original_Amount__c, Photo__c FROM Product__c WHERE Consumer__c = \'" + Id + "\'")
            return record
        except:
            return "False"
