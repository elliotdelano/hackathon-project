from flask import Flask , render_template, session, request, jsonify, redirect, url_for
from sentiment import main, json_reader
from sentiment.sentiment_score import clean_text, calculate_sentiment_score
from sentiment.reddit_scraper.reddit_scraper.spiders.reddit_post_scraper import RedditPostCrawler
from algo import chancer
from celery import Celery
import os
from scrapy.crawler import CrawlerProcess
import pandas as pd
import logging
import nltk


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def compute_sentiment(self,term):
    # Initial setup: Disable scrapy logs and download NLTK files
    logging.getLogger('scrapy').propagate = False
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)

    # Ask for user query
    # subreddit = input('Subreddit: ')
    subreddit = 'chanceme'
    # term = input('Search term: ')
    term = term.replace(' ', '+')

    # Start crawler process
    print('[LOG] Crawling Reddit, this will take a little time...')
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'jl',
        'FEED_URI': 'data_{}.jl'.format(term)
    })
    process.crawl(RedditPostCrawler,
                  domain=f'https://old.reddit.com/r/{subreddit}/search?q={term}&restrict_sr=on&sort=relevance&t=all')
    process.start()

    # Convert data file to class
    print('[LOG] Creating DataFrame table...')
    reddit_posts = json_reader.convert_json('data_{}.jl'.format(term))
    all_comments = []
    all_upvotes = []
    for post in reddit_posts:
        for comment in post.comments:
            all_comments.append(clean_text(comment.text))

            # Convert upvote text to float, e.g. '15.3k upvotes' -> 15300
            upvote = comment.upvotes.split(' ')[0]
            if 'k' in upvote:
                upvote = upvote[:-1]
                upvote = float(upvote) * 1000
            all_upvotes.append(float(upvote))

    df = pd.DataFrame({'comment': all_comments, 'upvotes': all_upvotes})
    df = df[df.upvotes >= 1]

    print('[LOG] Calculating sentiment score, this may take a longer time...')
    df = calculate_sentiment_score(df)

    # df.to_csv('results.csv')
    normalized_result = df.sentiment.mean()

    print('[LOG] Completed!\n')
    print('Average sentiment:', normalized_result)
    print('where +1 is most positive and -1 is most negative')

    os.remove('data_{}.jl'.format(term))
    sent = normalized_result
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': sent}

@app.route('/status/<task_id>')
def status(task_id):
    task = compute_sentiment.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chanceme',methods=["GET","POST"])
def chanceme():
    if request.method == "POST":
        sat = request.json['sat']
        gpa = request.json['gpa']
        ec_0 = request.json['ec_0']
        hr_0 = request.json['hr_0']
        ec_1 = request.json['ec_1']
        hr_1 = request.json['hr_1']
        ec_2 = request.json['ec_2']
        hr_2 = request.json['hr_2']
        ec_3 = request.json['ec_3']
        hr_3 = request.json['hr_3']
        ec_4 = request.json['ec_4']
        hr_4 = request.json['hr_4']
        ec_5 = request.json['ec_5']
        hr_5 = request.json['hr_5']
        ec_6 = request.json['ec_6']
        hr_6 = request.json['hr_6']
        ec_7 = request.json['ec_7']
        hr_7 = request.json['hr_7']
        ec_8 = request.json['ec_8']
        hr_8 = request.json['hr_8']
        ec_9 = request.json['ec_9']
        hr_9 = request.json['hr_9']
        school = request.json['school']
        ecs = [ec_0,ec_1,ec_2,ec_3,ec_4,ec_5,ec_6,ec_7,ec_8,ec_9]
        print(ecs)
        hrs = [hr_0, hr_1, hr_2, hr_3, hr_4, hr_5, hr_6, hr_7, hr_8, hr_9]
        ecs = zip(ecs,hrs)
        ids = []
        for ec in ecs:
            if ec[0] != "":
                task = compute_sentiment.apply_async([ec[0]])
                ids.append(url_for('status',task_id=task.id))

        bot = chancer.chancer(school, sat, gpa, ecs)
        sat_rating = bot.rate_sat()
        gpa_rating = bot.rate_gpa()
        ec_bonus = bot.ecs_bonus()
        acceptance_rate = bot.get_acceptance()
        goat_rating = bot.goat_status()

        return jsonify({"ids":ids,"sat_rating":sat_rating,"gpa_rating":gpa_rating,"ec_bonus":ec_bonus,"acceptance_rate":acceptance_rate,"goat_rating":goat_rating})


@app.route('/results',methods = ["GET","POST"])
def results():
    if request.method == "POST":
        ecs_sent = sum(request.json['sents'])
        profile = chancer.profile(request.json['acceptance_rate'], request.json['sat_rating'], request.json['gpa_rating'], ecs_sent, request.json['ecs_bonus'], request.json['goat_rating'])
        return render_template('results.html',res=profile.chance())


if __name__ == '__main__':
    app.run(debug=True)

