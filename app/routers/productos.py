from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, select
from sqlalchemy import func
from app.db import get_session
from app.auth import get_current_user
from app.models import Producto, ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter(prefix="/api/v1/productos", tags=["productos"], dependencies=[Depends(get_current_user)])

def apply_filters(query, q: Optional[str], min_price: Optional[float], max_price: Optional[float]):
    if q:
        query = query.where((Producto.nombre.contains(q)) | (Producto.descripcion.contains(q)))
    if min_price is not None:
        query = query.where(Producto.precio >= min_price)
    if max_price is not None:
        query = query.where(Producto.precio <= max_price)
    return query

def get_sort_attr(sort_by: str):
    allowed = {"id", "nombre", "precio", "fecha_creacion", "fecha_actualizacion"}
    if sort_by not in allowed:
        sort_by = "id"
    return getattr(Producto, sort_by)

@router.get("/", response_model=List[ProductoRead])
def list_productos(
    response: Response,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "nombre",
    sort_order: str = "asc",
):
    base = select(Producto)
    base = apply_filters(base, q, min_price, max_price)
    total_query = select(func.count(Producto.id))
    total_query = apply_filters(total_query, q, min_price, max_price)
    total = session.exec(total_query).one()
    response.headers["X-Total-Count"] = str(total)
    sort_attr = get_sort_attr(sort_by)
    if sort_order == "desc":
        base = base.order_by(sort_attr.desc())
    else:
        base = base.order_by(sort_attr.asc())
    items = session.exec(base.offset((page - 1) * size).limit(size)).all()
    return items

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(response: Response, data: ProductoCreate, session: Session = Depends(get_session)):
    item = Producto(**data.dict())
    session.add(item)
    session.commit()
    session.refresh(item)
    response.headers["Location"] = f"/api/v1/productos/{item.id}"
    return item

@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, session: Session = Depends(get_session)):
    item = session.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    return item

@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)):
    item = session.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(item, k, v)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    item = session.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    session.delete(item)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
