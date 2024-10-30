import pytest
import requests
from faker import Faker
from pydantic import BaseModel, Field
from enum import Enum

faker = Faker()

URL = 'http://127.0.0.1:8000/testcases/'

class Priority(str, Enum):
    low = "низкий"
    medium = "средний"
    high = "высокий"


class Data_case(BaseModel):
    id: int = Field(default=faker.random_number(4), ge=0, le=120)
    name: str = Field(default=faker.text(8))
    description: str = Field(default=faker.sentence(6))
    steps: list[str] = Field(default=[faker.text(8)])
    expected_result: str = Field(default=faker.sentence(6))
    priority: Priority = Field(default=Priority.medium)

data = Data_case().model_dump()
def create_tc():
    response = requests.post(URL, json=data)
    id = response.json()['id']
    return id

def test_create_tc():
    response = requests.get(URL+f'{create_tc()}')
    assert data['id'] == response.json()['id'] and data["name"] == response.json()["name"]

def test_create_tc_negative():
    name = faker.lexify(text="?" * 101)
    response = requests.post(URL, json=Data_case(name=name).model_dump())
    assert response.json()['detail'][0]['type'] == 'string_too_long'

def test_create_tc_negative_description():
    description = faker.lexify(text="?" * 1001)
    response = requests.post(URL, json=Data_case(description=description).model_dump())
    assert response.json()['detail'][0]['type'] == 'string_too_long'


def test_get_tc():
    create_tc()
    response = requests.get(URL)
    assert response.status_code == 200

def test_get_tc_by_id():
    response = requests.get(URL+f'{create_tc()}')
    assert response.status_code == 200

def test_update_tc():
    data2 = Data_case().model_dump()
    response = requests.put(URL+f'{create_tc()}', json=data2)
    assert data2['id'] == response.json()['id'] and data2["name"] == response.json()["name"]

def test_delete_tc():
    response = requests.delete(URL + f'{create_tc()}')
    assert response.json()['detail'] == 'Test case deleted.'
