import datetime

from pydantic import BaseModel, validator

class AnswerCreate(BaseModel):
    content: str

    #빈 문자열 허용하지 않기
    @validator('content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime

    class config:
        # 조회한 모델의 속성을 스키마에 매핑하기 위해 orm_mode를 True로 설정했다.
        orm_mode = True