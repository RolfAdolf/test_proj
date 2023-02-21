from fastapi import FastAPI

from src.api.base_router import router


tags_dict = [
    {
        'name': 'categories',
        'description': 'Категории статей',
    },
    {
        'name': 'articles',
        'description': 'Статьи (Без реализации)',
    }
]


app = FastAPI(
    title='Моё первое приложение FastAPI',
    description='Это моё первое приложение FastAPI!',
    version='0.0.1',
    openapi_tags=tags_dict
)

app.include_router(router)
