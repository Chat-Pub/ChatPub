# Backend Repository

## Database 생성 방법
```
pip install sqlalchemy
pip install alembic
alembic init migrations
```

- alembic.ini 의 값 수정
    - sqlalchemy.url = <드라이버>://<사용자>:<비밀번호>@<호스트>:<포트>/<데이터베이스>

- migrations/env.py 의 값 추가 및 수정
    - import models
    - target_metadata = models.Base.metadata

```
alembic revision --autogenerate
alembic upgrade head
```


DB와 TABLE이 생성된다.