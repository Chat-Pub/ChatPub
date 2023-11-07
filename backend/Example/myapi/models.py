from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "question"

    id=Column(Integer, primary_key=True)
    subject=Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    # user_id 속성은 User 모델을 Question 모델과 연결하기 위한 속성
    #  user 속성은 Question 모델에서 User 모델을 참조하기 위한 속성

class Answer(Base):
    __tablename__ = "answer"

    id=Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id")) # 어떠한 질문에 대한 대답인지
    question = relationship("Question", backref="answers")
    # relationship으로 question 속성을 생성하면 
    # 답변 객체(예: answer)에서 연결된 질문의 제목을 answer.question.subject처럼 참조할 수 있다.
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
