# tests/test_app.py
import os
import unittest

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Maninder (Kaurman) Kaur</title>" in html
        # More home page checks
        assert "About" in html or "about" in html.lower()
        assert "Experience" in html or "Work" in html or "Education" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        assert "timeline_posts" in response.get_json()
        assert len(response.get_json()["timeline_posts"]) == 0

        # POST a timeline post
        post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        assert post_response.status_code == 200
        assert post_response.is_json
        created = post_response.get_json()
        assert created["name"] == "John Doe"
        assert created["email"] == "john@example.com"
        assert created["content"] == "Hello world, I'm John!"

        # GET should now include the post
        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        posts = get_response.get_json()["timeline_posts"]
        assert len(posts) == 1
        assert posts[0]["name"] == "John Doe"

        # Timeline page should load
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        page_html = page_response.get_data(as_text=True)
        assert "Timeline" in page_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
