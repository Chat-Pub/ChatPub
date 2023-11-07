from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/answer",
)

# 입력 - answer_schema.AnswerCreate , 출력 - 없음
# 출력은 response_model을 사용하는 대신 status_code=status.HTTP_204_NO_CONTENT 를 사용했다.
# 이렇게 리턴할 응답이 없을 경우에는 응답코드 204를 리턴하여 "응답 없음"을 나타낼 수 있다.
@router.post("/create/{question_id}", response_model=question_schema.Question)
def answre_create(question_id: int, _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user=current_user)

    # redirect
    from domain.question.question_router import router as question_router
    url = question_router.url_path_for('question_detail',
                                       question_id=question_id)
    return RedirectResponse(url, status_code=303)

@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id : int, db: Session= Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate, 
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    
    if db_answer.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="권한이 없습니다.")
                            
    answer_crud.update_answer(db, db_answer=db_answer,
                              answer_update=_answer_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    
    if db_answer.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다.")
    
    answer_crud.delete_answer(db, db_answer=db_answer)

