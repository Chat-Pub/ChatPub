from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True) 
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True)
    birth = Column(String(16), nullable=False)
    gender = Column(String(255), nullable=False)
    job = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    money = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user_infos")

class Folder(Base):
    __tablename__ = "folder"

    id = Column(Integer, primary_key=True)
    folder_name = Column(String(1024), nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user_folders")
    
class FolderContent(Base):
    __tablename__ = "folder_content"

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    references = Column(Text, nullable=True)
    folder_id = Column(Integer, ForeignKey("folder.id"), nullable=False)
    folder = relationship("Folder", backref="folder_contents")

