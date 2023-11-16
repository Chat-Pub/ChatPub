from datetime import datetime
from sqlalchemy import and_

from domain.folder.folder_schema import FolderCreate, FolderUpdate, FolderDelete
from models import User, Folder
from sqlalchemy.orm import Session

def get_folder_list(db : Session):
    folder_list = db.query(Folder)\
        .order_by(Folder.create_date.desc())\
        .all()
    return folder_list

def get_folder(db: Session, folder_id: int):
    folder = db.query(Folder).get(folder_id)
    return folder

def create_folder(db: Session, folder_create: FolderCreate, user: User):
    db_question = Folder(folder_name=folder_create.folder_name,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()

def update_folder(db: Session, db_folder : Folder,
                  folder_update: FolderUpdate):
    db_folder.folder_name = folder_update.folder_name
    db.add(db_folder)
    db.commit()

def delete_folder(db: Session, db_folder : Folder):
    db.delete(db_folder)
    db.commit()


