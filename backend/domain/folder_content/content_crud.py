from datetime import datetime
from sqlalchemy import and_

from domain.folder_content.content_schema import FolderContentCreate, FolderContentUpdate, FolderContentDelete
from models import FolderContent, Folder
from sqlalchemy.orm import Session


def get_folder_content_memory(db : Session, folder_id: int):
    folder_content_list = db.query(FolderContent)\
        .filter(FolderContent.folder_id == folder_id)\
        .order_by(FolderContent.create_date.desc())\
        .limit(4)

    folder_content_list = folder_content_list.all()
    return folder_content_list


def get_folder_content_list(db : Session, folder_id: int):
    folder_content_list = db.query(FolderContent)\
        .filter(FolderContent.folder_id == folder_id)\
        .order_by(FolderContent.create_date.asc())
        
    total = folder_content_list.distinct().count()
    folder_content_list = folder_content_list.all()

    return total, folder_content_list


def get_folder_content(db: Session, folder_content_id: int):
    folder_content = db.query(FolderContent).get(folder_content_id)
    return folder_content

def create_folder_content(db: Session, folder_content_create: FolderContentCreate):
    folder = db.query(Folder).get(folder_content_create.folder_id)
    # 모델 클래스 생성 후 answer 받아오기  
    db_folder_content = FolderContent(create_date=datetime.now(),
                                    question=folder_content_create.question,
                                    answer=folder_content_create.answer,
                                    references='\n'.join(folder_content_create.references),
                                    folder=folder)
    
    db.add(db_folder_content)
    db.commit()


def update_folder_content(db: Session, db_folder_content : FolderContent,
                    folder_content_update: FolderContentUpdate):
        db_folder_content.question = folder_content_update.question
        db_folder_content.answer = folder_content_update.answer
        db_folder_content.references = folder_content_update.references
        db.add(db_folder_content)
        db.commit()

def delete_folder_content(db: Session, db_folder_content : FolderContent):
    db.delete(db_folder_content)
    db.commit()


