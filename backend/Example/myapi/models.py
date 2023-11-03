from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "question"

    id=Column(Integer, primary_key=True)
    subject=Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Answer(Base):
    __tablename__ = "answer"

    id=Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id")) # 어떠한 질문에 대한 대답인지
    question = relationship("Question", backref="answers")
    # relationship으로 question 속성을 생성하면 
    # 답변 객체(예: answer)에서 연결된 질문의 제목을 answer.question.subject처럼 참조할 수 있다.