from pydantic import BaseModel

from domain.user.user_schema import User

class UserInfo(BaseModel):
    id : int
    age : int
    gender : str
    job : str
    region : str
    user: User | None

    class Config:
        orm_mode = True

class UserInfoCreate(BaseModel):
    age : int
    gender : str
    job : str
    region : str

class UserInfoUpdate(BaseModel):
    age : int
    gender : str
    job : str
    region : str

class UserInfoDelete(BaseModel):
    user_id : int