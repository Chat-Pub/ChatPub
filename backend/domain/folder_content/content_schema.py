import datetime

from pydantic import BaseModel, validator

from domain.folder.folder_schema import Folder

class FolderContent(BaseModel):
    id: int
    create_date: datetime.datetime
    question: str
    answer: str | None
    references: str | None
    folder_id: int

    class Config:
        orm_mode = True

class FolderContentCreate(BaseModel):
    folder_id: int
    question: str
    answer: str 
    references: list[str] = []

    @validator('question')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class FolderContentCreateResponse(BaseModel):
    answer: str 
    references: list[str] = []

class FolderContentCreateRequest(BaseModel):
    folder_id: int
    question: str

    @validator('question')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class FolderContentList(BaseModel):
    total: int
    folder_content_list: list[FolderContent] = []

class FolderContentUpdate(FolderContentCreate):
    folder_content_id: int

class FolderContentDelete(BaseModel):
    folder_content_id: int

class FolderId(BaseModel):
    folder_id: int
    