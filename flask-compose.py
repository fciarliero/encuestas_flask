from app import app
'''
from flask import Flask
#from app import app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secreto'
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
