from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


# Post 클래스 = DB의 "posts" 테이블입니다.
# ORM(Object-Relational Mapping): Python 객체와 DB 테이블을 자동으로 연결해주는 방식입니다.
# 즉, SQL을 직접 쓰지 않고 Python 코드로 DB를 다룰 수 있게 해줍니다.
class Post(Base):
    __tablename__ = "posts"  # 실제 DB에 생성될 테이블 이름

    # Mapped[int]: 이 컬럼의 Python 타입이 int임을 명시합니다.
    # primary_key=True: 각 게시글을 고유하게 식별하는 ID입니다. 자동으로 1, 2, 3... 증가합니다.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200))   # 최대 200자 제목
    content: Mapped[str] = mapped_column(Text)         # 길이 제한 없는 본문
    author: Mapped[str] = mapped_column(String(100))   # 최대 100자 작성자명

    # 게시글이 처음 생성될 때 현재 시각을 자동으로 저장합니다.
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    # 게시글이 수정될 때마다 시각이 갱신됩니다.
    # SQLAlchemy의 onupdate는 ORM 방식에서 자동 작동이 불안정하므로,
    # 라우터(posts.py)에서 직접 갱신합니다.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
