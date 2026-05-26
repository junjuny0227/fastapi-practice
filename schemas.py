from datetime import datetime
from pydantic import BaseModel, Field

# 스키마(Schema)란?
# DB 모델(models.py)은 "DB에 저장하는 구조"를 정의하고,
# 스키마는 "API 요청/응답에서 주고받는 데이터 구조"를 정의합니다.
# Pydantic을 사용하면 타입 검증과 에러 메시지를 자동으로 처리해줍니다.


# 게시글 작성 시 클라이언트가 보내야 하는 데이터 형식입니다.
# Field(min_length=1): 빈 문자열을 허용하지 않습니다. 어기면 422 에러가 자동으로 반환됩니다.
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)


# 게시글 수정 시 보내는 데이터 형식입니다.
# 필드가 Optional(| None)이므로 제목만, 또는 내용만 수정할 수 있습니다.
class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)


# API가 클라이언트에게 돌려주는 응답 형식입니다.
# DB 모델에는 있지만 클라이언트에게 숨기고 싶은 필드가 있을 때 여기서 제외하면 됩니다.
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime

    # from_attributes=True: SQLAlchemy ORM 객체를 Pydantic 모델로 자동 변환할 수 있게 합니다.
    # 이 설정 없이는 DB에서 꺼낸 Post 객체를 바로 응답으로 반환할 수 없습니다.
    model_config = {"from_attributes": True}
