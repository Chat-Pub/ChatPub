
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
# from models import Question

# 라우팅이란 FastAPI가 요청받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위를 말한다.

router = APIRouter(
    #prefix 속성은 요청 URL에 항상 포함되어야 하는 값이다.
    prefix="/api/question",
)

# 라우터에 Pydantic 적용하기
# response_model=list[question_schema.Question]의 의미는 question_list 함수의 리턴값은 Question 스키마로 구성된 리스트임을 의미한다.
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    # # db = SessionLocal()
    # # _question_list = db.query(Questoion).order_by(Question.create_date.desc()).all()
    # # # db.close() 함수는 사용한 세션을 컨넥션 풀에 반환하는 함수이다. (세션을 종료하는 것으로 착각하지 말자.)
    # # # db 세션 객체를 생성한 후에 db.close()를 수행하지 않으면 SQLAlchemy가 사용하는 컨넥션 풀에 db 세션이 반환되지 않아 문제가 생긴다.
    # # # 우리가 만들 대부분의 API는 데이터베이스를 사용해야 하기 때문에 이러한 패턴이 반복될 것이다. 이 부분을 자동화할 수는 없을까?
    # # #  FastAPI의 "Dependency Injection"을 사용하면 이 부분을 깔끔하게 처리할 수 있다.
    # # # 프로그래밍에서 "Dependency Injection(의존성 주입)"의 뜻은 필요한 기능을 선언하여 사용할 수 있다는 의미이다.
    # # db.close()
    # with get_db() as db: 대신에 함수에 변수로서 넣을 수도 있다.
    
    _question_list = question_crud.get_question_list(db)

    return _question_list