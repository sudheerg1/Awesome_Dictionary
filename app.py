from flask import Flask, render_template, redirect, url_for, request
import requests
import json
from func import List2String
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():

    if request.method == "POST":
        word1 = request.form["nm"]
        return redirect(url_for("definition",word = word1))
    else:
        return render_template('index.html')
    

@app.route('/<word>')
def definition(word):

    if word is None:
        return render_template("index.html")

    key = os.getenv("api_key")
    end_point = "https://dictionaryapi.com/api/v3/references/learners/json/"+ word +"?key="+ key
    data = requests.get(end_point).text

    if str(data) == '[]':
        return render_template("notExists.html")

    elif str(data) != '[]':
        obj = json.loads(data)
        meaning = List2String(obj[0]["shortdef"])
        return render_template("definition.html", word=word, meaning=meaning)
    
    else:
        return render_template("suggested.html")

    

#Custom Error Pages 

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404 

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route('/about')
def about():

    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)





