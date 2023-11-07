from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base



# SQLAlchemy에서 ManyToMany 관계를 적용하는 방법
# ManyToMany 관계를 적용하기 위해서는 sqlalchemy의 Table을 사용하여 N:N 관계를 의미하는 테이블을 먼저 생성해야 한다.
question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)



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
    modify_date = Column(DateTime, nullable=True)
    # voter는 추천인이므로 기본적으로 User 모델과 연결된 속성
    # secondary 값으로 위에서 생성한 question_voter 테이블 객체를 지정해 주었다는 점이다. 
    # 이렇게 하면 Question 모델을 통해 추천인을 저장하면 
    # 실제 데이터는 question_voter 테이블에 저장되고 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조할수 있게 된다.
    voter = relationship('User', secondary=question_voter, backref='question_voters')


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
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
