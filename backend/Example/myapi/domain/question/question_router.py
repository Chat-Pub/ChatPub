from fastapi import APIRouter

from database import SessionLocal
from models import Question

# 라우팅이란 FastAPI가 요청받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위를 말한다.

router = APIRouter(
    #prefix 속성은 요청 URL에 항상 포함되어야 하는 값이다.
    prefix="/api/question",
)

@router.get("/list")
def question_list():
    db = SessionLocal()
    _question_list = db.query(Qeustoion).order_by(Question.create_date.desc()).all()
    #db.close() 함수는 사용한 세션을 컨넥션 풀에 반환하는 함수이다. (세션을 종료하는 것으로 착각하지 말자.)
    db.close()
    return _question_list