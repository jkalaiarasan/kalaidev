from flask import Flask, render_template, make_response
#from router.customerRoute import customer
#from router.consumerRoute import consumer

app = Flask(__name__)

#app.register_blueprint(customer)
#app.register_blueprint(consumer)

@app.route('/')
def homePage():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)