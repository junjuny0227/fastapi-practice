from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from routers import posts


# lifespan: 앱이 시작할 때와 종료할 때 실행할 코드를 정의합니다.
# yield 이전 = 시작 시 실행 / yield 이후 = 종료 시 실행
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시: DB 테이블이 없으면 자동으로 생성합니다.
    # models.py의 Post 클래스가 Base를 상속받아 등록되어 있으므로, posts 테이블이 만들어집니다.
    Base.metadata.create_all(bind=engine)
    yield  # 앱이 실행되는 동안 여기서 대기


# FastAPI 앱 인스턴스를 만듭니다.
# title은 /docs(Swagger UI)에 표시되는 이름입니다.
app = FastAPI(title="FastAPI 게시판", lifespan=lifespan)

# posts 라우터를 앱에 등록합니다.
# routers/posts.py에 정의한 엔드포인트들이 여기서 앱에 연결됩니다.
app.include_router(posts.router)
