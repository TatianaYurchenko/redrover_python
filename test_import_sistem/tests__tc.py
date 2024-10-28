import pytest
import requests
from faker import Faker

faker = Faker()

URL = 'http://127.0.0.1:8000/testcases/'
data = {
    "id": faker.random_number(3),
    "name": faker.text(8),
    "description": faker.sentence(6),
    "steps": [
        "string"
    ],
    "expected_result": "string",
    "priority": "низкий"
}
data2 = {
    "id": faker.random_number(4),
    "name": faker.text(8),
    "description": faker.sentence(6),
    "steps": [
        "string"
    ],
    "expected_result": "string",
    "priority": "высокий"
}
data3 = {
    "id": faker.random_number(4),
    "name": faker.lexify(text="?" * 101),
    "description": faker.sentence(6),
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

def test_create_tc_negative():
    response = requests.post(URL, json=data3)
    assert response.json()['detail'][0]['type'] == 'string_too_long'

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

def test_delete_tc():
    response = requests.delete(URL + f'{create_tc()}')
    assert response.json()['detail'] == 'Test case deleted.'
