from datetime import datetime
from sqlalchemy import and_

from domain.folder_content.content_schema import FolderContentCreate, FolderContentUpdate, FolderContentDelete
from models import FolderContent, Folder
from sqlalchemy.orm import Session




def get_folder_content_list(db : Session, folder_id: int):
    folder_content_list = db.query(FolderContent)\
        .filter(FolderContent.folder_id == folder_id)\
        .order_by(FolderContent.create_date.desc())\
        .all()
    return folder_content_list

def get_folder_content(db: Session, folder_content_id: int):
    folder_content = db.query(FolderContent).get(folder_content_id)
    return folder_content

def create_folder_content(db: Session, folder_content_create: FolderContentCreate, folder: Folder):
    db_folder_content = FolderContent(question=folder_content_create.question,
                                      answer=folder_content_create.answer,
                           create_date=datetime.now(),
                           folder=folder)
    db.add(db_folder_content)
    db.commit()

def update_folder_content(db: Session, db_folder_content : FolderContent,
                    folder_content_update: FolderContentUpdate):
        db_folder_content.question = folder_content_update.question
        db_folder_content.answer = folder_content_update.answer
        db.add(db_folder_content)
        db.commit()

def delete_folder_content(db: Session, db_folder_content : FolderContent):
    db.delete(db_folder_content)
    db.commit()


