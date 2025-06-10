from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.users_schemas import UserCreate, UserOut
from app.services.user_service import (
    get_all_users,
    create_user_service,
    delete_user_service,
)
from app.services.auth_service import login_service
from app.db.auth import Login, Token

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserOut],
    summary="Listar usuarios con roles",
)
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)



@router.post(
    "/crear-usuarios",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario y asignar roles por ID",
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_user_service(user_in, db)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario por ID",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_user_service(user_id, db)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión y obtener token",
)
async def login(
    credentials: Login,
    db: AsyncSession = Depends(get_db),
):
    """
    Verifica email+password, y devuelve un JWT válido por 60 minutos.
    """
    token = await login_service(credentials, db)
    return {"access_token": token}