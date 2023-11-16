import datetime

from pydantic import BaseModel, validator

from domain.folder.folder_schema import Folder

class FolderContent(BaseModel):
    id: int
    create_date: datetime.datetime
    question: str
    answer: str | None
    folder_id: int
    folder: Folder

    class Config:
        orm_mode = True

class FolderContentCreate(BaseModel):
    question: str
    answer: str | None
    @validator('question')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class FolderContentList(BaseModel):
    question_list: list[FolderContent] = []

class FolderContentUpdate(FolderContentCreate):
    folder_content_id: int

class FolderContentDelete(BaseModel):
    folder_content_id: int