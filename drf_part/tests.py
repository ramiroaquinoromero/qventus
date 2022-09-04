from django.test import TestCase, Client, RequestFactory
import sqlite3
import json
from drf_part import views

connection = sqlite3.connect("db.sqlite3")


class PartViewDRFTests(TestCase):
    def test_part_rest_list(self):
        request = RequestFactory().get('/part/')
        request.METHOD = 'GET'
        response = views.part_rest_list(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert len(data["data"]) > 0
        assert data["status"]

        c = Client()
        response = c.get("/part/", {}, HTTP_ACCEPT="application/json")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    def test_part_rest_list_get_by_id(self):
        request = RequestFactory().get('/part/?id=1')
        request.METHOD = 'GET'
        response = views.part_rest_list(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert len(data["data"]) > 0
        assert data["status"]

        c = Client()
        response = c.get("/part/?id=1", {}, HTTP_ACCEPT="application/json")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    def test_part_rest_list_post(self):
        data = json.dumps({"name": "Chip 1",
                           "sku": "OWDD823011DJAD",
                           "description": "Test Insert",
                           "weight_ounces": 30,
                           "is_active": "0"})
        request = RequestFactory().post('/part/', data, content_type='application/json')
        request.METHOD = 'POST'
        response = views.part_rest_list(request)
        data = json.loads(response.content)
        assert response.status_code == 201
        assert len(data["data"]) > 0
        assert data["status"]

        c_post = Client()
        data_post = {"name": "Chip 1", "sku": "OWDD823011DJAD", "description": "Test Insert", "weight_ounces": 30, "is_active": "0"}
        response_post = c_post.post("/part/", json.dumps(data_post), format='json', content_type='application/json')
        assert response_post.status_code == 201
        assert len(response_post.json()["data"]) > 0

    def test_part_rest_list_put(self):
        data = json.dumps({"id": 1, "is_active": "0"})
        request = RequestFactory().put('/part/', data, content_type='application/json')
        request.METHOD = 'PUT'
        response = views.part_rest_list(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert len(data["data"]) > 0
        assert data["status"]

        c_put = Client()
        data_put = {"id": 1, "is_active": "0"}
        response_post = c_put.put("/part/", json.dumps(data_put), format='json', content_type='application/json')
        assert response_post.status_code == 200
        assert len(response_post.json()["data"]) > 0

    def test_part_rest_list_delete(self):
        data = json.dumps({"id": 1})
        request = RequestFactory().delete('/part/', data, content_type='application/json')
        request.METHOD = 'PUT'
        response = views.part_rest_list(request)
        data = json.loads(response.content)
        assert response.status_code == 200
        assert len(data["data"]) == 0
        assert data["status"]

        c_delete = Client()
        data_delete = {"id": 2}
        response_delete = c_delete.delete("/part/", json.dumps(data_delete), format='json', content_type='application/json')
        assert response_delete.status_code == 200
        assert len(response_delete.json()["data"]) == 0
