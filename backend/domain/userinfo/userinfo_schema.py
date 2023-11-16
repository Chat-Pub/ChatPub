from pydantic import BaseModel

from domain.user.user_schema import User

class UserInfo(BaseModel):
    id : int
    birth : int
    gender : str
    job : str
    region : str
    money : int
    user: User
    class Config:
        orm_mode = True

class UserInfoCreate(BaseModel):
    birth : int
    gender : str
    job : str
    region : str
    money : int

class UserInfoUpdate(BaseModel):
    birth : int
    gender : str
    job : str
    region : str
    money : int

class UserInfoDelete(BaseModel):
    user_id : int