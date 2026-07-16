# tests/test_db.py
import os
import unittest

os.environ["TESTING"] = "true"

from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]

# Use an in-memory SQLite database for tests
test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I'm John!",
        )
        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello world, I'm Jane!",
        )
        assert second_post.id == 2

        # Get timeline posts and assert that they are correct
        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))
        assert len(posts) == 2

        # Newest first: Jane then John (Jane created after John)
        assert posts[0].id == 2
        assert posts[0].name == "Jane Doe"
        assert posts[0].email == "jane@example.com"
        assert posts[0].content == "Hello world, I'm Jane!"

        assert posts[1].id == 1
        assert posts[1].name == "John Doe"
        assert posts[1].email == "john@example.com"
        assert posts[1].content == "Hello world, I'm John!"
