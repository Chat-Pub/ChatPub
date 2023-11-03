from sqlalchemy import create_engine
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# create_engine은 컨넥션 풀을 생성한다. 컨넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말한다. (컨넥션 풀은 데이터 베이스에 접속하는 세션수를 제어하고, 
# 또 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용한다.)
engine = create_engine(
    # autocommit=False로 설정하면 데이터를 변경했을때 commit 이라는 사인을 주어야만 실제 저장이 된다.
    # 데이터를 잘못 저장했을 경우 rollback 사인으로 되돌리는 것이 가능하다.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal은 데이타베이스에 접속하기 위해 필요한 클래스
SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)
#declarative_base 함수에 의해 반환된 Base 클래스는 조금 후에 알아볼 데이터베이스 모델을 구성할 때 사용되는 클래스이다.
Base = declarative_base()


# with get_db as db: 를 통해 db 객체를 얻고 종료시 자동으로 반환하도록 할 수 있다(Dependency Injection)
# FastAPI의 Depends는 매개 변수로 전달 받은 함수를 실행시킨 결과를 리턴한다. 따라서 db: Session = Depends(get_db)의 db 객체에는 get_db 제너레이터에 의해 생성된 세션 객체가 주입된다. 이 때 get_db 함수에 자동으로 contextmanager가 적용되기 때문에(Depends에서 contextmanager를 적용하게끔 설계되어 있다.) 
# database.py의 get_db 함수는 다음과 같이 적용한 @contextlib.contextmanager 어노테이션을 제거해야 한다.
# @contextlib.contextmanager 어노테이션을 제거하지 않으면 2중으로 적용되어 오류가 발생한다.
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

