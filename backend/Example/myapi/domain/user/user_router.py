from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema

router = APIRouter(
    prefix="/api/user",
)

# 라우터 함수의 응답으로 response_model을 사용하는 대신 status_code=status.HTTP_204_NO_CONTENT 를 사용
@router.post("/create",status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db,user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_408_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")

    user_crud.create_user(db=db,user_create=_user_create)