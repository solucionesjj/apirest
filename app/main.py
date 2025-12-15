import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from app.db import init_db
from app.middleware import RequestLoggerMiddleware
from app.routers.productos import router as productos_router
from app.routers.usuarios import router as usuarios_router
from app.routers.status import router as status_router
from app.routers.auth import router as auth_router
from sqlmodel import Session, select
from app.db import engine
from app.models import Usuario
from app.security import hash_password

app = FastAPI()

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(RequestLoggerMiddleware)

app.include_router(productos_router)
app.include_router(usuarios_router)
app.include_router(status_router)
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    init_db()
    app.state.start_time = time.time()
    # Bootstrap admin user if none exists and env variables provided
    default_user = os.getenv("DEFAULT_ADMIN_USER")
    default_pass = os.getenv("DEFAULT_ADMIN_PASSWORD")
    if default_user and default_pass:
        with Session(engine) as session:
            count = session.exec(select(Usuario)).first()
            print("cantidad usuarios")
            print(count)
            print("cantidad usuarios")
            if not count:
                admin = Usuario(
                    usuario=default_user,
                    nombre="Administrador",
                    clave_hash=hash_password(default_pass),
                    perfil="admin",
                )
                session.add(admin)
                session.commit()
