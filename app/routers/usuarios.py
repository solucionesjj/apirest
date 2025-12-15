from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, select
from sqlalchemy import func
from app.db import get_session
from app.auth import get_current_user
from app.models import Usuario, UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.security import hash_password

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"], dependencies=[Depends(get_current_user)])

def apply_filters(query, q: Optional[str], perfil: Optional[str]):
    if q:
        query = query.where((Usuario.usuario.contains(q)) | (Usuario.nombre.contains(q)))
    if perfil:
        query = query.where(Usuario.perfil == perfil)
    return query

def get_sort_attr(sort_by: str):
    allowed = {"id", "usuario", "nombre", "perfil", "fecha_creacion", "fecha_actualizacion"}
    if sort_by not in allowed:
        sort_by = "id"
    return getattr(Usuario, sort_by)

@router.get("/", response_model=List[UsuarioRead])
def list_usuarios(
    response: Response,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    q: Optional[str] = None,
    perfil: Optional[str] = None,
    sort_by: str = "usuario",
    sort_order: str = "asc",
):
    base = select(Usuario)
    base = apply_filters(base, q, perfil)
    total_query = select(func.count(Usuario.id))
    total_query = apply_filters(total_query, q, perfil)
    total = session.exec(total_query).one()
    response.headers["X-Total-Count"] = str(total)
    sort_attr = get_sort_attr(sort_by)
    if sort_order == "desc":
        base = base.order_by(sort_attr.desc())
    else:
        base = base.order_by(sort_attr.asc())
    items = session.exec(base.offset((page - 1) * size).limit(size)).all()
    return items

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(response: Response, data: UsuarioCreate, session: Session = Depends(get_session)):
    exists = session.exec(select(Usuario).where(Usuario.usuario == data.usuario)).first()
    if exists:
        raise HTTPException(status_code=409, detail="Conflict: usuario duplicado")
    item = Usuario(
        usuario=data.usuario,
        nombre=data.nombre,
        clave_hash=hash_password(data.clave),
        perfil=data.perfil,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    response.headers["Location"] = f"/api/v1/usuarios/{item.id}"
    return item

@router.get("/{usuario_id}", response_model=UsuarioRead)
def get_usuario(usuario_id: int, session: Session = Depends(get_session)):
    item = session.get(Usuario, usuario_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    return item

@router.put("/{usuario_id}", response_model=UsuarioRead)
def update_usuario(usuario_id: int, data: UsuarioUpdate, session: Session = Depends(get_session)):
    item = session.get(Usuario, usuario_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    payload = data.dict(exclude_unset=True)
    if "clave" in payload and payload["clave"]:
        item.clave_hash = hash_password(payload.pop("clave"))
    for k, v in payload.items():
        setattr(item, k, v)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, session: Session = Depends(get_session)):
    item = session.get(Usuario, usuario_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not Found")
    session.delete(item)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
