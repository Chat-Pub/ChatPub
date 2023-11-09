
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.userinfo import userinfo_crud, userinfo_schema
from domain.user.user_router import get_current_user
from models import User


router = APIRouter(
    prefix="/api/userinfo",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_info_create(_user_info_create: userinfo_schema.UserInfoCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user_info = userinfo_crud.get_user_info(db=db, user_id=current_user.id)
    if db_user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{current_user.username}에 대한 정보가 이미 있습니다.")
    
    userinfo_crud.create_user_info(db=db,user_info_create=_user_info_create,
                                  user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def user_info_update(_user_info_update: userinfo_schema.UserInfoUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user_info = userinfo_crud.get_user_info(db=db, user_id=current_user.id)
    if not db_user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{current_user.id}에 대한 정보가 없습니다.")
    if current_user.id != db_user_info.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    
    userinfo_crud.update_user_info(db=db, db_user_info=db_user_info, user_info_update=_user_info_update)

@router.get("/detail", response_model=userinfo_schema.UserInfo)
def user_info_detail(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user_info = userinfo_crud.get_user_info(db=db, user_id=current_user.id)
    if not db_user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{current_user.id}에 대한 정보가 없습니다.")
    if current_user.id != db_user_info.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="조회 권한이 없습니다.")
    return db_user_info


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_info_delete(_user_info_delete: userinfo_schema.UserInfoDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user_info = userinfo_crud.get_user_info(db=db, user_id=_user_info_delete.user_id)
    if not db_user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{current_user.id}에 대한 정보가 없습니다.")
    if current_user.id != db_user_info.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    userinfo_crud.delete_user_info(db=db, db_user_info=db_user_info)