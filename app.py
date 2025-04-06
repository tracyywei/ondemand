from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    return ""
       
if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)