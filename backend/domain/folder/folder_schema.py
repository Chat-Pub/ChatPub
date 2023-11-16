import datetime

from pydantic import BaseModel, validator

from domain.user.user_schema import User

class Folder(BaseModel):
    id: int
    folder_name: str
    create_date: datetime.datetime
    user: User 

    class Config:
        orm_mode = True


class FolderCreate(BaseModel):
    folder_name: str

    @validator('content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class FolderList(BaseModel):
    total: int = 0
    Folder_list: list[Folder] = []


class FolderUpdate(FolderCreate):
    folder_id: int

class FolderDelete(BaseModel):
    folder_id: int
