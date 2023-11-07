import datetime

from pydantic import BaseModel, validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

# BaseModel을 상속한 Question 클래스를 만들었다.
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: User | None
    modify_date: datetime.datetime | None
    voter: list[User] = []
    # orm_mode 항목을 True로 설정하면 Question 모델의 항목들이 자동으로 Question 스키마로 매핑된다.
    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    subject: str
    content: str

    # subject와 content에는 빈 값을 허용하지 않도록 했다.
    @validator('subject','content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


# QuestionCreate 스키마에 이미 subject, content 항목이 있으므로 QuestionCreate 스키마를 상속하고 question_id 항목만 추가
class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id : int