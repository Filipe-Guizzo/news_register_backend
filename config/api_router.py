from ninja import NinjaAPI
from person.api import router as person
from authentication.api import router as auth, AuthBearer
from category.api import router as category
from news.api import router as news

api = NinjaAPI()

api.add_router('auth', auth)
api.add_router('persons', person)
api.add_router('categorys', category, auth=AuthBearer())
api.add_router('news', news, auth=AuthBearer())

