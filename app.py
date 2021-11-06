from flask import Flask , render_template, session, request, jsonify, redirect, url_for
from sentiment import main, json_reader
from sentiment.sentiment_score import clean_text, calculate_sentiment_score
from sentiment.reddit_scraper.reddit_scraper.spiders.reddit_post_scraper import RedditPostCrawler
from algo import chancer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/chanceme',methods=["GET","POST"])
def chanceme():
    if request.method == "POST":
        school = request.form['school']
        sat = request.form['sat']
        gpa = request.form['gpa']
        ec_0 = request.form['ec_0']
        ec_1 = request.form['ec_1']
        ec_2 = request.form['ec_2']
        ec_3 = request.form['ec_3']
        ec_4 = request.form['ec_4']
        ec_5 = request.form['ec_5']
        ec_6 = request.form['ec_6']
        ec_7 = request.form['ec_7']
        ec_8 = request.form['ec_8']
        ec_9 = request.form['ec_9']
        ecs = [ec_0,ec_1,ec_2,ec_3,ec_4,ec_5,ec_6,ec_7,ec_8,ec_9]
        bot = chancer.chancer(school,sat,gpa,ecs,[])
        for ec in ecs:
            sent = main.compute_sentiment(ec)
