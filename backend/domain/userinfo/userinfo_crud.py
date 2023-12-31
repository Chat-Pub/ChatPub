from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.userinfo.userinfo_schema import UserInfoCreate, UserInfoUpdate, UserInfoDelete
from models import UserInfo, User

def create_user_info(db: Session, user_info_create : UserInfoCreate, user: User):
    db_user = UserInfo(birth=user_info_create.birth,
                   gender=user_info_create.gender,
                   job=user_info_create.job,
                   region=user_info_create.region,
                    money=user_info_create.money,
                   user=user)
    db.add(db_user) 
    db.commit()

def get_user_info(db: Session, user_id: int):
    return db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

def update_user_info(db: Session, db_user_info: UserInfo, user_info_update: UserInfoUpdate):
    db_user_info.birth = user_info_update.birth
    db_user_info.gender = user_info_update.gender
    db_user_info.job = user_info_update.job
    db_user_info.region = user_info_update.region
    db_user_info.money = user_info_update.money
    db.add(db_user_info)
    db.commit()

def delete_user_info(db: Session, db_user_info: UserInfo):
    db.delete(db_user_info)
    db.commit()
