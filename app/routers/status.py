import time
from typing import Dict
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine, DATABASE_URL

router = APIRouter(prefix="/api/v1", tags=["status"])

def check_db() -> Dict[str, object]:
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        connected = True
    except SQLAlchemyError:
        connected = False
    driver = DATABASE_URL.split(":", 1)[0]
    return {"connected": connected, "driver": driver}

@router.get("/api-status")
def api_status():
    db = check_db()
    status = "ok" if db["connected"] else "error"
    return {
        "status": status,
        "database": db,
        "timestamp": int(time.time()),
    }
