from django.test import TestCase, Client
import sqlite3
import json

connection = sqlite3.connect("db.sqlite3")


class PartViewTests(TestCase):
    def test_update_part(self):
        c = Client()
        data = json.dumps({"is_active": "1"})
        response = c.put("/part/2", data, HTTP_ACCEPT="application/json")
        assert response.status_code == 200
        assert response.json()["data"]["is_active"] == 1
