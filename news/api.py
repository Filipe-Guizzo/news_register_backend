from ninja import Router, Schema, File
from ninja.files import UploadedFile
from typing import List
from .models import News
from authentication.api import MessageSchema
from datetime import date
from person.api import PersonSchema, Person
from category.api import CategorySchema, Category
from django.db.models import Q

class NewsSchema(Schema):
    id: int
    title: str
    subtitle: str
    content: str
    photo: str = None
    category: CategorySchema
    person: PersonSchema
    dt_create: date
    dt_update: date
    
class NewsSchemaIn(Schema):
    title: str
    subtitle: str
    content: str
    category: int
    person: int

router = Router()

@router.get('/', response={200: List[NewsSchema], 400: MessageSchema})
def get_all(request):
    try:
        news = News.objects.all()
            
        return 200, news
    except Exception as e:
        return 400, {
            'content': 'Error loading news',
            'status': 400,
            'error': str(e)
        }

@router.get('/search/', response={200: List[NewsSchema], 404: MessageSchema})
def search(request):
    try:
        query = request.GET
        
        title = query.get('title', 'null')
        subtitle = query.get('subtitle', 'null')
        content = query.get('content', 'null')
        category = query.get('category', 'null')
        person = query.get('person', 'null')
        dt_create = query.get('dt_create', '1980-01-01')
        dt_update = query.get('dt_update', '1980-01-01')
        
        news = News.objects.filter(
            Q(title__istartswith=title) |
            Q(subtitle__istartswith=subtitle) |
            Q(content__icontains=content) |
            Q(category__name__istartswith=category)  |
            Q(person__name__istartswith=person) |
            Q(dt_create=dt_create) |
            Q(dt_update=dt_update)
        )
        return 200, news
    except Exception as e:
        return 404, {
            'content': 'Error not found news',
            'status': 404,
            'error': str(e)
        }

@router.get('/{id}/', response={200: NewsSchema, 404: MessageSchema})
def get(request, id: int):
    try:
        news = News.objects.get(id=id)
        return 200, news
    except Exception as e:
        return 404, {
            'content': 'Error not found news',
            'status': 404,
            'error': str(e)
        }

@router.post('/', response={200: NewsSchema, 400: MessageSchema})
def create(request, paypload: NewsSchemaIn):
    try:
        json_data = paypload.dict()
        id_person = json_data['person']
        person = Person.objects.get(id=id_person)
        json_data['person'] = person
        id_category = json_data['category']
        category = Category.objects.get(id=id_category)
        json_data['category'] = category
        
        news = News.objects.create(**json_data)
        
        return 200, news
    except Exception as e:
        return 400, {
            'content': 'Error creating news',
            'status': 400,
            'error': str(e)
        }

@router.put('/{id}/', response={200: NewsSchema, 400: MessageSchema})
def update(request, id: int, paypload: NewsSchemaIn):
    try:
        json_data = paypload.dict()
        id_person = json_data['person']
        person = Person.objects.get(id=id_person)
        json_data['person'] = person
        id_category = json_data['category']
        category = Category.objects.get(id=id_category)
        json_data['category'] = category
        
        News.objects.filter(id=id).update(**json_data)
        news = News.objects.get(id=id)
        
        return 200, news
    except Exception as e:
        return 400, {
            'content': 'Error when updating news',
            'status': 400,
            'error': str(e)
        }

@router.delete('/{id}/', response={200: MessageSchema, 400: MessageSchema})
def delete(request, id: int):
    try:
        News.objects.get(id=id).delete()
        return 200,{
            'content': 'Successfully deleted news',
            'status': 400
        }
    except Exception as e:
        return 400, {
            'content': 'Error deleting news',
            'status': 400,
            'error': str(e)
        }

@router.post('/{id}/upload-file', response={200: NewsSchema, 400: MessageSchema})
def upload_file(request, id: int, file: UploadedFile = File(...)):
    try:
        news = News.objects.get(id=id)
        news.photo = file
        news.save()
        return 200, news
    except Exception as e:
        return 400, {
            'content': 'Error saving file',
            'status': 400,
            'error': str(e)
        }