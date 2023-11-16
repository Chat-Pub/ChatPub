
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.folder import folder_crud, folder_schema
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    #prefix 속성은 요청 URL에 항상 포함되어야 하는 값이다.
    prefix="/api/folder",
)

@router.get("/list", response_model=folder_schema.FolderList)
def folder_list(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    
    total, _folder_list = folder_crud.get_folder_list(db,current_user.id)

    return {
        'total' : total,
        'folder_list': _folder_list
    }



@router.get("/detail/{folder_id}", response_model=folder_schema.Folder)
def folder_detail(folder_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    folder = folder_crud.get_folder(db,folder_id=folder_id)
    return folder

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def folder_create(_folder_create: folder_schema.FolderCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    folder_crud.create_folder(db=db,folder_create=_folder_create,
                                  user=current_user)

@router.put("/update/{folder_id}",status_code=status.HTTP_204_NO_CONTENT)
def folder_update(_folder_update: folder_schema.FolderUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_folder = folder_crud.get_folder(db,folder_id=_folder_update.folder_id)
    if not db_folder:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    if current_user.id != db_folder.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    
    folder_crud.update_folder(db=db, db_folder=db_folder, folder_update=_folder_update)

@router.delete("/delete/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def folder_delete(_folder_delete: folder_schema.FolderDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_folder = folder_crud.get_folder(db,folder_id=_folder_delete.folder_id)
    if not db_folder:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    if current_user.id != db_folder.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    
    folder_crud.delete_folder(db=db, db_folder=db_folder)