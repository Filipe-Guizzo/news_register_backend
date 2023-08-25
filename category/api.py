from ninja import Router, Schema
from typing import List
from .models import Category
from authentication.api import MessageSchema
from datetime import date
from person.api import PersonSchema, Person

class CategorySchema(Schema):
    id: int
    name: str
    person: PersonSchema
    dt_create: date
    dt_update: date
    
class CategorySchemaIn(Schema):
    name: str
    person: int

router = Router()

@router.get('/', response={200: List[CategorySchema], 400: MessageSchema})
def get_all(request):
    try:
        categorys = Category.objects.all().order_by('id')
            
        return 200, categorys
    except Exception as e:
        return 400, {
            'content': 'Error loading categorys',
            'status': 400,
            'error': str(e)
        }

@router.get('/{id}/', response={200: CategorySchema, 404: MessageSchema})
def get(request, id: int):
    try:
        category = Category.objects.get(id=id)
        return 200, category
    except Exception as e:
        return 404, {
            'content': 'Error not found categorys',
            'status': 404,
            'error': str(e)
        }

@router.post('/', response={200: CategorySchema, 400: MessageSchema})
def create(request, paypload: CategorySchemaIn):
    try:
        json_data = paypload.dict()
        id_person = json_data['person']
        person = Person.objects.get(id=id_person)
        json_data['person'] = person
        
        category = Category.objects.create(**json_data)
        
        return 200, category
    except Exception as e:
        return 400, {
            'content': 'Error creating category',
            'status': 400,
            'error': str(e)
        }

@router.put('/{id}/', response={200: CategorySchema, 400: MessageSchema})
def update(request, id: int, paypload: CategorySchemaIn):
    try:
        json_data = paypload.dict()
        id_person = json_data['person']
        person = Person.objects.get(id=id_person)
        json_data['person'] = person
        
        Category.objects.filter(id=id).update(**json_data)
        category = Category.objects.get(id=id)
        
        return 200, category
    except Exception as e:
        return 400, {
            'content': 'Error when updating category',
            'status': 400,
            'error': str(e)
        }

@router.delete('/{id}/', response={200: MessageSchema, 400: MessageSchema})
def delete(request, id: int):
    try:
        Category.objects.get(id=id).delete()
        return 200,{
            'content': 'Successfully deleted category',
            'status': 400
        }
    except Exception as e:
        return 400, {
            'content': 'Error deleting category',
            'status': 400,
            'error': str(e)
        }
