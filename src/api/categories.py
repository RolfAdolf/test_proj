from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.category.category_request import CategoryRequest
from src.models.schemas.category.category_response import CategoryResponse
from src.services.categories import CategoriesService
from src.services.users import get_current_user_id

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.get('/all', response_model=List[CategoryResponse], name="Получить все категории")
def get(categories_service: CategoriesService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить все категории. Более подробное описание.
    """
    print(user_id)
    return categories_service.all()


@router.get('/get/{category_id}', response_model=CategoryResponse, name="Получить одну категорию")
def get(category_id: int, categories_service: CategoriesService = Depends()):
    return get_with_check(category_id, categories_service)


def get_with_check(category_id: int, categories_service: CategoriesService):
    result = categories_service.get(category_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(category_schema: CategoryRequest, categories_service: CategoriesService = Depends()):
    return categories_service.add(category_schema)


@router.put('/{category_id}', response_model=CategoryResponse, name="Обновить информацию о категории")
def put(category_id: int, category_schema: CategoryRequest, categories_service: CategoriesService = Depends()):
    get_with_check(category_id, categories_service)
    return categories_service.update(category_id, category_schema)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(category_id: int, categories_service: CategoriesService = Depends()):
    get_with_check(category_id, categories_service)
    return categories_service.delete(category_id)