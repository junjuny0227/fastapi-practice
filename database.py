from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import os

# 로컬 개발: ./board.db / Docker: DATABASE_URL 환경변수로 주입
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./board.db")

# engine: DB와 실제로 연결하는 객체입니다.
# check_same_thread=False 는 SQLite 전용 설정으로, FastAPI가 여러 스레드를 쓰기 때문에 필요합니다.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal: DB 작업(조회, 저장, 수정, 삭제)을 처리하는 세션을 만드는 팩토리입니다.
# 요청마다 세션을 새로 만들고, 요청이 끝나면 닫습니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base: 모든 DB 모델(테이블)이 상속받는 기본 클래스입니다.
# models.py에서 Post 클래스가 이것을 상속받아 DB 테이블로 등록됩니다.
class Base(DeclarativeBase):
    pass


# get_db: 각 API 요청마다 DB 세션을 제공하는 함수입니다.
# FastAPI의 Depends() 와 함께 사용하면 의존성 주입(Dependency Injection)이 됩니다.
# yield 를 쓰면 요청 처리가 끝난 뒤 finally 블록이 자동으로 실행되어 세션을 닫아줍니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
