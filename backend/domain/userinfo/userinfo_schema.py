from pydantic import BaseModel

from domain.user.user_schema import User

class UserInfo(BaseModel):
    id : int
    birth : str
    gender : str
    job : str
    region : str
    money : str
    user: User
    class Config:
        orm_mode = True

class UserInfoCreate(BaseModel):
    birth : str
    gender : str
    job : str
    region : str
    money : str

class UserInfoUpdate(BaseModel):
    birth : str
    gender : str
    job : str
    region : str
    money : str

class UserInfoDelete(BaseModel):
    user_id : int