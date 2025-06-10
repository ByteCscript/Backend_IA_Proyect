# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import insert
from fastapi import HTTPException, status
import bcrypt

from app.db.schemas_general import User, Role, enable_user_roles
from app.db.models.users_schemas import UserCreate


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(
        select(User).options(selectinload(User.roles))
    )
    return result.scalars().unique().all()


async def create_user_service(
    user_in: UserCreate,
    db: AsyncSession
) -> User:
    # 1) Verificar unicidad de email
    exists = (
        await db.execute(
            select(User).where(User.email == user_in.email)
        )
    ).scalars().first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # 2) Hashear la contraseña
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(user_in.password.encode(), salt).decode()

    # 3) Crear instancia de User
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        name=user_in.name,
    )
    db.add(new_user)
    await db.flush()  # para obtener new_user.id

    # 4) Insertar en la tabla intermedia user_roles
    mapping = [
        {"user_id": new_user.id, "role_id": rid}
        for rid in user_in.roles
    ]
    await db.execute(insert(enable_user_roles), mapping)

    # 5) Commit y recarga con roles
    await db.commit()
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == new_user.id)
    )
    return result.scalars().first()


async def delete_user_service(
    user_id: int,
    db: AsyncSession
) -> dict:
    # 1) Buscar usuario
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # 2) Eliminar y commit
    await db.delete(user)
    await db.commit()

    return {"message": f"Usuario {user.name or user.email} eliminado"}
