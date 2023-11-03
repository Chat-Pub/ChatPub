import datetime

from pydantic import BaseModel

# BaseModel을 상속한 Question 클래스를 만들었다.
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    # orm_mode 항목을 True로 설정하면 Question 모델의 항목들이 자동으로 Question 스키마로 매핑된다.
    class Config:
        orm_mode = True

