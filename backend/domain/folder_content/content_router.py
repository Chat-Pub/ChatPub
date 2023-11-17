
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.folder_content import content_crud, content_schema
from domain.user.user_router import get_current_user
from models import User


router = APIRouter(
    prefix="/api/folder_content",
)


@router.get("/list", response_model=content_schema.FolderContentList)
def folder_content_list(folder_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
        
        total, _folder_content_list = content_crud.get_folder_content_list(db,folder_id)
    
        return {
        'total' : total,
        'folder_content_list': _folder_content_list
    }
                        

@router.get("/detail/{folder_content_id}", response_model=content_schema.FolderContent)
def folder_content_detail(folder_content_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    folder_content = content_crud.get_folder_content(db,folder_content_id=folder_content_id)
    return folder_content

@router.post("/create", response_class=content_schema.FolderContent, status_code=status.HTTP_201_CREATED)
def folder_content_create(_folder_content_create: content_schema.FolderContentCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    # 모델 클래스 생성 후 answer 받아오기
    # 승빈님 코드
    # 필요한 데이터를 받아서 모델 클래스를 생성하고 데이터베이스에 저장한다.
    content_crud.create_folder_content(db=db,folder_content_create=_folder_content_create)

@router.put("/update",status_code=status.HTTP_204_NO_CONTENT)
def folder_content_update(_folder_content_update: content_schema.FolderContentUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_folder_content = content_crud.get_folder_content(db,folder_content_id=_folder_content_update.folder_content_id)
    if not db_folder_content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    content_crud.update_folder_content(db=db, db_folder_content=db_folder_content, folder_content_update=_folder_content_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def folder_content_delete(_folder_content_delete: content_schema.FolderContentDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_folder_content = content_crud.get_folder_content(db,folder_content_id=_folder_content_delete.folder_content_id)
    if not db_folder_content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    content_crud.delete_folder_content(db=db, db_folder_content=db_folder_content)
                    



