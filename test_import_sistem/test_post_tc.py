import pytest
from lesson1.smart_validation import User
import requests
from pprint import pprint
URL = 'http://127.0.0.1:8000/testcases/'
data = {
    "id": 0,
    "name": "test1",
    "description": "Проверить ответ от сервера",
    "steps": [
        "string"
    ],
    "expected_result": "string",
    "priority": "низкий"
}
data2 = {
    "id": 6,
    "name": "test2",
    "description": "проверить объект в формате JSON с запрошенными полями",
    "steps": [
        "string"
    ],
    "expected_result": "string",
    "priority": "высокий"
}
def create_tc():
    response = requests.post(URL, json=data)
    id = response.json()['id']
    return id
def test_create_tc():
    response = requests.get(URL+f'{create_tc()}')
    assert data['id'] == response.json()['id'] and data["name"] == response.json()["name"]
def test_get_tc():
    create_tc()
    response = requests.get(URL)
    assert response.status_code == 200

def test_get_tc_by_id():
    response = requests.get(URL+f'{create_tc()}')
    assert response.status_code == 200

def test_update_tc():
    response = requests.put(URL+f'{create_tc()}', json=data2)
    assert data2['id'] == response.json()['id'] and data2["name"] == response.json()["name"]
