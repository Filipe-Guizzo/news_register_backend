from ninja import Router, Schema, File
from ninja.files import UploadedFile
from typing import List
from .models import Person
from authentication.api import MessageSchema
import bcrypt
import jwt
from datetime import date
from authentication.api import AuthBearer

class PersonSchema(Schema):
    id: int
    name: str
    date_born: date
    sex: str
    email: str
    password: str
    token: str
    photo: str = None
    dt_create: date
    dt_update: date
    
class PersonSchemaIn(Schema):
    name: str
    date_born: str
    sex: str
    email: str
    password: str

router = Router()

@router.get('/', response={200: List[PersonSchema], 400: MessageSchema}, auth=AuthBearer())
def get_all(request):
    try:
        persons = Person.objects.all()
        return 200,persons
    except Exception as e:
        return 400, {
            'content': 'Error loading persons',
            'status': 400,
            'error': str(e)
        }
        
@router.get('/{id}/', response={200: PersonSchema, 404: MessageSchema}, auth=AuthBearer())
def get(request, id: int):
    try:
        person = Person.objects.get(id=id)
        return 200, person
    except Exception as e:
        return 404, {
            'content': 'Error not found persons',
            'status': 404,
            'error': str(e)
        }

@router.post('/', response={200: PersonSchema, 400: MessageSchema})
def create(request, paypload: PersonSchemaIn):
    try:
        json_data = paypload.dict()
        
        #password cryptography
        password = json_data['password']
        password_hashed = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt(14)).decode('utf-8')
        json_data['password'] = password_hashed
        
        #token JWT
        token = jwt.encode(json_data, password_hashed, algorithm="HS256")
        json_data['token'] = token
        
        person = Person.objects.create(**json_data)
        
        return 200, person
    except Exception as e:
        return 400, {
            'content': 'Error creating person',
            'status': 400,
            'error': str(e)
        }

@router.put('/{id}/', response={200: PersonSchema, 400: MessageSchema}, auth=AuthBearer())
def update(request, id: int, paypload: PersonSchemaIn):
    try:
        json_data = paypload.dict()
        
        #password cryptography
        password = json_data['password']
        password_hashed = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt(14)).decode('utf-8')
        json_data['password'] = password_hashed
        
        #token JWT
        token = jwt.encode(json_data, password_hashed, algorithm="HS256")
        json_data['token'] = token
        
        Person.objects.filter(id=id).update(**json_data)
        person = Person.objects.get(id=id)
        
        return 200, person
    except Exception as e:
        return 400, {
            'content': 'Error when updating person',
            'status': 400,
            'error': str(e)
        }

@router.delete('/{id}/', response={200: MessageSchema, 400: MessageSchema}, auth=AuthBearer())
def delete(request, id: int):
    try:
        Person.objects.get(id=id).delete()
        return 200,{
            'content': 'Successfully deleted person',
            'status': 400
        }
    except Exception as e:
        return 400, {
            'content': 'Error deleting person',
            'status': 400,
            'error': str(e)
        }

@router.post('/{id}/upload-file/', response={200: PersonSchema, 400: MessageSchema}, auth=AuthBearer())
def upload_file(request, id: int, file: UploadedFile = File(...)):
    try:
        person = Person.objects.get(id=id)
        person.photo = file
        person.save()
        return 200, person
    except Exception as e:
        return 400, {
            'content': 'Error saving file',
            'status': 400,
            'error': str(e)
        }