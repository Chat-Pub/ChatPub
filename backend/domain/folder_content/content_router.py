
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from domain.folder_content import content_crud, content_schema
from domain.user.user_router import get_current_user
from domain.userinfo.userinfo_crud import get_user_info
from models import User
from domain.model_util import chatbot_class

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

@router.post("/create", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
def folder_content_create(_folder_content_create: content_schema.FolderContentCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    
    user_info = get_user_info(db=db,user_id=current_user.id)
    if (user_info == None):
         user_info = ""

    # 모델 클래스 생성 후 answer 받아오기
    chatbot = chatbot_class.ChatBot() # 모델 클래스 생성, 모델 path 입력
    model_answer = chatbot.forward(user_info,_folder_content_create.question)
    
    # 필요한 데이터를 받아서 모델 클래스를 생성하고 데이터베이스에 저장한다.
    # "answer": "챗봇이 출력하는 답", # string
    # "references":["참조한 텍스트 1", "참조한 텍스트 2", "참조한 텍스트 3"] # 길이 가변 (0 ~ 3), 각 원소는 string
    _folder_content_create.answer = model_answer["answer"]
    _folder_content_create.references = model_answer["references"]

    content_crud.create_folder_content(db=db,folder_content_create=_folder_content_create)

    return _folder_content_create


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
                    



