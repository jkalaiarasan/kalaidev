from flask import Blueprint, render_template, request
from authentication.authenticateSalesforce import sf
import json

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/login')
def customerLoginPage():
    return render_template('customerlogin.html')

@customer.route('/register', methods = ['GET', 'POST'])
def customerRegisterPage():
    if request.method == 'POST':
        req = request.data
        data = json.loads(req)
        email = data["Email"]
        name = data["Name"]
        password = data["Password"]
        try:
            insert = sf.Customer__c.create({'Name':name, 'Email__c':email, 'Password__c':password})
            return insert
        except:
            return 'Sommething went wrong'
    if request.method == 'GET':
        return render_template('customerregister.html')
