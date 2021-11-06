from flask import Flask , render_template, session, request, jsonify, redirect, url_for
#from sentiment import main
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)