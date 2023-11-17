from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer  
# OAuth2PasswordRequestForm은 사용자가 입력한 username과 password를 받아온다.
from jose import jwt, JWTError
# jwt(Json Web Token)를 사용하여 액세스 토큰을 생성한다.
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context


# ACCESS_TOKEN_EXPIRE_MINUTES - 토큰의 유효기간을 의미한다. 분 단위로 설정한다.
# SECRET_KEY - 암호화시 사용하는 64자리의 랜덤한 문자열이다. => SECRET_KEY를 생성 : openssl rand -hex 32
# ALGORITHM - 토큰 생성시 사용하는 알고리즘을 의미하며 여기서는 HS256을 사용한다.
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "28f2ed7da28d587ccba3c38d335530d77aaff6dc2f1eb9b9ebaad2647b9ce93c"
ALGORITHM = "HS256"
# Auth2PasswordBearer(tokenUrl="/api/user/login")에서 사용한 tokenUrl은 로그인 API의 URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


router = APIRouter(
    prefix="/api/user",
)

# 라우터 함수의 응답으로 response_model을 사용하는 대신 status_code=status.HTTP_204_NO_CONTENT 를 사용
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # check username and password
    user = user_crud.get_user(db,form_data.username)
    # pwd_context의 verify함수는 암호화 되지 않은 비밀번호를 암호화하여 데이터베이스에 저장된 암호와 일치하는지 판단한다.
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            # 401 오류는 사용자 인증 오류를 의미한다. 
            # 보통 401 오류인 경우에는 인증 방식에 대한 추가 정보인 WWW-Authenticate 항목도 헤더 정보에 포함하여 함께 리턴해 준다.
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # create access token
    # sub 항목에 사용자명을 저장하고 exp 항목에 토큰의 유효기간을 설정하여 토큰을 생성했다. 
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

# 헤더 정보의 토큰값을 읽어 사용자 객체를 리턴하는 get_current_user 함수
# 매개변수로 사용한 token의 값은 FastAPI의 security 패키지에 있는 OAuth2PasswordBearer에 의해 자동으로 매핑
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
