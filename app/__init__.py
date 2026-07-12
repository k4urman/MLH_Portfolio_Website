import os
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
from flask import Flask, render_template, request
from dotenv import load_dotenv

from app.portfolio_data import ABOUT_TEXT, CONTACT, EDUCATION, HOBBIES, WORK_EXPERIENCES

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                     user=os.getenv("MYSQL_USER"),
                     password=os.getenv("MYSQL_PASSWORD"),
                     host=os.getenv("MYSQL_HOST"),
                     port=3306)

print(mydb)

class TimelinePost(Model):
        name = CharField()
        email = CharField()
        content = TextField()
        created_at = DateTimeField(default=datetime.datetime.now)

        class Meta:
                database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

#create POST /api/timeline_post
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)

        return model_to_dict(timeline_post)

#create GET /api/timeline_post
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
        return{
                'timeline_posts': [
                        model_to_dict(p)
                        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
                ]
        }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)
    if post is None:
        return {'error': 'Timeline post not found'}, 404

    post.delete_instance()
    return {'deleted': post_id}

# create Timeline Post Page
@app.route('/timeline')
def timeline():
        return render_template('timeline.html',title="Timeline")

# adds nav links to every template
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
    ],
    url=os.getenv("URL") # reads from .env — will be localhost:5000 locally,
                         # real domain in production when MLH deploys in future weeks
    )

@app.route('/')
def index():
        return render_template(
                'index.html',
                title="Maninder (Kaurman) Kaur",
                url=os.getenv("URL"),
                about_text=ABOUT_TEXT,
                contact=CONTACT,
                work_experiences=WORK_EXPERIENCES,
                education=EDUCATION,
        )

@app.route('/hobbies')
def hobbies():
        return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)

@app.route('/travel')
def travel():
        return render_template('travel.html', title="Travel Map")
