import os
import markdown
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# context_processor injects variables into EVERY template automatically.
@app.context_processor
def inject_nav():
    return dict(nav_pages=[
        {"label": "Home", "endpoint": "index"},
        # "index" matches the function name below: def index()
        # If we add blueprints later, this becomes "main.index" (blueprint_name.function_name)
        {"label": "Experience", "endpoint": "work"},
        {"label": "Hobbies", "endpoint": "hobbies"},
        {"label": "Travel", "endpoint": "travel"},
    ])

# @app.route() maps a URL path to a Python function — equivalent to app.get() in Express.
# The function name becomes the "endpoint" name used in url_for() and context_processor above.
@app.route('/')
def index():
    # render_template() finds the file in templates/, runs Jinja substitution,
    # returns HTML. Keyword args become variables available in the template.
    # os.getenv("URL") reads from .env via python-dotenv
    about_path = os.path.join(app.root_path, 'Markdown', 'about.md')
    with open(about_path, encoding='utf-8') as about_file:
        about_markdown = about_file.read()
    about_html = markdown.markdown(about_markdown, extensions=['extra', 'sane_lists'])
    return render_template('index.html', title="Amandaleeanne Schock", url=os.getenv("URL"), about_html=about_html)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies")

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel Map")


@app.route('/experience')
def work():
    return render_template('work.html', title="Experience")