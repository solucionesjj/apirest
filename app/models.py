from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    precio: float = Field(index=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

class ProductoCreate(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float

class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    fecha_creacion: datetime
    fecha_actualizacion: datetime

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: str = Field(sa_column=Column(String(255), unique=True, index=True))
    nombre: str
    clave_hash: str
    perfil: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

class UsuarioCreate(SQLModel):
    usuario: str
    nombre: str
    clave: str
    perfil: Optional[str] = None

class UsuarioRead(SQLModel):
    id: int
    usuario: str
    nombre: str
    perfil: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

class UsuarioUpdate(SQLModel):
    usuario: Optional[str] = None
    nombre: Optional[str] = None
    clave: Optional[str] = None
    perfil: Optional[str] = None
