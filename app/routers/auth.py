from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.db import get_session
from app.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/api/v1", tags=["auth"])

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    token = create_access_token(sub=user.usuario, user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}

