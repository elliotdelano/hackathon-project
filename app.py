from flask import Flask , render_template, session, request, jsonify, redirect, url_for
from sentiment import main, json_reader
from sentiment.sentiment_score import clean_text, calculate_sentiment_score
from sentiment.reddit_scraper.reddit_scraper.spiders.reddit_post_scraper import RedditPostCrawler
from algo import chancer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chanceme',methods=["GET","POST"])
def chanceme():
    if request.method == "POST":
        sat = request.form['sat']
        school = request.form['school']
        gpa = request.form['gpa']
        ec_0 = request.form['ec_0']
        hr_0 = request.form['hr_0']
        ec_1 = request.form['ec_1']
        hr_1 = request.form['hr_0']
        ec_2 = request.form['ec_2']
        hr_2 = request.form['hr_0']
        ec_3 = request.form['ec_3']
        hr_3 = request.form['hr_0']
        ec_4 = request.form['ec_4']
        hr_4 = request.form['hr_0']
        ec_5 = request.form['ec_5']
        hr_5 = request.form['hr_0']
        ec_6 = request.form['ec_6']
        hr_6 = request.form['hr_0']
        ec_7 = request.form['ec_7']
        hr_7 = request.form['hr_0']
        ec_8 = request.form['ec_8']
        hr_8 = request.form['hr_0']
        ec_9 = request.form['ec_9']
        hr_9 = request.form['hr_0']
        ecs = [ec_0,ec_1,ec_2,ec_3,ec_4,ec_5,ec_6,ec_7,ec_8,ec_9]
        hrs = [hr_0, hr_1, hr_2, hr_3, hr_4, hr_5, hr_6, hr_7, hr_8, hr_9]
        ecs = zip(ecs,hrs)
        bot = chancer.chancer(school,sat,gpa,ecs,[])
        ec_sent = 0
        for ec in ecs:
            sent = main.compute_sentiment(ec[0])
            ec_sent = ec_sent + sent

        sat_rating = bot.rate_sat()
        gpa_rating = bot.rate_gpa()
        ec_bonus = bot.ecs_bonus()


if __name__ == '__main__':
    app.run(debug=True)

