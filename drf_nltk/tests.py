from django.test import TestCase, RequestFactory
import sqlite3
import json
from drf_nltk import views
from mock import Mock

connection = sqlite3.connect("db.sqlite3")


class NlktViewDRFTests(TestCase):
    def test_nltk_rest_list(self):
        request = RequestFactory().get('/nltk/')
        request.METHOD = 'GET'
        text_common_words = "The 3 words most commons are: 'ramiro, aquino, romero'."
        views.get_common_word = Mock(return_value=text_common_words)
        response = views.part_common_word_list(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert len(data["data"]) > 0
        assert text_common_words in data["data"][0]["description"]
        assert data["status"]
