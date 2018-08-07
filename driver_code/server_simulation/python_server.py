from flask import *
app = Flask(__name__)
import os

@app.route("/test/", methods=['POST'])
def send_file():
    print("Someone requested a file!")
    cwd = os.getcwd()
    print(cwd)
    response = send_from_directory(directory = cwd + '/evaluation_scripts/', filename='large_text.txt')
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response

@app.route("/")
def hello():
    print("I am alive!")
    return "Hello World!"

if __name__ == '__main__':
    print("Server Started")
    app.run(threaded = False, host = '127.0.0.1', port=8020 )

