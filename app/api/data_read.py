from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.schemas_general import Productivity, Sale, Report
from app.db.models.data_schemas import ProductivityOut, SaleOut, ReportOut

router = APIRouter(prefix="/data", tags=["data"])

@router.get(
    "/productivity",
    response_model=list[ProductivityOut],
    summary="Listar métricas de productividad",
)
async def get_productivity(db: AsyncSession = Depends(get_db)):
    """ Devuelve todas las filas de la tabla productivity. """
    res = await db.execute(select(Productivity))
    return res.scalars().all()

@router.get(
    "/sales",
    response_model=list[SaleOut],
    summary="Listar registros de ventas",
)
async def get_sales(db: AsyncSession = Depends(get_db)):
    """ Devuelve todas las filas de la tabla sales. """
    res = await db.execute(select(Sale))
    return res.scalars().all()

@router.get(
    "/reports",
    response_model=list[ReportOut],
    summary="Listar historial de reportes",
)
async def get_reports(db: AsyncSession = Depends(get_db)):
    """ Devuelve todas las filas de la tabla reports. """
    res = await db.execute(select(Report))
    return res.scalars().all()
