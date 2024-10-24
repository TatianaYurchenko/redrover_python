from pydantic import BaseModel
from faker import Faker

faker = Faker()


user_dict = {"name": faker.name(), "age": faker.random_number(3)}

class User(BaseModel):
    name: str
    age: int

print(User(**user_dict).model_dump())
a = faker.text(8)
print(a)