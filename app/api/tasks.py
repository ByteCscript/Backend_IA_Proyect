from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
import pandas as pd

from app.db.session import get_db
from app.db.schemas_general import Task  # o la tabla metadata si prefieres
from app.db.schemas_general import (
    enable_user_roles,        # la tabla role_tasks
    user_task_logs_table,
    role_tasks_table, Productivity, Sale, Report    # la tabla user_task_logs
) # si usas Table(...) importa la metadata
# o: from app.db.models import tasks_table

router = APIRouter()

@router.post(
    "/tasks",
    summary="Cargar CSV de tareas",
    status_code=status.HTTP_201_CREATED,
)
async def upload_tasks(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Sólo se admiten archivos CSV")

    # 1) Leer CSV en DataFrame
    df = pd.read_csv(file.file)
    required = {"id", "name", "description"}
    if not required.issubset(df.columns):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Columnas requeridas: {', '.join(required)}"
        )

    # 2) Preparar INSERT
    records = df.to_dict(orient="records")
    # Si usas ORM:
    tasks = [Task(**r) for r in records]
    db.add_all(tasks)

    # Si usar Table + insert:
    # await db.execute(insert(tasks_table), records)

    # 3) Commit
    await db.commit()
    return {"inserted": len(records)}


@router.post(
    "/role-tasks",
    summary="Cargar CSV de roles-tareas",
    status_code=status.HTTP_201_CREATED,
)
async def upload_role_tasks(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Sólo se admiten archivos CSV")

    df = pd.read_csv(file.file)
    required = {"role_id", "task_id"}
    if not required.issubset(df.columns):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Columnas requeridas: {', '.join(required)}"
        )

    # Convertir cada fila en un dict con ambas claves
    records = df[["role_id", "task_id"]].to_dict(orient="records")

    # Bulk-insert en role_tasks_table, no en user_roles
    await db.execute(insert(role_tasks_table), records)
    await db.commit()
    return {"inserted": len(records)}


@router.post(
    "/task-logs",
    summary="Cargar CSV de logs de tareas",
    status_code=status.HTTP_201_CREATED,
)
async def upload_task_logs(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Sólo se admiten archivos CSV")

    # 1) Leer CSV
    df = pd.read_csv(file.file)

    # 2) Validar columnas
    required = {"user_id", "task_id", "date", "quantity"}
    if not required.issubset(df.columns):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Columnas requeridas: {', '.join(required)}"
        )

    # 3) Convertir la columna date a datetime.date
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # 4) Preparar registros
    records = df.to_dict(orient="records")

    # 5) Bulk insert usando la tabla correcta
    await db.execute(insert(user_task_logs_table), records)
    await db.commit()
    return {"inserted": len(records)}


@router.post("/productivity", status_code=status.HTTP_201_CREATED)
async def upload_productivity(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Sólo CSV")
    df = pd.read_csv(file.file)
    if not {"user_id","date","value"}.issubset(df.columns):
        raise HTTPException(422, "Columnas requeridas: user_id, date, value")
    df["date"] = pd.to_datetime(df["date"]).dt.date
    records = [Productivity(**r) for r in df.to_dict(orient="records")]
    db.add_all(records)
    await db.commit()
    return {"inserted": len(records)}

@router.post("/sales", status_code=status.HTTP_201_CREATED)
async def upload_sales(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Sólo CSV")
    df = pd.read_csv(file.file)
    if not {"user_id","date","amount"}.issubset(df.columns):
        raise HTTPException(422, "Columnas requeridas: user_id, date, amount")
    df["date"] = pd.to_datetime(df["date"]).dt.date
    records = [Sale(**r) for r in df.to_dict(orient="records")]
    db.add_all(records)
    await db.commit()
    return {"inserted": len(records)}

@router.post("/reports", status_code=status.HTTP_201_CREATED)
async def upload_reports(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Sólo CSV")
    df = pd.read_csv(file.file)
    if not {"user_id","created_at","type"}.issubset(df.columns):
        raise HTTPException(422, "Columnas requeridas: user_id, created_at, type")
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    records = [Report(**r) for r in df.to_dict(orient="records")]
    db.add_all(records)
    await db.commit()
    return {"inserted": len(records)}