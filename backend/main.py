from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router
from domain.userinfo import userinfo_router

app = FastAPI()

# 오류의 내용은 복잡하지만 간단히 말해 CORS 정책에 의해 요청이 거부되었다는 말이다.
# 즉, 프론트엔드에서 FastAPI 백엔드 서버로 호출이 불가능한 상황이다.
# 이 오류는 FastAPI에 CORS 예외 URL을 등록하여 해결할 수 있다.
origins = [
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(userinfo_router.router)